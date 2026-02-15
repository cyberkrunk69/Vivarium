#!/usr/bin/env bash
set -euo pipefail

# Organize/prioritize existing GitHub issues for Scout hardening.
# Usage:
#   ./devtools/triage-issues.sh [owner/repo] [--close-resolved]

REPO="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
CLOSE_RESOLVED="${2:-}"

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
  gh issue close 85 --comment "Closing as completed by hook hardening + smoke validation in PR #95/#97." --repo "$REPO"
  gh issue close 87 --comment "Closing as completed: CI now runs Scout smoke checks via .github/workflows/ci.yml." --repo "$REPO"
  gh issue close 91 --comment "Closing as completed: doc_sync repair returns 0 on fresh docs (smoke test validates)." --repo "$REPO"
  gh issue close 92 --comment "Closing as completed: legacy vivarium/scout/cli.py entrypoint removed; canonical cli/main.py remains." --repo "$REPO"
fi

echo "Issue triage plan applied."
