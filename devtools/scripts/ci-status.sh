#!/usr/bin/env bash
# ci-status.sh — Smart CI/CD status (orchestrator: dry-run + confirmation + execute)
# Uses unified API confirmation. See devtools/README.md for details.
# Outputs: devtools/ci-status/ci-status_*.md, *.log

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVTOOLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$DEVTOOLS_ROOT/.." && pwd)"

DRY_RUN_SCRIPT="$DEVTOOLS_ROOT/_internal/ci-status/ci-status-dry-run.sh"
EXECUTE_SCRIPT="$DEVTOOLS_ROOT/_internal/ci-status/ci-status-execute.sh"

# Run dry-run
"$DRY_RUN_SCRIPT"

# Find latest plan
PLAN_PATH=""
for f in /tmp/ci_status_plan_*.json; do
  [[ -f "$f" ]] || continue
  if [[ -z "$PLAN_PATH" ]] || [[ "$f" -nt "$PLAN_PATH" ]]; then
    PLAN_PATH="$f"
  fi
done

if [[ -z "$PLAN_PATH" ]] || [[ ! -f "$PLAN_PATH" ]]; then
  echo "❌ No plan file found after dry-run."
  exit 1
fi

ESTIMATED_COST=$(jq -r '.estimated_cost' "$PLAN_PATH")
N_JOBS=$(jq -r '.n_jobs' "$PLAN_PATH")
USE_AI=$(jq -r '.use_ai_summary' "$PLAN_PATH")

# Confirmation: skip if no AI needed; otherwise use unified mechanism
if [[ "$USE_AI" == "true" ]] && [[ "$N_JOBS" -gt 0 ]]; then
  # shellcheck source=../_internal/common/api-confirm.sh
  source "$DEVTOOLS_ROOT/_internal/common/api-confirm.sh"
  cost_msg="Estimated Groq API cost: \$$ESTIMATED_COST for $N_JOBS job(s)."
  if ! confirm_api_call "$cost_msg" "Execute with this cost? [y/n] "; then
    echo "Proceeding with programmatic extraction only (no API calls)."
    export VIVARIUM_CI_SKIP_AI=1
  else
    export VIVARIUM_CONFIRM_AI=1
  fi
fi

# Run execute (VIVARIUM_CONFIRM_AI=1 skips re-prompt; VIVARIUM_CI_SKIP_AI=1 uses programmatic only)
"$EXECUTE_SCRIPT" "$PLAN_PATH"
