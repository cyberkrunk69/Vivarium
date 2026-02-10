# Repository Structure

This repository is organized around a strict golden runtime path.

## Top-level domains

- `vivarium/physics/`
  - Swarm-world invariants and control surface (`world_physics.py`) plus
    shared math primitives.
- `vivarium/swarm_environment/`
  - Fresh, isolated environment API for new swarm interaction.
- `vivarium/runtime/`
  - Canonical runtime modules (safety, quality gates, routing, onboarding,
    enrichment, and queue contracts).
- `vivarium/world/`
  - Persistent world state roots for runtime-controlled mutable/fresh spaces.
- `docs/`
  - Operational references, roadmap, and architecture documentation.

## Golden path policy

Canonical runtime execution enters through package entrypoints:
- `vivarium/runtime/worker_runtime.py`
- `vivarium/runtime/swarm_api.py`
- `vivarium/runtime/control_panel_app.py`

No optional detached runner path is considered canonical for production flow.

## New work policy

- New runtime features should target `vivarium/swarm_environment/` and runtime modules
  under `vivarium/runtime/`.
- New constraints and controls should be expressed in `vivarium/physics/world_physics.py`.

