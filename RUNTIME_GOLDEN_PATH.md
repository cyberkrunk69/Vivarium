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
pytest -q tests/test_runtime_phase0_phase1.py
```
