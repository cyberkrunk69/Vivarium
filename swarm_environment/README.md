# Fresh Swarm Environment

This folder contains a clean, isolated environment for new swarm interaction.

## Design goals

- No dependency on legacy spawner state/files.
- Explicit state boundaries (`inbox/`, `outbox/`, `state/`, `audit/`, `scratch/`).
- Small, testable API for task queueing and event logging.

## Quick start

```bash
python -m swarm_environment.new_swarm --reset
```

This creates `vivarium/world/fresh_swarm` with a fresh task queue and audit log.

