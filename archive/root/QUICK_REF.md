# Quick Reference Card - All Commands

## resident runtime (worker.py)
| Command | Description | Example |
|---------|-------------|---------|
| `python worker.py run` | Start resident runtime, run until no tasks (default) | `python worker.py run` |
| `python worker.py run [N]` | Start resident runtime, execute max N tasks | `python worker.py run 5` |
| `python worker.py add <id> <instruction>` | Add task programmatically | `python worker.py add task_001 "Run unit tests"` |
| `python worker.py add <id> <instruction> <deps>` | Add task with dependencies (comma-separated) | `python worker.py add task_002 "Deploy" task_001` |

## swarm API (swarm.py)
| Command | Description | Example |
|---------|-------------|---------|
| `uvicorn swarm:app --host 127.0.0.1 --port 8420` | Start local execution API | `uvicorn swarm:app --host 127.0.0.1 --port 8420` |
| `curl http://127.0.0.1:8420/status` | Check queue/runtime API status | `curl http://127.0.0.1:8420/status` |

## Key Configuration Files
| File | Purpose |
|------|---------|
| `queue.json` | Task queue (residents read; humans or /plan write) |
| `execution_log.jsonl` | Task execution status and progress |
| `task_locks/` | Lock files for parallel coordination |
| `runtime_contract.py` | Canonical queue contract and status vocabulary |
| `RUNTIME_GOLDEN_PATH.md` | Golden-path invariants and operations |

## Quick Start Workflows

### Single Sequential Task
```
rm -f task_locks/*.lock
> execution_log.jsonl
python worker.py add task_001 "Run unit tests"
python worker.py run 1
```

### Parallel Multi-Resident Tasks
```
rm -f task_locks/*.lock
> execution_log.jsonl
python worker.py add task_001 "Audit safety rules"
python worker.py add task_002 "Review API docs"
python worker.py run
```

### Check System Status
```
curl http://127.0.0.1:8420/status
```
