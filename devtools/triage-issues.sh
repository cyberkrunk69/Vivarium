#!/usr/bin/env bash
set -euo pipefail

# Organize/prioritize existing GitHub issues for Scout hardening.
# Usage:
#   ./devtools/triage-issues.sh [owner/repo] [--close-resolved] [--create-gaps] [--update-tracker]

# First non-flag arg is repo
REPO=""
for a in "$@"; do
  if [[ "$a" != --* ]]; then
    REPO="$a"
    break
  fi
done
REPO="${REPO:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
CLOSE_RESOLVED=""
for a in "$@"; do [[ "$a" == "--close-resolved" ]] && CLOSE_RESOLVED="$a" && break; done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required." >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "gh CLI is not authenticated." >&2
  exit 1
fi

echo "Applying issue triage plan to $REPO"

# Priority labels
gh label create "priority:p0" --color "B60205" --description "Highest urgency; block/critical" --force --repo "$REPO"
gh label create "priority:p1" --color "D93F0B" --description "High priority; next sprint" --force --repo "$REPO"
gh label create "priority:p2" --color "FBCA04" --description "Important but not urgent" --force --repo "$REPO"

# Taxonomy labels
gh label create "type:tracker" --color "5319E7" --description "Tracking/meta issue" --force --repo "$REPO"
gh label create "area:security-governance" --color "1D76DB" --description "Branch protection, ownership, policy" --force --repo "$REPO"
gh label create "area:ci-quality" --color "0E8A16" --description "CI, tests, lint, coverage, quality gates" --force --repo "$REPO"
gh label create "area:scout" --color "0052CC" --description "Scout tooling and workflows" --force --repo "$REPO"

# Tracker
gh issue edit 93 --add-label "type:tracker,priority:p0,area:scout,area:ci-quality" --repo "$REPO"

# Open hardening items still requiring delivery
gh issue edit 89 --add-label "priority:p0,area:scout,area:ci-quality" --repo "$REPO"
gh issue edit 90 --add-label "priority:p0,area:scout,area:ci-quality" --repo "$REPO"
gh issue edit 88 --add-label "priority:p1,area:scout" --repo "$REPO"
gh issue edit 86 --add-label "priority:p1,area:scout" --repo "$REPO"

# Candidate-complete items (kept open by default; optional auto-close)
gh issue edit 85 --add-label "priority:p1,area:scout,area:ci-quality" --repo "$REPO"
gh issue edit 87 --add-label "priority:p1,area:scout,area:ci-quality" --repo "$REPO"
gh issue edit 91 --add-label "priority:p1,area:scout,area:ci-quality" --repo "$REPO"
gh issue edit 92 --add-label "priority:p1,area:scout,area:ci-quality" --repo "$REPO"

if [[ "$CLOSE_RESOLVED" == "--close-resolved" ]]; then
  gh issue close 85 --comment "Closing as completed by PR #97. Hooks source utils.sh; find_python works; smoke test Test 4 validates. devtools/scout-autonomy enable-commit installs prepare-commit-msg. Evidence: devtools/scout-autonomy, devtools/_internal/common/utils.sh, devtools/scout-smoke-test.sh" --repo "$REPO"
  gh issue close 87 --comment "Closing as completed by PR #97. CI runs Scout Smoke Tests via .github/workflows/ci.yml (line 34-35). Smoke test covers wrappers, find_python, hooks, doc_sync repair. Evidence: ci.yml, devtools/scout-smoke-test.sh" --repo "$REPO"
  gh issue close 91 --comment "Closing as completed by PR #97. doc_sync repair returns 0 on success (no stale + repaired). Evidence: vivarium/scout/cli/doc_sync.py _handle_repair (lines 384-437), devtools/scout-smoke-test.sh Test 6" --repo "$REPO"
  gh issue close 92 --comment "Closing as completed by PR #97. Legacy vivarium/scout/cli.py removed; canonical cli/ package. Wrappers use vivarium.scout.cli.* submodules. Evidence: no cli.py in vivarium/scout/" --repo "$REPO"
fi

# Optional: update tracker #93 body (run with --update-tracker)
for arg in "$@"; do
  if [[ "$arg" == "--update-tracker" ]]; then
    gh issue edit 93 --body-file "$REPO_ROOT/.github/ISSUE_93_BODY_UPDATE.md" --repo "$REPO"
    echo "Updated #93 body."
    break
  fi
done

# Optional: create new issues for real gaps (run with --create-gaps)
for arg in "$@"; do
  if [[ "$arg" != "--create-gaps" ]]; then continue; fi
  echo "Creating new gap issues..."
  gh issue create --title "Ruleset hygiene: single canonical ruleset, remove stale/disabled confusion" \
    --body "Define single canonical ruleset; remove or document disabled/stale rules; align branch protection with policy_guard.py expectations. See docs/ISSUE_TRIAGE_REPORT_20260214.md" \
    --label "priority:p1,area:security-governance" --repo "$REPO"
  gh issue create --title "CI: add validate-content check for [GAP]/[FALLBACK]/[PLACEHOLDER] invariant" \
    --body "scout-doc-sync validate-content exists but is not run in CI. Add step to ci.yml to fail when generated docs contain forbidden markers. Complements #89." \
    --label "priority:p0,area:ci-quality,area:scout" --repo "$REPO"
  gh issue create --title "Scout doc fidelity: add regression tests for enum/method/async attribution" \
    --body "Add tests (or expand test_ast_facts.py) to guard enum attribution, method_signatures extraction, async function handling. Prevents regression of AST fact extraction fidelity." \
    --label "priority:p2,area:scout,area:ci-quality" --repo "$REPO"
  gh issue create --title "Lint debt strategy: incremental ratchet vs full reformat plan" \
    --body "CI enforces lint on changed files. Global repo has formatting debt. Document strategy: incremental ratchet (current) vs one-time full reformat. Decide and document." \
    --label "priority:p2,area:ci-quality" --repo "$REPO"
  break
done

echo "Issue triage plan applied."
