# Scout Technical README

## Scope

This document describes Scout as currently implemented in this repository:

- architecture and major modules,
- command surfaces that are available now,
- data artifacts Scout reads/writes,
- operational workflows,
- known technical edges under active hardening.

It is intentionally implementation-focused and should be read alongside:

- `README_VISION.md`
- `../../.github/PR_WHITEPAPER.md`
- `CONFIGURATION.md`
- `AUDIT_SCHEMA.md`

## Package Layout

Primary package: `vivarium/scout/`

Major module groups:

- Core generation and synthesis
  - `doc_generation.py`
  - `adapters/` (python, javascript, plain_text)
- Drafting and Git integration
  - `git_drafts.py`
  - `git_analyzer.py`
  - `router.py`
- LLM clients
  - `llm.py` (Groq integration)
  - `big_brain.py` (Gemini integration for selected paths)
- Policy and safety
  - `config.py`
  - `ignore.py`
  - `validator.py`
  - `audit.py`
- Extended behavior
  - `deps.py`
  - `middle_manager.py`
  - `raw_briefs.py`
  - `ui/` (whimsy/hype helpers)
- CLI modules
  - `cli/root.py`
  - `cli/doc_sync.py`
  - `cli/nav.py`
  - `cli/index.py`
  - `cli/brief.py`
  - `cli/roast.py`
  - `cli/status.py`
  - `cli/ci_guard.py`
  - `cli/query.py`
  - `cli/main.py`

## Core Data Artifacts

Scout relies on plain-text artifacts inside and outside the repo.

### Living docs

- Local docs next to source:
  - `<source_dir>/.docs/<filename>.tldr.md`
  - `<source_dir>/.docs/<filename>.deep.md`
  - `<source_dir>/.docs/<filename>.eliv.md`
- Central mirror:
  - `docs/livingDoc/<path>/<filename>.<kind>.md`

### Freshness metadata

- `<filename>.tldr.md.meta`
  - includes source hash and per-symbol hashes/content snapshots used for
    diff-aware reuse.

### Draft artifacts

- `docs/drafts/<stem>.commit.txt`
- `docs/drafts/<stem>.pr.txt` or `.pr.md`
- optional impact snippets depending on router config path.

### Graph and analysis artifacts

- `vivarium/.docs/call_graph.json` (when generated for vivarium scope)
- `~/.scout/dependency_graph.v2.json` (dependency graph cache)
- `~/.scout/raw_briefs/*.md` (optional stored raw gate briefs)

### Audit log

- `~/.scout/audit.jsonl`
  - append-only event stream for costs, models, confidence, and workflow events.

## Command Surfaces (Current)

Use module invocations as canonical behavior; wrappers may vary by environment.

### Canonical Python entrypoints

- `python -m vivarium.scout`
  - config and hook-oriented commands.
- `python -m vivarium.scout.cli.root`
  - `commit`, `pr`, `status`, `ship`.
- `python -m vivarium.scout.cli.doc_sync`
  - `generate`, `repair`, `export`, `validate`.
- Other direct CLIs:
  - `python -m vivarium.scout.cli.nav`
  - `python -m vivarium.scout.cli.index`
  - `python -m vivarium.scout.cli.brief`
  - `python -m vivarium.scout.cli.roast`
  - `python -m vivarium.scout.cli.ci_guard`

### Wrapper scripts

- `devtools/scripts/scout-nav`
- `devtools/scripts/scout-index`
- `devtools/scripts/scout-brief`
- `devtools/scripts/scout-roast`
- `devtools/scout-autonomy`

Top-level wrappers `devtools/scout-doc-sync`, `devtools/scout-commit`,
`devtools/scout-pr` are present and should be treated as hardening targets if
they diverge from module behavior.

## Primary Workflows

## 1) Living doc generation

Typical module command:

```bash
python -m vivarium.scout.cli.doc_sync generate --target vivarium/scout --recursive
```

Key behavior:

- parses supported files via adapter registry,
- computes source/symbol hashes,
- skips unchanged symbols where hashes match meta,
- generates missing/changed symbol docs via LLM,
- writes local + central mirrors,
- optionally updates module briefs and call graph.

## 2) Commit draft flow

High-level behavior:

1. staged changes are examined,
2. router draft generation may create per-file commit snippets,
3. `assemble_commit_message()` merges staged-file draft text.

Command:

```bash
python -m vivarium.scout.cli.root commit --preview
```

## 3) PR draft / synthesis flow

Two paths:

- staged/diff-based aggregation:
  - `assemble_pr_description()`
- docs-scoped aggregation:
  - `assemble_pr_description_from_docs()`

Then synthesis:

- `synthesize_pr_description()` (Gemini when configured, otherwise Groq path).

Command:

```bash
python -m vivarium.scout.cli.root pr --from-docs vivarium/scout --preview
```

## 4) Ship flow

`ship` orchestrates:

- doc sync (changed/staged scope),
- draft generation,
- commit,
- push,
- PR draft writing (or create path with flags).

Command:

```bash
python -m vivarium.scout.cli.root ship --dry-run-full
```

## 5) Navigation and briefing

Navigation:

- local index first (free),
- LLM fallback with validator checks and escalation path.

Briefing:

- nav target -> git context -> dependency map -> model-generated briefing.

## Configuration and Runtime Controls

Configuration layering is implemented in `config.py`:

1. default config
2. `~/.scout/config.yaml`
3. `.scout/config.yaml`
4. env variable overrides

Hard caps are non-overridable in code:

- per-event maximum cost,
- hourly budget ceiling,
- escalation cap values.

Operationally relevant env vars include:

- `GROQ_API_KEY`
- `GEMINI_API_KEY` (for big-brain paths)
- `SCOUT_MAX_CONCURRENT_CALLS`

See full schema and usage examples in `CONFIGURATION.md`.

## Testing Surface

Scout-focused tests live in `tests/scout/` and cover:

- audit behavior and performance,
- config resolution and hard caps,
- router orchestration paths,
- navigation and roast CLI behavior,
- whimsy relevance checks.

Recommended targeted runs:

```bash
pytest tests/scout -q
pytest tests/scout/cli -q
```

## Operational Hardening Areas

Current technical hardening priority areas:

1. wrapper/module command-surface consistency,
2. hook template correctness and install reliability,
3. clearer user-facing error paths for budget/concurrency failures,
4. stronger drift guards between docs and executable behavior.

The issue tracker should remain the source of truth for active work items and
status transitions.

## Troubleshooting Quick Reference

### Missing API key

- Symptom: environment/key error from LLM path.
- Action: set `GROQ_API_KEY` (and `GEMINI_API_KEY` if using big-brain paths).

### No draft produced in ship/commit flow

- Check staged files exist.
- Check hourly budget and per-event limits in Scout config.
- Check `docs/drafts/` outputs for current staged stems.

### Stale docs

Use validate/repair commands:

```bash
python -m vivarium.scout.cli.doc_sync validate --target vivarium --recursive
python -m vivarium.scout.cli.doc_sync repair --target vivarium --recursive
```

### Hook behavior unexpected

- Re-run installer:
  - `./devtools/scout-autonomy enable`
  - `./devtools/scout-autonomy enable-commit`
- Inspect `.git/hooks/*` for actual installed script content.

## Status Summary

Scout currently provides substantial documentation, drafting, and analysis
capability with working core modules. The next technical milestone is
integration hardening: ensure every documented command and hook path is
deterministic on fresh clone and continuously validated by smoke checks.
