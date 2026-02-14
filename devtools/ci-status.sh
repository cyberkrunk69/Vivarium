#!/usr/bin/env bash
# ci-status.sh — Smart CI/CD status with processing log
# Outputs:
#   - devtools/outputs/ci-status/ci-status_YYYY-MM-DD_HH-MM-SS.md (summary)
#   - devtools/outputs/ci-status/ci-status_YYYY-MM-DD_HH-MM-SS.log (processing details)
# READ-ONLY: Never modifies repo state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVTOOLS_ROOT="$SCRIPT_DIR"
REPO_ROOT="$(cd "$DEVTOOLS_ROOT/.." && pwd)"
[[ -f "$REPO_ROOT/requirements.txt" ]] || { echo "❌ Not a Vivarium repo root"; exit 1; }
cd "$REPO_ROOT"

# Source common utilities
# shellcheck source=_internal/ci-status/ci-status-common.sh
source "$SCRIPT_DIR/_internal/ci-status/ci-status-common.sh"
ensure_path
load_dotenv "$REPO_ROOT"
ensure_gh || exit 1
gh auth status &>/dev/null || { echo "❌ gh not authenticated"; exit 1; }

GROQ_API_KEY="${GROQ_API_KEY:-}"
USE_AI_SUMMARY=false
if [[ -n "$GROQ_API_KEY" ]]; then
  USE_AI_SUMMARY=true
  command -v curl &>/dev/null || { echo "❌ curl required for GROQ API"; exit 1; }
fi

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUT_DIR="$DEVTOOLS_ROOT/outputs/ci-status"
ARCHIVE_DIR="$OUT_DIR/archive"
SUMMARY_FILE="$OUT_DIR/ci-status_${TIMESTAMP}.md"
LOG_FILE="$OUT_DIR/ci-status_${TIMESTAMP}.log"
mkdir -p "$OUT_DIR"

# Archive existing ci-status output files before generating new ones
archive_ci_status_files "$OUT_DIR"

BRANCH="${CI_STATUS_BRANCH:-$(git branch --show-current)}"
LIMIT="${CI_STATUS_LIMIT:-20}"

# Log initial setup
{
    echo "=== CI Status Processing Log ==="
    echo "Timestamp: $TIMESTAMP"
    echo "Branch: $BRANCH"
    echo "Limit: $LIMIT"
    echo "AI Summary: $USE_AI_SUMMARY"
    if [[ $archived_count -gt 0 ]]; then
      echo "Archived: $archived_count previous output file(s) to $ARCHIVE_DIR"
    fi
    echo "--------------------------------"
} > "$LOG_FILE"

RUNS_JSON=$(gh run list --branch "$BRANCH" --limit "$LIMIT" \
  --json databaseId,workflowName,conclusion,status,name,number,headBranch,url,createdAt,updatedAt,displayTitle 2>>"$LOG_FILE") || {
  echo "❌ Failed to fetch runs" >> "$LOG_FILE"
  exit 1
}

# Log fetched run count
RUN_COUNT=$(echo "$RUNS_JSON" | jq 'length')
FAILED_COUNT=$(echo "$RUNS_JSON" | jq '[.[] | select((.conclusion // "") | test("failure|cancelled|timed_out|startup_failure"; "i"))] | length')
echo "Fetched $RUN_COUNT runs ($FAILED_COUNT failed)" >> "$LOG_FILE"
if [[ "$USE_AI_SUMMARY" == true ]] && [[ "$FAILED_COUNT" -eq 0 ]]; then
  echo "No failed runs to summarize; AI confirmation skipped." >> "$LOG_FILE"
fi

RUNS_TMP=$(mktemp)
trap 'rm -f "$RUNS_TMP"' EXIT
echo "$RUNS_JSON" > "$RUNS_TMP"

# Verify/install Python deps for AI mode; exit if required and install fails
if [[ "$USE_AI_SUMMARY" == true ]]; then
  if ! ensure_python_deps "$LOG_FILE" requests; then
    echo "❌ Required dependency 'requests' could not be installed. Install manually: pip install requests" >> "$LOG_FILE"
    echo "❌ AI summarization requires 'requests'. Install with: pip install requests"
    exit 1
  fi
fi

LIB_PATH="$SCRIPT_DIR/_internal/ci-status/ci-status-lib.py"

# Run Python (single execution; prompt handled inside Python)
run_ci_status_python() {
  python3 - "$RUNS_TMP" "$BRANCH" "$TIMESTAMP" "$SUMMARY_FILE" "$USE_AI_SUMMARY" "$GROQ_API_KEY" "$LIB_PATH" "$LOG_FILE" << 'PY'
import os
import json
import subprocess
import sys
import importlib.util

lib_path = sys.argv[7]
spec = importlib.util.spec_from_file_location("ci_status_lib", lib_path)
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)
preprocess_log_for_ai = lib.preprocess_log_for_ai
estimate_cost_for_condensed_log = lib.estimate_cost_for_condensed_log
call_groq_api = lib.call_groq_api
extract_programmatic_summary = lib.extract_programmatic_summary
log_processing_details = lib.log_processing_details

runs_json_path = sys.argv[1]
branch = sys.argv[2]
timestamp = sys.argv[3]
out_file = sys.argv[4]
use_ai_summary = (sys.argv[5] or "").lower() in ('true', '1', 'yes')  # Bash passes lowercase "true"
groq_api_key = sys.argv[6]
log_file_path = sys.argv[8]

with open(runs_json_path) as f:
    runs = json.load(f)

passed = []
failed = []
pending = []

for r in runs:
    c = (r.get("conclusion") or "").lower()
    s = (r.get("status") or "").lower()
    if c in ("failure", "cancelled", "timed_out", "startup_failure"):
        failed.append(r)
    elif s in ("in_progress", "queued", "waiting", "requested", "pending") or c == "":
        pending.append(r)
    else:
        passed.append(r)

failed_job_items = []

# Log stats
with open(log_file_path, 'a') as log_f:
    log_f.write(f"\n--- Run Breakdown ---\n")
    log_f.write(f"Total Runs: {len(runs)}\n")
    log_f.write(f"Passed: {len(passed)}\n")
    log_f.write(f"Failed: {len(failed)}\n")
    log_f.write(f"Pending: {len(pending)}\n")
    log_f.write("----------------------\n")

total_cost = 0.0  # Sum of API costs when GROQ_API_KEY is used
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

if failed:
    # Collect failed job data (fetch logs, preprocess)
    failed_job_items = []
    print(f"Fetching logs for {len(failed)} failed run(s)...", flush=True)

    for r in failed:
        run_id = r.get("databaseId")
        wn = r.get("workflowName") or r.get("name") or "?"
        url = r.get("url") or ""
        created = r.get("createdAt") or ""
        updated = r.get("updatedAt") or ""
        conclusion = r.get("conclusion") or "?"
        run_number = r.get("number", "?")

        try:
            job_out = subprocess.run(
                ["gh", "run", "view", str(run_id), "--json", "jobs"],
                capture_output=True, text=True, timeout=30
            )
            if job_out.returncode == 0 and job_out.stdout:
                jobs = json.loads(job_out.stdout).get("jobs") or []
                failed_jobs = [j for j in jobs if (j.get("conclusion") or "").lower() in
                    ("failure", "cancelled", "timed_out", "startup_failure")]

                for j in failed_jobs:
                    jname = j.get("name") or "?"
                    jconcl = j.get("conclusion") or "?"
                    jstarted = j.get("startedAt") or ""

                    jid = j.get("databaseId")
                    if jid:
                        log_out = subprocess.run(
                            ["gh", "run", "view", str(run_id), "--log"],
                            capture_output=True, text=True, timeout=120
                        )

                        if log_out.returncode == 0 and log_out.stdout:
                            original_log = log_out.stdout
                            original_size = len(original_log)
                            condensed_log = preprocess_log_for_ai(original_log)
                            condensed_size = len(condensed_log)
                            failed_job_items.append({
                                "run": r, "wn": wn, "url": url, "created": created, "updated": updated,
                                "conclusion": conclusion, "run_number": run_number,
                                "jname": jname, "jconcl": jconcl, "jstarted": jstarted,
                                "original_log": original_log, "condensed_log": condensed_log,
                                "original_size": original_size, "condensed_size": condensed_size,
                            })
                        else:
                            failed_job_items.append({
                                "run": r, "wn": wn, "url": url, "created": created, "updated": updated,
                                "conclusion": conclusion, "run_number": run_number,
                                "jname": jname, "jconcl": jconcl, "jstarted": jstarted,
                                "original_log": None, "condensed_log": None,
                                "original_size": 0, "condensed_size": 0,
                            })
        except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
            pass

    # Prompt user for Groq API when AI is enabled and we have failed jobs
    if use_ai_summary and failed_job_items:
        estimated_total = sum(
            estimate_cost_for_condensed_log(it["condensed_log"] or "")
            for it in failed_job_items
        )
        n_jobs = sum(1 for it in failed_job_items if it.get("condensed_log") and len(it["condensed_log"]) >= 50)
        print(f"\nEstimated Groq API cost: ${estimated_total:.4f} for {n_jobs} job(s).", flush=True)
        non_interactive = False
        try:
            reply = input("Send it? [y/n]: ").strip().lower()
        except EOFError:
            reply = "n"
            non_interactive = True
        use_ai_summary = reply in ('y', 'yes')
        with open(log_file_path, 'a') as log_f:
            log_f.write(f"\n--- Groq Confirmation ---\n")
            log_f.write(f"Estimated cost: ${estimated_total:.4f} for {n_jobs} job(s)\n")
            log_f.write(f"User response: {reply!r} -> use_ai_summary={use_ai_summary}\n")
            if non_interactive:
                log_f.write("Non-interactive (EOF on input); defaulted to pre-process only\n")
            log_f.write("--- End Groq Confirmation ---\n")

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

        if it["original_log"] is None:
            lines.append("*Could not retrieve log.*")
            lines.append("")
            continue

        original_size = it["original_size"]
        condensed_size = it["condensed_size"]
        condensed_log = it["condensed_log"]
        jname = it["jname"]
        run_number = it["run_number"]

        cost_info = None
        if use_ai_summary:
            final_summary, cost_info = call_groq_api(condensed_log, groq_api_key)
            if cost_info:
                total_cost += cost_info['cost_usd']
            lines.append("**AI Summary (from condensed log):**")
            lines.append("```")
            lines.append(final_summary)
            lines.append("```")
        else:
            final_summary = extract_programmatic_summary(condensed_log)
            lines.append("**Pre-processed Summary:**")
            lines.append("```")
            lines.append(final_summary)
            lines.append("```")

        log_processing_details(log_file_path, original_size, condensed_size, use_ai_summary, jname, run_number, cost_info)
        lines.append("")

if not runs:
    lines.append("No workflow runs found for this branch.")
    lines.append("")

# Add total API cost when GROQ_API_KEY was used and costs were incurred
if total_cost > 0:
    lines.append("---")
    lines.append(f"**Total API Cost Incurred:** ${total_cost:.4f}")
    lines.append("")

with open(out_file, "w") as f:
    f.write("\n".join(lines))

print("Wrote " + out_file)
PY
}
run_ci_status_python
echo "Python exit code: $?" >> "$LOG_FILE"

[[ "$(uname -s)" == "Darwin" ]] && pbcopy < "$SUMMARY_FILE" 2>/dev/null || true

echo ""
echo "✅ CI status captured: $BRANCH"
echo "   Summary: $SUMMARY_FILE"
echo "   Processing Log: $LOG_FILE"
echo "   Copied to clipboard."
if [[ "$USE_AI_SUMMARY" == true ]]; then
  echo "   Pre-processing + AI Summarization: ON"
else
  echo "   Pre-processing only: ON"
fi
