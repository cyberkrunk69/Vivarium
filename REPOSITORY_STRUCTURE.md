# Repository Structure

This repository has been reorganized to isolate legacy code and keep a clean
surface for new swarm/runtime work.

## Top-level domains

- `physics/`
  - Shared mathematical primitives (`math_utils.py`).
- `legacy_code/`
  - Archived generated artifacts and non-canonical leftovers.
- `legacy_swarm_gen/`
  - Legacy swarm generation/spawner/orchestrator scripts.
- `swarm_environment/`
  - Fresh, isolated environment API for new swarm interaction.

## Compatibility policy

Root-level compatibility shims are preserved for major historical module names
(`grind_spawner.py`, `grind_spawner_unified.py`, `spawn_opus.py`, etc.) so
existing tooling can keep running during transition.

## New work policy

- New runtime features should target `swarm_environment/` and canonical runtime
  entrypoints (`worker.py`, `swarm.py`).
- Legacy fixes only should go under `legacy_swarm_gen/` or `legacy_code/`.

