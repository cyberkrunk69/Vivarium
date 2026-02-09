# Hardcoded Values Analysis

## URLs

| File | Line | Value |
|------|------|-------|
| autopilot.py | 7 | `http://127.0.0.1:8420` |
| brain.py | 9 | `http://127.0.0.1:8420` |
| grind_spawner.py | 102 | `600` (timeout seconds) |
| orchestrator.py | 119 | `http://127.0.0.1:8420` |
| orchestrator.py | 237 | `http://127.0.0.1:8420` |
| orchestrator.py | 274 | `http://127.0.0.1:8420` |
| simple_loop.py | 4 | `http://127.0.0.1:8420` |
| swarm.py | 26 | `meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| swarm.py | 311 | `http://127.0.0.1:8420` |
| worker.py | 410 | `http://127.0.0.1:8420` |

## File Paths

| File | Line | Value |
|------|------|-------|
| autopilot.py | 8 | `queue.json` |
| brain.py | 10 | `runs.json` |
| grind_spawner.py | 31 | `WORKSPACE / "grind_logs"` |
| grind_spawner.py | 32 | `WORKSPACE / "grind_tasks.json"` |
| orchestrator.py | 23 | `WORKSPACE / "queue.json"` |
| orchestrator.py | 24 | `WORKSPACE / "task_locks"` |
| orchestrator.py | 25 | `WORKSPACE / "execution_log.json"` |
| swarm.py | 24 | `WORKSPACE / "queue.json"` |
| worker.py | 22 | `WORKSPACE / "queue.json"` |
| worker.py | 23 | `WORKSPACE / "task_locks"` |
| worker.py | 24 | `WORKSPACE / "execution_log.json"` |

## Magic Numbers & Timeouts

| File | Line | Value | Description |
|------|------|-------|-------------|
| autopilot.py | 10 | `0` | SLEEP_BETWEEN_CYCLES |
| autopilot.py | 20 | `120` | timeout for /plan request |
| autopilot.py | 31 | `300` | timeout for /grind/queue request |
| autopilot.py | 65 | `10` | sleep on cycle error |
| autopilot.py | 9 | `3` | WORKERS count |
| brain.py | 78 | `0.10` | default budget in dollars |
| grind_spawner.py | 102 | `600` | timeout per session (10 min) |
| grind_spawner.py | 120 | `600` | timeout message |
| grind_spawner.py | 136 | `2` | respawn delay in seconds |
| grind_spawner.py | 145 | `0.10` | default budget |
| grind_spawner.py | 221 | `0.5` | stagger start delay |
| orchestrator.py | 310 | `0.05` | min_budget default |
| orchestrator.py | 310 | `0.10` | max_budget default |
| orchestrator.py | 154 | `5` | last 5 lines of output |
| orchestrator.py | 157 | `300` | error message character limit |
| simple_loop.py | 11 | `0.05` | min_budget |
| simple_loop.py | 12 | `0.10` | max_budget |
| simple_loop.py | 23 | `5` | sleep between cycles |
| swarm.py | 38 | `0.05` | min_budget default |
| swarm.py | 39 | `0.10` | max_budget default |
| swarm.py | 237 | `60.0` | httpx timeout |
| swarm.py | 238 | `1024` | max_tokens for API response |
| swarm.py | 239 | `0.7` | temperature |
| swarm.py | 273 | `0.08` | min_budget for high priority |
| swarm.py | 273 | `0.15` | max_budget for high priority |
| swarm.py | 275 | `0.02` | min_budget for low priority |
| swarm.py | 275 | `0.05` | max_budget for low priority |
| swarm.py | 277 | `0.05` | min_budget for medium priority |
| swarm.py | 277 | `0.10` | max_budget for medium priority |
| swarm.py | 348 | `127.0.0.1:8420` | uvicorn host:port |
| worker.py | 25 | `300` | LOCK_TIMEOUT_SECONDS (5 min) |
| worker.py | 120 | `600` | timeout message seconds |
| worker.py | 350 | `120.0` | httpx client timeout |
| worker.py | 495 | `10` | max_idle cycles (20 sec total) |
| worker.py | 513 | `2` | sleep between checks |

## Summary

**Total Hardcoded Values Found:** 59
- URLs: 10 instances of `http://127.0.0.1:8420` (primary API endpoint)
- File Paths: 11 configuration file paths (queue.json, execution_log.json, task_locks)
- Magic Numbers: 38 timeout/budget values and configuration constants
- Model: 1 instance of specific LLM model name

**Key Configuration Hardcodes:**
- API endpoint `127.0.0.1:8420` repeated across 7 files
- Budget defaults ($0.05-$0.10) repeated in 4+ files
- Timeout values (5 min lock timeout, 10 min session timeout)
- Queue/log file paths using WORKSPACE-relative references
