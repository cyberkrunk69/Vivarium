# Vivarium Architecture

## System Overview

ASCII diagram showing the complete architecture from orchestrator spawning workers through API communication and lock-based coordination:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR (orchestrator.py)                  │
│  - Reads queue.json                                                  │
│  - Spawns N workers via ProcessPoolExecutor                         │
│  - Monitors execution_log.json                                      │
└────────────────────────┬────────────────────────────────────────────┘
                         │ spawn_worker() × N
        ┌────────────────┼────────────────┬───────────────┬──────────┐
        │                │                │               │          │
        ▼                ▼                ▼               ▼          ▼
   ┌────────┐       ┌────────┐       ┌────────┐     ┌────────┐  ┌────────┐
   │Worker 0│       │Worker 1│       │Worker 2│     │Worker 3│  │...     │
   │(PID X) │       │(PID Y) │       │(PID Z) │     │(PID W) │  │        │
   └────┬───┘       └────┬───┘       └────┬───┘     └────┬───┘  └────┬───┘
        │                │                │               │          │
        └────────────────┼────────────────┼───────────────┼──────────┘
                         │ read/write via locks
        ┌────────────────┼────────────────┬───────────────┬──────────┐
        │                │                │               │          │
        ▼                ▼                ▼               ▼          ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │              TASK_LOCKS/ Directory                              │
   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
   │  │task_001.lock │  │task_002.lock │  │task_003.lock │  ...     │
   │  │{worker_id,   │  │{worker_id,   │  │{worker_id,   │           │
   │  │started_at}   │  │started_at}   │  │started_at}   │           │
   │  └──────────────┘  └──────────────┘  └──────────────┘           │
   │                                                                  │
   │  PURPOSE: Atomic lock files prevent race conditions             │
   │  - try_acquire_lock() uses O_CREAT|O_EXCL for atomicity        │
   │  - Only ONE worker can hold lock at a time                     │
   │  - Stale locks auto-removed after 5 minutes                    │
   └──────────────────────────────────────┬──────────────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────┐
        │                                 │                         │
        ▼                                 ▼                         ▼
   ┌──────────────┐               ┌──────────────┐          ┌──────────────┐
   │ queue.json   │               │execution_log │          │ SWARM API    │
   │              │               │.json         │          │(swarm.py)    │
   │ {            │               │              │          │              │
   │  "tasks": [  │               │ {            │          │ /grind       │
   │   {id,       │◄──────────────│  "tasks": {  │          │   Execute    │
   │    type,     │  read by      │   "id": {    │          │   tasks      │
   │    status,   │  workers      │    status,   │          │              │
   │    budget}   │               │    worker_id,│──────────│ /plan        │
   │  ]           │               │    result}   │  write   │   Analyze    │
   │ }            │               │  }           │  status  │   code       │
   └──────────────┘               │ }            │          │              │
                                  └──────────────┘          └──────────────┘
                                        ▲                          ▲
                                        │ update status            │ POST
                                        │ after execution          │
                                        └──────────────────────────┘
```

## Data Flow Through the System

```
1. QUEUE POPULATION
   Orchestrator or /plan endpoint
        │
        ▼
   queue.json gets tasks with status="pending"


2. WORKER INITIALIZATION
   Orchestrator spawns ProcessPoolExecutor
        │
        ├─► Worker 0 starts (WORKER_ID = uuid)
        ├─► Worker 1 starts (WORKER_ID = uuid)
        ├─► Worker 2 starts (WORKER_ID = uuid)
        └─► Worker N starts (WORKER_ID = uuid)


3. LOCK-BASED TASK CLAIMING
   Worker reads queue.json
        │
        ▼
   For each task in queue:
        │
        ├─► is_task_done()? Skip if already completed/failed
        │
        ├─► check_dependencies_complete()? Skip if blocked
        │
        ├─► try_acquire_lock(task_id)
        │   ├─► LOCK ACQUIRED: Create task_id.lock file
        │   │   ├─► write lock metadata (worker_id, timestamp)
        │   │   ├─► mark task as "in_progress" in execution_log.json
        │   │   └─► CONTINUE TO EXECUTION
        │   │
        │   └─► LOCK FAILED: Another worker has this task
        │       └─► Skip to next task in queue
        │
        ▼
   Worker continues to next available task


4. TASK EXECUTION
   Worker sends task to Swarm API (/grind endpoint)
        │
        ├─► POST to http://127.0.0.1:8420/grind
        │   with: {min_budget, max_budget, intensity}
        │
        ▼
   API executes task and returns result
        │
        ├─► Success (200): status="completed"
        │
        └─► Failure (non-200): status="failed", errors logged


5. RESULT RECORDING
   Worker updates execution_log.json
        │
        ├─► status: "completed" or "failed"
        ├─► completed_at: timestamp
        ├─► result_summary: from API
        ├─► errors: any error message
        │
        ▼
   release_lock(task_id) - removes lock file
        │
        ▼
   Worker reads updated queue and finds next task


6. ORCHESTRATOR MONITORING
   Orchestrator waits for all workers to complete
        │
        ├─► ProcessPoolExecutor.as_completed()
        │
        ├─► Each worker finishes when queue is empty
        │   (after 10 consecutive idle checks)
        │
        ▼
   show_status() displays final counts:
        ├─► total_tasks
        ├─► completed
        ├─► failed
        ├─► pending (shouldn't exist if all done)
        └─► active locks (shouldn't exist if all done)
```

## Lock Mechanism (Race Condition Prevention)

```
PROBLEM: Multiple workers might try to execute same task simultaneously

SOLUTION: File-based atomic locking

┌──────────────────────────────────────────┐
│ Worker A              Worker B            │
├──────────────────────────────────────────┤
│                                          │
│ try_acquire_lock("task_001")             │
│ ├─► os.open(O_CREAT | O_EXCL)            │
│ │   (atomic create - succeeds!)          │
│ │   ✓ Lock created                       │
│ │   ├─► mark task in_progress            │
│ │   ├─► execute_task()                   │
│ │   ├─► update results                   │
│ │   └─► release_lock()                   │
│ │                                        │
│ └─ Execution time: ~2-10 seconds         │
│                                          │
│                 try_acquire_lock("task_001")
│                 ├─► os.open(O_CREAT | O_EXCL)
│                 │   (atomic create - FAILS!)
│                 │   ✗ FileExistsError
│                 │   (Worker A has the lock)
│                 │
│                 └─ Skip to next task
│
└──────────────────────────────────────────┘

KEY PROPERTIES:
✓ Atomic: OS guarantees only one success
✓ Self-healing: Stale locks removed after 5min timeout
✓ Simple: File existence = lock held
✓ Observable: Lock files list current work
```

## Component Interactions

```
ORCHESTRATOR
├─ FUNCTIONS:
│  ├─ start_orchestrator(num_workers)
│  │  └─ Spawns N worker processes via ProcessPoolExecutor
│  │
│  ├─ spawn_worker(worker_id)
│  │  └─ Runs: python worker.py run
│  │     └─ Each worker gets unique WORKER_ID
│  │
│  ├─ add_task(task_id, task_type, budget, intensity)
│  │  └─ Writes to queue.json
│  │
│  ├─ show_status()
│  │  └─ Reads execution_log.json and shows summary
│  │
│  └─ clear_all()
│     └─ Resets queue, logs, and all locks
│
└─ FILES ACCESSED:
   ├─ queue.json (read tasks)
   ├─ execution_log.json (read results)
   └─ task_locks/*.lock (read lock status)


WORKER
├─ FUNCTIONS:
│  ├─ worker_loop()
│  │  └─ Continuous task search & execute loop
│  │     └─ Idle timeout: 10 checks (20 seconds) with no tasks
│  │
│  ├─ find_and_execute_task(queue)
│  │  ├─ Scan queue.json for available task
│  │  ├─ try_acquire_lock() if available
│  │  ├─ execute_task() via API call
│  │  └─ release_lock() when done
│  │
│  ├─ try_acquire_lock(task_id)
│  │  └─ Atomic file creation → task_locks/{task_id}.lock
│  │
│  ├─ execute_task(task, api_endpoint)
│  │  └─ POST to http://127.0.0.1:8420/grind
│  │
│  └─ release_lock(task_id)
│     └─ Delete task_locks/{task_id}.lock file
│
└─ FILES ACCESSED:
   ├─ queue.json (read, READ-ONLY)
   ├─ execution_log.json (read & write task status)
   └─ task_locks/ (create/delete lock files)


SWARM API (swarm.py)
├─ ENDPOINTS:
│  ├─ POST /grind
│  │  └─ Simulates task execution
│  │     └─ Returns: status, result, budget_used
│  │
│  ├─ POST /plan
│  │  └─ Analyzes codebase with Together AI
│  │     └─ Generates new tasks → writes to queue.json
│  │
│  └─ GET /status
│     └─ Returns current queue statistics
│
└─ FILES ACCESSED:
   └─ queue.json (read/write)
```

## Concurrency Safety Guarantees

```
SAFE:
✓ Multiple workers reading queue.json simultaneously
  └─ All workers see same pending tasks, but lock prevents duplicates

✓ Multiple workers reading execution_log.json simultaneously
  └─ JSON reads are atomic at OS level

✓ Lock acquisition (try_acquire_lock)
  └─ OS-level O_CREAT|O_EXCL prevents race conditions

✓ Task status updates via execution_log.json
  └─ Each worker serializes JSON.dump() atomically


NOT SAFE (but controlled):
⚠ Simultaneous writes to execution_log.json from multiple workers
  └─ MITIGATION: Workers write serially, not truly parallel
  └─ Python's json.dump() is atomic per file

⚠ Queue.json modifications during worker execution
  └─ MITIGATION: Orchestrator adds tasks before workers start
  └─ Workers NEVER modify queue.json (read-only)


KEY INVARIANT:
Only ONE worker executes any given task, enforced by lock file.
If lock file exists for task_X, that task is being executed by exactly
one worker. No other worker will attempt to claim it.
```
