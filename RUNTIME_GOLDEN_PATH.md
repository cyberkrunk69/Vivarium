# Runtime Golden Path (Phase 0)

This is the canonical production path for task execution.

## Canonical runtime entrypoints

1. `worker.py` - queue polling, dependency checks, lock acquisition, execution event logging
2. `swarm.py` - `/grind` execution API (`llm` + `local`), `/plan`, `/status`
3. `control_panel.py` - human control and observability surface

## Explicitly non-canonical (experimental)

- `swarm_orchestrator_v2.py`
- `worker_pool.py`

These files are not part of the production import path and should be treated as
experimental until repaired and re-validated.

## Task/event contract

- Queue contract is normalized via `runtime_contract.py`:
  - required top-level keys: `version`, `api_endpoint`, `tasks`, `completed`, `failed`
  - task defaults: `type=grind`, `depends_on=[]`, `parallel_safe=true`, `status=pending`
- Execution events are appended to `execution_log.jsonl` from `worker.py` and use
  the canonical status vocabulary in `runtime_contract.KNOWN_EXECUTION_STATUSES`.
- Post-execution review lifecycle is now explicit in the worker path:
  - `pending_review` -> `approved` for accepted outputs
  - `pending_review` -> `requeue` (or `failed` after retry limit) for rejected outputs
  - quality-gate state is mirrored in `quality_gate_queue.json` (`needs_qa` / `rejected`)
- Tool-first routing lifecycle is now explicit in the worker path:
  - prompt tasks are routed through `tool_router` before `/grind` LLM dispatch
  - matched tool context is injected into the prompt for reuse-first execution
  - route metadata is recorded in execution events (`tool_route`, `tool_name`, `tool_confidence`)
- Intent-preserving planning lifecycle is now explicit in the worker path:
  - prompt tasks are checked with deterministic Phase 4 gut-check heuristics
  - complex tasks are atomized into dependency-aware queue subtasks before execution
  - extracted intent is persisted and injected into downstream prompts to reduce drift

## Safety and budget guarantees in this path

- Worker preflight safety: `SafetyGateway.pre_execute_safety_check(...)` is called
  before task dispatch in `worker.py`.
- API safety defense-in-depth: `/grind` runs safety checks again in `swarm.py`.
- LLM calls route through `SecureAPIWrapper` for:
  - rate limiting
  - budget enforcement
  - audit logging
- `mode=local` commands are evaluated against explicit allowlist + denylist policy.

## Smoke checks

```bash
python3 -m py_compile worker.py swarm.py control_panel.py runtime_contract.py
pytest -q tests/test_runtime_phase0_phase1.py tests/test_runtime_phase2_quality_review.py tests/test_runtime_phase3_tool_routing.py tests/test_runtime_phase4_intent_decomposition.py
```
