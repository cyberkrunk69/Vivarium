# JSONL Log Analysis – Data Flow & Bug Report

**Date:** 2026-02-10  
**Scope:** `action_log.jsonl`, `execution_log.jsonl`, `messages_to_human.jsonl` and related flows.

---

## 1. Log Files & Data Flow

| File | Path | Written By | Purpose |
|------|------|------------|---------|
| action_log.jsonl | `vivarium/meta/audit/action_log.jsonl` | `action_logger.ActionLogger` | All swarm actions (TOOL, SOCIAL, IDENTITY, etc.) |
| execution_log.jsonl | `vivarium/meta/audit/execution_log.jsonl` | `worker_runtime.append_execution_event` | Task lifecycle (queued, in_progress, completed, pending_review) |
| messages_to_human.jsonl | `workspace/.swarm/messages_to_human.jsonl` | `_notify_human_task_pending_approval`, `message_human` | Inbound messages to operator |

---

## 2. Data Loss & Bug Findings

### 2.1 Result preview truncation in approval messages (FIXED)

**Evidence:** `messages_to_human.jsonl` line 1:

```json
"content": "... Result preview: To work on my identities... This in..."
```

**Cause:** Content was truncated at write time. `_human_friendly_result_preview` no longer truncates (max_len param unused). Existing truncated messages came from older code.

**Status:** Backend no longer truncates; UI uses overflow/scroll. New messages store full preview.

---

### 2.2 Approval messages missing identity (worker/identity_phase5)

**Evidence:** `messages_to_human.jsonl` lines 2–6:

```json
{"from_id": "worker", "from_name": "Resident", "task_id": "task_phase2_ok"}
{"from_id": "identity_phase5", "from_name": "identity_phase5", "task_id": "task_phase5_reward"}
```

**Cause:**

- **Real tasks:** `resident_ctx` can be missing in some paths; `identity_id`/`identity_name` now fall back to execution log (FIXED).
- **Test tasks:** `task_phase2_ok`, `task_phase5_reward`, etc. come from `test_runtime_phase2_quality_review.py` with `resident_ctx=None`. These tasks have no identity in the execution log (tests use `tmp_path`). Identity falls back to `"worker"` / `"Resident"` or `"identity_phase5"`.

**Fix:** Tests should patch `messages_to_human` path so they don’t pollute the real workspace. For production: test tasks are synthetic; execution log has no identity. Control-panel fallback only works when execution log has an entry for that `task_id`.

---

### 2.3 Tests writing to real messages_to_human.jsonl

**Evidence:** Messages with `task_id` in `task_phase2_*`, `task_phase5_*` appear in the real `messages_to_human.jsonl`.

**Cause:** Tests monkeypatch `EXECUTION_LOG` to `tmp_path` but not the messages file. `_notify_human_task_pending_approval` uses `WORKSPACE / ".swarm" / "messages_to_human.jsonl"` directly.

**Fix:** Patch the messages file path in tests (e.g. `worker.MESSAGES_TO_HUMAN_PATH = tmp_path / "messages_to_human.jsonl"`).

---

### 2.4 Action log detail truncation for chat/social

**Evidence:** `action_log.jsonl` line 3:

```json
"detail": "Task suggestion-1770783709629 update: To work on my identities and get to kno..."
```

**Cause:** `swarm_enrichment.post_discussion_message` passes a 77-character preview to `action_logger.log` for display. The full discussion content is stored in `discussions/town_hall.jsonl`; only the action log detail is shortened.

**Status:** Intentional for readability. `action_logger` `max_detail_length` is 16000; truncation is in the caller’s preview. No data loss in primary storage.

---

### 2.5 Execution log: identity_name in older events

**Evidence:** Early `in_progress` events had `identity_id` but not `identity_name`.

**Cause:** `append_execution_event` previously only passed `identity_id` in `identity_fields`.

**Fix:** `identity_name` is now included in all execution events when `resident_ctx` is available.

---

### 2.6 Execution log lookup for test tasks

**Evidence:** Control panel fallback uses `read_execution_log().get("tasks", {}).get(task_id)` to resolve identity. For `task_phase2_ok`, `task_phase5_reward`, etc., there is no execution log entry (tests use `tmp_path`).

**Impact:** For synthetic test tasks, fallback cannot resolve identity; UI shows "Resident" or "identity_phase5".

**Mitigation:**  
- Tests should not write to production `messages_to_human`.  
- Optional: For known synthetic task IDs (`task_phase2_*`, `task_phase5_*`), display as "Test task" or similar instead of "Resident".

---

### 2.7 Duplicate notifications (deduplication)

**Evidence:** Bug catalog Issue 9: same task notified multiple times.

**Fix:** `_already_notified_task_pending_approval` window increased from 100 to 500 messages. Mailbox API uses `seen_task_approvals` to deduplicate by `task_id` when building threads.

---

### 2.8 Discussion content clipped at 1200 chars

**Location:** `swarm_enrichment.post_discussion_message` line 561:

```python
clipped = text[:1200]
```

**Impact:** Discussion messages longer than 1200 chars are truncated in `discussions/*.jsonl`. No overflow/append.

**Recommendation:** Consider increasing or documenting; 1200 may be sufficient for most updates.

---

### 2.9 Discussion preview truncation for action log (77 chars)

**Location:** `swarm_enrichment.post_discussion_message` lines 580–581:

```python
if len(preview) > 80:
    preview = preview[:77] + "..."
```

**Impact:** Action log shows a short preview only. Full content is in discussions. No change needed unless action log should show more.

---

## 3. Summary of Fixes Applied

| Bug | Fix |
|-----|-----|
| Result preview truncation | `_human_friendly_result_preview` no longer truncates; UI scroll |
| Missing identity in approval | Fallback to execution log `identity_id`/`identity_name`; `identity_name` added to execution events |
| Test tasks polluting real inbox | Tests should patch `MESSAGES_TO_HUMAN_PATH` |
| Execution log missing identity_name | `identity_fields` now includes `identity_name` |
| Duplicate notifications | Dedup window 100→500; mailbox API dedupes by `task_id` |

---

## 4. Recommendations

1. **Tests:** Patch `MESSAGES_TO_HUMAN_PATH` so phase2/phase5 tests do not write to the real workspace.
2. **Synthetic tasks:** Optional UX tweak for `task_phase2_*` / `task_phase5_*` to show "Test task" instead of "Resident".
3. **Discussion length:** Document or adjust the 1200-char limit in `post_discussion_message` if needed.
4. **Audit:** Add a small script to validate logs (e.g. no duplicate `daily_wind_down_allowance` per identity per cycle, timestamps UTC, etc.).
