# Physics

Swarm-world invariants and simulation controls.

Modules:

- `world_physics.py`
  - Immutable swarm-world properties (state layout, contract versions, status
    vocabulary).
  - Runtime control surface for queue/task payload bounds.
- `math_utils.py`
  - Shared vector similarity, distance, normalization, and utility transforms
    used by ranking and intent systems.

This folder is intentionally independent from legacy swarm generation code and
is the canonical location for swarm-simulation world rules.

