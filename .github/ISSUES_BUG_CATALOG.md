# Bug Catalog Issues - Log Analysis (2026-02-10)

Issues created at https://github.com/cyberkrunk69/Vivarium/issues

| # | Issue | GitHub |
|---|-------|--------|
| 1 | Duplicate daily_wind_down_allowance | [#58](https://github.com/cyberkrunk69/Vivarium/issues/58) |
| 2 | Phase 4 subtask prompt fragmentation | [#59](https://github.com/cyberkrunk69/Vivarium/issues/59) |
| 3 | LLM plans instead of executing tools | [#60](https://github.com/cyberkrunk69/Vivarium/issues/60) |
| 4 | phase4_skip not honored | [#61](https://github.com/cyberkrunk69/Vivarium/issues/61) |
| 5 | Timestamp/timezone inconsistency | [#62](https://github.com/cyberkrunk69/Vivarium/issues/62) |
| 6 | Approval messages missing identity | [#63](https://github.com/cyberkrunk69/Vivarium/issues/63) |
| 7 | safety_report.task truncated | [#64](https://github.com/cyberkrunk69/Vivarium/issues/64) |
| 8 | Phase 4 parent blocked by pending_review | [#65](https://github.com/cyberkrunk69/Vivarium/issues/65) |
| 9 | Duplicate test task notifications | [#66](https://github.com/cyberkrunk69/Vivarium/issues/66) |
| 10 | Resident day advancing while paused | [#67](https://github.com/cyberkrunk69/Vivarium/issues/67) |

## Fixed In Current Working Tree

- #3 LLM plans instead of executing tools
  - Runtime now rejects planning-only docs outputs during post-execution review and requeues them.
  - Docs-only tasks that fail to persist artifacts are also requeued instead of passing to pending review.
- Additional (not yet tracked as GitHub issues):
  - Control panel day display now uses relative resident day index (no more epoch-sized `Day N` values).
  - Test enrichment writes now use workspace-scoped logs, preventing pollution of live audit logs.

---

## Issue 1: Duplicate daily_wind_down_allowance grants same identity twice

**Title:** Duplicate daily_wind_down_allowance grants same identity twice per cycle

**Labels:** bug, tokens

**Body:**

```
## Summary

From action_log.jsonl: the same identity (oc_a107a5) received `daily_wind_down_allowance` (+150 tokens) twice within the same second.

## Evidence

```
{"timestamp": "2026-02-10T20:56:51.189", "actor": "oc_a107a5", "action_type": "IDENTITY", "action": "daily_wind_down_allowance", "detail": "+150 free-time tokens", ...}
{"timestamp": "2026-02-10T20:56:51.197", "actor": "oc_a107a5", "action_type": "IDENTITY", "action": "daily_wind_down_allowance", "detail": "+150 free-time tokens", ...}
```

## Impact

Double token grant: identity receives 300 tokens instead of 150 for wind-down allowance.

## Suggested Fix

Add idempotency / deduplication for `daily_wind_down_allowance` per identity per cycle (e.g. track last_cycle_id when granting, skip if already granted this cycle).

## Files

- vivarium/runtime/swarm_enrichment.py (wind_down, daily allowance logic)
```

---

## Issue 2: Phase 4 subtask prompts fragmented by comma-splitting

**Title:** Phase 4 subtask prompts fragmented—comma-splitting produces incoherent focus areas

**Labels:** bug, phase4, prompts

**Body:**

```
## Summary

Phase 4 decomposition splits prompts by commas into "features", which become subtask focus areas. This produces nonsensical fragments.

## Evidence (from queue.json)

- phase4_01: "Focus area: Human replied to my message. Read their response and take one concrete" (truncated mid-sentence)
- phase4_02: "Focus area: action that advances collaboration. Human response" (awkward fragment)
- phase4_03: "Focus area: that's correct. good job. do you know how to edit your identity or where to put the document / text?" (human message used as focus)

## Impact

Subtask prompts are incoherent. Residents receive unclear instructions and produce generic "proposal" text instead of taking concrete action.

## Suggested Fix

Use semantic or sentence-based splitting instead of comma-splitting. Consider keeping the full human message as context for the first subtask rather than fragmenting it.

## Files

- vivarium/runtime/worker_runtime.py (_maybe_compile_phase4_plan)
- vivarium/runtime/resident_facets.py (intent decomposition)
```

---

## Issue 3: LLM outputs planning text instead of executing tools

**Title:** Residents output planning/proposal text instead of calling tools to create documents

**Labels:** bug, llm, tool-use

**Body:**

```
## Summary

From execution_log.jsonl: residents repeatedly produce result_summary like "I will create...", "The document will be...", "Proposal: ..." but never actually call write_file, edit_profile_ui, or similar tools to create the artifact.

## Evidence

Multiple execution entries for suggestion-1770782204017 show result_summary containing:
- "The document will be a markdown file named crystallize_personality.md..."
- "I will create a markdown proposal in library/community_library/resident_suggestions/oc_a107a5/..."
- "Here is the proposal: [markdown structure]"

No actual file write or tool call is recorded.

## Impact

Tasks that require creating documents (personality crystallization, proposals) never produce artifacts. Human sees planning text, not deliverables.

## Suggested Fix

- Strengthen prompts to require concrete tool calls (write_file, persist_artifact, etc.) for document-creation tasks
- Add verification step that rejects "I will..." style outputs when tools are available
- Consider few-shot examples of correct tool-calling behavior
```

---

## Issue 4: phase4_skip not honored—skip subtasks still executed

**Title:** phase4_skip subtasks are still executed instead of being skipped

**Labels:** bug, phase4

**Body:**

```
## Summary

Tasks with `phase4_skip: true` are intended to be skipped (e.g. when decomposition produced redundant subtasks). The execution log shows phase4_01 with phase4_skip: true was still executed and reached pending_review.

## Evidence

From queue.json:
```json
{"id": "mailbox-followup-oc_02df05-1770783020532__phase4_01", "phase4_skip": true, ...}
```

From execution_log.jsonl: phase4_01 was executed (in_progress → completed → pending_review).

## Impact

Wasted compute and tokens on subtasks that should have been skipped. Possible confusion in dependency resolution.

## Suggested Fix

In find_and_execute_task or _select_tasks_for_scan, filter out tasks where phase4_skip is true. Ensure the phase4 logic that sets phase4_skip is consistent with the task-selection logic.
```

---

## Issue 5: Timestamp/timezone inconsistency across logs

**Title:** action_log and execution_log use different timestamp formats and timezones

**Labels:** bug, observability

**Body:**

```
## Summary

action_log.jsonl uses timestamps like "2026-02-10T20:56:51.189" (no timezone, likely local).
execution_log.jsonl uses "2026-02-11T03:56:51.193146+00:00" (UTC).

Same moment appears as different dates (Feb 10 vs Feb 11), making cross-log correlation difficult.

## Impact

Hard to correlate events across logs. Resident-day calculations may be inconsistent.

## Suggested Fix

Standardize on UTC for both logs. Include timezone in action_log timestamps. Ensure parsers handle both formats during migration.
```

---

## Issue 6: Approval messages missing identity when from_id is "worker"

**Title:** task_pending_approval messages show from_id "worker" instead of actual identity

**Labels:** bug, mailbox, ui

**Body:**

```
## Summary

From messages_to_human.jsonl: some approval messages have from_id "worker" or "identity_phase5" instead of the resident identity. Human cannot tell which identity completed the task.

## Evidence

```json
{"from_id": "worker", "from_name": "Resident", "content": "Task \"task_phase2_ok\" is ready for your approval...", "task_id": "task_phase2_ok"}
{"from_id": "identity_phase5", "from_name": "identity_phase5", "content": "Task \"task_phase5_reward\" is ready for your approval...", "task_id": "task_phase5_reward"}
```

## Impact

Mailbox UI shows "Resident" or "identity_phase5" instead of the real identity name. Reduces clarity for human operator.

## Suggested Fix

When appending task_pending_approval messages, always pass identity_id and identity_name from the task/execution context. Fallback to "worker" only when identity is truly unavailable.
```

---

## Issue 7: safety_report.task field truncated

**Title:** safety_report.task field truncated in execution log

**Labels:** bug, safety, logging

**Body:**

```
## Summary

From execution_log.jsonl: safety_report.task ends with "\\n\\nB" (truncated). Likely a character limit during serialization.

## Evidence

```json
"safety_report": {
  "task": "## USER INTENT (Do not deviate)\\nGOAL: work on your identities...\\n\\nB",
  ...
}
```

## Impact

Safety audit trail incomplete. Partial task context may affect debugging.

## Suggested Fix

Check for truncation in safety_report serialization. Increase limit or store full task separately if needed.
```

---

## Issue 8: Phase 4 parent task blocked when subtask stuck in pending_review

**Title:** Phase 4 parent cannot complete when subtask is pending_review

**Labels:** bug, phase4, dependencies

**Body:**

```
## Summary

Parent task has depends_on: [phase4_01, phase4_02, phase4_03]. When phase4_01 reaches pending_review, check_dependencies_complete may not consider it "done" (depending on implementation). Parent remains blocked until human approves.

## Evidence

From queue.json: mailbox-followup parent has depends_on including phase4_01 (pending_review), phase4_02 and phase4_03 (pending). Parent status: pending.

## Impact

Decomposed tasks can stall if any subtask requires human approval. Parent never runs, potentially leaving workflow incomplete.

## Suggested Fix

Ensure pending_review is treated as "dependency satisfied" for parent task scheduling. Or: avoid requiring human approval for internal phase4 subtasks when the parent will aggregate results.
```

---

## Issue 9: Duplicate notifications for same task (test tasks)

**Title:** task_phase2_reject and task_phase5_once produce duplicate approval notifications

**Labels:** bug, notifications, tests

**Body:**

```
## Summary

From messages_to_human.jsonl: task_phase2_reject appears twice (lines 9–10), task_phase5_once appears twice (lines 13–14). Likely from test runs or duplicate notification paths.

## Evidence

Duplicate messages with same task_id and nearly identical timestamps.

## Impact

Mailbox clutter. Duplicate notifications for same task.

## Suggested Fix

Ensure _already_notified_task_pending_approval (or equivalent) is applied to all notification paths, including test/phase2/phase5 flows. Extend deduplication to cover these task types.
```

---

## Issue 10: Resident day advancing while residents are paused

**Title:** Resident day / cycle advances with wall-clock time even when residents are paused (HALT)

**Labels:** bug, time, pause, ui

**Body:**

```
## Summary

When residents are paused (HALT), the resident day and cycle_id continue to advance because they are derived from wall-clock time (`time.time() // cycle_seconds`), not from whether the worker loop is running.

## Evidence

- `_current_cycle_id()` in `resident_onboarding.py` uses `int(timestamp // cycle_seconds)` with no check for stop/pause status.
- `_get_day_count_for_identity()` advances `day_count` whenever `cycle_id > last_cycle_id`; cycle_id is purely time-based.
- Control panel / spawner status shows "stopped" but time keeps ticking.

## Impact

Resident days "run" even when no one is active. After pausing overnight, resume shows residents at a higher day than expected. Breaks intuition that "paused" means time stops.

## Suggested Fix

- Option A: Gate `_current_cycle_id()` on stop/pause status (e.g. read stop file, return last cycle when halted).
- Option B: Persist "effective cycle" when halted and advance only when worker is running.
- Option C: Document as intended (days = real time) and rename UI to clarify.

## Files

- vivarium/runtime/resident_onboarding.py (_current_cycle_id, _get_day_count_for_identity)
- vivarium/runtime/control_panel_app.py (get_runtime_speed, cycle display)
- vivarium/runtime/config.py (stop file path)
```

---

## Summary Table

| # | Issue | Severity | GitHub |
|---|-------|----------|--------|
| 1 | Duplicate daily_wind_down_allowance | Medium | [#58](https://github.com/cyberkrunk69/Vivarium/issues/58) |
| 2 | Phase 4 subtask prompt fragmentation | Medium | [#59](https://github.com/cyberkrunk69/Vivarium/issues/59) |
| 3 | LLM plans instead of executing tools | High | [#60](https://github.com/cyberkrunk69/Vivarium/issues/60) |
| 4 | phase4_skip not honored | Medium | [#61](https://github.com/cyberkrunk69/Vivarium/issues/61) |
| 5 | Timestamp/timezone inconsistency | Low | [#62](https://github.com/cyberkrunk69/Vivarium/issues/62) |
| 6 | Approval messages missing identity | Low | [#63](https://github.com/cyberkrunk69/Vivarium/issues/63) |
| 7 | safety_report.task truncated | Low | [#64](https://github.com/cyberkrunk69/Vivarium/issues/64) |
| 8 | Phase 4 parent blocked by pending_review subtask | Medium | [#65](https://github.com/cyberkrunk69/Vivarium/issues/65) |
| 9 | Duplicate test task notifications | Low | [#66](https://github.com/cyberkrunk69/Vivarium/issues/66) |
| 10 | Resident day advancing while paused | Medium | [#67](https://github.com/cyberkrunk69/Vivarium/issues/67) |

---

## Additional findings logged (2026-02-11)

| # | Issue | Severity | Status | GitHub |
|---|-------|----------|--------|--------|
| 10 | Control panel day column used absolute epoch cycle id (e.g. `Day 354157620`) instead of a human-usable resident day index | Medium | Fixed | [#69](https://github.com/cyberkrunk69/Vivarium/issues/69) |
| 11 | Test enrichment fixtures wrote social/journal lines into shared runtime action log (`vivarium/meta/audit/action_log.*`) | High | Fixed | [#68](https://github.com/cyberkrunk69/Vivarium/issues/68) |
| 12 | Tests write to real messages_to_human.jsonl (pollute production workspace) | Medium | Open | [#70](https://github.com/cyberkrunk69/Vivarium/issues/70) |
| 13 | Log UI does not update in real-time (or at all) when worker runs | High | Open | [#71](https://github.com/cyberkrunk69/Vivarium/issues/71) |
| 14 | Log UI: empty cells collapse column width, causing misalignment | Low | Open | [#72](https://github.com/cyberkrunk69/Vivarium/issues/72) |
| 15 | Log UI: resident-created task name and detail show arbitrary values (IDs, timestamps) | Medium | Open | [#73](https://github.com/cyberkrunk69/Vivarium/issues/73) |

## Initiatives

| Initiative | Description | GitHub |
|------------|-------------|--------|
| Bandaid Hunt | Find and fix papered-over root causes (no bandaids) | [#74](https://github.com/cyberkrunk69/Vivarium/issues/74) |

## Tech debt

| Issue | Description | GitHub |
|-------|-------------|--------|
| IT'S OVER NINE THOUSAND!!! | control_panel_app.py ~9,656 lines; split into modules | [#75](https://github.com/cyberkrunk69/Vivarium/issues/75) |
