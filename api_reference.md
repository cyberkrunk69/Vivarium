# Vivarium API Reference

## API Overview
- **Title**: Vivarium
- **Version**: 1.0
- **Base URL**: `http://127.0.0.1:8420`
- **Primary execution endpoint**: `/cycle`

---

## Human timescale framing

Vivarium executes in **cycles** and reports progress in compressed human windows:
- **Today**: currently active cycles
- **This week**: grouped outcomes and quality trends
- **Next week**: queued improvements and follow-ups

---

## Auth and locality rules

- `/cycle` and `/plan` are **loopback-only**.
- `/cycle` and `/plan` require:
  - `X-Vivarium-Internal-Token: <token>`
- `/status` is loopback-only (no token required).

---

## Endpoints

### 1) POST /cycle
Execute one cycle task (`llm` or `local` mode).

**Request body (common fields):**
```json
{
  "prompt": "optional llm instruction",
  "task": "optional local command",
  "mode": "llm|local",
  "model": "optional model id",
  "min_budget": 0.05,
  "max_budget": 0.10,
  "intensity": "low|medium|high",
  "task_id": "optional task id"
}
```

**Response (shape):**
```json
{
  "status": "completed|failed",
  "result": "human-readable summary",
  "model": "model used",
  "task_id": "optional echoed id",
  "budget_used": 0.0123,
  "exit_code": 0,
  "safety_report": {
    "passed": true
  }
}
```

**Example (local mode):**
```bash
curl -X POST http://127.0.0.1:8420/cycle \
  -H "Content-Type: application/json" \
  -H "X-Vivarium-Internal-Token: <token>" \
  -d '{"mode":"local","task":"git status","task_id":"cycle_001"}'
```

### 2) POST /plan
Scan the codebase with Groq-backed analysis and write planned tasks to queue.

**Response schema:**
```json
{
  "status": "planned",
  "files_scanned": 3,
  "total_lines": 350,
  "tasks_created": 4
}
```

---

### 3) GET /status
Return queue counts by state.

**Response schema:**
```json
{
  "tasks": 5,
  "completed": 2,
  "failed": 0
}
```

---

## Queue task format (`queue.json`)

```json
{
  "version": "1.1",
  "api_endpoint": "http://127.0.0.1:8420",
  "tasks": [
    {
      "id": "task_001",
      "type": "cycle",
      "prompt": "Task description",
      "min_budget": 0.05,
      "max_budget": 0.15,
      "intensity": "high|medium|low",
      "status": "pending",
      "depends_on": [],
      "parallel_safe": true
    }
  ],
  "completed": [],
  "failed": []
}
```

---

## Environment requirements

- `GROQ_API_KEY`: required for LLM planning/execution paths.
- `VIVARIUM_INTERNAL_EXECUTION_TOKEN`: optional override for internal execution token.
