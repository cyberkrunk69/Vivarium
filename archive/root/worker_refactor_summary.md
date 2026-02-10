# Worker.py Production-Ready Refactoring Summary

## Overview
Comprehensive refactoring of `worker.py` to production standards with proper error handling, type hints, logging, and code organization.

## Changes Made

### 1. Constants & Configuration (Lines 1-40)
**What Changed:**
- Moved all magic numbers to module-level constants with descriptive names
- Added type hints to all constants
- Organized constants into logical sections

**Why:**
- Single source of truth for configuration values
- Easy to adjust timeouts, budgets, and thresholds without code search
- Clearer intent (e.g., `LOCK_TIMEOUT_SECONDS` vs hardcoded `300`)

**New Constants:**
- `API_REQUEST_TIMEOUT: float = 120.0` - HTTP request timeout
- `WORKER_CHECK_INTERVAL: float = 2.0` - Delay between queue checks
- `MAX_IDLE_CYCLES: int = 10` - Exit threshold for idle workers
- `DEFAULT_MIN_BUDGET`, `DEFAULT_MAX_BUDGET`, `DEFAULT_INTENSITY` - Task defaults

### 2. Logging System (Lines 42-50)
**What Changed:**
- Added `_log(level: str, message: str)` function for centralized logging
- All `print()` statements replaced with `_log()` calls
- Log format includes ISO timestamp, log level, worker ID

**Why:**
- Distributed workers need synchronized, structured logs
- Timestamps enable performance analysis and debugging
- Log levels (INFO, ERROR, WARN, DEBUG) allow filtering and monitoring
- Single function means logging changes affect entire app

**Example Output:**
```
[2024-02-03T14:23:45.123456+00:00] [INFO] [worker_a1b2c3d4] Acquired lock for task_001
```

### 3. Type Hints (All Functions)
**What Changed:**
- Added type hints to all function parameters and return types
- Used `Dict[str, Any]`, `List[str]`, `Optional[int]` for precise typing
- Return type `-> None` for void functions

**Functions Updated:**
- `ensure_directories() -> None`
- `read_queue() -> Dict[str, Any]`
- `read_execution_log() -> Dict[str, Any]`
- `write_execution_log(log: Dict[str, Any]) -> None`
- `is_lock_stale(lock_path: Path) -> bool`
- `try_acquire_lock(task_id: str) -> bool`
- `execute_task(task: Dict[str, Any], api_endpoint: str) -> Dict[str, Any]`
- `find_and_execute_task(queue: Dict[str, Any]) -> bool`
- `add_task(task_id: str, instruction: str, depends_on: Optional[List[str]] = None) -> None`

**Why:**
- IDE autocomplete and type checking tools can now validate calls
- Documents function contracts without separate documentation
- Catches type errors before runtime (mypy, pyright, IDE inspection)

### 4. Error Handling Improvements

#### File I/O Operations
**Before:**
```python
with open(QUEUE_FILE, "r") as f:
    return json.load(f)
```

**After:**
```python
try:
    if not QUEUE_FILE.exists():
        return {"tasks": [], "completed": [], "failed": []}
    with open(QUEUE_FILE, "r") as f:
        data = json.load(f)
        return data
except (json.JSONDecodeError, IOError) as e:
    _log("ERROR", f"Failed to read queue file: {e}")
    return {"tasks": [], "completed": [], "failed": []}
```

**Why:**
- Corrupted JSON files no longer crash the worker
- Graceful fallback to safe defaults
- Error is logged for debugging

#### HTTP Requests
**Before:**
```python
except httpx.ConnectError:
    return {"status": "failed", ...}
except Exception as e:
    return {"status": "failed", ...}
```

**After:**
```python
except httpx.ConnectError as e:
    error_msg = f"Cannot connect to API at {api_endpoint}: {e}"
    _log("ERROR", error_msg)
    return {"status": "failed", "errors": error_msg}
except httpx.TimeoutException as e:
    error_msg = f"API request timeout: {e}"
    _log("ERROR", error_msg)
    return {"status": "failed", "errors": error_msg}
except Exception as e:
    error_msg = f"Unexpected error executing task: {type(e).__name__}: {e}"
    _log("ERROR", error_msg)
    return {"status": "failed", "errors": error_msg}
```

**Why:**
- Distinguishes between network issues (ConnectError), timeouts (TimeoutException), and other errors
- Detailed error messages include exception type and message
- Different issues can be handled differently (e.g., retry logic)

#### File Operations (Locks)
**New:**
```python
try:
    if lock_path.exists():
        lock_path.unlink()
except OSError as e:
    _log("ERROR", f"Failed to release lock ({task_id}): {e}")
```

**Why:**
- OSError covers Windows-specific file permission issues
- Non-fatal error (allows worker to continue even if lock cleanup fails)
- Logged for debugging

#### Main Entry Point
**Before:**
```python
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "add" and len(sys.argv) >= 4:
            ...
        else:
            print("Usage: ...")
    else:
        worker_loop()
```

**After:**
```python
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "add" and len(sys.argv) >= 4:
                deps = sys.argv[4].split(",") if len(sys.argv) > 4 else None
                add_task(sys.argv[2], sys.argv[3], deps)
            elif sys.argv[1] == "run":
                try:
                    max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else None
                    worker_loop(max_iter)
                except ValueError:
                    _log("ERROR", f"Invalid max_iterations: {sys.argv[2]}")
                    sys.exit(1)
            else:
                print("Usage: ...")
                sys.exit(1)
        else:
            worker_loop()
    except KeyboardInterrupt:
        _log("INFO", "Program interrupted")
        sys.exit(0)
    except Exception as e:
        _log("ERROR", f"Fatal error: {type(e).__name__}: {e}")
        sys.exit(1)
```

**Why:**
- Validates CLI input (max_iterations must be numeric)
- Distinguishes KeyboardInterrupt (user action) from errors
- All unhandled exceptions logged before exit
- Clear exit codes (0 = clean exit, 1 = error)

### 5. Worker Loop Robustness (Lines 459-495)
**Before:**
```python
while True:
    if max_iterations and iterations >= max_iterations:
        print(f"[{WORKER_ID}] Reached max iterations ({max_iterations})")
        break

    queue = read_queue()

    if find_and_execute_task(queue):
        iterations += 1
        idle_count = 0
    else:
        idle_count += 1
        if idle_count >= max_idle:
            print(f"[{WORKER_ID}] No tasks available after {max_idle} checks. Exiting.")
            break
        print(f"[{WORKER_ID}] No tasks available, waiting...")
        time.sleep(2)
```

**After:**
```python
while True:
    if max_iterations and iterations >= max_iterations:
        _log("INFO", f"Reached max iterations ({max_iterations})")
        break

    try:
        queue = read_queue()

        if find_and_execute_task(queue):
            iterations += 1
            idle_count = 0
        else:
            idle_count += 1
            if idle_count >= MAX_IDLE_CYCLES:
                _log("INFO", f"No tasks available after {MAX_IDLE_CYCLES} checks. Exiting.")
                break
            _log("INFO", f"No tasks available, waiting... ({idle_count}/{MAX_IDLE_CYCLES})")
            time.sleep(WORKER_CHECK_INTERVAL)
    except KeyboardInterrupt:
        _log("INFO", "Interrupted by user")
        break
    except Exception as e:
        _log("ERROR", f"Unexpected error in worker loop: {type(e).__name__}: {e}")
        idle_count += 1
        if idle_count >= MAX_IDLE_CYCLES:
            break
        time.sleep(WORKER_CHECK_INTERVAL)
```

**Why:**
- Exception inside loop doesn't crash worker, it's logged and retried
- KeyboardInterrupt handled separately for graceful shutdown
- Uses module constants instead of magic numbers
- Proper logging instead of print statements

### 6. Documentation Cleanup
**What Changed:**
- Removed verbose docstring examples (kept concise descriptions)
- Docstrings now document "what" not "how to use" (readers can infer from type hints)

**Example:**
```python
def get_timestamp() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()
```

**Why:**
- Type hints (`-> str`) make intent clear
- Concise docstrings reduce maintenance burden
- Detailed docstring examples often become outdated

## Code Quality Metrics

| Aspect | Before | After |
|--------|--------|-------|
| Type Hints | ~20% functions | 100% functions |
| Try/Except Blocks | 2 | 10+ |
| Magic Numbers | 6 | 0 |
| Log Calls | print() statements | _log() with levels |
| Error Messages | Basic | Detailed with context |
| Specific Exceptions | 2 types | 6+ types (httpx, OSError, ValueError, etc.) |

## Key Learnings Documented

1. **Type Hints Matter** - Dict[str, Any] and Optional types document data structure explicitly
2. **Centralized Logging** - Single _log() function enables monitoring and debugging of distributed workers
3. **Specific Exception Types** - ConnectError vs TimeoutException vs general Exception allow targeted handling
4. **Constants over Magic Numbers** - LOCK_TIMEOUT_SECONDS is clearer than hardcoded 300
5. **File I/O Resilience** - Graceful fallback to defaults when files are corrupted
6. **OSError Handling** - Windows and Unix file errors need explicit handling
7. **KeyboardInterrupt Separation** - User interruption shouldn't be logged as an error
8. **CLI Input Validation** - Validate and provide feedback at boundaries, not deep in code
9. **Try/Finally for Locks** - Always release locks even if task execution fails (prevented in original with try/finally pattern)
10. **Guard Clauses** - Early return/raise for error conditions reduces nesting

## Testing Recommendations

1. **Test lock timeout** - Simulate stale lock file, verify removal and reacquisition
2. **Test corrupted JSON** - Manually corrupt queue.json, verify graceful fallback
3. **Test network failures** - Mock httpx to raise ConnectError and TimeoutException
4. **Test CLI validation** - Pass non-numeric max_iterations, verify error message
5. **Test concurrent workers** - Run multiple workers simultaneously, verify no race conditions
6. **Test lock cleanup** - Verify locks are released even if execute_task() raises exception

## Files Modified

- **worker.py** - Complete refactoring with all above changes
- **learned_lessons.json** - Added 10 new worker refactoring lessons
- **worker_refactor_summary.md** - This file

## Deployment Notes

- No breaking changes to CLI or function signatures
- Default behavior unchanged (calls with no args still work)
- Production deployment recommended: Use structured logging aggregation to collect worker logs
- Monitor error rates from _log() calls: spikes indicate API issues or lock contention
