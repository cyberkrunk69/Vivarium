# Error Handling Audit Report

**Audit Date:** 2026-02-03
**Files Audited:** 7 Python files
**Status:** Analysis Complete

---

## Executive Summary

This audit identified several locations where exceptions could crash the system silently or cause data loss. The codebase has partial error handling but several critical gaps exist, particularly around file I/O operations and JSON parsing.

---

## Critical Issues Found

### 1. **brain.py:21-23** - `save_runs()` lacks error handling
```python
def save_runs(runs):
    with open(RUNS_FILE, "w") as f:
        json.dump(runs, f, indent=2)
```
**Risk:** If file write fails (disk full, permissions), data loss occurs silently.
**Status:** NEEDS FIX

---

### 2. **autopilot.py:41** - Unhandled `FileNotFoundError` and `JSONDecodeError`
```python
queue = json.loads(QUEUE_PATH.read_text())
```
**Risk:** If `queue.json` doesn't exist or is corrupted, the entire cycle crashes.
**Status:** NEEDS FIX

---

### 3. **worker.py:79-80** - `read_queue()` missing `json.JSONDecodeError` handling
```python
with open(QUEUE_FILE, "r") as f:
    return json.load(f)
```
**Risk:** Corrupted queue file will crash the worker.
**Status:** NEEDS FIX

---

### 4. **worker.py:101-102** - `read_execution_log()` missing error handling
```python
with open(EXECUTION_LOG, "r") as f:
    return json.load(f)
```
**Risk:** Corrupted execution log crashes workers.
**Status:** NEEDS FIX

---

### 5. **worker.py:135-136** - `write_execution_log()` no error handling
```python
with open(EXECUTION_LOG, "w") as f:
    json.dump(log, f, indent=2)
```
**Risk:** Write failures lose task state silently.
**Status:** NEEDS FIX

---

### 6. **worker.py:548-549** - `add_task()` file write unprotected
```python
with open(QUEUE_FILE, "w") as f:
    json.dump(queue, f, indent=2)
```
**Risk:** Failed writes lose the new task.
**Status:** NEEDS FIX

---

### 7. **orchestrator.py:44-45** - `read_json()` missing `JSONDecodeError` handling
```python
with open(path) as f:
    return json.load(f)
```
**Risk:** Corrupted JSON files crash the orchestrator.
**Status:** NEEDS FIX

---

### 8. **orchestrator.py:59-60** - `write_json()` no error handling
```python
with open(path, "w") as f:
    json.dump(data, f, indent=2)
```
**Risk:** Write failures silently fail.
**Status:** NEEDS FIX

---

### 9. **orchestrator.py:85-94** - `spawn_worker()` subprocess errors unhandled
```python
result = subprocess.run(
    [sys.executable, str(WORKSPACE / "worker.py"), "run"],
    capture_output=True,
    text=True
)
```
**Risk:** Subprocess exceptions (e.g., worker.py not found) crash the orchestrator.
**Status:** NEEDS FIX

---

### 10. **orchestrator.py:297** - CLI argument parsing unprotected
```python
num = int(sys.argv[2]) if len(sys.argv) > 2 else 4
```
**Risk:** Non-integer argument crashes with `ValueError`.
**Status:** NEEDS FIX

---

### 11. **grind_spawner.py:161-162** - Task file JSON parsing unprotected
```python
with open(TASKS_FILE, "r") as f:
    tasks_data = json.load(f)
```
**Risk:** Corrupted `grind_tasks.json` crashes spawner.
**Status:** NEEDS FIX

---

### 12. **swarm.py:335-336** - `/status` endpoint JSON parsing unprotected
```python
with open(QUEUE_FILE) as f:
    queue = json.load(f)
```
**Risk:** Corrupted queue file crashes the API endpoint.
**Status:** NEEDS FIX

---

### 13. **swarm.py:244-245** - Together API response parsing unprotected
```python
result = response.json()
content = result["choices"][0]["message"]["content"]
```
**Risk:** Malformed API response causes `KeyError` crash.
**Status:** NEEDS FIX

---

## Good Error Handling Already Present

The following locations have appropriate error handling:

| File | Location | Description |
|------|----------|-------------|
| brain.py:13-18 | `load_runs()` | Catches `FileNotFoundError` and `JSONDecodeError` |
| brain.py:28-35 | `health()` | Generic exception handler with user feedback |
| brain.py:42-65 | `grind()` | Generic exception handler with logging |
| autopilot.py:19-26 | `/plan` request | Catches exceptions, returns early |
| autopilot.py:30-38 | `/grind/queue` request | Catches exceptions, prints error |
| autopilot.py:53-62 | Main loop | Catches `KeyboardInterrupt` and general exceptions |
| simple_loop.py:9-20 | Main loop | Catches exceptions per cycle |
| grind_spawner.py:119-124 | `run_once()` | Catches `TimeoutExpired` and general exceptions |
| grind_spawner.py:227-231 | Main | Catches `KeyboardInterrupt` for clean shutdown |
| worker.py:179-188 | `is_lock_stale()` | Catches JSON/key/value errors, treats as stale |
| worker.py:232-240 | `try_acquire_lock()` | Catches `FileExistsError` for atomic lock |
| worker.py:349-384 | `execute_task()` | Catches `ConnectError` and general exceptions |
| swarm.py:166-167 | `scan_codebase()` | Silent exception pass (continues on file read error) |
| swarm.py:248-262 | JSON parsing | Fallback tasks on `JSONDecodeError` |

---

## Recommendations Summary

### High Priority (Risk of Silent Data Loss)
1. All file write operations need try/except with logging
2. JSON parsing operations need `JSONDecodeError` handling

### Medium Priority (Risk of Crash)
3. Subprocess execution needs exception handling
4. CLI argument parsing needs validation
5. External API response parsing needs defensive coding

### Low Priority (Minor Impact)
6. Add structured logging throughout (currently uses print statements)

---

## Statistics

- **Total issues found:** 13 locations needing fixes
- **Good handling present:** 14 locations
- **Error handling coverage:** ~52% (14/27 critical points)

---

## Note

Due to the system configuration constraints, code modifications were not made. This report documents the analysis findings for manual remediation.
