<!-- FACT_CHECKSUM: 7429377021be07c09da1f5ed10e921adbe8c3e6cbff878ab665d0c3c1682aeae -->

# ELIV
This module provides activity logging.

## Module Constants
- `logger`: (used at lines 231)
- `DEFAULT_AUDIT_PATH`: Path('~/.scout/audit.jsonl').expanduser() (used at line 70)
- `EVENT_TYPES`: frozenset({'nav', 'brief', 'cascade', 'validation_fail', 'budget', 'skip', 'trigger', 'tldr', 'tldr_auto_generated', 'deep', 'doc_sync', 'commit_draft', 'pr_snippet', 'impact_analysis', 'module_brief', 'pr_synthesis', 'roast_with_docs'}) (used at lines (none))
- `FSYNC_EVERY_N_LINES`: 10 (used at line 126)
- `FSYNC_INTERVAL_SEC`: 1.0 (used at line 127)
- `ROTATION_SIZE_BYTES`: 10MB (used at line 97)

# AuditLog
Append-only JSONL event log with line buffering, fsync cadence, and crash recovery.

## Constants
- `_SESSION_ID`: None (used at lines 53, 55)
- `_SESSION_LOCK`: threading.Lock() (used at line 52)

## Methods
- `__init__(self, path: Path=None)`: implementation
- `_ensure_open()`: implementation
- `_maybe_rotate()`: implementation
- `_close_file()`: implementation
- `_fsync_if_needed()`: implementation
- `log()`: implementation
- `_iter_lines()`: implementation
- `_parse_line()`: implementation
- `query()`: implementation
- `hourly_spend()`: implementation
- `last_events()`: implementation
- `accuracy_metrics()`: implementation
- `gate_metrics()`: implementation
- `flush()`: implementation
- `close()`: implementation
- `__enter__()`: implementation
- `__exit__()`: implementation

# _get_session_id
Return uuid4 session ID, one per process.