#!/usr/bin/env bash
# devtools/_internal/common/utils.sh — Shared utilities for devtools scripts
# Sourced by branch-status, repo-map, ci-status. Do not run directly.

# Ensure PATH includes common install locations (for GUI launch; Finder doesn't inherit shell profile)
ensure_path() {
  export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
}

# Load .env from repo root if present (for API keys, etc.)
# Usage: load_dotenv "$REPO_ROOT"
load_dotenv() {
  local repo_root="${1:-}"
  [[ -z "$repo_root" ]] && return 0
  if [[ -f "$repo_root/.env" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$repo_root/.env"
    set +a
  fi
}

# Ensure gh CLI is available; tries to install via Homebrew if missing.
# Returns 0 if gh is available, 1 otherwise.
ensure_gh() {
  ensure_path
  if command -v gh &>/dev/null; then
    return 0
  fi
  if command -v brew &>/dev/null; then
    echo "Installing gh CLI via Homebrew..."
    if brew install gh 2>&1; then
      ensure_path
      command -v gh &>/dev/null && return 0
    fi
  fi
  echo "❌ gh CLI not found. Install with: brew install gh"
  echo "   https://cli.github.com/"
  return 1
}

# Ensure required Python modules; install via pip if missing.
# Usage: ensure_python_deps "$log_file" mod1 [mod2 ...]
# Returns 0 if all modules available, 1 if any install fails.
# log_file can be /dev/null if logging not needed.
ensure_python_deps() {
  local log_file="$1"
  shift
  local modules=("$@")
  [[ -n "$log_file" ]] && echo "--- Dependencies ---" >> "$log_file"
  for mod in "${modules[@]}"; do
    if python3 -c "import ${mod}" 2>/dev/null; then
      [[ -n "$log_file" ]] && echo "  ${mod}: already present" >> "$log_file"
    else
      [[ -n "$log_file" ]] && echo "  ${mod}: installing..." >> "$log_file"
      if ! python3 -m pip install "$mod" -q 2>>"${log_file:-/dev/null}"; then
        [[ -n "$log_file" ]] && echo "  ${mod}: install failed" >> "$log_file"
        [[ -n "$log_file" ]] && echo "--- End Dependencies ---" >> "$log_file"
        return 1
      fi
      [[ -n "$log_file" ]] && echo "  ${mod}: installed successfully" >> "$log_file"
    fi
  done
  [[ -n "$log_file" ]] && echo "--- End Dependencies ---" >> "$log_file"
  return 0
}

# Archive existing devtools output files before generating new ones.
# Usage: archive_devtools_output "$out_dir" pattern1 [pattern2 ...]
# Sets ARCHIVE_TIMESTAMP and archived_count.
# Example: archive_devtools_output "$OUT_DIR" "branch-status_*.md"
# Example: archive_devtools_output "$OUT_DIR" "ci-status_*.md" "ci-status_*.log"
archive_devtools_output() {
  local out_dir="$1"
  shift
  local patterns=("$@")
  local archive_dir="${out_dir}/archive"
  ARCHIVE_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  archived_count=0
  if [[ -d "$out_dir" ]]; then
    for pattern in "${patterns[@]}"; do
      for f in "$out_dir"/$pattern; do
        [[ -f "$f" ]] || continue
        base=$(basename "$f")
        ext="${base##*.}"
        stem="${base%.*}"
        mkdir -p "$archive_dir"
        dest="$archive_dir/${stem}_archived_${ARCHIVE_TIMESTAMP}.${ext}"
        if mv "$f" "$dest" 2>/dev/null; then
          ((archived_count++)) || true
        fi
      done
    done
  fi
}
