# Quick Reference Card - All Commands

## brain.py
| Command | Description | Example |
|---------|-------------|---------|
| `python brain.py health` | Check swarm health status | `python brain.py health` |
| `python brain.py grind --budget AMOUNT` | Start a grind with specified budget | `python brain.py grind --budget 0.10` |

## orchestrator.py
| Command | Description | Example |
|---------|-------------|---------|
| `python orchestrator.py start [N]` | Start orchestrator with N workers (default: 4) | `python orchestrator.py start 8` |
| `python orchestrator.py status` | Show execution status summary | `python orchestrator.py status` |
| `python orchestrator.py add <id> <type>` | Add task to queue | `python orchestrator.py add task_001 grind` |
| `python orchestrator.py add <id> <type> --min X --max Y` | Add task with budget range | `python orchestrator.py add task_001 grind --min 0.05 --max 0.10` |
| `python orchestrator.py add <id> <type> --intensity LEVEL` | Add task with intensity (low/medium/high) | `python orchestrator.py add task_001 grind --intensity high` |
| `python orchestrator.py clear` | Clear all tasks, logs, and locks | `python orchestrator.py clear` |

## worker.py
| Command | Description | Example |
|---------|-------------|---------|
| `python worker.py run` | Start worker, run until no tasks (default) | `python worker.py run` |
| `python worker.py run [N]` | Start worker, execute max N tasks | `python worker.py run 5` |
| `python worker.py add <id> <instruction>` | Add task programmatically | `python worker.py add task_001 "Run unit tests"` |
| `python worker.py add <id> <instruction> <deps>` | Add task with dependencies (comma-separated) | `python worker.py add task_002 "Deploy" task_001` |

## grind_spawner.py
| Command | Description | Example |
|---------|-------------|---------|
| `python grind_spawner.py --task "TEXT"` | Spawn 1 session with task (default) | `python grind_spawner.py --task "Fix UI bugs"` |
| `python grind_spawner.py --sessions N --task "TEXT"` | Spawn N parallel sessions with same task | `python grind_spawner.py --sessions 5 --task "Add docs"` |
| `python grind_spawner.py --model MODEL --task "TEXT"` | Specify model: haiku (default), sonnet, opus | `python grind_spawner.py --model opus --task "Refactor"` |
| `python grind_spawner.py --budget AMOUNT --task "TEXT"` | Set budget per session | `python grind_spawner.py --budget 0.10 --task "Test"` |
| `python grind_spawner.py --workspace PATH --task "TEXT"` | Target specific repo | `python grind_spawner.py --workspace D:/repo --task "Docs"` |
| `python grind_spawner.py --delegate` | Read tasks from grind_tasks.json | `python grind_spawner.py --delegate --model opus` |
| `python grind_spawner.py --once --task "TEXT"` | Run once per session, no respawn | `python grind_spawner.py --once --task "Quick fix"` |

## Key Configuration Files
| File | Purpose |
|------|---------|
| `queue.json` | Task queue (orchestrator reads/workers read) |
| `execution_log.json` | Task execution status and progress |
| `task_locks/` | Lock files for parallel coordination |
| `grind_logs/` | Session output logs (spawner only) |
| `grind_tasks.json` | Delegation task list (spawner only) |
| `runs.json` | Historical run records (brain only) |

## Quick Start Workflows

### Single Sequential Task
```
python orchestrator.py clear
python orchestrator.py add task_001 grind --min 0.05 --max 0.10
python orchestrator.py start 1
```

### Parallel Multi-Worker Tasks
```
python orchestrator.py clear
python orchestrator.py add task_001 grind
python orchestrator.py add task_002 grind
python orchestrator.py start 4
```

### Spawner Delegation Mode
```
# Create grind_tasks.json with task list
python grind_spawner.py --delegate --model opus --budget 0.20
```

### Check System Status
```
python brain.py health
python orchestrator.py status
```
