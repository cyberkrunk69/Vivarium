#!/usr/bin/env bash
set -euo pipefail

# Apply strict branch protection to master/main for owner-controlled merges.
# Usage:
#   ./devtools/apply-branch-protection.sh [owner/repo] [owner-login]

REPO="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
POLICY_OWNER="${2:-cyberkrunk69}"

REQUIRED_CHECKS=("policy" "tests" "integration" "lint")

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required." >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

echo "Applying protection for repo: $REPO"
echo "Owner-locking push access to: $POLICY_OWNER"
echo "Required checks: ${REQUIRED_CHECKS[*]}"

apply_branch_protection() {
  local branch="$1"
  local payload_file
  payload_file="$(mktemp)"

  cat >"$payload_file" <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["policy", "tests", "integration", "lint"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1,
    "require_last_push_approval": true
  },
  "restrictions": {
    "users": ["$POLICY_OWNER"],
    "teams": [],
    "apps": []
  },
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": true
}
EOF

  echo "  -> Protecting branch '$branch'"
  gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "repos/$REPO/branches/$branch/protection" \
    --input "$payload_file" >/dev/null

  rm -f "$payload_file"
}

for branch in master main; do
  if gh api "repos/$REPO/branches/$branch" >/dev/null 2>&1; then
    apply_branch_protection "$branch"
  else
    echo "  -> Skipping '$branch' (branch does not exist)"
  fi
done

echo ""
echo "Branch protection applied successfully."
echo "Tip: run 'gh pr checks <pr-number>' to confirm required check names are correct."
