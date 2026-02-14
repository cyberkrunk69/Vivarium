# Scout Current-State White Paper
## Vivarium Scout as Implemented at HEAD

**Date:** 2026-02-14  
**Supersedes:** PR #80 white paper (2026-02-12)  
**Repository snapshot:** `f68d7ad`  
**Branch context:** `cursor/scout-feature-white-paper-5620`

**Companion docs:**
- Vision README: `../docs/scout/README_VISION.md`
- Technical README: `../docs/scout/README_TECHNICAL.md`

---

## Executive Summary

Scout today is a Python-first, Git-native documentation and drafting system with a larger experimental perimeter around confidence gating and "whimsy" UX. The core engine is real and substantial:

- living documentation generation (`.tldr.md`, `.deep.md`, `.eliv.md`) with diff-aware symbol reuse
- commit/PR draft generation and assembly
- PR synthesis from docs without relying on staged Git diffs
- call graph export and downstream impact summaries
- local index + navigation fallback
- audit logging and budget guardrails

At the same time, the current state has clear delivery gaps:

- several top-level `devtools` wrappers are broken at runtime
- hook installer output references code paths that are missing or stale
- documented launcher surface and actual launcher surface have drifted
- middle-manager gate modules exist but are not yet wired into mainstream CLI flows

This white paper describes what Scout is **now**, not what it was at PR #80 launch and not what the docs claim aspirationally.

---

## 1. What Changed Since Yesterday's White Paper

Yesterday's white paper captured the PR #80 release shape. Since then, Scout gained or changed behavior in these areas (from commits on 2026-02-13):

- `318a651`: ship flow behavior updates (gate/budget/draft edge handling in root CLI)
- `fe18faf`: `middle_manager.py` introduced confidence-gate parsing/compression logic
- `70c661c`: configuration and raw brief handling updates
- `bd5f0a5`: dependency graph module (`deps.py`) additions
- `9ec9f44`: UI whimsy layer modules (`ui/hype.py`, `ui/whimsy.py`, `ui/whimsy_data.py`)
- `f68d7ad`: merge of fix branch into mainline branch history

Net effect: core Scout is broader than PR #80, but integration quality is uneven.

---

## 2. Product Definition (Current)

Scout is currently a **composable toolkit** centered on these capabilities:

1. **Generate and maintain living docs near source code**  
   Symbol-level docs are generated and mirrored for centralized browsing.

2. **Produce and assemble commit/PR drafts from docs and staged diffs**  
   Draft writing can be LLM-backed; assembly is deterministic and file-based.

3. **Navigate code with zero-cost-first strategy**  
   Use local index when possible, fall back to LLM with validator-driven retries/escalation.

4. **Enforce spend and confidence hygiene**  
   Configurable soft limits, hard non-overridable caps, and JSONL audit trails.

5. **Support autonomous-ish Git workflows via hooks and ship command**  
   Implemented in code, but some wrapper-level reliability issues remain.

---

## 3. Architecture and Module Topology

### 3.1 Core package layout

`vivarium/scout/` currently contains 39 Python modules, including:

- **Generation and synthesis**
  - `doc_generation.py`
  - `adapters/{python,javascript,plain_text}.py`
- **Draft and Git integration**
  - `git_drafts.py`
  - `git_analyzer.py`
  - `router.py`
- **LLM clients and model routing**
  - `llm.py` (Groq)
  - `big_brain.py` (Gemini, optional)
- **Policy and safety**
  - `config.py`
  - `ignore.py`
  - `validator.py`
  - `audit.py`
- **Extended/experimental logic**
  - `deps.py`
  - `middle_manager.py`
  - `raw_briefs.py`
  - `ui/{whimsy,hype,whimsy_data}.py`
- **CLI modules**
  - `cli/{root,doc_sync,nav,index,brief,status,ci_guard,roast,query,main}.py`

### 3.2 Living docs footprint

Current repo snapshot includes:

- **57** local Scout docs in `vivarium/scout/.docs/`
- **93** mirrored docs in `docs/livingDoc/vivarium/scout/`
- freshness metadata via `*.tldr.md.meta`

---

## 4. Detailed Capability: What Works Today

## 4.1 Living Documentation Engine

Implemented in `doc_generation.py` and adapters:

- Supports Python, JS (`.js/.mjs/.cjs`), and plain-text fallback adapters.
- Generates three doc levels:
  - `.tldr.md`
  - `.deep.md`
  - `.eliv.md` (can be disabled)
- Writes local docs to `<source_dir>/.docs/` and mirrors to `docs/livingDoc/...`.
- Optional versioned mirror support via `--versioned`.

### Freshness and diff-awareness

- File-level hash: `source_hash` in `*.tldr.md.meta`
- Symbol-level hash per symbol source span
- Unchanged symbols are reused from meta to avoid unnecessary LLM calls
- `repair` and `validate` paths detect stale docs from hash mismatch

### Cost and throughput controls

- Optional hard run budget (`--budget`) raises `BudgetExceededError` and cancels workers
- Worker count auto-derived from model RPM metadata when available
- `SCOUT_MAX_CONCURRENT_CALLS` controls global async semaphore
- Fallback templating supported when LLM calls fail (`--fallback-template`)

### Module briefs

- Package-level `__init__.py.module.md` is auto-generated from traced roles + child TLDRs
- Written to both local `.docs/` and central `docs/livingDoc/...`
- Guarded by `drafts.enable_module_briefs`

### Call graph and impact

- `export_call_graph()` writes `call_graph.json` (nodes + edges)
- `get_downstream_impact()` computes transitive module effects for changed files
- Used by PR drafting logic for impact sections

---

## 4.2 Draft Generation and Assembly

### Generation paths

Within `TriggerRouter.prepare_commit_msg()` and related router methods:

- can generate:
  - `docs/drafts/<stem>.commit.txt`
  - `docs/drafts/<stem>.pr.txt`
  - optional impact snippets
- commit drafts and PR snippets are LLM-produced from staged diffs + local symbol docs
- generation is bounded by config, ignore patterns, and semaphore constraints

### Assembly paths (`git_drafts.py`)

- `assemble_commit_message()` merges per-file commit drafts deterministically
- `assemble_pr_description()` groups by package and includes module summaries when present
- `assemble_pr_description_from_docs()` supports **Git-independent** PR generation from `.docs/`

### PR synthesis

- `synthesize_pr_description()` unifies raw summaries into narrative form
- uses Gemini when `GEMINI_API_KEY` is present, otherwise Groq
- `--fallback-template` returns raw summaries if synthesis fails

---

## 4.3 Root Workflow CLI (Commit / PR / Status / Ship)

`python -m vivarium.scout.cli.root` exposes:

- `commit`
- `pr`
- `status`
- `ship`

### Key implemented behaviors

- `pr --from-docs PATH` ignores Git changed-files and synthesizes from docs scope
- `pr --auto-draft` writes `.github/pr-draft.md`
- `ship` orchestrates doc sync -> draft generation -> commit -> push -> PR draft
- `ship --dry-run-full` executes full pre-PR generation flow without commit/push
- optional outcome hype when `SCOUT_WHIMSY=1`

### Notable quirks

- `commit` currently filters staged files to `.py` only in CLI path (assembly function supports broader suffixes).
- Ship path invokes `python -m vivarium.scout.cli.doc_sync ...` directly (works only when dependencies are installed in runtime environment).

---

## 4.4 Navigation, Indexing, Briefing, Roast

### Local index (`cli/index.py`)

- ctags + SQLite FTS5 index in `.scout/index.db`
- query, build, update, stats, watch subcommands
- zero LLM calls for indexed lookups

### Navigation (`cli/nav.py` + router)

- index-first navigation for cheap/fast answers
- fallback to Groq 8B with validator feedback loop
- escalation to 70B on persistent validation failure
- file-specific Q&A mode supported

### Brief generation (`cli/brief.py`)

- flow: nav -> git context -> dependency map -> 8B structure -> optional 70B enhancement
- complexity scoring decides whether 70B enhancement is used
- outputs "Recommended Deep Model Prompt" section for downstream model handoff

### Roast (`cli/roast.py`)

- audit-based savings reports (`today/week/month`)
- optional docs-aware critique mode for target files
- tracks roast events in audit log

---

## 4.5 Config, Budgets, and Audit

### Config layering (`config.py`)

Precedence:

1. defaults
2. `~/.scout/config.yaml`
3. `.scout/config.yaml`
4. env overrides

Hard caps (non-overridable):

- max cost per event: 1.00
- max hourly budget: 10.00
- max auto escalations: 3

### Model defaults

Current defaults in `DEFAULT_CONFIG` and generation fallback constants:

- TLDR: `llama-3.1-8b-instant`
- DEEP: `llama-3.3-70b-versatile` in config, but fallback constants in `doc_generation.py` are 8B
- ELIV: `llama-3.1-8b-instant`

### Audit (`audit.py`)

- append-only JSONL (`~/.scout/audit.jsonl`)
- line-buffered writes with fsync cadence
- auto-rotation at 10MB with gz archives
- query APIs for spend, recent events, and accuracy metrics

---

## 4.6 Dependency Graph and Gate Modules (Present but Partially Integrated)

### Dependency graph (`deps.py`)

- builds bidirectional symbol dependency graph
- stores cache at `~/.scout/dependency_graph.v2.json`
- supports proactive invalidation cascade from changed files

### Middle manager / gate (`middle_manager.py`)

- parses confidence outputs
- supports retry, gap extraction, and escalation strategy
- stores raw briefs via `raw_briefs.py`

### Current integration status

- gate and whimsy modules are implemented and tested in isolation paths
- they are **not deeply integrated into the mainstream root CLI data path yet**
- code comments reference intended gate behavior in places where runtime path still uses legacy draft generation logic

---

## 5. Launcher and Command Surface: Verified Runtime Status

The following status reflects direct command checks in this environment.

| Interface | Status | Notes |
|---|---|---|
| `python -m vivarium.scout --help` | OK | Exposes `config`, `on-commit`, `prepare-commit-msg` |
| `python -m vivarium.scout.cli.root --help` | OK | Exposes `commit`, `pr`, `status`, `ship` |
| `python -m vivarium.scout.cli.root status` | OK | Runtime verified |
| `python -m vivarium.scout.cli.ci_guard --help` | OK | Module exists and runs |
| `python -m vivarium.scout.cli.doc_sync --help` | DEPENDENCY REQUIRED | Fails without `python-dotenv` installed |
| `devtools/scripts/scout-nav` | OK | Wrapper works |
| `devtools/scripts/scout-index` | OK | Wrapper works |
| `devtools/scripts/scout-brief` | OK | Wrapper works |
| `devtools/scripts/scout-roast` | OK | Wrapper works |
| `devtools/scout-doc-sync` | BROKEN | Calls undefined `find_python` helper |
| `devtools/scout-commit` | BROKEN | Calls undefined `find_python` helper |
| `devtools/scout-pr` | BROKEN | Calls undefined `find_python` helper |
| `devtools/scout-autonomy` | PARTIAL | Runs, but installs hooks that call broken wrappers and missing helper paths |

---

## 6. Hook Automation State

`devtools/scout-autonomy` supports:

- `enable`
- `enable-commit`
- `disable`

Current reliability caveats:

1. Installed pre-commit and pre-push hooks call `./devtools/scout-doc-sync` / `./devtools/scout-pr`, which are currently broken due missing `find_python`.
2. Installed post-commit content references `get_files_in_last_commit` from `git_analyzer`, but that helper does not exist.
3. Hook scripts use `|| true` in key places, so failure can be silent.

Result: autonomy hooks are conceptually present, but operational reliability is currently degraded.

---

## 7. Testing and Validation Posture

Scout-specific test inventory includes 9 test files under `tests/scout/`, covering:

- config layering and hard caps
- audit log correctness/performance/rotation
- router trigger/validation/cascade behavior
- nav CLI parsing and escalation behaviors
- roast reporting
- whimsy factual relevance checks

Current testing gaps:

- no robust end-to-end tests for `scout-autonomy` installed hooks
- limited integration tests for `middle_manager` gate in production command paths
- no automated tests guarding launcher-script drift (`devtools/README` vs actual scripts)

---

## 8. Known Technical Debt and Delivery Gaps

1. **Wrapper breakage:** `devtools/scout-{doc-sync,commit,pr}` rely on missing `find_python` helper.
2. **Hook script mismatch:** installed post-commit script references nonexistent `get_files_in_last_commit`.
3. **Command surface drift:** docs mention wrappers not present (`scout-ship`, `scout-status`, `scout-ci-guard` launchers).
4. **Optional dependency friction:** `python-dotenv` required for some CLIs but not guaranteed in minimal runtime.
5. **Gate integration gap:** middle-manager gate code exists but is not fully wired across root workflow.
6. **Behavioral oddity:** `doc_sync repair` currently returns exit code `1` even after processing stale docs.
7. **Duplicate CLI entry modules:** overlapping `cli.py` and `cli/main.py` surfaces increase maintenance risk.

---

## 9. Current-State Conclusion

Scout is no longer just the PR #80 living-doc prototype. It is now a broader operational toolkit with:

- strong core documentation and drafting internals
- meaningful navigation/indexing/reporting capabilities
- real cost/audit controls

However, release hardening has not kept pace with feature growth. The largest practical blockers are at integration boundaries (wrappers/hooks/docs drift), not at the core engine level.

In short: **the engine is substantially capable; the packaging and operational envelope need consolidation.**

---

## Appendix A: Key Paths

| Path | Role |
|---|---|
| `vivarium/scout/doc_generation.py` | living-doc generation, freshness, synthesis |
| `vivarium/scout/git_drafts.py` | commit/PR assembly from drafts/docs |
| `vivarium/scout/router.py` | trigger orchestration, draft generation, nav integration |
| `vivarium/scout/config.py` | layered config + hard safety caps |
| `vivarium/scout/audit.py` | append-only audit log + spend metrics |
| `vivarium/scout/cli/root.py` | commit/pr/status/ship command surface |
| `vivarium/scout/cli/doc_sync.py` | generate/repair/export/validate docs |
| `vivarium/scout/cli/nav.py` | task navigation and file Q&A |
| `vivarium/scout/cli/index.py` | local ctags/SQLite index |
| `vivarium/scout/cli/brief.py` | investigation brief generation |
| `vivarium/scout/cli/roast.py` | savings reports and critique |
| `vivarium/scout/cli/ci_guard.py` | CI guardrails for docs/confidence/spend |
| `vivarium/scout/deps.py` | dependency graph + invalidation cascade |
| `vivarium/scout/middle_manager.py` | confidence gate/compression logic |
| `devtools/scout-autonomy` | hook installer |

