# Utils Integration Guide

## Overview
The `utils.py` module provides shared utilities for JSON operations, timestamp handling, path management, and error formatting. This guide shows how to integrate it into existing files.

## Quick Start

Add import to any file:
```python
from utils import read_json, write_json, get_timestamp, ensure_dir, format_error
```

## Integration by File

### worker.py
**Status**: High priority - contains most duplication

**Changes**:
1. Line 31-43: Replace with import
2. Line 46-58: Replace with `ensure_dir(LOCKS_DIR)`
3. Line 79-80: Replace with `read_json(QUEUE_FILE)`
4. Line 101-102: Replace with `read_json(EXECUTION_LOG)`
5. Line 135-136: Replace with `write_json(EXECUTION_LOG, log)`
6. Line 228: Already uses local `get_timestamp()` - replace with imported version
7. Line 383: Replace `str(e)` with `format_error(e)` in exception handlers

**Before/After Example**:
```python
# BEFORE
def read_queue() -> dict:
    if not QUEUE_FILE.exists():
        return {"tasks": [], "completed": [], "failed": []}
    with open(QUEUE_FILE, "r") as f:
        return json.load(f)

# AFTER
def read_queue() -> dict:
    data = read_json(QUEUE_FILE)
    return data if data else {"tasks": [], "completed": [], "failed": []}
```

### orchestrator.py
**Status**: High priority - has own read_json/write_json

**Changes**:
1. Remove lines 28-61 (read_json, write_json functions)
2. Add import: `from utils import read_json, write_json, ensure_dir, get_timestamp`
3. Line 123: Replace `LOCKS_DIR.mkdir(exist_ok=True)` with `ensure_dir(LOCKS_DIR)`
4. Line 129: Replace `datetime.now(timezone.utc).isoformat()` with `get_timestamp()`

**Before/After Example**:
```python
# BEFORE (local functions)
def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

# AFTER (use imported)
queue = read_json(QUEUE_FILE)
```

### swarm.py
**Status**: Medium priority - uses raw json.dump/load

**Changes**:
1. Line 317-318: Replace with `write_json(QUEUE_FILE, queue)`
2. Line 336-337: Replace with `read_json(QUEUE_FILE)`
3. Line 179-240: Add error handling using `format_error()` in exception blocks

**Before/After Example**:
```python
# BEFORE
with open(QUEUE_FILE, "w") as f:
    json.dump(queue, f, indent=2)

# AFTER
write_json(QUEUE_FILE, queue)
```

### log_result.py
**Status**: Lower priority - minimal JSON ops

**Changes**:
1. Lines 12-15: Replace with `data = read_json(log_file)`
2. Lines 31-32: Replace with `write_json(log_file, data)`
3. Line 19: Replace with `get_timestamp()`

### grind_spawner.py
**Status**: Lower priority - one-off file reads

**Changes**:
1. Lines 78, 166-173: Replace json.load with `read_json()` for consistency
2. Line 137: Replace `str(e)` with `format_error(e)`

### cost_tracker.py
**Status**: Low priority - minimal changes

**Changes**:
1. Lines 14-21: Replace try-except block with `read_json()` call

## Benefits After Integration

| Benefit | Impact |
|---------|--------|
| **Single point of maintenance** | JSON format changes only need fixing in one place |
| **Consistent error handling** | All files handle missing/corrupted JSON the same way |
| **Timezone consistency** | All timestamps are UTC ISO format |
| **Reduced code duplication** | ~150 lines of code eliminated across codebase |
| **Better testability** | Utilities can be unit tested separately |
| **Easier debugging** | Standardized error messages help troubleshooting |

## Implementation Order

1. **Phase 1**: orchestrator.py (remove local functions, add imports)
2. **Phase 2**: worker.py (most duplication, test thoroughly)
3. **Phase 3**: swarm.py (API module, test with /grind endpoint)
4. **Phase 4**: log_result.py, cost_tracker.py, grind_spawner.py (polish)

## Testing

After each integration, verify:
- JSON files created/read correctly
- Timestamps are ISO format
- Directories created with full paths
- Error messages format properly

Example test:
```bash
python worker.py add test_001 "Test task"
python orchestrator.py status
```

## Migration Checklist

- [ ] Import utils in target file
- [ ] Replace function calls with imported versions
- [ ] Remove duplicate functions
- [ ] Remove old imports (json, datetime.timezone) if no longer needed
- [ ] Test file operations (read/write JSON)
- [ ] Test path operations (mkdir calls)
- [ ] Run original test suite if available
