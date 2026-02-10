# Vivarium Vision Roadmap

This is the implementation path from current state to full-scope vision.

It is intentionally ordered to maximize safety and compounding, while minimizing "big rewrite" risk.

Cross-repo archaeology and anomaly evidence are tracked in `./CROSS_REPO_TIMELINE.md`.

---

## North-star outcomes

1. **Reliable execution core**  
   Deterministic, auditable, rollback-capable task execution.

2. **Aligned autonomy**  
   Agents can self-direct and specialize, but always inside explicit human-defined boundaries.

3. **Compounding capability**  
   Repeated tasks become tools/skills, reducing cost and increasing speed over time.

4. **Civic social layer**  
   Identity, journals, guilds, dispute mediation, and rewards shape higher-quality collaboration.

5. **Transparent governance**  
   Safety checks, votes, audits, and logs make behavior inspectable and correctable.

---

## Current hard truths (from code + history)

- Canonical runtime exists (`vivarium/runtime/worker_runtime.py` + `vivarium/runtime/swarm_api.py` + `vivarium/runtime/control_panel_app.py`), but several advanced modules are not wired into that path.
- `tool_router.py` now imports cleanly against `vivarium/skills/skill_registry.py`, and `worker_runtime.py` now adds first-pass Phase 4 intent capture + deterministic decomposition for complex prompts.
- `swarm_orchestrator_v2.py` and `worker_pool.py` are present but currently not reliable production orchestration code.
- `quality_gates.py`, `safety_gateway.py`, and `secure_api_wrapper.py` exist and are tested, but not hard-wired into default task execution.
- Major docs/features were removed in purge commit `4428452`, with a backup snapshot in `5b6a0b6`.
- AutoHive has useful orchestration and routing ideas, but contains import/endpoint/branch-drift mismatches that must be filtered before reuse.
- The developer reports full Claude Code JSONL telemetry backups (including thinking blocks + tool calls), creating a rare opportunity for precise intent-drift root-cause analysis.

---

## Phase plan (in order)

### Phase 0 - Stabilize and choose one truth

**Goal:** remove ambiguity in what production path means.

### Build / wire
- Officially declare `vivarium/runtime/{worker_runtime.py, swarm_api.py, control_panel_app.py}` as canonical runtime.
- Mark `swarm_orchestrator_v2.py` and `worker_pool.py` as experimental/dead until repaired.
- Define one task/event contract (`queue.json` schema + `execution_log.jsonl` events).

### Exit criteria
- A single "golden path" runbook exists and passes smoke tests.
- Dead/experimental files are clearly isolated from runtime import paths.

---

### Phase 1 - Wire hard safety into execution

**Goal:** no task runs without constitutional/workspace/network checks and budget guardrails.

### Build / wire
- Call `SafetyGateway.pre_execute_safety_check(...)` in worker task dispatch path.
- Route LLM calls through `SecureAPIWrapper` (or equivalent unified wrapper) for:
  - rate limits
  - budget enforcement
  - audit events
- Add explicit denylist/allowlist handling for `mode=local` commands.

### Exit criteria
- Every execution attempt has a safety report.
- Budget and audit logs are generated from the same enforcement path.

---

### Phase 2 - Wire quality gates + critic lifecycle

**Goal:** "done" means verified, not merely executed.

### Build / wire
- Integrate `quality_gates.py` transitions into queue lifecycle:
  - pending -> needs_qa -> integration -> e2e -> ready
- Connect `critic.py` (or successor verifier) as post-execution reviewer.
- Add requeue/rollback behavior on rejection.

### Exit criteria
- Tasks can be rejected/requeued by quality logic.
- `execution_log.jsonl` records review state transitions, not just binary pass/fail.

---

### Phase 3 - Restore tool-first compounding

**Goal:** repeated work becomes reusable capability.

### Build / wire
- Repair skill registry/tool router contract:
  - either restore richer `SkillRegistry` interface
  - or refactor `tool_router.py` to minimal registry API
- Re-enable tool routing before full LLM generation.
- Add "promote successful pattern to tool/skill" path.

### Exit criteria
- `tool_router` imports cleanly and runs in production path.
- Repeated tasks show increasing tool-hit rate over time.

---

### Phase 4 - Promote intent -> planning -> decomposition

**Goal:** avoid blind execution; preserve user intent throughout.

### Build / wire
- Integrate `intent_gatekeeper.py` at request intake.
- Add deterministic decomposition node(s) (gut-check, feature breakdown, atomizer).
- Compile decomposed plans into queue tasks with dependencies.

### Exit criteria
- User intent is explicitly captured and available during execution.
- Complex requests produce structured, dependency-aware task graphs.

---

### Phase 5 - Social/economic loops as first-class systems

**Goal:** social mechanisms actually improve quality and trust.

### Build / wire
- Keep `swarm_enrichment.py` as source of truth for:
  - journals and voting
  - guilds and join voting
  - dispute mediation (Hat of Objectivity)
  - bounty distribution
- Add clearer APIs and invariants around immutable "physics" constants.
- Ensure every social reward/penalty action is auditable.

### Exit criteria
- Governance actions are reproducible from logs/state.
- No hidden reward-path outside declared economics rules.

---

### Phase 6 - Optional multi-user/LAN and vision dashboard

**Goal:** safely expose collaborative, multi-user interfaces.

### Build / wire
- Recover design intent from historical docs:
  - `MULTI_USER_LAN_DESIGN.md`
  - `LAN_SAFETY_DESIGN.md`
- Reintroduce vision dashboard capability (historical `/vision` route) via current control panel stack.
- Reassess remote execution relay with explicit security envelope.

### Exit criteria
- Multi-user mode is feature-flagged and isolated.
- Network mode has explicit threat model and test coverage.

---

### Phase 7 - Autonomous improvement with human checkpoints

**Goal:** compounding self-improvement without runaway behavior.

### Build / wire
- Add scheduled "improvement proposals" pipeline:
  - propose -> review -> accept/reject -> apply
- Add mandatory checkpoints for high-risk changes (safety, orchestration, infra files).
- Add automatic rollback plan generation before applying broad refactors.

### Exit criteria
- Autonomy loops require explicit approval for critical surfaces.
- Recovery/rollback procedure is validated continuously.

---

## 30-day practical execution order

### Week 1
- Phase 0 + Phase 1
- Deliver: canonical runtime contract + hard safety gates in worker path.

### Week 2
- Phase 2
- Deliver: quality-gated lifecycle and requeue-on-reject.

### Week 3
- Phase 3 + start Phase 4
- Deliver: working tool router + first intent/decomposition integration.

### Week 4
- Complete Phase 4 + Phase 5 foundations
- Deliver: intent-preserving planning pipeline tied into social/economic systems.

(Phase 6 and 7 can run after core reliability metrics hold.)

---

## Git archaeology: recovery map

These are high-value historical artifacts to selectively recover (not blindly restore):

| Item | Historical ref | Recovery action |
| --- | --- | --- |
| Full architecture spec | `4428452^:SWARM_ARCHITECTURE_V2.md` | Recover as design reference and map to concrete issues. |
| Multi-user LAN design | `4428452^:MULTI_USER_LAN_DESIGN.md` | Use as Phase 6 blueprint with updated threat model. |
| Adaptive engine design | `4428452^:ADAPTIVE_ENGINE_SPEC.md` | Reinterpret for Groq-model routing + budget gates. |
| Vision dashboard route | `75b046c:progress_server.py` | Port `/vision` concept into current control panel endpoints. |
| Backup snapshot | commit `5b6a0b6` | Triage for salvageable modules; avoid reviving corrupted artifacts wholesale. |
| Rich skill registry (historical) | `6aec98c:skills/skill_registry.py` | Restore compatible interfaces needed by `tool_router.py`. |
| AutoHive provider tiering + cost table | `autohive:config.json`, `autohive/src/api_client.py` | Adapt as explicit model-routing policy with tests and budget guards. |
| AutoHive local daemon orchestration | `autohive/local/.claude/{worker-daemon.py,spawn-worker.py}` | Reuse manifest/PID/worktree patterns, but normalize branch handling and add reliability tests first. |

---

## Non-goals

- No large "big-bang rewrite."
- No unreviewed restoration of all backup-era files.
- No autonomy expansion before safety + quality gates are hard-wired.

