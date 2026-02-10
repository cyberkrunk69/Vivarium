# Implementation Log V2: Observability and Runtime Logs

## Overview
This log documents the current observability surface in Vivarium.
It replaces placeholder V2 notes that referenced files not present in this repo.

## Files and outputs (present in repo)
- action_logger.py -> action_log.jsonl + action_log.log (runtime, human-readable stream)
- logger.py -> structured_logs.jsonl (structured JSONL entries)
- worker.py -> execution_log.jsonl (task-level status events)
- performance_tracker.py -> performance_history.json (session metrics)
- api_audit.log (API cost/usage/budget events)
- kernel_run.log (orchestrator and safety output from large runs)

## Example entries (real excerpts)
Structured sessions (structured_logs.jsonl):
```
{"timestamp": "2026-02-03T05:44:03.267569", "level": "INFO", "message": "GrindSession started", "worker_id": "default", "context": {"session_id": 1, "run": 1, "task": "ARCHITECTURE REVIEW: Wave 11 Code Audit\n\nYou are a", "model": "opus"}}
{"timestamp": "2026-02-03T05:45:43.075211", "level": "INFO", "message": "GrindSession completed", "worker_id": "default", "context": {"session_id": 2, "run": 1, "elapsed_seconds": 99.807641, "returncode": 0, "success": true}}
```

API audit and budgets (api_audit.log):
```
{"timestamp": "2026-02-03T22:41:31.839648", "event": "API_CALL_FAILURE", "user": "admin", "role": "admin", "error": "GROQ_API_KEY not found. Set it via environment variable or pass to constructor.\nGet your key at: https://console.groq.com/keys"}
{"timestamp": "2026-02-03T22:42:15.023457", "event": "BUDGET_EXCEEDED", "user": "admin", "role": "admin", "remaining": 0.019124550000000004, "requested": 0.026945}
```

Spawner and file guardrails (kernel_run.log):
```
BLOCKED: Attempt to write to protected file: experiments/exp_20260203_220119_unified_session_89/grind_spawner_unified.py
CAUTION: Writing to sensitive file: inference_engine.py
```

## Notes on use
- Logs are append-only artifacts; treat them as evidence, not marketing.
- Some entries include legacy paths from earlier environments. Keep them for audit,
  but filter if you need repo-local analytics.
