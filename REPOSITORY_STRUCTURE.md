# Repository Structure

This repository is organized around a strict golden runtime path.

## Top-level domains

- `physics/`
  - Swarm-world invariants and control surface (`world_physics.py`) plus
    shared math primitives.
- `swarm_environment/`
  - Fresh, isolated environment API for new swarm interaction.
- `vivarium/world/`
  - Persistent world state roots for runtime-controlled mutable/fresh spaces.

## Golden path policy

Canonical runtime execution is:
`worker.py` + `swarm.py` + `control_panel.py`

No optional detached runner path is considered canonical for production flow.

## New work policy

- New runtime features should target `swarm_environment/` and canonical runtime
  entrypoints (`worker.py`, `swarm.py`).
- New constraints and controls should be expressed in `physics/world_physics.py`.

