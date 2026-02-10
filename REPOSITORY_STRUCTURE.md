# Repository Structure

This repository has been reorganized to isolate legacy code and keep a clean
surface for new swarm/runtime work.

## Top-level domains

- `physics/`
  - Swarm-world invariants and control surface (`world_physics.py`) plus
    shared math primitives.
- `legacy_code/`
  - Archived generated artifacts and non-canonical leftovers.
- `legacy_swarm_gen/`
  - Legacy swarm generation/spawner/orchestrator scripts.
- `swarm_environment/`
  - Fresh, isolated environment API for new swarm interaction.

## Compatibility policy

Root-level compatibility shims have been retired. Legacy entrypoints now live
under `legacy_swarm_gen/` and are intentionally isolated from the canonical
runtime surface.

## New work policy

- New runtime features should target `swarm_environment/` and canonical runtime
  entrypoints (`worker.py`, `swarm.py`).
- Legacy fixes only should go under `legacy_swarm_gen/` or `legacy_code/`.

