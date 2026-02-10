# Current Capabilities (Runtime Truth)

**Date:** 2026-02-09  
**Scope:** What is implemented and wired in the canonical runtime path today.

---

## 1) Canonical runtime capabilities

| Capability area | Status | Current behavior |
| --- | --- | --- |
| Canonical execution path (Phase 0) | Implemented | `worker.py` polls `queue.json`, enforces dependencies/locks, executes via `swarm.py`, and records execution events. |
| Safety gating (Phase 1) | Implemented in worker path | Worker runs pre-execution safety checks and the API path applies defense-in-depth checks. |
| Quality/critic lifecycle (Phase 2) | Implemented | Outputs enter `pending_review`; accepted tasks become `approved`; rejected tasks `requeue` (or `failed` after retry cap). |
| Tool-first reuse routing (Phase 3) | Implemented | Prompt tasks are routed through `tool_router` before LLM dispatch, with route metadata persisted to events. |
| Intent + decomposition foundation (Phase 4) | Implemented | Complex prompts are detected and can be decomposed into dependency-aware queue subtasks. |
| Social/economic reward hook (Phase 5, initial) | Implemented | Approved under-budget tasks can grant identity rewards through `swarm_enrichment`. |
| Phase 5 reward idempotency + audit | Implemented | Grants are deduplicated per `task_id + identity_id` and persisted in `.swarm/phase5_reward_ledger.json`. |

---

## 2) Observability and contract guarantees

- Queue normalization and status vocabulary are defined by `runtime_contract.py`.
- Execution event logs are appended to `execution_log.jsonl`.
- Review and reward metadata emitted from worker flow includes:
  - review: `review_verdict`, `review_confidence`, `review_attempt`, issues/suggestions, quality-gate fields
  - phase 5 reward: `phase5_reward_applied`, `phase5_reward_tokens_requested`, `phase5_reward_tokens_awarded`, `phase5_reward_identity`, `phase5_reward_reason`, `phase5_reward_granted_at`, `phase5_reward_ledger_recorded`, `phase5_reward_error`
- Runtime social state and reward balances are stored under `.swarm/` (including `.swarm/free_time_balances.json` and `.swarm/phase5_reward_ledger.json`).

---

## 3) Available but not hard-wired into all paths

These modules exist and are used in canonical worker flow; execution API routes are now guarded by loopback + internal-token checks:

- `safety_gateway.py`
- `secure_api_wrapper.py`
- `quality_gates.py`
- `tool_router.py`
- `intent_gatekeeper.py`
- `swarm_enrichment.py`

---

## 4) Known limitations and active gaps

- Direct human-triggered `/cycle` calls are blocked; the intended operator flow is localhost control panel -> worker runtime -> internal API.
- `swarm_orchestrator_v2.py` and `worker_pool.py` remain experimental/non-canonical.
- Phase 6 (multi-user/LAN + vision dashboard) and Phase 7 (autonomous improvement checkpoints) are still planned, not runtime defaults.
- System remains experimental; operational use should stay in isolated environments.

---

## 5) Latest validated checks

```bash
python3 -m pytest -q tests/test_runtime_phase2_quality_review.py tests/test_runtime_phase0_phase1.py tests/test_runtime_phase3_tool_routing.py tests/test_runtime_phase4_intent_decomposition.py
# Result: 22 passed
```

---

## 6) Short summary

The current Vivarium runtime is a queue-driven, safety-checked, quality-reviewed execution system with implemented Phase 0-5 foundations in the canonical worker path. Operational language now frames execution in compressed human timescales (today/this week cycle planning), with Phase 6/7 still deferred roadmap work.
