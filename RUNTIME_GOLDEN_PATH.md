# Runtime Golden Path (Phase 0)

This is the canonical production path for task execution.

Operational framing uses compressed human timescales:
- **today** = active cycles
- **this week** = grouped cycle outcomes
- **next week** = queued improvements

## Runtime state snapshot (2026-02-09)

| Runtime layer | Status | Notes |
| --- | --- | --- |
| Phase 0 - canonical runtime path | Implemented | `worker.py + swarm.py + control_panel.py` are the default execution path. |
| Phase 1 - safety preflight | Implemented | Worker dispatch calls `SafetyGateway.pre_execute_safety_check(...)` before execution. |
| Phase 2 - post-execution quality review | Implemented | Critic/quality lifecycle emits `pending_review`, then `approved` or `requeue`/`failed`. |
| Phase 3 - tool-first routing | Implemented | Prompt tasks route through `tool_router` before standard `/cycle` LLM dispatch. |
| Phase 4 - intent/decomposition foundation | Implemented | Complex prompts can decompose into dependency-aware queue subtasks. |
| Phase 5 - social/economic reward hook | Implemented (initial) | Under-budget approved tasks can grant identity rewards through `swarm_enrichment`. |

Latest validated runtime regression:

```bash
python3 -m pytest -q tests/test_runtime_phase2_quality_review.py tests/test_runtime_phase0_phase1.py tests/test_runtime_phase3_tool_routing.py tests/test_runtime_phase4_intent_decomposition.py
# Result: 22 passed
```

## Canonical runtime entrypoints

1. `worker.py` - queue polling, dependency checks, lock acquisition, execution event logging
2. `swarm.py` - `/cycle` execution API (`llm` + `local`), `/plan`, `/status`
3. `control_panel.py` - human control and observability surface

## Enforcement

- Detached/alternate runners are not part of the supported production flow.
- Control-panel spawner lifecycle endpoints are disabled in golden-path mode.
- Queue execution must enter through `worker.py` against `queue.json`.

## Task/event contract

- Queue contract is normalized via `runtime_contract.py`:
  - required top-level keys: `version`, `api_endpoint`, `tasks`, `completed`, `failed`
  - task defaults: `type=cycle`, `depends_on=[]`, `parallel_safe=true`, `status=pending`
- Execution events are appended to `execution_log.jsonl` from `worker.py` and use
  the canonical status vocabulary in `runtime_contract.KNOWN_EXECUTION_STATUSES`.
- Post-execution review lifecycle is now explicit in the worker path:
  - `pending_review` -> `approved` for accepted outputs
  - `pending_review` -> `requeue` (or `failed` after retry limit) for rejected outputs
  - quality-gate state is mirrored in `quality_gate_queue.json` (`needs_qa` / `rejected`)
- Tool-first routing lifecycle is now explicit in the worker path:
  - prompt tasks are routed through `tool_router` before `/cycle` LLM dispatch
  - matched tool context is injected into the prompt for reuse-first execution
  - route metadata is recorded in execution events (`tool_route`, `tool_name`, `tool_confidence`)
- Intent-preserving planning lifecycle is now explicit in the worker path:
  - prompt tasks are checked with deterministic Phase 4 gut-check heuristics
  - complex tasks are atomized into dependency-aware queue subtasks before execution
  - extracted intent is persisted and injected into downstream prompts to reduce drift
- Phase 5 social/economic reward lifecycle has an initial worker hook:
  - approved tasks with measurable budget savings can grant identity free-time/journal tokens
  - reward grants flow through `swarm_enrichment`, are reflected in execution event metadata, and are deduplicated per task+identity via `.swarm/phase5_reward_ledger.json`
  - reward events include: `phase5_reward_applied`, `phase5_reward_tokens_requested`, `phase5_reward_tokens_awarded`, `phase5_reward_identity`, `phase5_reward_reason`, `phase5_reward_granted_at`, `phase5_reward_ledger_recorded`, and `phase5_reward_error` (on failure)

## Known caveats in this path

- `/cycle` and `/plan` are now loopback-only and require the internal execution token; intended human operation is via localhost control panel.
- `worker_pool.py` remains experimental and is not in the canonical import path.

## Safety and budget guarantees in this path

- Worker preflight safety: `SafetyGateway.pre_execute_safety_check(...)` is called
  before task dispatch in `worker.py`.
- API safety defense-in-depth: `/cycle` runs safety checks again in `swarm.py`.
- LLM calls route through `SecureAPIWrapper` for:
  - rate limiting
  - budget enforcement
  - audit logging
- `mode=local` commands are evaluated against explicit allowlist + denylist policy.

## Smoke checks

```bash
python3 -m py_compile worker.py swarm.py control_panel.py runtime_contract.py
python3 -m pytest -q tests/test_runtime_phase0_phase1.py tests/test_runtime_phase2_quality_review.py tests/test_runtime_phase3_tool_routing.py tests/test_runtime_phase4_intent_decomposition.py
```
