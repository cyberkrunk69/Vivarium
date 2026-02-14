<!-- FACT_CHECKSUM: d8c9359a81a478a800e5c1470cda0604799759975242dd772f19453b22c4221a -->

## Constants
### AuditLog Class Constants
No constants found for `AuditLog` class.

### Other Constants
#### DEFAULT_AUDIT_PATH
* Value: `Path('~/.scout/audit.jsonl').expanduser()`
* Used at lines: 70

#### EVENT_TYPES
* Value: `frozenset({'nav', 'brief', 'cascade', 'validation_fail', 'budget', 'skip', 'trigger', 'tldr', 'tldr_auto_generated', 'deep', 'doc_sync', 'commit_draft', 'pr_snippet', 'impact_analysis', 'module_brief', 'pr_synthesis', 'roast_with_docs'})`
* Used at lines: (none)

#### FSYNC_EVERY_N_LINES
* Value: `10`
* Used at lines: 126

#### FSYNC_INTERVAL_SEC
* Value: `1.0`
* Used at lines: 127

#### ROTATION_SIZE_BYTES
* Value: `10 * 1024 * 1024`
* Used at lines: 97

#### _SESSION_ID
* Value: `None`
* Type: `Optional[str]`
* Used at lines: 53, 55

#### _SESSION_LOCK
* Value: `threading.Lock()`
* Used at lines: 52

#### logger
* Value: `logging.getLogger(__name__)`
* Used at lines: 231

## Methods
### AuditLog Class Methods
#### __init__
* Used at lines: (none)

#### _ensure_open
* Used at lines: (none)

#### _maybe_rotate
* Used at lines: (none)

#### _close_file
* Used at lines: (none)

#### _fsync_if_needed
* Used at lines: (none)

#### log
* Used at lines: (none)

#### _iter_lines
* Used at lines: (none)

#### _parse_line
* Used at lines: (none)

#### query
* Used at lines: (none)

#### hourly_spend
* Used at lines: (none)

#### last_events
* Used at lines: (none)

#### accuracy_metrics
* Used at lines: (none)

#### gate_metrics
* Used at lines: (none)

#### flush
* Used at lines: (none)

#### close
* Used at lines: (none)

#### __enter__
* Used at lines: (none)

#### __exit__
* Used at lines: (none)

## Control Flow
### Functions
#### _get_session_id
* Used at lines: 172