#!/usr/bin/env bash
# pr-message-gen.sh — Generate draft PR description from branch status, CI status, repo map
# Uses structured outputs from branch-status, ci-status, repo-map (programmatic analysis).
# Output: devtools/pr-message-gen/PR_DESCRIPTION_YYYYMMDD_HHMMSS.md (and optionally clipboard)
# READ-ONLY: Never modifies repo state.

set -euo pipefail

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

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUT_DIR="$DEVTOOLS_ROOT/pr-message-gen"
OUT_FILE="$OUT_DIR/PR_DESCRIPTION_${TIMESTAMP}.md"
mkdir -p "$OUT_DIR"

SCRIPTS_DIR="$DEVTOOLS_ROOT/scripts"

# --- 1. Branch status ---
echo "Fetching branch status..."
BRANCH_STATUS_FILE=""
if "$SCRIPTS_DIR/branch-status.sh" 2>/dev/null; then
  LATEST=$(ls -t "$DEVTOOLS_ROOT/branch-status"/branch-status_*.md 2>/dev/null | head -1)
  [[ -n "$LATEST" ]] && BRANCH_STATUS_FILE="$LATEST"
fi

if [[ -z "$BRANCH_STATUS_FILE" ]] || [[ ! -f "$BRANCH_STATUS_FILE" ]]; then
  echo "❌ Could not get branch status. Run ./devtools/scripts/branch-status.sh first."
  exit 1
fi

# --- 2. CI status (non-interactive: skip AI summarization, use programmatic extraction) ---
CI_STATUS_FILE=""
echo "Fetching CI status..."
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  if echo "n" | "$SCRIPTS_DIR/ci-status.sh" 2>/dev/null; then
    LATEST=$(ls -t "$DEVTOOLS_ROOT/ci-status"/ci-status_*.md 2>/dev/null | head -1)
    [[ -n "$LATEST" ]] && CI_STATUS_FILE="$LATEST"
  fi
fi
if [[ -z "$CI_STATUS_FILE" ]] || [[ ! -f "$CI_STATUS_FILE" ]]; then
  echo "⚠️  CI status not available (gh may not be authenticated). Using placeholder."
  CI_STATUS_FILE=""
fi

# --- 3. Repo map ---
REPO_MAP_FILE=""
echo "Fetching repo map..."
if [[ -x "$SCRIPTS_DIR/repo-map.sh" ]]; then
  if "$SCRIPTS_DIR/repo-map.sh" 2>/dev/null; then
    LATEST=$(ls -t "$DEVTOOLS_ROOT/repo-map"/repo-map_*.md 2>/dev/null | head -1)
    [[ -n "$LATEST" ]] && REPO_MAP_FILE="$LATEST"
  fi
fi

if [[ -z "$REPO_MAP_FILE" ]] || [[ ! -f "$REPO_MAP_FILE" ]]; then
  echo "⚠️  Repo map not available. Using branch status only."
  REPO_MAP_FILE=""
fi

# --- 4. Related issues (gh search) ---
GH_ISSUES=""
BRANCH_NAME=$(git branch --show-current 2>/dev/null || echo "")
if [[ -n "$BRANCH_NAME" ]] && command -v gh &>/dev/null && gh auth status &>/dev/null; then
  ISSUES_RAW=$(gh issue list --search "$BRANCH_NAME" --limit 5 --json number 2>/dev/null || true)
  if [[ -n "$ISSUES_RAW" ]]; then
    GH_ISSUES=$(echo "$ISSUES_RAW" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(','.join('#' + str(i['number']) for i in data))
except: pass
" 2>/dev/null || true)
  fi
fi

# --- 5. Run Python to build PR description (programmatic parsing, no LLM) ---
LIB_PATH="$DEVTOOLS_ROOT/_internal/pr-message-gen/pr-message-lib.py"

# Create empty temp files if paths missing (Python will handle empty content)
CI_INPUT="${CI_STATUS_FILE:-/dev/null}"
REPO_INPUT="${REPO_MAP_FILE:-/dev/null}"

GENERATED=$(python3 "$LIB_PATH" "$BRANCH_STATUS_FILE" "$CI_INPUT" "$REPO_INPUT" "$GH_ISSUES" 2>/dev/null) || {
  echo "❌ Failed to generate PR description."
  exit 1
}

echo "$GENERATED" > "$OUT_FILE"

# Optional: copy to clipboard
COPY_CLIPBOARD="${COPY_CLIPBOARD:-1}"
if [[ "$COPY_CLIPBOARD" == "1" ]] && [[ "$(uname -s)" == "Darwin" ]]; then
  pbcopy < "$OUT_FILE" 2>/dev/null && echo "📋 Copied to clipboard."
fi

echo ""
echo "✅ PR description generated: $OUT_FILE"
echo "   Run 'open $OUT_FILE' to open in editor."
