# Legacy Swarm Generation

This folder contains legacy swarm-generation and orchestration scripts that were
previously at the repository root.

## Why this exists

- Keeps historical scripts available for compatibility and archaeology.
- Prevents old swarm-generation code from polluting the root runtime surface.
- Makes room for a clean `swarm_environment/` path for new swarm interactions.

## Notes

- Root-level compatibility shims remain for old entrypoints (`grind_spawner.py`,
  `grind_spawner_unified.py`, `spawn_opus.py`, etc.).
- New development should not add features here unless the change is explicitly a
  legacy compatibility fix.

