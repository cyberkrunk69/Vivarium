#!/usr/bin/env bash
# branch-status.sh — Branch status, unmerged commits, PR info, diff-stat vs master
# Output: devtools/branch-status/branch-status_YYYY-MM-DD_HH-MM-SS.md (single artifact, lean)
# READ-ONLY: Never modifies repo state.

set -euo pipefail

MAX_COMMITS=50
MAX_SUBJECT_LEN=65

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVTOOLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$DEVTOOLS_ROOT/.." && pwd)"
[[ -f "$REPO_ROOT/requirements.txt" ]] || { echo "❌ Not a Vivarium repo root (requirements.txt missing)"; exit 1; }
cd "$REPO_ROOT"

# Source common utilities
# shellcheck source=../_internal/common/utils.sh
source "$DEVTOOLS_ROOT/_internal/common/utils.sh"
ensure_path
load_dotenv "$REPO_ROOT"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUT_DIR="$DEVTOOLS_ROOT/branch-status"
OUT_FILE="$OUT_DIR/branch-status_${TIMESTAMP}.md"
mkdir -p "$OUT_DIR"

# Archive existing branch-status output files before generating new ones
archive_devtools_output "$OUT_DIR" "branch-status_*.md"

BRANCH=$(git branch --show-current)
BASE="${BASE_BRANCH:-master}"
git rev-parse -q "origin/$BASE" 2>/dev/null >/dev/null && BASE_REF="origin/$BASE" || BASE_REF="$BASE"

# --- PR status (gh if available) ---
PR_STATUS="(gh not installed)"
if command -v gh &>/dev/null; then
  PR_STATUS=$(gh pr view --json number,title,state,url 2>/dev/null | python3 -c "
import sys, json
try:
  d = json.load(sys.stdin)
  t = (d.get('title') or '')[:60]
  print(f\"#{d.get('number','?')}: {t} | {d.get('state','')} | {d.get('url','')}\")
except: print('(no PR for this branch)')
" 2>/dev/null) || PR_STATUS="(no PR for this branch)"
fi

# --- Commits on branch (not in base) ---
COMMITS_RAW=$(git log "$BASE_REF..HEAD" --format="%H|%an|%ae|%aI|%s" -$MAX_COMMITS 2>/dev/null) || true
COMMIT_COUNT=$(git rev-list --count "$BASE_REF..HEAD" 2>/dev/null || echo 0)

# --- Diff stat only (lean) ---
DIFF_STAT=$(git diff "$BASE_REF..HEAD" --stat 2>/dev/null) || true

# --- Build single .md file ---
{
  echo "# Branch Status: $BRANCH"
  echo "Generated: $TIMESTAMP"
  echo ""
  echo "## Summary"
  echo "- **Branch:** $BRANCH"
  echo "- **Base:** $BASE_REF"
  echo "- **Commits ahead:** $COMMIT_COUNT"
  echo "- **PR:** $PR_STATUS"
  echo ""
  echo "## Commits"
  echo ""
  echo "| Hash | Subject |"
  echo "|------|---------|"
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    H=$(echo "$line" | cut -d'|' -f1 | cut -c1-7)
    S=$(echo "$line" | cut -d'|' -f5 | sed 's/|/\\|/g' | cut -c1-$MAX_SUBJECT_LEN)
    echo "| $H | $S |"
  done <<< "$COMMITS_RAW"
  [[ $COMMIT_COUNT -gt $MAX_COMMITS ]] && echo "| ... | *($((COMMIT_COUNT - MAX_COMMITS)) more)* |"
  echo ""
  echo "## Diff vs $BASE_REF (stat)"
  echo ""
  echo '```'
  echo "$DIFF_STAT"
  echo '```'
} > "$OUT_FILE"

# Copy to clipboard (macOS)
[[ "$(uname -s)" == "Darwin" ]] && pbcopy < "$OUT_FILE" 2>/dev/null || true

echo ""
echo "✅ Branch status captured: $BRANCH ($COMMIT_COUNT commits ahead of $BASE_REF)"
echo "   Output: $OUT_FILE"
[[ ${archived_count:-0} -gt 0 ]] && echo "   Archived: $archived_count previous output file(s) to $OUT_DIR/archive"
echo "   Copied to clipboard."
