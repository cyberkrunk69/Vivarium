# Vivarium API Reference

## API Overview
- **Title**: Vivarium
- **Version**: 1.0
- **Base URL**: http://127.0.0.1:8420

---

## Endpoints

### 1. POST /grind
Execute a grind task with budget parameters.

**Request Body Schema:**
```json
{
  "min_budget": float,        // Minimum budget in dollars (default: 0.05)
  "max_budget": float,        // Maximum budget in dollars (default: 0.10)
  "intensity": string         // Task intensity: "low", "medium", or "high" (default: "medium")
}
```

**Response Schema:**
```json
{
  "status": string,           // Execution status ("completed" or "failed")
  "result": string,           // Human-readable result message
  "budget_used": float        // Actual budget consumed (between min and max)
}
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8420/grind \
  -H "Content-Type: application/json" \
  -d '{"min_budget": 0.05, "max_budget": 0.10, "intensity": "high"}'
```

**Example Response:**
```json
{
  "status": "completed",
  "result": "Grind completed with intensity=high",
  "budget_used": 0.0873
}
```

---

### 2. POST /plan
Scan codebase, analyze with Together AI, write tasks to queue.

**Request Body Schema:**
None (no parameters)

**Response Schema:**
```json
{
  "status": string,           // "planned"
  "files_scanned": integer,   // Number of Python files found
  "total_lines": integer,     // Total lines of code analyzed
  "tasks_created": integer    // Number of improvement tasks created
}
```

**Process:**
1. Scan workspace for .py files and collect metadata
2. Send scan results to Together AI (Llama 3.3 70B) for analysis
3. Write suggested improvement tasks to queue.json

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8420/plan
```

**Example Response:**
```json
{
  "status": "planned",
  "files_scanned": 3,
  "total_lines": 350,
  "tasks_created": 4
}
```

**Error Handling:**
- Returns 500 HTTPException if `TOGETHER_API_KEY` environment variable is not set.

---

### 3. GET /status
Get current queue status with task counts by state.

**Request Body Schema:**
None (no parameters)

**Response Schema:**
```json
{
  "tasks": integer,           // Number of pending tasks
  "completed": integer,       // Number of completed tasks
  "failed": integer           // Number of failed tasks
}
```

**Example Request:**
```bash
curl http://127.0.0.1:8420/status
```

**Example Response:**
```json
{
  "tasks": 5,
  "completed": 2,
  "failed": 0
}
```

---

## Task Queue Format (queue.json)

Tasks written by `/plan` endpoint follow this structure:
```json
{
  "version": "1.0",
  "api_endpoint": "http://127.0.0.1:8420",
  "tasks": [
    {
      "id": "task_001",
      "type": "grind",
      "description": "Task description",
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

## Priority to Budget Mapping

Budget allocation is determined by task priority:

| Priority | Intensity | Min Budget | Max Budget |
|----------|-----------|-----------|-----------|
| high     | high      | $0.08     | $0.15     |
| medium   | medium    | $0.05     | $0.10     |
| low      | low       | $0.02     | $0.05     |

---

## Environment Requirements

- `TOGETHER_API_KEY`: API key for Together AI (required for `/plan` endpoint)
- `TOGETHER_MODEL`: Model name (default: "meta-llama/Llama-3.3-70B-Instruct-Turbo")
