# Vivarium Usage Guide

This guide covers common workflows for the Vivarium parallel task orchestration system.

## Architecture Overview

- **swarm.py** - FastAPI server with `/grind`, `/plan`, and `/status` endpoints
- **orchestrator.py** - Spawns and manages parallel worker processes
- **worker.py** - Individual worker that claims and executes tasks using file locks

## Prerequisites

```bash
pip install fastapi uvicorn httpx pydantic python-dotenv
```

For AI-powered task planning, set your Together AI API key:
```bash
export TOGETHER_API_KEY=your_key_here
```

---

## Workflow 1: Manual Task Execution

Add tasks manually and run workers to execute them.

### Step 1: Clear Previous State
```bash
python orchestrator.py clear
```

### Step 2: Add Tasks
```bash
# Basic task
python orchestrator.py add task_001 grind

# Task with custom budget and intensity
python orchestrator.py add task_002 grind --min 0.08 --max 0.15 --intensity high

# Add multiple tasks
python orchestrator.py add task_003 grind --intensity low
python orchestrator.py add task_004 grind --intensity medium
```

### Step 3: Start the API Server
```bash
python swarm.py
# Server runs at http://127.0.0.1:8420
```

### Step 4: Run the Orchestrator (in another terminal)
```bash
# Default: 4 parallel workers
python orchestrator.py start

# Custom worker count
python orchestrator.py start 8
```

### Step 5: Check Status
```bash
python orchestrator.py status
```

---

## Workflow 2: AI-Powered Task Planning

Let Together AI analyze your codebase and generate improvement tasks.

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

### Step 3: Run the Orchestrator
```bash
python orchestrator.py start
```

---

## Workflow 3: Single Worker Execution

Run a single worker for debugging or lightweight tasks.

```bash
# Run indefinitely until no tasks remain
python worker.py run

# Run for exactly 5 tasks
python worker.py run 5
```

---

## Workflow 4: Check Execution Progress

### Via CLI
```bash
python orchestrator.py status
```

### Via API
```bash
curl http://127.0.0.1:8420/status
```

### View Execution Log
```bash
cat execution_log.json
```

Sample output:
```json
{
  "version": "1.0",
  "tasks": {
    "task_001": {
      "worker_id": "worker_a1b2c3d4",
      "status": "completed",
      "started_at": "2024-01-15T10:30:00+00:00",
      "completed_at": "2024-01-15T10:30:05+00:00"
    }
  },
  "swarm_summary": {
    "total_tasks": 4,
    "completed": 3,
    "in_progress": 1,
    "pending": 0,
    "failed": 0
  }
}
```

---

## Workflow 5: Handle Failed Tasks

### Identify Failures
```bash
python orchestrator.py status
# Shows failed tasks with error messages
```

### Clear Stale Locks
If workers crashed, locks may be stale. They auto-expire after 5 minutes, or:
```bash
rm task_locks/*.lock
```

### Retry Failed Tasks
1. Check `execution_log.json` for failed task IDs
2. Reset their status manually or clear and re-add
3. Run orchestrator again

---

## File Reference

| File | Purpose |
|------|---------|
| `queue.json` | Task queue (read by workers, written by orchestrator) |
| `execution_log.json` | Task status and progress tracking |
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
  -d '{"min_budget": 0.05, "max_budget": 0.10, "intensity": "medium"}'
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

### Workers Exit Immediately
- Check `queue.json` has tasks: `cat queue.json`
- Verify tasks aren't already completed in `execution_log.json`

### Stale Locks
- Locks auto-expire after 5 minutes
- Manual removal: `rm task_locks/*.lock`

### Together AI Errors
- Verify `TOGETHER_API_KEY` is set
- Check API response in server logs
