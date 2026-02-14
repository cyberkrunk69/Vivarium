#!/usr/bin/env bash
# commit-message-gen.sh — Generate draft conventional commit message from staged changes
# Output: stdout (and optionally clipboard)
# READ-ONLY: Never modifies repo state (does not commit).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVTOOLS_ROOT="$SCRIPT_DIR"
REPO_ROOT="$(cd "$DEVTOOLS_ROOT/.." && pwd)"
[[ -f "$REPO_ROOT/requirements.txt" ]] || { echo "❌ Not a Vivarium repo root (requirements.txt missing)"; exit 1; }
cd "$REPO_ROOT"

# Source common utilities
# shellcheck source=_internal/common/utils.sh
source "$SCRIPT_DIR/_internal/common/utils.sh"
ensure_path
load_dotenv "$REPO_ROOT"

# --- Check for staged files ---
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null) || true
if [[ -z "$STAGED_FILES" ]]; then
  echo "❌ No staged files. Stage changes with: git add <files>"
  exit 1
fi

# --- Get staged diff ---
STAGED_DIFF=$(git diff --cached 2>/dev/null) || true
if [[ -z "$STAGED_DIFF" ]]; then
  echo "❌ Could not get staged diff."
  exit 1
fi

# --- Run Python analyzer ---
LIB_PATH="$SCRIPT_DIR/_internal/commit-message-gen/commit-message-lib.py"
STAGED_PATHS=$(echo "$STAGED_FILES" | tr '\n' ' ')

GENERATED=$(echo "$STAGED_DIFF" | python3 "$LIB_PATH" "$STAGED_PATHS" 2>/dev/null) || {
  echo "❌ Failed to generate commit message."
  exit 1
}

echo "$GENERATED"

# Optional: copy to clipboard (macOS)
COPY_CLIPBOARD="${COPY_CLIPBOARD:-1}"
if [[ "$COPY_CLIPBOARD" == "1" ]] && [[ "$(uname -s)" == "Darwin" ]]; then
  if echo "$GENERATED" | pbcopy 2>/dev/null; then
    echo "" && echo "📋 Copied to clipboard."
  fi
fi
