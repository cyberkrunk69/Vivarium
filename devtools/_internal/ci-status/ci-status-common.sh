#!/usr/bin/env bash
# ci-status-common.sh — Shared logic for ci-status-dry-run and ci-status-execute
# Sourced by both scripts. Do not run directly.

# Requires: REPO_ROOT, LOG_FILE (for ensure_python_deps)
# Ensures: ensure_gh, ensure_python_deps, archive_ci_status_files

COMMON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../common" && pwd)"
# shellcheck source=../common/utils.sh
source "$COMMON_ROOT/utils.sh"

# Wrapper for ci-status-specific archive pattern (backward compatibility)
archive_ci_status_files() {
  archive_devtools_output "$1" "ci-status_*.md" "ci-status_*.log"
}
