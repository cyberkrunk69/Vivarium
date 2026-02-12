# EXAMPLE_swarm_state — Bootstrap Template

This directory is the **committed reference** for minimal `.swarm` state structure.

**Never commit** the actual runtime directory: `vivarium/world/mutable/.swarm/`

Runtime creates `.swarm/` at bootstrap via `ensure_scope_layout()` and seeds
`resident_days.json`, `identity_locks.json`, and `identities/` on first use
or fresh reset. This EXAMPLE exists so new clones have a canonical structure.
