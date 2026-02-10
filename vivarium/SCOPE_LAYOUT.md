# Vivarium Scope Layout

This repository now separates runtime world scopes explicitly:

```
vivarium/
  world/
    mutable/        # The only swarm-mutable scope
  meta/
    audit/          # Execution and safety audit trails
    security/       # Security constraints/configuration
    change_control/ # Auto-checkpoint journal + rollback metadata
```

## Design goals

1. **Swarm writes only in `vivarium/world/mutable`**
2. **Security/audit data lives outside swarm mutable scope**
3. **Change record + rollback is automatic for mutable scope**
4. **Separation remains inside one repository for transparency**

## Enforcement points

- `vivarium/runtime/swarm_api.py` local command execution:
  - uses `vivarium/world/mutable` as working directory
  - validates command/path tokens to prevent scope escape
  - allows Git network remotes only for approved hosts
- `vivarium/runtime/worker_runtime.py`:
  - reads queue/locks from mutable scope
  - writes execution logs in `vivarium/meta/audit`
  - auto-checkpoints mutable changes into a dedicated mutable-scope Git repo
- `vivarium_scope.py`:
  - owns canonical paths
  - initializes layout
  - journals checkpoints and rollbacks

## Change journal

Auto-checkpoint/rollback entries are appended to:

`vivarium/meta/change_control/change_journal.jsonl`

This provides a local, append-only operational timeline for mutable-world changes.
