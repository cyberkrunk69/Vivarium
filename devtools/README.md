# Devtools

Developer utilities for Vivarium. Each script produces a single `.md` artifact. Output directories are gitignored.

## Directory Structure

```
devtools/
├── scripts/                    # Executable scripts (CLI entry points)
│   ├── ci-status.sh
│   ├── branch-status.sh
│   ├── repo-map.sh
│   ├── commit-message-gen.sh
│   └── pr-message-gen.sh
├── _internal/                  # Internal logic, shared libs, supporting files
│   ├── ci-status/              # Dry-run + execute split, ci-status-lib.py
│   ├── common/                 # utils.sh, api-confirm.sh
│   ├── commit-message-gen/     # commit-message-lib.py
│   └── pr-message-gen/         # pr-message-lib.py
├── ci-status-gui.app           # GUI launchers (one-click from Finder)
├── branch-status-gui.app
├── repo-map-gui.app
├── commit-message-gen-gui.app
├── pr-message-gen-gui.app
└── README.md
```

## Usage

**One-click execution:** Double-click the `.app` files in Finder:

- `ci-status-gui.app` — CI/CD status (native dialog for cost confirmation)
- `branch-status-gui.app` — Branch status, PR info, diff-stat
- `repo-map-gui.app` — Structural inventory for Python/GitHub repos
- `commit-message-gen-gui.app` — Generate conventional commit message from staged changes
- `pr-message-gen-gui.app` — Generate PR description from branch, CI, and repo map

**Command line:** Run the scripts in `devtools/scripts/`:

- `./devtools/scripts/ci-status.sh` or `CI_STATUS_BRANCH=main ./devtools/scripts/ci-status.sh`
- `./devtools/scripts/branch-status.sh` or `BASE_BRANCH=main ./devtools/scripts/branch-status.sh`
- `./devtools/scripts/repo-map.sh`
- `./devtools/scripts/commit-message-gen.sh` — requires staged files (`git add` first)
- `./devtools/scripts/pr-message-gen.sh`

## Unified API Confirmation

Scripts that may incur API costs (e.g., ci-status with Groq) use a consistent confirmation system:

- **Environment variable:** `VIVARIUM_CONFIRM_AI=1` — Skip interactive prompt, auto-confirm API calls.
- **Interactive:** When run from terminal, prompts for confirmation before making API calls.
- **Non-interactive:** When stdin is piped (e.g. `echo "n" | ci-status.sh`), defaults to no API calls and uses programmatic extraction only.
- **Cost estimation:** Every script that uses APIs estimates and displays costs before proceeding.

## branch-status

Branch status, unmerged commits, PR info, and diff-stat vs base (master). Lean output (~10KB).

**Output:** `devtools/branch-status/branch-status_YYYY-MM-DD_HH-MM-SS.md`

## commit-message-gen

Generate a draft conventional commit message from staged changes. Uses programmatic diff analysis (path + content keywords) — no LLM. Infers type (feat, fix, docs, style, refactor, test, chore), scope from file paths, and suggests `BREAKING CHANGE` when appropriate.

**Output:** stdout (and clipboard on macOS)

**Requirements:** Staged files (`git add` first). Exits with error if nothing is staged.

**Options:** `COPY_CLIPBOARD=0` to disable clipboard copy.

## pr-message-gen

Generate a draft PR description from branch commits, CI status, and repo map. Runs `branch-status.sh`, `ci-status.sh`, and `repo-map.sh` to gather data, then formats a Markdown template with Summary, Affected Areas, CI Status, Testing checklist, and Related Issues. Uses programmatic parsing only — no LLM.

**Output:** `devtools/pr-message-gen/PR_DESCRIPTION_YYYYMMDD_HHMMSS.md` (and clipboard on macOS)

**Requirements:** `gh` optionally for CI status and related issues. Repo map requires macOS.

**Options:** `COPY_CLIPBOARD=0` to disable clipboard copy.

## repo-map

Pure structural inventory for Python/GitHub repos. Uses programmatic discovery (find, grep, awk) — no LLM. Output includes file tree, dependencies, workflows, imports, tests, docs, git signals, and markers (TODO/FIXME).

**Output:** `devtools/repo-map/repo-map_YYYY-MM-DD_HH-MM-SS.md`

## ci-status

CI/CD status for current branch (workflows, jobs, runs). Compact summaries for passing jobs; full details (workflow, job, conclusion, timestamps, failure logs) for failed jobs.

**Output:** `devtools/ci-status/ci-status_YYYY-MM-DD_HH-MM-SS.md`

Requires `gh` CLI (authenticated). Uses `gh run list` and `gh run view`.

### Analysis approach

- **Programmatic first:** Logs are filtered (noise, ANSI escape codes, timestamps) and condensed to failure-relevant blocks.
- **AI summarization (optional):** When `GROQ_API_KEY` is set and there are failed jobs, Groq API can summarize logs. Always prompts for confirmation (or respects `VIVARIUM_CONFIRM_AI=1`).
- **Fallback:** Programmatic extraction (coverage, AssertionError, ImportError patterns) when AI is declined or not configured.

### GUI (one-click)

Double-click `ci-status-gui.app` in Finder for a native macOS permission gate:

1. Runs the dry-run script to estimate cost
2. Shows a dialog: *"Estimated Groq API cost: $X.XX for N job(s). Execute with this cost? [Yes/No]"*
3. If **Yes**: opens Terminal and runs the execute script (auto-confirms)
4. If **No**: quits without making API calls

### Two-step process (dry-run + execute)

When using AI summarization, the workflow is split into two scripts for reliable terminal prompting:

1. **Dry run** — `./devtools/_internal/ci-status/ci-status-dry-run.sh`
   - Fetches runs, identifies failed ones, preprocesses logs, estimates costs
   - Prints estimated cost to the terminal
   - Saves job data to `/tmp/ci_status_plan_YYYYMMDD_HHMMSS.json`
   - Does **not** make any Groq API calls

2. **Execute** — `./devtools/_internal/ci-status/ci-status-execute.sh`
   - Finds the latest plan file in `/tmp`
   - Prompts: `Execute with estimated cost: $X.XX for N job(s)? [y/n]`
   - If `y` or `yes`, or `VIVARIUM_CONFIRM_AI=1`: makes Groq API calls and generates the summary markdown
   - If `n` or non-interactive: exits without making API calls (or uses programmatic extraction when called via orchestrated flow)

### AI summarization and costs

When `GROQ_API_KEY` is set, the execute script uses Groq's API (llama3-8b-8192) to summarize failed-job logs. **This incurs API costs.**

- **Pre-run confirmation:** The execute script (or `ci-status.sh` orchestrator) prompts before any Groq calls.
- **Token-efficient pre-processing:** Logs are filtered and condensed before calling the API.
- **Cost breakdown:** See the processing log (`.log` file) for per-request cost and token counts. The summary markdown ends with **Total API Cost Incurred: $X.XX** when costs were incurred.
