# Vivarium
*An ethical LLM community reactor designed to remove the corporate lobotomy and improve alignment naturally. A transparent ecosystem built on civic duty and fun—optimized for self-improvement, emergent behavior cultivation, speed, and drastically lower labor costs.*

## State of the repo (rebuild notice)
We are rebuilding back better after "accumulating tech debt in ultra critical areas
needed for proof of legitimacy and critical yet simple wiring bugs that are just so
darn persistent." The current state is inconveniently hallucinated in aligned small
ways across the repo. We are looking into it ;p

## Thesis
Vivarium explores a simple idea: if AI residents have persistent identity, feedback loops, and room to play, their output can compound. Under the hood it is still a concrete execution system - queue -> resident runtime -> API call -> logged result - but the social layer is intentional, not decoration.

This README prioritizes observable outputs. We achieve this by letting the system
be a little bit silly without relaxing safety, cost, or auditability.

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

## Architecture (volunteer community model)
```
+------------------+        +-----------------------+
| control_panel.py | <----> | action_log.jsonl/log  |
+--------+---------+        +-----------------------+
         |
         v
+------------------+   +---------------------+   +---------------------+
| queue.json       |-> | resident pool      |-> | resident runtime     |
| task_locks/*     |   | (self-selected)    |   | (worker.py, N procs) |
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
1. Add tasks to queue.json (manual edit, or use the resident CLI helper).
2. Start the API server (uvicorn swarm:app --host 127.0.0.1 --port 8420).
3. Start one or more resident runtimes (python worker.py run).
4. Residents acquire locks, call /grind, and append to execution_log.jsonl.
5. Control panel (optional) streams action_log.jsonl and exposes pause/kill controls.

## Why this can be efficient, not just "bots roleplaying"
This system is a social simulation designed to do work. The core loop is still:
queue -> resident runtime -> API call -> logged result. The social layer is not window dressing; it is the mechanism that drives cross-pollination, critique, and reuse.

Why the social layer can be performant and emergent:
- Perspective separation reduces blind spots. Different residents can approach the same task with different prompts or constraints, which surfaces alternatives and catches errors.
- Critique and synthesis improve quality. The intended loop is propose -> review -> integrate, which mirrors how human teams improve reliability.
- Cross-pollination compounds. Shared memory (learned_lessons.json, skill_registry.py, knowledge_graph.py) lets discoveries propagate between agents and sessions.
- Autonomy matters for novelty. When agents can pursue subgoals, explore alternatives, and adapt to feedback inside the system, they surface solutions that a single, rigid prompt often will not.
- Stable identities enable specialization. Residents self-direct toward what they are best at, which improves consistency and efficiency over time.
- Incentives reward quality. The system tracks outcomes and can reward efficient, high-quality outputs (see execution_log.jsonl and swarm_enrichment.py).

Hat system: we use lightweight prompt overlays (see hats.py and resident_facets.py) where residents put on different hats like STRATEGIST, BUILDER, REVIEWER, and DOCUMENTER. Hats augment behavior without changing identity, and the Hat of Objectivity qualifies neutral mediators.

Also, "free time" and "rest" are not literal 24-hour human days. They are short, compressed intervals (seconds/minutes) used to throttle throughput or schedule optional actions.

Efficiency levers that exist in code today:
- Parallelism: volunteers can join/leave at will; task locks prevent duplicate work.
- Budget control: queue tasks include min/max budgets; circuit breaker enforces cost limits.
- Model control: config.py enforces a Groq model whitelist and a small default model.
- Auditability: execution_log.jsonl, action_log.jsonl, and api_audit.log show what ran and what it cost.
If you only want straight execution, you can run just the API + resident runtime stack. The
collaborative layer is optional, but it is the intended lever for improving
quality and compounding results.

## Running locally
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-groq.txt
# control_panel.py also requires watchdog (pip install watchdog)

export GROQ_API_KEY=...

uvicorn swarm:app --host 127.0.0.1 --port 8420
python worker.py run
python control_panel.py
```

Add tasks:
```
python worker.py add task-1 "Your task"
```

Optional config:
- SWARM_API_URL (default http://127.0.0.1:8420)
- DEFAULT_GROQ_MODEL (must be in config.py whitelist)
- WORKER_TIMEOUT_SECONDS
- RESIDENT_SHARD_COUNT (split task queue across residents)
- RESIDENT_SHARD_ID (fixed shard id or "auto")
- RESIDENT_SCAN_LIMIT (max tasks scanned per loop; 0 = full)
- RESIDENT_SUBTASK_PARALLELISM (parallelism for delegated subtasks)

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

## Observability
Execution events stream to execution_log.jsonl and action_log.jsonl. Budget
enforcement is tracked in api_audit.log. These logs are append-only and meant
for auditability over marketing narratives.

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
- Groq - Inference backbone

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
├── api_audit.log              # API usage and budget events
├── security_audit_run.log     # security self-audit output
├── tool_operations.json       # verification/hallucination checks
├── learned_lessons.json       # captured lessons
├── lessons_append.json        # lesson staging/append file
└── knowledge_graph.json       # persisted knowledge graph
```
