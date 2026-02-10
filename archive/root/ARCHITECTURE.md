# Vivarium Architecture (Volunteer Community Model)

## System Overview

Vivarium is a volunteer-first system: tasks are posted to a shared queue and
residents self-select what to do. There is no mandatory central coordinator.

```
┌──────────────────────────────────────────────────────────────────────┐
│                           TASK BOARD                                 │
│  queue.json  +  task_locks/*  +  execution_log.jsonl                 │
└──────────────────────────────────────────────────────────────────────┘
                 ▲                                  ▲
                 │                                  │
                 │                                  │
┌────────────────┴───────────────┐       ┌──────────┴───────────┐
│ Resident Runtime(s)            │       │ Optional Planning    │
│ worker.py run                  │       │ /plan (swarm.py)     │
│ - Claims tasks via lock files  │       │ - Groq task planning │
│ - Calls /grind                 │       │ - Writes queue.json  │
└───────────────────────────────┘       └──────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                            SWARM API                                 │
│  swarm.py                                                            │
│  - /grind (Groq or local execution)                                  │
│  - /status                                                           │
└──────────────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                               GROQ                                   │
└──────────────────────────────────────────────────────────────────────┘
```

## Core Components

- **queue.json**: Shared task board. Anyone can post tasks (manual edit or CLI helper).
- **task_locks/**: Atomic file locks prevent duplicate execution.
- **execution_log.jsonl**: Append-only task event log.
- **worker.py**: Resident runtimes that pull tasks, lock, execute, and log.
- **swarm.py**: API that executes tasks (Groq LLM or local command).
- **control_panel.py** (optional): UI to monitor, pause, and coordinate runs.

## Data Flow (Community Pull Model)

1. **Task creation**
   - A human posts tasks to queue.json, or
   - `/plan` uses Groq to generate tasks and writes queue.json.
2. **Residents join**
   - Any number of residents run `python worker.py run`.
3. **Lock-based claiming**
   - Residents scan queue.json and acquire `task_locks/<task_id>.lock`.
4. **Execution**
   - Residents call `/grind` with either:
     - LLM prompt (Groq) or
     - Local command (mode = local).
5. **Logging**
   - Residents append events to execution_log.jsonl and release locks.

## Proven Coordination Technique (Locks)

We keep the proven file-lock protocol:
- Atomic lock creation via `O_CREAT | O_EXCL`.
- Stale lock cleanup based on timestamps.
- Clear, observable state in `task_locks/`.

This preserves the reliability of parallel runs without a central controller.

## Ethics & Safety (New Design)

The system is intentionally volunteer-first and consent-based:
- **No coercion**: Residents choose tasks; no forced execution.
- **Transparent audits**: Logs are append-only and human-readable.
- **Budget enforcement**: Hard limits in config and API wrapper.
- **Sandboxing**: File and network safety checks before execution.

## Legacy Note

`orchestrator.py` still exists for backwards compatibility (status/clear helpers),
but it is no longer the intended control plane. The community pull model is the
default architecture.
