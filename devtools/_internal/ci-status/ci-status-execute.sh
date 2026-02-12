#!/usr/bin/env bash
# ci-status-execute.sh — Execute CI status plan: prompt for confirmation, run Groq API, generate summary
# Reads latest /tmp/ci_status_plan_*.json from dry-run. Prompts before making API calls.
# Outputs: devtools/ci-status/ci-status_YYYY-MM-DD_HH-MM-SS.md (from plan)
# READ-ONLY: Never modifies repo state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVTOOLS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd "$DEVTOOLS_ROOT/.." && pwd)"
# shellcheck source=ci-status-common.sh
source "$SCRIPT_DIR/ci-status-common.sh"

[[ -f "$REPO_ROOT/requirements.txt" ]] || { echo "❌ Not a Vivarium repo root"; exit 1; }
cd "$REPO_ROOT"

ensure_path
load_dotenv "$REPO_ROOT"

# Find latest plan file
PLAN_PATH=""
if [[ -n "${1:-}" ]] && [[ -f "$1" ]]; then
  PLAN_PATH="$1"
else
  for f in /tmp/ci_status_plan_*.json; do
    [[ -f "$f" ]] || continue
    if [[ -z "$PLAN_PATH" ]] || [[ "$f" -nt "$PLAN_PATH" ]]; then
      PLAN_PATH="$f"
    fi
  done
fi

if [[ -z "$PLAN_PATH" ]] || [[ ! -f "$PLAN_PATH" ]]; then
  echo "❌ No plan file found. Run ./devtools/_internal/ci-status/ci-status-dry-run.sh first."
  echo "   Looked for: /tmp/ci_status_plan_*.json"
  exit 1
fi

ESTIMATED_COST=$(jq -r '.estimated_cost' "$PLAN_PATH")
N_JOBS=$(jq -r '.n_jobs' "$PLAN_PATH")
USE_AI=$(jq -r '.use_ai_summary' "$PLAN_PATH")

# Prompt for confirmation when AI would be used and there are jobs to summarize
# Skip prompt if VIVARIUM_CONFIRM_AI=1 (caller has already confirmed)
if [[ "$USE_AI" == "true" ]] && [[ "$N_JOBS" -gt 0 ]]; then
  if [[ "${VIVARIUM_CONFIRM_AI:-}" != "1" ]] && [[ "${VIVARIUM_CONFIRM_AI:-}" != "yes" ]]; then
    echo "Execute with estimated cost: \$$ESTIMATED_COST for $N_JOBS job(s)? [y/n]"
    read -r REPLY
    REPLY_LOWER=$(echo "$REPLY" | tr '[:upper:]' '[:lower:]')
    if [[ "$REPLY_LOWER" != "y" ]] && [[ "$REPLY_LOWER" != "yes" ]]; then
      echo "Aborted. No API calls made."
      exit 0
    fi
  fi
fi

GROQ_API_KEY="${GROQ_API_KEY:-}"
if [[ "$USE_AI" == "true" ]] && [[ -z "$GROQ_API_KEY" ]]; then
  echo "❌ GROQ_API_KEY not set. Cannot run AI summarization."
  exit 1
fi

LOG_FILE=$(jq -r '.log_file' "$PLAN_PATH")
if [[ "$USE_AI" == "true" ]] && [[ -n "$LOG_FILE" ]]; then
  if ! ensure_python_deps "$LOG_FILE" requests 2>/dev/null; then
    echo "❌ Required dependency 'requests' could not be installed."
    exit 1
  fi
fi

LIB_PATH="$SCRIPT_DIR/ci-status-lib.py"

# Run Python: read plan, call API if confirmed, write summary
# VIVARIUM_CI_SKIP_AI=1 overrides plan to use programmatic extraction only (no API calls)
OUTPUT=$(VIVARIUM_CI_SKIP_AI="${VIVARIUM_CI_SKIP_AI:-0}" python3 - "$PLAN_PATH" "$GROQ_API_KEY" "$LIB_PATH" << 'PY'
import json
import sys
import os

plan_path = sys.argv[1]
groq_api_key = sys.argv[2]
lib_path = sys.argv[3]

sys.path.insert(0, os.path.dirname(os.path.abspath(lib_path)))
import importlib.util
spec = importlib.util.spec_from_file_location("ci_status_lib", lib_path)
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)
call_groq_api = lib.call_groq_api
extract_programmatic_summary = lib.extract_programmatic_summary
log_processing_details = lib.log_processing_details

with open(plan_path) as f:
    plan = json.load(f)

branch = plan["branch"]
timestamp = plan["timestamp"]
summary_file = plan["summary_file"]
log_file_path = plan["log_file"]
passed = plan["passed"]
failed = plan["failed"]
pending = plan["pending"]
failed_job_items = plan["failed_job_items"]
use_ai_summary = plan["use_ai_summary"]
if os.environ.get("VIVARIUM_CI_SKIP_AI") == "1":
    use_ai_summary = False

# Log execution
with open(log_file_path, "a") as log_f:
    log_f.write("\n--- Execute Confirmation ---\n")
    log_f.write(f"Plan: {plan_path}\n")
    log_f.write(f"User approved AI summarization: {use_ai_summary}\n")
    log_f.write("--- End Confirmation ---\n")

lines = []
lines.append("# CI Status: " + branch)
lines.append("Generated: " + timestamp)
lines.append("")
lines.append("## Summary")
lines.append("- **Branch:** " + branch)
lines.append("- **Passing:** " + str(len(passed)))
lines.append("- **Failed:** " + str(len(failed)))
lines.append("- **Pending:** " + str(len(pending)))
lines.append("")

if passed:
    lines.append("## Passing (compact)")
    lines.append("")
    lines.append("| Workflow | Run # | Conclusion | Created |")
    lines.append("|----------|-------|------------|---------|")
    for r in passed:
        wn = (r.get("workflowName") or r.get("name") or "?").replace("|", "\\|")
        num = r.get("number", "?")
        c = r.get("conclusion") or "success"
        created = (r.get("createdAt") or "")[:19].replace("T", " ")
        lines.append(f"| {wn} | #{num} | {c} | {created} |")
    lines.append("")

total_cost = 0.0
total_input_tokens = 0
total_output_tokens = 0
if failed_job_items:
    method_note = " (Pre-proc + AI)" if use_ai_summary else " (Pre-proc only)"
    lines.append(f"## Failed{method_note}")
    lines.append("")

    for it in failed_job_items:
        lines.append(f"### {it['wn']} (run #{it['run_number']})")
        lines.append("")
        lines.append(f"- **Conclusion:** {it['conclusion']}")
        lines.append(f"- **Created:** {it['created']}")
        lines.append(f"- **Updated:** {it['updated']}")
        lines.append(f"- **URL:** {it['url']}")
        lines.append("")
        lines.append(f"#### Job: {it['jname']}")
        lines.append(f"- **Conclusion:** {it['jconcl']}")
        lines.append(f"- **Started:** {it['jstarted']}")
        lines.append("")

        condensed_log = it.get("condensed_log")
        original_size = it.get("original_size", 0)
        condensed_size = it.get("condensed_size", 0)
        jname = it["jname"]
        run_number = it["run_number"]

        if condensed_log is None or original_size == 0:
            lines.append("*Could not retrieve log.*")
            lines.append("")
            continue

        cost_info = None
        if use_ai_summary and groq_api_key:
            final_summary, cost_info = call_groq_api(condensed_log, groq_api_key)
            if cost_info:
                total_cost += cost_info["cost_usd"]
                total_input_tokens += cost_info.get("input_tokens", 0)
                total_output_tokens += cost_info.get("output_tokens", 0)
            lines.append("**AI Summary (from condensed log):**")
        else:
            final_summary = extract_programmatic_summary(condensed_log)
            lines.append("**Pre-processed Summary:**")

        lines.append("```")
        lines.append(final_summary)
        lines.append("```")
        lines.append("")

        log_processing_details(
            log_file_path, original_size, condensed_size, use_ai_summary,
            jname, run_number, cost_info
        )

if not (passed or failed or pending):
    lines.append("No workflow runs found for this branch.")
    lines.append("")

if total_cost > 0:
    lines.append("---")
    lines.append(f"**Total API Cost Incurred:** ${total_cost:.4f}")
    lines.append("")

with open(summary_file, "w") as f:
    f.write("\n".join(lines))

print(f"CI_STATUS_REAL_COST:{total_cost:.4f}")
print(f"CI_STATUS_REAL_TOKENS:{total_input_tokens}+{total_output_tokens}")
print(summary_file)
PY
)

REAL_COST=$(echo "$OUTPUT" | grep "CI_STATUS_REAL_COST:" | cut -d: -f2)
REAL_TOKENS=$(echo "$OUTPUT" | grep "CI_STATUS_REAL_TOKENS:" | cut -d: -f2)
SUMMARY_FILE=$(echo "$OUTPUT" | tail -1)

[[ "$(uname -s)" == "Darwin" ]] && [[ -f "$SUMMARY_FILE" ]] && pbcopy < "$SUMMARY_FILE" 2>/dev/null || true

if [[ -n "$REAL_COST" ]] && [[ "$REAL_COST" != "0" ]] && [[ "$REAL_COST" != "0.0" ]]; then
  notif_msg="Total API cost: \$$REAL_COST"
  [[ -n "$REAL_TOKENS" ]] && [[ "$REAL_TOKENS" != "0+0" ]] && notif_msg="($REAL_TOKENS tokens) $notif_msg"
  osascript -e "display notification \"$notif_msg\" with title \"CI Status Complete\""
fi

echo ""
echo "✅ CI status captured: $(jq -r '.branch' "$PLAN_PATH")"
echo "   Summary: $SUMMARY_FILE"
echo "   Processing Log: $LOG_FILE"
[[ -n "$REAL_COST" ]] && [[ "$REAL_COST" != "0" ]] && [[ "$REAL_COST" != "0.0" ]] && echo "   Total API cost: \$$REAL_COST"
[[ -n "$REAL_TOKENS" ]] && [[ "$REAL_TOKENS" != "0+0" ]] && echo "   Tokens used: $REAL_TOKENS (in+out)"
[[ "$(uname -s)" == "Darwin" ]] && echo "   Copied to clipboard."
if [[ "$USE_AI" == "true" ]]; then
  echo "   Pre-processing + AI Summarization: ON"
else
  echo "   Pre-processing only: ON"
fi
