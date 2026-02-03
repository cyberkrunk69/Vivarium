# Codebase Pattern Analysis

## Pattern Inventory

### Execution Patterns (3 competing approaches)
- **simple_loop.py**: Basic sync loop with requests.post + 5s sleep
- **autopilot.py**: Higher-level orchestration with /plan + /grind/queue endpoints
- **orchestrator.py**: ProcessPoolExecutor with file-based task queue + locks
- **grind_spawner.py**: ThreadPoolExecutor with subprocess.run + prompt piping to claude CLI

**Finding**: No unified execution model. Each implements its own task management logic.

### API/Network Patterns
- All use requests or httpx for API calls
- Base URL hardcoded as "http://127.0.0.1:8420" in 6+ files
- No retry logic except grind_spawner (2 retries with 3s delay)
- Timeout values vary: 120s (worker), 300s (orchestrator), 600s (grind_spawner)

### File I/O Patterns
- JSON used for queue, logs, and execution tracking
- orchestrator.py has `read_json()`/`write_json()` utility functions (lines 28-60)
- **Inconsistency**: worker.py reimplements this inline; grind_spawner uses pathlib.read_text()
- No atomic write guarantees except orchestrator's exclusive file creation (os.O_EXCL)

### Coordination Patterns
- **Lock-based** (worker.py): File-based locks with stale timeout (300s), atomic creation
- **Process-based** (orchestrator.py): ProcessPoolExecutor spawning independent workers
- **Thread-based** (grind_spawner.py): ThreadPoolExecutor calling subprocess
- **Queue-based** (swarm.py): Central queue file that workers poll

### Task Status Tracking
Three separate tracking systems:
1. **execution_log.json**: {"tasks": {task_id: {status, worker_id, timestamps, errors}}, "swarm_summary": {counts}}
2. **grind_logs/*.json**: Individual grind session logs with cost data
3. **learning_log.json**: Task type / model / success records

### Configuration Patterns
- Constants defined in module scope: WORKSPACE, QUEUE_FILE, LOCKS_DIR
- Budget parameters: min_budget (default 0.05), max_budget (default 0.10)
- Intensity levels: "low", "medium", "high"
- No config file used; all CLI args or hardcoded

### Error Handling Patterns
- **worker.py**: Detailed - distinguishes ConnectError, timeout, JSON parse errors
- **orchestrator.py**: Minimal - try/except with print statements
- **swarm.py**: Generic - except Exception: print(f"Error: {e}")
- **grind_spawner.py**: Retry logic + max attempts before failing

### Testing Patterns
- **Tested**: orchestrator.py (19 test classes, 50+ tests), worker.py (20 test classes, 60+ tests)
- **Untested**: brain.py, swarm.py, autopilot.py, grind_spawner.py, cost_tracker.py, log_result.py
- **No integration tests** across multiple modules

### Logging Patterns
- **No structured logging** - all use `print()` statements
- **No log levels** - everything printed regardless
- **Worker identification**: WORKER_ID generated per process with uuid.uuid4().hex[:8]
- **Timestamps**: Inconsistent - get_timestamp() in worker vs datetime.now().isoformat() elsewhere

## Consistency Issues Ranked by Severity

### High Priority
1. **API Endpoint Hardcoding** (affects 6+ files)
   - Location: autopilot.py:7, brain.py:9, orchestrator.py, worker.py:410, swarm.py:4, simple_loop.py:4
   - Should use: Environment variable `SWARM_API_ENDPOINT` with fallback to default

2. **JSON I/O Utility Duplication**
   - orchestrator.py has working implementation (lines 28-60)
   - worker.py reimplements inline (lines 61-103)
   - grind_spawner.py uses pathlib directly
   - Should: Extract to `utils.py` and import everywhere

3. **Task Status Tracking Fragmentation**
   - Three separate formats: execution_log, grind_logs, learning_log
   - Makes queries difficult and inconsistent
   - Should: Unified schema in execution_log

### Medium Priority
4. **Lock Protocol Not Used by Orchestrator**
   - orchestrator.py spawns workers but doesn't use task locks
   - worker.py implements full lock protocol but orchestrator bypasses it
   - grind_spawner.py doesn't interact with locks at all
   - Should: Orchestrator acquire lock before worker executes, or use queue-based coordination

5. **Timestamp Handling Inconsistency**
   - worker.py: `get_timestamp()` → ISO with timezone
   - orchestrator.py: `datetime.now(timezone.utc).isoformat()`
   - swarm.py: `datetime.now().isoformat()` (no timezone)
   - Should: Use worker's get_timestamp() everywhere

6. **Configuration Scattering**
   - Budget defaults repeated: orchestrator line 226, worker.execute_task line 343
   - Intensity validation in orchestrator line 336 not enforced elsewhere
   - Should: Create config.py with all constants

### Low Priority
7. **Error Handling Inconsistency**
   - worker.py distinguishes error types; others use generic Exception
   - orchestrator never checks execute_task results in spawn_worker

8. **Test Coverage Gaps**
   - swarm.py, autopilot.py, grind_spawner.py completely untested
   - Missing integration tests between orchestrator → worker flow

## Recommended Shared Utilities to Create

### 1. `utils/config.py`
```python
API_ENDPOINT = os.environ.get('SWARM_API_ENDPOINT', 'http://127.0.0.1:8420')
MIN_BUDGET = 0.05
MAX_BUDGET = 0.10
VALID_INTENSITIES = ["low", "medium", "high"]
LOCK_TIMEOUT_SECONDS = 300
```

### 2. `utils/io.py`
```python
def read_json(path: Path) -> dict
def write_json(path: Path, data: dict)
```

### 3. `utils/logging.py`
```python
def setup_logging(module_name: str, level=logging.INFO)
def log_task(task_id, status, duration, worker_id, errors=None)
```

### 4. `utils/timestamps.py`
```python
def get_timestamp() -> str  # Standardize on worker.py version
def parse_timestamp(ts: str) -> datetime
```

### 5. `models/task.py`
```python
class Task(BaseModel):
    id: str
    type: str
    min_budget: float = MIN_BUDGET
    max_budget: float = MAX_BUDGET
    intensity: str = "medium"
    depends_on: list = []
    parallel_safe: bool = True
    status: str = "pending"
```

## Priority Improvement Order

1. **Extract config.py** (1 file, fixes 6+ hardcodings)
2. **Centralize JSON I/O** (1 file, reduces duplication)
3. **Unify timestamp handling** (3 file changes)
4. **Consolidate status tracking** (add unified schema to execution_log)
5. **Add structured logging** (setup in utils/logging.py, used in all modules)
6. **Implement missing tests** (swarm, autopilot, grind_spawner)
7. **Add integration tests** (orchestrator → worker → swarm flow)
8. **Create shared models** (Task, Result schemas)

## Best Practices Observed

✓ File-based locks with stale detection (worker.py)
✓ Comprehensive docstrings in orchestrator/worker
✓ Separate test files with fixtures
✓ Type hints in function signatures (partial)
✓ Dependency injection in tests via patching

## Anti-Patterns Detected

✗ No structured logging (all print statements)
✗ Hardcoded configuration across multiple files
✗ Three competing execution patterns without abstraction
✗ No error aggregation or reporting
✗ Race conditions possible in concurrent file writes
✗ No graceful shutdown handling in spawned processes
✗ WORKER_ID generated but not coordinated with orchestrator
