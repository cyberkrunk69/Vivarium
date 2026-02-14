#!/usr/bin/env bash
# scout-reset-lib.sh — Helper functions for scout-reset CLI
# Sourced by devtools/scout-reset. Do not run directly.

# Discover all Scout-generated artifact paths.
# Sets DISCOVERED_PATHS (array) and optionally FULL_PATHS when --full.
# Usage: discover_scout_artifacts "$REPO_ROOT" [full]
discover_scout_artifacts() {
  local repo_root="${1:?}"
  local include_full="${2:-}"
  DISCOVERED_PATHS=()

  # Repo-local: living docs (*/.docs/*)
  while IFS= read -r -d '' p; do
    [[ -n "$p" ]] && [[ -f "$p" ]] && DISCOVERED_PATHS+=("$p")
  done < <(find "$repo_root" -path "*/.docs/*" -type f -print0 2>/dev/null)

  # Repo-local: docs/livingDoc
  while IFS= read -r -d '' p; do
    [[ -n "$p" ]] && [[ -f "$p" ]] && DISCOVERED_PATHS+=("$p")
  done < <(find "$repo_root" -path "*/docs/livingDoc/*" -type f -print0 2>/dev/null)

  # Repo-local: drafts (commit/pr only)
  shopt -s nullglob 2>/dev/null || true
  for ext in commit.txt pr.md pr.txt; do
    for f in "$repo_root/docs/drafts/"*."$ext"; do
      [[ -f "$f" ]] && DISCOVERED_PATHS+=("$f")
    done
  done
  shopt -u nullglob 2>/dev/null || true

  # Repo-local: .scout/index.db
  [[ -f "$repo_root/.scout/index.db" ]] && DISCOVERED_PATHS+=("$repo_root/.scout/index.db")

  # Repo-local: call_graph.json under .docs
  while IFS= read -r -d '' p; do
    [[ -n "$p" ]] && [[ -f "$p" ]] && DISCOVERED_PATHS+=("$p")
  done < <(find "$repo_root" -path "*/.docs/call_graph.json" -type f -print0 2>/dev/null)

  # Repo-local: devtools/outputs (exclude scout-reset logs for audit trail)
  if [[ -d "$repo_root/devtools/outputs" ]]; then
    while IFS= read -r -d '' p; do
      [[ -n "$p" ]] && [[ -f "$p" ]] && [[ "$p" != *"outputs/scout-reset"* ]] && DISCOVERED_PATHS+=("$p")
    done < <(find "$repo_root/devtools/outputs" -type f -print0 2>/dev/null)
  fi

  # Global: ~/.scout/
  local scout_home="${HOME}/.scout"
  [[ -f "$scout_home/dependency_graph.v2.json" ]] && DISCOVERED_PATHS+=("$scout_home/dependency_graph.v2.json")
  if [[ -d "$scout_home/raw_briefs" ]]; then
    for f in "$scout_home/raw_briefs"/*.md; do
      [[ -f "$f" ]] && DISCOVERED_PATHS+=("$f")
    done
  fi
  shopt -u nullglob 2>/dev/null || true

  # --full: audit and config
  if [[ "$include_full" == "full" ]]; then
    [[ -f "$scout_home/audit.jsonl" ]] && DISCOVERED_PATHS+=("$scout_home/audit.jsonl")
    [[ -f "$scout_home/config.yaml" ]] && DISCOVERED_PATHS+=("$scout_home/config.yaml")
    [[ -f "$repo_root/.scout/config.yaml" ]] && DISCOVERED_PATHS+=("$repo_root/.scout/config.yaml")
  fi

  # Filter out empty, non-existent, or scout-reset log paths
  local filtered=()
  local i p
  for ((i=0; i<${#DISCOVERED_PATHS[@]}; i++)); do
    p="${DISCOVERED_PATHS[i]}"
    [[ -z "$p" ]] && continue
    [[ -f "$p" ]] || continue
    [[ "$p" == *"outputs/scout-reset"* ]] && continue
    filtered+=("$p")
  done
  if [[ ${#filtered[@]} -gt 0 ]]; then
    DISCOVERED_PATHS=("${filtered[@]}")
  else
    DISCOVERED_PATHS=()
  fi
}

# Filter DISCOVERED_PATHS by category. Modifies DISCOVERED_PATHS in place.
# Usage: filter_by_category "$REPO_ROOT" docs-only|drafts-only|cache-only|outputs-only
filter_by_category() {
  local repo_root="${1:?}"
  local cat="${2:?}"
  local scout_home="${HOME}/.scout"
  local filtered=()
  local p

  for p in "${DISCOVERED_PATHS[@]}"; do
    case "$cat" in
      docs-only)
        [[ "$p" == *"/.docs/"* ]] || [[ "$p" == *"/docs/livingDoc/"* ]] && filtered+=("$p")
        ;;
      drafts-only)
        [[ "$p" == *"/docs/drafts/"* ]] && filtered+=("$p")
        ;;
      cache-only)
        [[ "$p" == *"/.scout/index.db" ]] || \
        [[ "$p" == "$scout_home/dependency_graph.v2.json" ]] || \
        [[ "$p" == "$scout_home/raw_briefs/"* ]] || \
        [[ "$p" == *"/.docs/call_graph.json" ]] && filtered+=("$p")
        ;;
      outputs-only)
        [[ "$p" == *"/devtools/outputs/"* ]] && [[ "$p" != *"/outputs/scout-reset/"* ]] && filtered+=("$p")
        ;;
      *) filtered+=("$p") ;;
    esac
  done
  DISCOVERED_PATHS=("${filtered[@]}")
}

# Calculate file count and total size. Sets ARTIFACT_COUNT and ARTIFACT_SIZE_BYTES.
calculate_impact() {
  DISCOVERED_PATHS=("${DISCOVERED_PATHS[@]:-}")
  ARTIFACT_COUNT=${#DISCOVERED_PATHS[@]}
  ARTIFACT_SIZE_BYTES=0
  local p
  for p in "${DISCOVERED_PATHS[@]:-}"; do
    if [[ -f "$p" ]]; then
      local sz
      sz=$(stat -f%z "$p" 2>/dev/null) || sz=$(stat -c%s "$p" 2>/dev/null) || sz=0
      ARTIFACT_SIZE_BYTES=$((ARTIFACT_SIZE_BYTES + sz))
    fi
  done
}

# Human-readable size
format_size() {
  local bytes="${1:-0}"
  if [[ "$bytes" -ge 1048576 ]]; then
    echo "$((bytes / 1048576))M"
  elif [[ "$bytes" -ge 1024 ]]; then
    echo "$((bytes / 1024))K"
  else
    echo "${bytes}B"
  fi
}

# Perform deletion with logging. Requires LOG_FILE, REPO_ROOT, and DISCOVERED_PATHS.
# Usage: reset_scout
reset_scout() {
  local log_file="${LOG_FILE:?}"
  local p
  {
    echo "=== Scout Reset Log ==="
    echo "Timestamp: $(date +%Y-%m-%d_%H-%M-%S)"
    echo "Files deleted: ${#DISCOVERED_PATHS[@]}"
    echo "--------------------------------"
  } >> "$log_file"
  for p in "${DISCOVERED_PATHS[@]}"; do
    if [[ -f "$p" ]] && rm -f "$p" 2>/dev/null; then
      echo "Deleted: $p" >> "$log_file"
      echo "  Deleted: $p"
    elif [[ -f "$p" ]]; then
      echo "FAILED: $p" >> "$log_file"
      echo "  Failed: $p" >&2
    fi
  done
  # Remove empty .docs and raw_briefs dirs
  find "$REPO_ROOT" -type d -name ".docs" -empty -delete 2>/dev/null || true
  [[ -d "${HOME}/.scout/raw_briefs" ]] && rmdir "${HOME}/.scout/raw_briefs" 2>/dev/null || true
}
