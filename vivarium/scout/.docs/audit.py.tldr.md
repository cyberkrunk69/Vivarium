<!-- FACT_CHECKSUM: d8c9359a81a478a800e5c1470cda0604799759975242dd772f19453b22c4221a -->

## Module Constants
- `logger`: (used at lines 231)
- `DEFAULT_AUDIT_PATH`: Path('~/.scout/audit.jsonl').expanduser() (used at lines 70)
- `EVENT_TYPES`: frozenset({'nav', 'brief', 'cascade', 'validation_fail', 'budget', 'skip', 'trigger', 'tldr', 'tldr_auto_generated', 'deep', 'doc_sync', 'commit_draft', 'pr_snippet', 'impact_analysis', 'module_brief', 'pr_synthesis', 'roast_with_docs'}) (used at lines (none))
- `FSYNC_EVERY_N_LINES`: 10 (used at lines 126)
- `FSYNC_INTERVAL_SEC`: 1.0 (used at lines 127)
- `ROTATION_SIZE_BYTES`: 10 * 1024 * 1024 (used at lines 97)
- `_SESSION_ID`: None (used at lines 53, 55)
- `_SESSION_LOCK`: threading.Lock() (used at lines 52)

# AuditLog
Class for managing audit logs.

## Constants
- `name`: (used at lines (none))

## Methods
- `__init__`: 
- `_ensure_open`: 
- `_maybe_rotate`: 
- `_close_file`: 
- `_fsync_if_needed`: 
- `log`: 
- `_iter_lines`: 
- `_parse_line`: 
- `query`: 
- `hourly_spend`: 
- `last_events`: 
- `accuracy_metrics`: 
- `gate_metrics`: 
- `flush`: 
- `close`: 
- `__enter__`: 
- `__exit__`: