# Vivarium Next Evolution Roadmap (Fresh Context)

**Updated:** 2026-02-10  
**Baseline branch state:** `cursor/vivarium-next-steps-a3c1`  
**Canonical runtime:** `control_panel.py` (localhost UI) -> `worker.py` -> `swarm.py` (internal token + loopback-only)

---

## Scope for this cycle

### In scope
- Make the **UI** the practical operator entrypoint for normal task flow.
- Keep execution **localhost-only** and hardened.
- Improve operator visibility and reliability of the canonical worker path.
- Provide tests and docs so future agents can continue with low discovery overhead.

### Explicitly out of scope
- Multi-user / LAN expansion.
- Reintroducing non-local exposure modes.
- Big-bang orchestration rewrites.

---

## Ordered execution plan

Primary task file: **`grind_tasks.json`**

| Order | Task ID | Outcome | Primary files to open first |
|---|---|---|---|
| 0 | `ctx-bootstrap-00` | Establish clean cycle context before coding | `README.md`, `CURRENT_CAPABILITIES.md`, `RUNTIME_GOLDEN_PATH.md`, `control_panel.py`, `worker.py`, `swarm.py` |
| 1 | `ui-golden-01-queue-intake` | UI can create/edit queue tasks safely | `control_panel.py`, `runtime_contract.py`, `vivarium_scope.py`, `worker.py` |
| 2 | `ui-golden-02-worker-lifecycle` | UI controls canonical worker process | `control_panel.py`, `worker.py`, `grind_spawner_unified.py` |
| 3 | `ui-golden-03-execution-timeline` | UI shows real task lifecycle timeline | `control_panel.py`, `worker.py`, `runtime_contract.py` |
| 4 | `ui-golden-04-backend-status-proxy` | UI gets runtime status via backend-safe token handling | `control_panel.py`, `swarm.py`, `vivarium_scope.py` |
| 5 | `ui-golden-05-security-polish` | Tighten UI security posture while preserving localhost-only behavior | `control_panel.py`, `README.md` |
| 6 | `ui-golden-06-tests` | Test coverage for UI-first hardened path | `tests/test_runtime_phase0_phase1.py`, `control_panel.py`, `swarm.py`, `worker.py` |
| 7 | `ui-golden-07-docs-and-handoff` | Docs + runbook finalized for next agent loop | `README.md`, `CURRENT_CAPABILITIES.md`, `RUNTIME_GOLDEN_PATH.md`, `vivarium/SCOPE_LAYOUT.md`, `vivarium_rollback.py` |

---

## Agent startup protocol (fast path)

1. Read this file and `grind_tasks.json`.
2. Start with the first `pending` task whose dependencies are complete.
3. Open **only** files listed in that task's `relevant_file_context` initially.
4. Run targeted `rg` probes from that task's `pre_execution_exploration` before editing.
5. Implement minimally, verify, then update docs/tests as required by `done_criteria`.

---

## Safety and architecture guardrails

- Keep control panel and API paths **loopback-only**.
- Never expose internal execution token to browser JS.
- Keep writes constrained to mutable world scope.
- Treat LAN/multi-user as deferred roadmap work, not active implementation.
- Preserve canonical path: UI -> worker -> swarm.

---

## Success criteria for this roadmap cycle

- Human operators can run normal task flow entirely from localhost UI.
- Queue intake and worker lifecycle are observable and usable without CLI.
- Security constraints remain strict and tested.
- Documentation is clean enough for a new agent to start in minutes.

