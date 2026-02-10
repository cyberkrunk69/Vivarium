# Vivarium Usage Guide

This guide covers common workflows for the Vivarium parallel task orchestration system.

## Architecture Overview

- **swarm.py** - FastAPI server with `/grind`, `/plan`, and `/status` endpoints
- **worker.py** - Resident runtime that claims and executes tasks using file locks
- **queue.json** - Shared task board
- **task_locks/** - Atomic lock files for parallel coordination
- **execution_log.jsonl** - Append-only task events

## Prerequisites

```bash
pip install fastapi uvicorn httpx pydantic python-dotenv
```

For AI-powered task planning, set your Groq API key:
```bash
export GROQ_API_KEY=your_key_here
```

---

## Workflow 1: Manual Task Execution (Volunteer Pull)

Add tasks manually and run residents to execute them.

## Scaling knobs (for large resident counts)
- RESIDENT_SHARD_COUNT: divide queue into shards by task id hash.
- RESIDENT_SHARD_ID: fixed shard id or "auto" (default).
- RESIDENT_SCAN_LIMIT: cap tasks scanned per loop (0 = full scan).
- RESIDENT_SUBTASK_PARALLELISM: parallelism for delegated subtasks.
- RESIDENT_BACKOFF_MAX / RESIDENT_JITTER_MAX: tune idle backoff.

### Step 1: Clear Previous State (optional)
```bash
rm -f task_locks/*.lock
> execution_log.jsonl
```

### Step 2: Add Tasks
```bash
# Basic task
python worker.py add task_001 "Summarize current errors"

# Add multiple tasks
python worker.py add task_002 "Audit safety rules"
python worker.py add task_003 "Refactor queue handling"
```

### Step 3: Start the API Server
```bash
python swarm.py
# Server runs at http://127.0.0.1:8420
```

### Step 4: Run Resident Runtimes (in other terminals)
```bash
python worker.py run
```
Run as many resident processes as you want in parallel.

### Step 5: Check Status
```bash
curl http://127.0.0.1:8420/status
```

---

## Workflow 2: AI-Powered Task Planning

Let Groq analyze your codebase and generate improvement tasks.

### Step 1: Start the API Server
```bash
python swarm.py
```

### Step 2: Trigger Planning (in another terminal)
```bash
curl -X POST http://127.0.0.1:8420/plan
```

This will:
1. Scan all `.py` files in the workspace
2. Send metadata to Llama 3.3 70B for analysis
3. Write 3-5 improvement tasks to `queue.json`

### Step 3: Run Resident Runtimes
```bash
python worker.py run
```

---

## Workflow 3: Single Resident Session

Run a single resident session for debugging or lightweight tasks.

```bash
# Run indefinitely until no tasks remain
python worker.py run

# Run for exactly 5 tasks
python worker.py run 5
```

---

## Workflow 4: Check Execution Progress

### Via API
```bash
curl http://127.0.0.1:8420/status
```

### View Execution Log
```bash
cat execution_log.jsonl
```

Sample output (JSONL entries):
```json
{"task_id":"task_001","worker_id":"worker_a1b2c3d4","status":"in_progress","timestamp":"2024-01-15T10:30:00+00:00"}
{"task_id":"task_001","worker_id":"worker_a1b2c3d4","status":"completed","timestamp":"2024-01-15T10:30:05+00:00"}
```

---

## Workflow 5: Handle Failed Tasks

### Identify Failures
Review `execution_log.jsonl` for failed statuses.

### Clear Stale Locks
If resident sessions crashed, locks may be stale. They auto-expire after 5 minutes, or:
```bash
rm task_locks/*.lock
```

### Retry Failed Tasks
1. Check `execution_log.jsonl` for failed task IDs
2. Reset their status manually or clear and re-add
3. Run residents again

---

## Workflow 6: Control Panel UI (Web)

Use the control panel for real-time monitoring, budgets, and spawner controls.

### Step 1: Install UI dependencies
```bash
pip install -r requirements-groq.txt
pip install watchdog
```

### Step 2: Start the UI
```bash
python control_panel.py
```
Open http://localhost:8421

### Step 3: Use the UI
- START launches the spawner with the current settings (sessions, budget, model).
- PAUSE DAY toggles pause/resume for the spawner.
- STOP triggers an emergency kill for the spawner process.
- Budget & Model lets you adjust sessions/budget/model and Save Config.
- The sidebar shows identities, collaboration requests, messages, chat rooms,
  and bounties.

### One-click scripts (bash/batch)
- macOS/Linux: `./one_click_server.sh` (or `bash one_click_server.sh`)
- Windows: `one_click_server.bat`

---

## File Reference

| File | Purpose |
|------|---------|
| `queue.json` | Task queue (read by residents, written by humans or /plan) |
| `execution_log.jsonl` | Task status and progress tracking |
| `task_locks/*.lock` | File-based locks for parallel coordination |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/grind` | POST | Execute a grind task with budget params |
| `/plan` | POST | AI-analyze codebase and create tasks |
| `/status` | GET | Get current queue status counts |

### Example: /grind Request
```bash
curl -X POST http://127.0.0.1:8420/grind \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize the resident queue design"}'
```

Response:
```json
{
  "status": "completed",
  "result": "Grind completed with intensity=medium",
  "budget_used": 0.0723
}
```

---

## Troubleshooting

### "Cannot connect to API"
- Ensure `swarm.py` is running: `python swarm.py`
- Check it's on port 8420: `curl http://127.0.0.1:8420/status`

### Residents Exit Immediately
- Check `queue.json` has tasks: `cat queue.json`
- Verify tasks aren't already completed in `execution_log.jsonl`

### Stale Locks
- Locks auto-expire after 5 minutes
- Manual removal: `rm task_locks/*.lock`

### Groq API Errors
- Verify `GROQ_API_KEY` is set
- Check API response in server logs
