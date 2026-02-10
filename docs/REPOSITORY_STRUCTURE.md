# Repository Structure

This repository is organized around a strict golden runtime path.

## Top-level domains

- `physics/`
  - Swarm-world invariants and control surface (`world_physics.py`) plus
    shared math primitives.
- `swarm_environment/`
  - Fresh, isolated environment API for new swarm interaction.
- `vivarium/runtime/`
  - Canonical runtime modules (safety, quality gates, routing, onboarding,
    enrichment, and queue contracts).
- `vivarium/world/`
  - Persistent world state roots for runtime-controlled mutable/fresh spaces.
- `docs/`
  - Operational references, roadmap, and architecture documentation.

## Golden path policy

Canonical runtime execution is:
`worker.py` + `swarm.py` + `control_panel.py`

No optional detached runner path is considered canonical for production flow.

## New work policy

- New runtime features should target `swarm_environment/` and runtime modules
  under `vivarium/runtime/`, surfaced via canonical entrypoints (`worker.py`,
  `swarm.py`).
- New constraints and controls should be expressed in `physics/world_physics.py`.

