# Fresh Swarm Environment

This folder contains a clean, isolated environment for new swarm interaction.

## Design goals

- No dependency on non-canonical runner state/files.
- Explicit state boundaries (`inbox/`, `outbox/`, `state/`, `audit/`, `scratch/`).
- Small, testable API for task queueing and event logging.
- Enforce world invariants and payload controls from `physics/world_physics.py`.

## Quick start

```bash
python -m swarm_environment.new_swarm --reset
```

This creates `vivarium/world/fresh_swarm` with a fresh task queue and audit log.

You can tune control limits at bootstrap time:

```bash
python -m swarm_environment.new_swarm --reset --max-tasks 512 --max-instruction-chars 3000
```

The generated `manifest.json` captures both immutable `world_physics` and the
applied control values.

