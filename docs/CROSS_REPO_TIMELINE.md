# Cross-Repo Timeline and AI-Assisted Anomaly Map

This document reconstructs the development arc across related repos, extracts high-value ideas ("gold"), and flags concrete drift introduced during rapid AI-assisted iteration.

Last updated: 2026-02-09

---

## Scope and access status

| Repo | Access status | Notes |
| --- | --- | --- |
| `cyberkrunk69/Vivarium` | Available locally | Primary codebase in this workspace. |
| `cyberkrunk69/autohive` | Public and cloned (`/workspace/autohive`) | Source of additional orchestration and cost-routing ideas. |
| `cyberkrunk69/claude-code-orchestrator` | Not accessible (`404`) | `gh repo view` fails and URL resolves to 404 at time of analysis. |

---

## Developer-declared provenance (important context)

- The developer states both repos were **entirely vibe-coded** in practice.
- The developer estimates only about **10-20 lines of code were manually typed** across their full lifecycle.
- The developer reports having **complete Claude Code JSONL telemetry** for the full development process.
- The backup JSON records are stated to include **full thinking-block data** and **tool-call traces**.
- The planned next step is to have the swarm analyze this origin data to map:
  - where clear user intent was lost,
  - why model behavior drifted the way it did,
  - and what repeatable controls should be added to prevent recurrence.

This provenance is developer-reported and should be treated as a first-class input to future root-cause analysis.
The developer expects substantial insight can be mined from this record once full swarm forensics are run.

---

## Unified timeline (key commits)

### AutoHive (origin signals)

| Date (local commit tz) | Commit | What changed | Signal |
| --- | --- | --- | --- |
| 2026-01-31 17:01 -0600 | `dd1dd31` | Initial AutoHive drop (`15 files`, `+2678`). | Fast bootstrap: single-file `swarm.py` plus modular `src/*` architecture launched together. |
| 2026-01-31 21:31 -0600 | `9cfa96f` | README expansion (`+334/-71`). | Vision expanded to dynamic scaling, worker specialization, economics framing. |
| 2026-01-31 21:38 -0600 | `36e0d42` | Local orchestrator runner (`12 files`, `+3500`). | Added cross-platform local daemon flow (`local/.claude/*`) and worker orchestration playbook. |

### Vivarium (core + turbulence + rebuild)

| Date (local commit tz) | Commit | What changed | Signal |
| --- | --- | --- | --- |
| 2026-02-03 05:50 -0600 | `d9908f6` | Initial Vivarium drop (`107 files`, `+23831`). | Large foundation commit with architecture, docs, orchestration primitives. |
| 2026-02-03 10:43 -0600 | `4239726` | Massive expansion (`301 files`, `+66523/-9816`). | Added broad research and architecture systemization artifacts. |
| 2026-02-03 20:47 -0600 | `3e623eb` | `SWARM_ARCHITECTURE_V2.md` + many node modules. | Peak explicit multi-node vision (intent/planning/atomizer/critic/consensus). |
| 2026-02-04 02:38 -0600 | `5b6a0b6` | Backup snapshot (`3300 files`, `+455283`). | Historical preservation point before rollback/cleanup. |
| 2026-02-08 04:08 +0000 | `7f98509` | Core hardening (`+369/-548`). | Shift toward stricter runtime reliability and Groq-focused path. |
| 2026-02-08 04:15 +0000 | `019683b` | Large prune (`1408 files`, `-151420`). | Major contraction; many experiments/designs removed. |
| 2026-02-09 15:25 +0000 | `4428452` | Purge commit (`115 files`, `-44917`). | Removed many Claude/Anthropic-era docs/specs from active tree. |
| 2026-02-09 19:34 +0000 | `c91614d` | Documentation pivot (`+171/-542`). | Reframed architecture around volunteer/social model. |
| 2026-02-09 21:24 +0000 | `e3412df` | README rewrite to current runtime/data flow. | Returned documentation to concrete implementation truth. |
| 2026-02-09 21:37 +0000 | `9b5498f` | Narrative + roadmap reintroduced. | Connected practical runtime truth back to long-term vision path. |

---

## High-value "gold" recovered from AutoHive

These are ideas worth importing into Vivarium deliberately (not by wholesale copy):

1. **Manifest-driven local orchestration loop**
   - Files: `autohive/local/.claude/worker-daemon.py`, `spawn-worker.py`
   - Value: explicit worker spawn protocol, PID verification, worktree lifecycle, dependency progression.

2. **Tiered model economics as first-class config**
   - Files: `autohive/config.json`, `autohive/src/api_client.py`
   - Value: clear per-provider cost tables + tiered recommended routing (`worker_cheap`, `orchestrator`, etc.).

3. **Role-specific worker contracts**
   - Files: `autohive/local/.claude/MASTER_WORKER_SYSTEM.md`, `HELPER_WORKER_SYSTEM.md`
   - Value: explicit behavior, budget boundaries, and reporting formats that can reduce orchestration ambiguity.

4. **Cross-platform local runner UX**
   - Files: `autohive/local/claude-orch.sh`, `claude-orch.bat`, `local/README.md`
   - Value: lower-friction operator loop for running autonomous swarms on Mac/Windows/Linux.

---

## AI-assisted anomaly map (evidence-based)

### A) Cadence and churn anomalies

- Vivarium shows extreme burst activity: `64 commits` on 2026-02-08 alone.
- `README.md` was revised repeatedly (`42` total README-touching commits), including many same-day rewrites.
- Pattern indicates rapid prompt-loop refinement and frequent narrative/architecture reframing.

### B) Vision-to-runtime drift

- Historical vision nodes were created and then largely removed from active runtime paths.
- Large deletion events (`019683b`, `4428452`) removed many specs/modules that previously encoded design intent.
- Result: implementation truth and vision truth diverged, then were partially reconnected by docs recovery.
- A high-value telemetry corpus exists to trace this drift at decision granularity (prompt/thinking/tool-call chronology), not just commit-level symptoms.

### C) AutoHive internal wiring mismatches (important before reuse)

1. **Server entrypoint import mismatch**
   - `autohive/run.py` imports `from server import run_server`.
   - `autohive/src/server.py` uses relative imports (`from .api_client ...`).
   - Observed runtime: `ImportError: attempted relative import with no known parent package` when invoking server path through `run.py`.

2. **Client class contract mismatch**
   - `autohive/src/worker_manager.py` imports `APIClient`.
   - `autohive/src/api_client.py` defines `MultiProviderClient` (no `APIClient` symbol).
   - Observed runtime: `ImportError: cannot import name 'APIClient' from 'src.api_client'`.

3. **Endpoint contract mismatch**
   - `autohive/config.json` advertises `/api/status`.
   - `autohive/src/server.py` exposes `/api/stats` (no `/api/status` route).

4. **Branch-name assumption drift**
   - Repo default branch is `master`.
   - Worker instructions/automation still hardcode `main` in critical spots:
     - `local/.claude/MASTER_WORKER_SYSTEM.md`
     - `local/.claude/spawn-worker.py`
     - `local/.claude/worker-daemon.py` auto-merge path
   - This can break autonomous merge/checkout flows depending on environment.

5. **Claimed scaling vs implemented execution**
   - README frames 1000+ dynamic scaling and live adjustment loops.
   - `autohive/swarm.py` worker execution is a fixed thread pool (`max_workers` default `20`) without the described live autoscale controller in code.

---

## Practical synthesis for Vivarium (ordered)

Use AutoHive "gold" in this order to avoid importing the same drift:

1. **Import economics model first**
   - Port provider cost table + routing tier config into Vivarium inference path.
   - Gate with explicit tests for cost estimation and fallback behavior.

2. **Import orchestration protocol second**
   - Reuse manifest/PID/worktree patterns, but normalize branch handling (`main`/`master`) before integration.

3. **Import role contracts third**
   - Adapt worker protocol docs into machine-checkable state transitions in Vivarium queue lifecycle.

4. **Delay UX portability last**
   - Bring in cross-platform launcher ergonomics only after runtime safety/quality wiring is complete.

---

## Open provenance gap

`claude-code-orchestrator` is currently inaccessible from this environment.  
If/when it becomes public, next archaeology pass should extract:

- worker daemon ancestry and diffs vs `autohive/local/.claude/worker-daemon.py`
- original initiative schema and merge governance model
- any "eye/vision" dashboard lineage not present in current public repos

