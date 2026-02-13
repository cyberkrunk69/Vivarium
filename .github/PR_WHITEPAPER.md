# Scout Living Documentation: A Technical White Paper

## Pull Request #80 — Add living documentation (scout) and devtools

**Author:** Vivarium Team  
**Branch:** `livingDocumentation` → `master`  
**Status:** Open

---

## Executive Summary

This pull request introduces **Scout** — an autonomous, editor-agnostic development partner that generates living documentation, assembles commit and PR drafts from staged changes, and provides impact-aware code critique. Scout operates entirely via plain-text artifacts, integrates natively with Git, and is designed for cost predictability and full auditability.

The central innovation is **living documentation**: `.tldr.md`, `.deep.md`, and `.eliv.md` files generated alongside source code, which serve as persistent context for AI-assisted workflows without locking developers into any IDE or model vendor. Scout augments the existing Vivarium devtools with a complete documentation-to-draft pipeline: from source analysis → symbol-level docs → commit/PR drafts → human review.

**Key contributions:**

- **vivarium/scout** — Python package for doc generation, draft assembly, audit logging, config management, and multi-language adapters (Python, JavaScript, plain text)
- **devtools** — CLI launchers: scout-doc-sync, scout-commit, scout-pr, scout-nav, scout-brief, scout-roast, scout-status, scout-ci-guard, scout-index
- **Living docs** — 50,000+ lines of generated documentation across scout modules
- **--from-docs mode** — PR description synthesis from `.tldr.md` files without requiring Git changes
- **UX improvements** — Auto-load `.env`, symbol-level progress, no screen clearing on chained commands

---

## 1. Background & Motivation

### 1.1 The Context Problem

Modern codebases are large and dense. When an AI assistant (or a human) needs to understand a module, they typically rely on:

- Docstrings (often sparse or stale)
- README files (high-level only)
- Ad-hoc grep and navigation

This creates a **context gap**: the AI lacks structured, up-to-date summaries of what each symbol does, how it fits into the system, and what it depends on. The result is generic or hallucinated responses.

### 1.2 The Vendor Lock-in Problem

Many AI-assisted development tools are tightly coupled to:

- A specific IDE (VS Code, Cursor, etc.)
- A specific model vendor (OpenAI, Anthropic, etc.)
- Opaque, non-auditable API usage

Teams that value flexibility, cost control, and auditability are underserved.

### 1.3 The Cost Surprise Problem

LLM usage is expensive and unpredictable when:

- Full file contents are sent repeatedly
- There is no diff-awareness (regenerating unchanged content)
- There is no audit trail of what was called and at what cost

### 1.4 Design Goals

Scout was designed to address these issues:

| Goal | Approach |
|------|----------|
| **Editor-agnostic** | All artifacts are plain text. No IDE extensions required. |
| **Model-agnostic** | Default: Groq (llama-3.1-8b-instant, llama-3.3-70b-versatile). Supports local LLMs. |
| **Git-native** | Docs and drafts live in the repo. Human-in-the-loop at every step. |
| **Cost-aware** | Audit logs, hourly caps, confidence thresholds. No surprise bills. |
| **Auditable** | Every LLM call logged to `~/.scout/audit.jsonl` with cost, model, tokens. |

---

## 2. Problem Statement

**How do we provide AI assistants (and developers) with structured, current, and cost-efficient context about a codebase — without IDE lock-in or vendor lock-in?**

Sub-problems:

1. **Documentation generation**: Produce meaningful summaries at the symbol level (functions, classes, modules) that capture purpose, logic flow, and dependencies.
2. **Draft assembly**: Use these docs to assemble commit messages and PR descriptions without additional LLM calls at commit/PR time.
3. **Diff-awareness**: Only regenerate documentation for symbols whose source has changed (hash-based).
4. **Multi-language support**: Handle Python, JavaScript, and plain text with pluggable adapters.
5. **PR from docs**: Support generating PR descriptions for entire packages even when no files are "changed" in Git (e.g., for documentation-only or refactor PRs).

---

## 3. Solution Architecture

### 3.1 High-Level Pipeline

```
Source Files (.py, .js, ...)
        │
        ▼
   Static Analysis (AST, import map)
        │
        ▼
   Symbol Extraction (per-file, per-symbol)
        │
        ▼
   Hash Check (skip unchanged symbols)
        │
        ▼
   LLM Generation (tldr, deep, eliv per symbol)
        │
        ▼
   .tldr.md, .deep.md, .eliv.md → <source>/.docs/
        │
        ▼
   Mirror to docs/livingDoc/<path>/
        │
        ▼
   Hooks / Manual: drafts → docs/drafts/*.commit.txt, *.pr.md
        │
        ▼
   scout-commit / scout-pr: assemble from drafts (no LLM)
```

### 3.2 Component Overview

| Component | Responsibility |
|-----------|----------------|
| **vivarium/scout/doc_generation** | Trace files, partition symbols, call LLM, write docs, manage concurrency and budget |
| **vivarium/scout/adapters** | Pluggable parsers: Python (AST), JavaScript (tree-sitter), plain text |
| **vivarium/scout/git_drafts** | Assemble commit/PR from `docs/drafts/*` or `.tldr.md` (--from-docs) |
| **vivarium/scout/llm** | Groq API client, rate-limit handling, cost estimation |
| **vivarium/scout/audit** | Append-only JSONL logging of all events |
| **vivarium/scout/config** | YAML config merge, triggers, limits |
| **vivarium/scout/validator** | Path validation, hallucination detection |

### 3.3 Data Flow

```
.tldr.md     → Compact per-symbol summary
.deep.md     → Detailed logic, dependencies, edge cases
.eliv.md     → "Explain Like I'm Very Young" — simplified
*.tldr.md.meta → JSON: source_hash, symbol hashes (freshness)
call_graph.json → Nodes (path::symbol), edges (calls)
```

---

## 4. Key Features & Components

### 4.1 Living Documentation

**Formats:**

- **`.tldr.md`** — One paragraph per symbol. Purpose, key calls, types. Optimized for fast context loading.
- **`.deep.md`** — Full logic overview, dependency interactions, potential considerations. For deep dives.
- **`.eliv.md`** — Simplified explanations. For onboarding or non-experts.

**Placement:**

- **Local:** `<source_dir>/.docs/<filename>.tldr.md` (e.g. `vivarium/scout/.docs/doc_generation.py.tldr.md`)
- **Central:** `docs/livingDoc/<path>/<filename>.tldr.md` (mirrored for central browsing)

**Freshness:**

- `.tldr.md.meta` stores `source_hash` and per-symbol hashes.
- Regeneration skips symbols whose source snippet hash matches.
- Enables incremental updates with minimal LLM cost.

### 4.2 Commit & PR Draft Assembly

**scout-commit:**

- Reads `docs/drafts/{stem}.commit.txt` for each staged `.py` file.
- Aggregates into a single message.
- No LLM at commit time — drafts are pre-generated by hooks or doc-sync.

**scout-pr (Git-based):**

- Resolves files: `--files`, `--base-branch`, upstream, or staged.
- Reads `docs/drafts/{stem}.pr.md` per file.
- Groups by package, includes `__init__.py.module.md` summaries.
- Calls `synthesize_pr_description` (LLM) to produce cohesive narrative.

**scout-pr --from-docs (NEW):**

- **Ignores Git entirely.**
- Reads all `.tldr.md` files under `PATH/.docs/` (e.g. `vivarium/scout`).
- Appends call graph summary (caller → callee edges within scope).
- Synthesizes PR description via LLM.
- **Works when no files are "changed"** — ideal for documenting a whole package or refactor PRs.

```bash
./devtools/scout-pr --from-docs vivarium/scout --preview > SCOUT_PR.md
```

### 4.3 Auto-Load `.env`

- **python-dotenv** added to `requirements-dev.txt`.
- `load_dotenv()` at startup in `vivarium/scout/cli/root.py` and `vivarium/scout/cli/doc_sync.py`.
- Ensures `GROQ_API_KEY` and other secrets are loaded when running `python -m vivarium.scout.cli.root pr` directly (e.g. from a different cwd).

### 4.4 Fail-Fast on Missing API Key

- **Before:** Silent fallback to raw summaries when `GROQ_API_KEY` missing.
- **After:** `EnvironmentError("GROQ_API_KEY missing. Set it in .env or environment.")` — no silent degradation.
- **Opt-in fallback:** `--fallback-template` flag restores fallback behavior when explicitly set.

### 4.5 UX Fixes

| Issue | Fix |
|-------|-----|
| Screen cleared at doc-sync end | Replaced `_CLEAR_SCREEN` with newline — preserves last dashboard frame when chained with another command |
| Large files appear frozen | Symbol-level progress `[12/85]` in dashboard for files with 2+ symbols to generate |
| Implicit fallback | `--fallback-template` required for raw-on-failure; default is raise |
| Unclear auto-draft behavior | `--no-auto-draft` added; only write `.github/pr-draft.md` when `--auto-draft` used |

### 4.6 Devtools Launchers

| Launcher | Purpose |
|----------|---------|
| **scout-doc-sync** | Generate living docs (parallel workers, budget, `--no-eliv`, `--force`) |
| **scout-commit** | Assemble commit from drafts; `--preview` for stdout |
| **scout-pr** | Assemble PR from drafts or `--from-docs`; `--preview`, `--auto-draft`, `--create` |
| **scout-nav** | Natural-language navigation (index-first, LLM fallback) |
| **scout-brief** | Investigation plan for expensive models |
| **scout-roast** | Efficiency reports + impact-aware critique |
| **scout-status** | Dashboard: doc/draft/audit health, spend, hooks |
| **scout-ci-guard** | CI validation: coverage, confidence, spend limits |
| **scout-index** | Local search (ctags + SQLite, zero LLM) |

---

## 5. Implementation Details

### 5.1 Symbol Extraction

- **Python:** `ast` module → `PythonAdapter` → `SymbolTree` with `name`, `calls`, `types`, `exports`, `lineno`, `end_lineno`.
- **JavaScript:** `tree-sitter` (optional) → `JavaScriptAdapter`. Falls back to plain text if unavailable.
- **Plain text:** Line-based heuristics.

### 5.2 Diff-Aware Generation

For each symbol:

1. Compute `symbol_hash` = SHA256 of source snippet (lines `lineno`–`end_lineno`).
2. Read `.tldr.md.meta` → `symbols[name].hash`.
3. If match → reuse `tldr`, `deep`, `eliv` from meta. No LLM call.
4. Else → generate via LLM, store in meta.

### 5.3 Concurrency & Rate Limits

- **File-level:** `asyncio.Semaphore(workers)` — default from `min(8, cpu_count)` or model RPM.
- **Symbol-level:** `per_file_concurrency=3` — max 3 concurrent LLM calls per file.
- **Global:** `SCOUT_MAX_CONCURRENT_CALLS` env var caps total in-flight calls.
- **Rate limit (429):** Automatic retry with backoff; fallback to 8b model when 70b rate-limited.

### 5.4 Call Graph

- **Export:** `doc_generation.export_call_graph(target_path)` → `call_graph.json` with `nodes` (path::symbol) and `edges` (from, to, type).
- **Downstream impact:** `get_downstream_impact(changed_files, call_graph_path, repo_root)` → transitive callees from changed files.
- **--from-docs:** `_call_graph_summary_for_scope()` extracts edges within scope, appends to raw PR body.

### 5.5 Audit Log

- **Path:** `~/.scout/audit.jsonl`
- **Format:** One JSON object per line. Fields: `ts`, `event`, `session_id`, `cost`, `model`, `input_t`, `output_t`, `symbol`, `package`, etc.
- **Events:** `tldr`, `deep`, `eliv`, `module_brief`, `pr_synthesis`, `doc_sync`, `tldr_fallback_template`, etc.

---

## 6. Usage & Workflows

### 6.1 Basic Doc Sync → Commit

```bash
# 1. Generate docs for a module
./devtools/scout-doc-sync generate --target vivarium/scout --recursive

# 2. Make a change
echo "# change" >> vivarium/scout/router.py
git add vivarium/scout/router.py

# 3. (Optional) Hooks regenerate drafts on post-commit
# Or run doc-sync again for changed files

# 4. Preview assembled commit message
./devtools/scout-commit --preview

# 5. Commit
./devtools/scout-commit
```

### 6.2 PR from Living Docs (No Git Changes)

```bash
# Generate docs for entire package
./devtools/scout-doc-sync generate --target vivarium/scout --recursive --no-eliv

# Synthesize PR description from .tldr.md files (ignores Git)
./devtools/scout-pr --from-docs vivarium/scout --preview > SCOUT_PR.md

# Or with auto-draft
./devtools/scout-pr --from-docs vivarium/scout --auto-draft
# Writes .github/pr-draft.md
```

### 6.3 CI Integration

```bash
# scout-ci-guard: exit 1 if quality gates fail
./devtools/scout-ci-guard --base-branch origin/master --hourly-limit 5
```

### 6.4 Scout Autonomy (Git Hooks)

```bash
./devtools/scout-autonomy enable
# Installs pre-commit (doc-sync for changed files) and pre-push (validate + PR draft)
```

---

## 7. Design Decisions

### 7.1 Plain Text Over Binary

All artifacts are Markdown or JSON. Benefits:

- Versionable, diffable, grep-able
- No proprietary format
- Human-readable for debugging

### 7.2 Local-First Docs

Docs live next to source (`<source>/.docs/`). Benefits:

- Colocation: when you open a file, docs are nearby
- Package-scoped: each package owns its docs
- Mirror to central `docs/livingDoc/` for browsing

### 7.3 No Silent Fallbacks

Default: fail loudly when LLM or API key is missing. Rationale:

- Predictability: users know when something is wrong
- `--fallback-template` opt-in for degraded mode

### 7.4 Groq as Default

- Fast inference (llama-3.1-8b-instant)
- Predictable pricing
- Avoid `groq/compound` for doc generation (agentic; unpredictable cost)

---

## 8. Testing & Validation

- **Unit tests:** `tests/scout/` — draft assembly, git analyzer, config
- **Smoke test:** `./devtools/scout-smoke-test.sh` — full loop offline
- **Draft system:** `pytest tests/scout/test_draft_*.py`

---

## 9. Migration & Rollout

1. **Install dependencies:** `pip install -r requirements-groq.txt` (and `requirements-dev.txt` for python-dotenv)
2. **Set API key:** `GROQ_API_KEY` in `.env` or environment
3. **Generate docs:** `./devtools/scout-doc-sync generate -t vivarium/scout -r`
4. **Optional hooks:** `./devtools/scout-autonomy enable`

No breaking changes to existing workflows. Scout is additive.

---

## 10. Future Work

- **Module brief cascading:** Improve `__init__.py.module.md` generation from child `.tldr.md` and call graph
- **Knowledge graph export:** `doc_generation.export_knowledge_graph()` — entity-relation extraction
- **Local LLM support:** Pluggable backend for Ollama, LM Studio, etc.
- **More languages:** TypeScript, Go, Rust via tree-sitter adapters

---

## 11. Appendix

### A. File Inventory (Scout-Related)

| Path | Purpose |
|------|---------|
| `vivarium/scout/` | Core package |
| `vivarium/scout/cli/` | CLI subcommands (root, doc_sync, nav, brief, roast, etc.) |
| `vivarium/scout/adapters/` | Python, JavaScript, plain text parsers |
| `docs/livingDoc/vivarium/scout/` | Mirrored living docs |
| `docs/drafts/` | Commit and PR drafts |
| `devtools/scout-*` | Launcher scripts |
| `~/.scout/audit.jsonl` | Event log |

### B. Environment Variables

| Variable | Purpose |
|----------|---------|
| `GROQ_API_KEY` | Required for LLM calls |
| `SCOUT_MAX_CONCURRENT_CALLS` | Cap in-flight LLM calls |
| `GROQ_API_URL` | Override API endpoint |

### C. Commit Summary

```
538fa03 feat(scout): --from-docs mode, dotenv, UX fixes
ab28b1f docs(scout): regenerate living documentation
0b6db9a [__init__.py]: No draft available
f113120 feat(scout): Add documentation for changed symbols
34b5717 Load .env for scout scripts; relax audit query perf threshold for CI
a9eded8 Add living documentation (scout) and devtools
```

---

## Gatekeeper Checklist

- [ ] Tests pass (`pytest`)
- [ ] I understand this repo requires approval from **@cyberkrunk69**
- [ ] This change is submitted via a PR (no direct pushes)
- [ ] Any security impact has been considered and documented
