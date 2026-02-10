# TASK_DEPENDENCY_DESIGN.md
# Task Dependency Gating System Design

## 1. Overview
The Task Dependency Gating System automatically resolves and enforces dependencies between swarm tasks.  
It performs the following pipeline:

1. **Scan** the task queue for pending tasks.  
2. **Identify** explicit dependencies declared by each task.  
3. **Build** a directed‑acyclic graph (DAG) representing those dependencies.  
4. **Execute** all tasks that have no unmet dependencies in parallel.  
5. **Wait** for dependent tasks to finish before launching the next set, dynamically re‑scheduling as tasks complete.

The system is deliberately decoupled from the existing swarm core so it can be added without touching the protected files (`grind_spawner.py`, `orchestrator.py`, `roles.py`, `safety_gateway.py`, `safety_constitutional.py`).

---

## 2. Task Dependency Annotation Format
Tasks are described by a JSON‑compatible Python dictionary.  The only required fields are:

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | `str` | Unique identifier for the task. |
| `payload` | `any` | Arbitrary data the task needs to run (function name, arguments, etc.). |
| `dependencies` | `list[str]` (optional) | List of `task_id`s that **must complete successfully** before this task may start. |
| `metadata` | `dict` (optional) | Additional information (priority, retry policy, etc.). |

**Example**