<!-- FACT_CHECKSUM: 7429377021be07c09da1f5ed10e921adbe8c3e6cbff878ab665d0c3c1682aeae -->

# ELIV
This module provides activity logging.

## Constants

### Configuration Constants

* `DEFAULT_AUDIT_PATH`: `Path('~/.scout/audit.jsonl').expanduser()`
  * Used at lines: 70
* `EVENT_TYPES`: `frozenset({'nav', 'brief', 'cascade', 'validation_fail', 'budget', 'skip', 'trigger', 'tldr', 'tldr_auto_generated', 'deep', 'doc_sync', 'commit_draft', 'pr_snippet', 'impact_analysis', 'module_brief', 'pr_synthesis', 'roast_with_docs'})`
  * Used at lines: (none)
* `FSYNC_EVERY_N_LINES`: `10`
  * Used at lines: 126
* `FSYNC_INTERVAL_SEC`: `1.0`
  * Used at lines: 127
* `ROTATION_SIZE_BYTES`: `10 * 1024 * 1024`
  * Docstring: 10MB
  * Used at lines: 97

### Implementation Constants

* `_SESSION_ID`: `None`
  * Type: `Optional[str]`
  * Used at lines: 53, 55
* `_SESSION_LOCK`: `threading.Lock()`
  * Used at lines: 52

## Methods

### AuditLog Class Methods

* `__init__`: `def __init__(self, path: Path=None)`
  * Semantic role: implementation
  * Used at lines: (none)
* `_ensure_open`: (no docstring)
  * Used at lines: (none)
* `_maybe_rotate`: (no docstring)
  * Used at lines: (none)
* `_close_file`: (no docstring)
  * Used at lines: (none)
* `_fsync_if_needed`: (no docstring)
  * Used at lines: (none)
* `log`: (no docstring)
  * Used at lines: (none)
* `_iter_lines`: (no docstring)
  * Used at lines: (none)
* `_parse_line`: (no docstring)
  * Used at lines: (none)
* `query`: (no docstring)
  * Used at lines: (none)
* `hourly_spend`: (no docstring)
  * Used at lines: (none)
* `last_events`: (no docstring)
  * Used at lines: (none)
* `accuracy_metrics`: (no docstring)
  * Used at lines: (none)
* `gate_metrics`: (no docstring)
  * Used at lines: (none)
* `flush`: (no docstring)
  * Used at lines: (none)
* `close`: (no docstring)
  * Used at lines: (none)
* `__enter__`: (no docstring)
  * Used at lines: (none)
* `__exit__`: (no docstring)
  * Used at lines: (none)

### Functions

* `_get_session_id`: `def _get_session_id() -> str`
  * Docstring: Return uuid4 session ID, one per process.
  * Semantic role: implementation
  * Used at lines: 172

## Control Flow

* `logger`: `logging.getLogger(__name__)`
  * Purpose hint: audit logging
  * Semantic role: configuration
  * Used at lines: 231