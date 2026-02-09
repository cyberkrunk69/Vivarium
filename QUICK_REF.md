# Quick Reference Card - All Commands

## brain.py
| Command | Description | Example |
|---------|-------------|---------|
| `python brain.py health` | Check swarm health status | `python brain.py health` |
| `python brain.py grind --budget AMOUNT` | Start a grind with specified budget | `python brain.py grind --budget 0.10` |

## resident runtime (worker.py)
| Command | Description | Example |
|---------|-------------|---------|
| `python worker.py run` | Start resident runtime, run until no tasks (default) | `python worker.py run` |
| `python worker.py run [N]` | Start resident runtime, execute max N tasks | `python worker.py run 5` |
| `python worker.py add <id> <instruction>` | Add task programmatically | `python worker.py add task_001 "Run unit tests"` |
| `python worker.py add <id> <instruction> <deps>` | Add task with dependencies (comma-separated) | `python worker.py add task_002 "Deploy" task_001` |

## grind_spawner_unified.py
| Command | Description | Example |
|---------|-------------|---------|
| `python grind_spawner_unified.py --task "TEXT"` | Spawn 1 session with task (default) | `python grind_spawner_unified.py --task "Fix UI bugs"` |
| `python grind_spawner_unified.py --sessions N --task "TEXT"` | Spawn N parallel sessions with same task | `python grind_spawner_unified.py --sessions 5 --task "Add docs"` |
| `python grind_spawner_unified.py --model MODEL --task "TEXT"` | Specify Groq model | `python grind_spawner_unified.py --model llama-3.3-70b-versatile --task "Refactor"` |
| `python grind_spawner_unified.py --budget AMOUNT --task "TEXT"` | Set budget per session | `python grind_spawner_unified.py --budget 0.10 --task "Test"` |
| `python grind_spawner_unified.py --workspace PATH --task "TEXT"` | Target specific repo | `python grind_spawner_unified.py --workspace D:/repo --task "Docs"` |
| `python grind_spawner_unified.py --delegate` | Read tasks from grind_tasks.json | `python grind_spawner_unified.py --delegate --model llama-3.3-70b-versatile` |
| `python grind_spawner_unified.py --once --task "TEXT"` | Run once per session, no respawn | `python grind_spawner_unified.py --once --task "Quick fix"` |

## Key Configuration Files
| File | Purpose |
|------|---------|
| `queue.json` | Task queue (residents read; humans or /plan write) |
| `execution_log.jsonl` | Task execution status and progress |
| `task_locks/` | Lock files for parallel coordination |
| `grind_logs/` | Session output logs (spawner only) |
| `grind_tasks.json` | Delegation task list (spawner only) |
| `runs.json` | Historical run records (brain only) |

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

### Spawner Delegation Mode
```
# Create grind_tasks.json with task list
python grind_spawner_unified.py --delegate --model llama-3.3-70b-versatile --budget 0.20
```

### Check System Status
```
python brain.py health
curl http://127.0.0.1:8420/status
```
