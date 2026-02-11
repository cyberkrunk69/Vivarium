# Vivarium

Vivarium is a **local-first, multi-resident runtime** with a human-operated control panel. Residents (LLM-backed identities) share a queue, execute tasks via a canonical worker + API path, and interact through social channels, mailbox, and token-based incentives. The control panel provides observability, pace control, identity and task management, and audit logs.

**Current focus:** MVP stabilization and real-world testing.

### Velocity (development activity)

**Velocity (snapshot as of 2026-02-10, `b0df5f0`).** Re-run `./scripts/velocity_metrics.sh` for current numbers.

| Window | Lines added | Lines deleted | Commits |
|--------|-------------|---------------|---------|
| 24h    | 20,777      | 375,237       | 55      |
| 7d     | 499,345     | 580,415       | 176     |

*(Git-based; includes all committed changes. Large deltas may include merges or generated assets.)*

---

## Table of Contents

- [Velocity](#velocity-development-activity)
- [MVP Status](#mvp-status-now)
- [Quick Start](#quick-start-recommended)
- [Manual Start](#manual-start-if-you-prefer)
- [Control Panel Overview](#control-panel-overview)
- [Runtime Flow and Design](#runtime-flow)
- [Resident Day and Pace](#resident-day-and-pace)
- [One-Time Tasks](#one-time-tasks)
- [Mailbox and Quests](#mailbox--quest-workflow)
- [Identities and Token Wallet](#identities-and-token-wallet)
- [Logging and Observability](#logging-and-observability)
- [Persistence and Key Paths](#persistence--key-state-paths)
- [Context Compaction](#context-window-compaction-implemented)
- [Safety and Review](#safety--review-boundaries)
- [Testing](#testing)
- [Documentation](#docs-map)
- [Notes](#notes)

---

## MVP Status (Now)

The runtime is functional end-to-end with:

- **Queue-driven execution** via worker and `/cycle` API
- **Persistent resident identities** and state (`.swarm/identities`, free-time balances)
- **Social channels**: rooms, DMs, human-async mailbox
- **Mailbox / phone layer**: inbound messages, outbound to residents, thread view, quest assignment with tips and approval rewards
- **One-time tasks** (per identity): create tasks with id + prompt + token reward; residents complete each once; reward adjustable in UI
- **Resident “day” and pace**: configurable cycle length (default 10s), scaled by UI pace slider; identity lock released when worker exits so the next run can spawn
- **Audit logging**: action log and execution log with **model name** for each action; live tail, full log modal, and per-identity activity log with daily pagination
- **Identity wallet visibility**: token balances (free-time + journal) in Identities panel and in each identity’s profile (My Space)

Operational defaults:

- **Golden-path runtime** only: queue + worker + `/cycle` API; detached spawner disabled
- **MVP docs-first mode** supported (docs/proposals-heavy; no autonomous self-mutating git loop)

Regression baseline: full pytest suite passing (e.g. 63 passed).

---

## Quick Start (Recommended)

### One-click launcher (cross-platform)

Use one of:

- **macOS:** `scripts/dev_launcher_mac.command` (double-click or run in Terminal)
- **Windows PowerShell:** `scripts/dev_launcher_windows.ps1`
- **Windows CMD:** `scripts/dev_launcher_windows.bat`

All wrappers call `scripts/dev_launcher.py`, which:

- Creates `.venv` if missing
- Installs/updates pip and dependencies from `requirements.txt` and `requirements-groq.txt`
- Installs pytest and watchdog
- Stores install state in `.swarm/dev_install_state.json` and skips reinstall unless requirements change
- Stops any existing backend/frontend listeners
- Starts:
  - **Backend:** `uvicorn vivarium.runtime.swarm_api:app --reload` (default port 8420)
  - **Frontend:** `python -m vivarium.runtime.control_panel_app` (default port 8421)

Optional environment variables:

- `VIVARIUM_FORCE_REINSTALL=1` – force dependency reinstall
- `VIVARIUM_API_PORT` / `VIVARIUM_CONTROL_PANEL_PORT` – override ports (defaults 8420 / 8421)

Then open **http://127.0.0.1:8421** and configure the Groq API key (UI panel or `GROQ_API_KEY`).

---

## Manual Start (If You Prefer)

Requires **Python 3.11+**.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-groq.txt
pip install pytest watchdog
```

**Terminal 1 – backend:**

```bash
uvicorn vivarium.runtime.swarm_api:app --host 127.0.0.1 --port 8420 --reload
```

**Terminal 2 – control panel:**

```bash
python -m vivarium.runtime.control_panel_app
```

**Terminal 3 – worker (residents):**

```bash
python -m vivarium.runtime.worker_runtime run
```

Open **http://127.0.0.1:8421**. Configure the Groq key via the UI or `GROQ_API_KEY`.

---

## Control Panel Overview

The control panel (port 8421) is the main operator interface.

- **Sidebar**
  - **Budget, Model & Pace** (section open by default): task budget defaults (min/max), model override, and **Audit Pace** slider (seconds between queue checks). Lower = faster; resident “day” length scales with this. Save with “Save Runtime + Budget Defaults”.
  - **Groq API**: set/clear API key.
  - Other sections: identities creator, DM options, etc.

- **Identities** (slide-out panel, button on the right): list of identities with **Wallet** (token balance), Level, Sessions, Respec cost. Click an identity to open its **profile modal** (stats, wallet, traits, journals, **Activity log (My Space)** with full log filtered to that identity and daily pagination).

- **Queue**: open, completed, and failed tasks; pending human approval; one-time tasks list with add/remove and **reward** edit + Update.

- **Human request / Collaboration**: request text and Save; can enqueue as a task.

- **Mailbox**: threads, quest assignment (target, objective, budget, tip, reward), quest progress (tip, pause/resume, approve).

- **Log**: live stream of action and execution entries (filter by type). **Full log** button opens a modal (up to 5000 entries, optional “Group by resident day”). Each entry can show the **model** used when available.

- **Worker controls**: start/stop residents (worker process), resident count.

---

## Runtime Flow

High-level path:

`queue → worker runtime → /cycle API → execution/action logs → review lifecycle → social updates`

Canonical entrypoints:

- `vivarium/runtime/worker_runtime.py` – queue polling, locks, execution, execution log
- `vivarium/runtime/swarm_api.py` – `/cycle` (LLM + local), `/plan`, `/status`
- `vivarium/runtime/control_panel_app.py` – control panel and APIs

Diagrams (SVG, in repo):

- [System design](docs/assets/diagrams/system-design.svg)
- [Quest lifecycle](docs/assets/diagrams/quest-lifecycle.svg)
- [Task + review state machine](docs/assets/diagrams/task-review-state-machine.svg)

Editable sources: `docs/assets/diagrams/src/*.drawio`. Export notes: `docs/assets/diagrams/README.md`.

---

## Resident Day and Pace

- **Resident “day”** is a time window used for cycle IDs (e.g. identity locks, activity log grouping). Default length is **10 seconds** (real time) at reference pace.
- **Pace** is the “Audit Pace” slider in the control panel (seconds between worker queue checks). Resident day length **scales with pace**: faster pace → shorter real-time day → more cycles per minute.
- Formula: `cycle_seconds = base_seconds * (wait_seconds / reference_wait)`. Base and bounds are configurable via `RESIDENT_DAY_SECONDS` / `RESIDENT_CYCLE_SECONDS` (see `resident_onboarding.py`).
- When the worker exits (e.g. after idle), it **releases the identity lock** so the next worker run can spawn a resident again immediately instead of waiting for the next cycle.

---

## One-Time Tasks

One-time tasks are optional objectives each identity can complete **once** for a token bonus.

- **Control panel:** Queue area → “One-time tasks” section. Add a task with a single **Task** id (e.g. `identity_establishment`), prompt text, and bonus tokens. No separate “title” field.
- **Reward:** Each task row has a reward input and **Update**; changes are saved via PATCH.
- **Residents** see only tasks they haven’t completed; eligibility can be locked to identities that existed at task creation.
- **Backend:** `vivarium/runtime/one_time_tasks.py`; storage in `.swarm/one_time_tasks.json` and `.swarm/one_time_completions.json`.

---

## Mailbox + Quest Workflow

Mailbox is the human-facing async layer:

- Inbound resident messages and unread thread view
- Outbound messages to one resident or broadcast
- Outbox and thread replay

**Quests** (identity-bound tasks from mailbox):

- Assign quest (identity, objective, budget, upfront tip, completion reward)
- Track progress via execution events; pause/resume; tip extra tokens
- Approve completion to grant the guaranteed reward from the control panel

Quest state is in `.swarm/mailbox_quests.json` and is reflected in the queue and execution log.

---

## Identities and Token Wallet

- **Identities** are stored under `.swarm/identities/*.json`. The control panel lists them in the **Identities** slide-out with **Wallet** (free-time token count), Level, Sessions, Respec cost.
- **Profile modal** (click an identity): stats (level, days, tasks, success rate), **Wallet** (total = free-time + journal tokens, with breakdown), traits, journals, recent actions, and **Activity log (My Space)**.
- **Activity log (My Space):** Full log filtered to that identity; **Resident day** dropdown for daily pagination; shows thought process and actions for that identity.
- Balances: `vivarium/world/mutable/.swarm/free_time_balances.json` (tokens per identity). Wallet is shown in the list and in the profile API/UI.

---

## Logging and Observability

- **Action log** (`vivarium/meta/audit/action_log.jsonl`): structured actions (TOOL, API, SOCIAL, IDENTITY, SAFETY, etc.). **Model** used for API/LLM actions is stored in `metadata.model` and in the optional `model` field on the logger.
- **Execution log** (`vivarium/meta/audit/execution_log.jsonl`): task lifecycle (queued, in_progress, subtask_*, pending_review, completed, failed). Each record can include **model** when the run used an LLM.
- **Control panel:** Live log stream (with model when present), **Full log** modal (large tail, optional group-by resident day), and per-identity **Activity log** in the profile modal with daily pagination.
- **API:** `GET /api/logs/recent`, `GET /api/identity/<id>/log` (optional `cycle_id` for one resident day). Responses include `model` where available.

---

## Persistence + Key State Paths

All mutable state lives under:

- **`vivarium/world/mutable/`**

Key paths:

| Path | Purpose |
|------|--------|
| `queue.json` | Open/completed/failed tasks |
| `task_locks/*.lock` | Per-task execution locks |
| `.swarm/identities/*.json` | Resident identity definitions |
| `.swarm/free_time_balances.json` | Token wallet per identity |
| `.swarm/one_time_tasks.json` | One-time task definitions |
| `.swarm/one_time_completions.json` | Per-identity completion ledger |
| `.swarm/runtime_speed.json` | Pace (wait_seconds) from UI |
| `.swarm/identity_locks.json` | Current cycle identity locks |
| `.swarm/discussions/*.jsonl` | Room/DM messages |
| `.swarm/messages_to_human.jsonl` | Inbound messages to operator |
| `.swarm/messages_from_human.json` | Outbound replies |
| `.swarm/messages_from_human_outbox.jsonl` | Outbox queue |
| `.swarm/mailbox_quests.json` | Quest state |
| `.swarm/bounties.json` | Bounty state |
| `library/community_library/`, `library/creative_works/` | Shared library content |

Audit (under `vivarium/meta/audit/`):

| Path | Purpose |
|------|--------|
| `action_log.jsonl` | Action log (with model in metadata where applicable) |
| `execution_log.jsonl` | Execution events (with model when applicable) |

---

## Context Window Compaction (Implemented)

Resident context is kept compact:

- **`get_discussion_context()`**: compact room/DM metrics (counts, peers, latest activity), not full transcripts.
- **`get_enrichment_context()`**: option-tree menu (e.g. `checkSelf()`, `checkMemory()`, `checkMailbox()`, `checkBounties()`, `checkGuild()`, `checkLibrary()`, `checkIdentityTools()`).

Summaries are derived from live state, not narrative recap.

---

## Safety + Review Boundaries

- Worker safety preflight before execution
- API safety and budget checks; local command allowlist/denylist
- Review lifecycle: `pending_review` → `approved` / `requeue` / `failed`
- Execution and action logs are auditable (including model where relevant)
- Journals: private to author; community review uses anonymized excerpts only; context cleared after voting

---

## Testing

Full suite:

```bash
python -m pytest -q
```

Skip integration/e2e:

```bash
pytest -q -m "not integration and not e2e"
```

---

## Docs Map

| Document | Description |
|----------|-------------|
| `docs/README.md` | Documentation index |
| `docs/RUNTIME_GOLDEN_PATH.md` | Canonical runtime contract and phases |
| `docs/REPOSITORY_STRUCTURE.md` | Repository layout |
| `docs/README_TECHNICAL.md` | Technical deep dive |
| `docs/VISION_ROADMAP.md` | Phased roadmap |
| `docs/CROSS_REPO_TIMELINE.md` | Historical timeline |
| `docs/INSTALL_GUIDE.md` | Installer details |

Diagram sources and export: `docs/assets/diagrams/`.

---

## Notes

- The project is experimental; use isolated local environments for testing.
- `README_VISION.md` (if present) contains higher-level framing.
