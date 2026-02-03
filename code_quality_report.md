# Code Quality Report

## Summary

Analyzed 7 Python files for bugs, race conditions, resource leaks, and code smells.

---

## Critical Issues

### 1. Race Condition in Lock Acquisition (`worker.py:214-240`)

**File:** `worker.py` - `try_acquire_lock()`

**Issue:** TOCTOU (time-of-check-time-of-use) race condition. Between checking if the lock is stale (line 217-223) and attempting to create a new lock (line 234), another worker could create the lock first.

```python
if lock_path.exists():
    if is_lock_stale(lock_path):
        lock_path.unlink()  # Race: another worker could unlink too
    else:
        return False

# Gap here - another worker could create lock

try:
    fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
```

**Impact:** Two workers could both remove a stale lock and then race to acquire it. The atomic file creation (O_EXCL) prevents duplicate locks, but the stale lock removal itself is not atomic.

**Fix Difficulty:** Medium - Requires proper lock implementation (e.g., fcntl.flock on Unix, or retry with backoff)

---

### 2. File Not Found Error (`autopilot.py:41`)

**File:** `autopilot.py` - `run_cycle()`

**Issue:** Reading `queue.json` without checking if file exists:

```python
queue = json.loads(QUEUE_PATH.read_text())  # Crashes if file doesn't exist
```

**Impact:** Application crashes if queue.json is missing or was deleted between cycles.

**Fix Difficulty:** Easy

---

### 3. Execution Log Race Condition (`worker.py:443-456`)

**File:** `worker.py` - `find_and_execute_task()`

**Issue:** Read-modify-write on execution log without locking:

```python
execution_log = read_execution_log()           # Read
execution_log["tasks"][task_id].update({...})  # Modify
write_execution_log(execution_log)             # Write
# ... task executes ...
execution_log["tasks"][task_id].update({...})  # Modify again
write_execution_log(execution_log)             # Write again
```

**Impact:** If multiple workers update the log simultaneously, updates can be lost.

**Fix Difficulty:** Medium - Requires file locking or atomic update mechanism

---

## Medium Issues

### 4. Broad Exception Catching (Multiple Files)

**Files:** `brain.py:33`, `autopilot.py:24,37,60`, `simple_loop.py:19`, `grind_spawner.py:122`

**Issue:** Using bare `except Exception as e:` catches all exceptions including KeyboardInterrupt, SystemExit in some contexts.

```python
except Exception as e:
    print(f"Error: {e}")
```

**Impact:** Hides root cause of errors, makes debugging difficult.

**Fix Difficulty:** Easy - Catch specific exceptions

---

### 5. Hardcoded Paths (`swarm.py:22,143`)

**File:** `swarm.py`

**Issue:** Absolute Windows paths hardcoded:

```python
QUEUE_FILE = Path(r"D:\codingProjects\claude_parasite_brain_suck\queue.json")
workspace = Path(r"D:\codingProjects\claude_parasite_brain_suck")
```

**Impact:** Code won't work on other machines or if project is moved.

**Fix Difficulty:** Easy - Use `Path(__file__).parent` like other files

---

### 6. Unused Import (`autopilot.py:2`)

**File:** `autopilot.py`

**Issue:** `subprocess` is imported but never used.

```python
import subprocess  # Never used
```

**Fix Difficulty:** Easy

---

### 7. Unused Variable (`autopilot.py:9,49`)

**File:** `autopilot.py`

**Issue:** `WORKERS = 3` is defined and printed but never used in the logic.

**Fix Difficulty:** Easy - Remove or implement

---

### 8. Missing Comment Step (`autopilot.py:29,42`)

**File:** `autopilot.py` - `run_cycle()`

**Issue:** Steps jump from [2] to [4], missing [3].

```python
print(f"\n[2] Executing tasks via /grind/queue...")
# ... code ...
print(f"\n[4] Results:")  # Step 3 is missing
```

**Fix Difficulty:** Easy

---

### 9. No Timeout Handling (`simple_loop.py`)

**File:** `simple_loop.py`

**Issue:** Infinite loop with no clean exit mechanism except Ctrl+C. No handling of network failures that could leave the loop running indefinitely.

**Fix Difficulty:** Easy - Add max iterations or signal handler

---

### 10. Import Inside Function (`swarm.py:74`)

**File:** `swarm.py` - `grind()`

**Issue:** `import random` inside function instead of at module level:

```python
async def grind(req: GrindRequest):
    import random  # Should be at top
```

**Impact:** Minor performance hit on each call, unconventional style.

**Fix Difficulty:** Easy

---

## Low Priority / Code Smells

### 11. Inconsistent HTTP Libraries

**Issue:** Project uses both `requests` (brain.py, autopilot.py, simple_loop.py) and `httpx` (worker.py, swarm.py).

**Impact:** Inconsistent API usage, larger dependency footprint.

**Recommendation:** Standardize on `httpx` since it supports async.

---

### 12. No Request Retry Logic

**Files:** All HTTP client files

**Issue:** HTTP requests have no retry mechanism for transient failures.

**Recommendation:** Add retry with exponential backoff for network resilience.

---

### 13. Subprocess Without Shell=False Verification (`grind_spawner.py:96-103`)

**File:** `grind_spawner.py`

**Issue:** While `subprocess.run()` is used safely (no shell=True), the `cmd` list is built with user input (`self.model`) that could be manipulated if model validation is weak.

**Recommendation:** Validate model against allowed list.

---

### 14. Daemon Threads Without Cleanup (`grind_spawner.py:218`)

**File:** `grind_spawner.py`

**Issue:** Threads are created as daemons, which means they're killed abruptly on main thread exit. The `session.running = False` signal may not be respected if main thread exits quickly.

```python
t = threading.Thread(target=session.grind_loop, daemon=True)
```

**Fix Difficulty:** Medium - Use non-daemon threads with proper join

---

### 15. ProcessPoolExecutor Max Workers Bug (`grind_spawner.py:209`)

**File:** `grind_spawner.py`

**Issue:** In `--once` mode, `max_workers=args.sessions` but in delegate mode `args.sessions` is ignored (num tasks comes from file).

```python
with ThreadPoolExecutor(max_workers=args.sessions) as executor:
    futures = [executor.submit(s.run_once) for s in sessions]
```

**Impact:** May create more threads than `max_workers` allows to process, causing unnecessary queuing.

**Fix Difficulty:** Easy - Use `len(sessions)` instead

---

## Files Reviewed

| File | Lines | Issues Found |
|------|-------|--------------|
| brain.py | 89 | 1 |
| autopilot.py | 63 | 4 |
| simple_loop.py | 23 | 1 |
| grind_spawner.py | 240 | 3 |
| worker.py | 571 | 2 |
| orchestrator.py | 325 | 0 |
| swarm.py | 348 | 3 |

**Total Issues:** 15 (3 critical, 7 medium, 5 low)

---

## Recommended Priority

1. **Fix race conditions** in worker.py lock handling (Critical)
2. **Add file existence check** in autopilot.py (Easy, prevents crashes)
3. **Fix hardcoded paths** in swarm.py (Easy, portability)
4. **Remove unused imports** and fix step numbering (Easy cleanup)
5. **Standardize HTTP library** to httpx (Cleanup)
