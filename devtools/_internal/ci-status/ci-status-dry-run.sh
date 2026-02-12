#!/usr/bin/env bash
# ci-status-dry-run.sh — CI status dry run: fetch runs, preprocess logs, estimate costs
# Does NOT make any Groq API calls. Saves plan to /tmp/ci_status_plan_YYYYMMDD_HHMMSS.json
# Outputs: devtools/ci-status/ci-status_YYYY-MM-DD_HH-MM-SS.log (up to estimation point)
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
ensure_gh || exit 1
gh auth status &>/dev/null || { echo "❌ gh not authenticated"; exit 1; }

GROQ_API_KEY="${GROQ_API_KEY:-}"
USE_AI_SUMMARY=false
if [[ -n "$GROQ_API_KEY" ]]; then
  USE_AI_SUMMARY=true
  command -v curl &>/dev/null || { echo "❌ curl required for GROQ API"; exit 1; }
fi

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUT_DIR="$DEVTOOLS_ROOT/ci-status"
ARCHIVE_DIR="$OUT_DIR/archive"
LOG_FILE="$OUT_DIR/ci-status_${TIMESTAMP}.log"
SUMMARY_FILE="$OUT_DIR/ci-status_${TIMESTAMP}.md"
mkdir -p "$OUT_DIR"

archive_ci_status_files "$OUT_DIR"

BRANCH="${CI_STATUS_BRANCH:-$(git branch --show-current)}"
LIMIT="${CI_STATUS_LIMIT:-20}"

# Log initial setup
{
  echo "=== CI Status Processing Log (Dry Run) ==="
  echo "Timestamp: $TIMESTAMP"
  echo "Branch: $BRANCH"
  echo "Limit: $LIMIT"
  echo "AI Summary: $USE_AI_SUMMARY"
  if [[ ${archived_count:-0} -gt 0 ]]; then
    echo "Archived: $archived_count previous output file(s) to $ARCHIVE_DIR"
  fi
  echo "--------------------------------"
} > "$LOG_FILE"

RUNS_JSON=$(gh run list --branch "$BRANCH" --limit "$LIMIT" \
  --json databaseId,workflowName,conclusion,status,name,number,headBranch,url,createdAt,updatedAt,displayTitle 2>>"$LOG_FILE") || {
  echo "❌ Failed to fetch runs" >> "$LOG_FILE"
  exit 1
}

RUN_COUNT=$(echo "$RUNS_JSON" | jq 'length')
FAILED_COUNT=$(echo "$RUNS_JSON" | jq '[.[] | select((.conclusion // "") | test("failure|cancelled|timed_out|startup_failure"; "i"))] | length')
echo "Fetched $RUN_COUNT runs ($FAILED_COUNT failed)" >> "$LOG_FILE"
if [[ "$USE_AI_SUMMARY" == true ]] && [[ "$FAILED_COUNT" -eq 0 ]]; then
  echo "No failed runs to summarize; AI confirmation skipped." >> "$LOG_FILE"
fi

RUNS_TMP=$(mktemp)
trap 'rm -f "$RUNS_TMP"' EXIT
echo "$RUNS_JSON" > "$RUNS_TMP"

if [[ "$USE_AI_SUMMARY" == true ]]; then
  if ! ensure_python_deps "$LOG_FILE" requests; then
    echo "❌ Required dependency 'requests' could not be installed." >> "$LOG_FILE"
    echo "❌ AI summarization requires 'requests'. Install with: pip install requests"
    exit 1
  fi
fi

LIB_PATH="$SCRIPT_DIR/ci-status-lib.py"

# Run Python: process runs, fetch logs, preprocess, estimate, write plan
PLAN_FILE=$(python3 - "$RUNS_TMP" "$BRANCH" "$TIMESTAMP" "$SUMMARY_FILE" "$LOG_FILE" "$USE_AI_SUMMARY" "$LIB_PATH" << 'PY'
import json
import subprocess
import sys
import os

runs_json_path = sys.argv[1]
branch = sys.argv[2]
timestamp = sys.argv[3]
summary_file = sys.argv[4]
log_file_path = sys.argv[5]
use_ai_summary = (sys.argv[6] or "").lower() in ("true", "1", "yes")

sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[7])))
import importlib.util
spec = importlib.util.spec_from_file_location("ci_status_lib", sys.argv[7])
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)
preprocess_log_for_ai = lib.preprocess_log_for_ai
estimate_cost_for_condensed_log = lib.estimate_cost_for_condensed_log
estimate_tokens_and_cost_for_condensed_log = lib.estimate_tokens_and_cost_for_condensed_log

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

# Log stats
with open(log_file_path, "a") as log_f:
    log_f.write("\n--- Run Breakdown ---\n")
    log_f.write(f"Total Runs: {len(runs)}\n")
    log_f.write(f"Passed: {len(passed)}\n")
    log_f.write(f"Failed: {len(failed)}\n")
    log_f.write(f"Pending: {len(pending)}\n")
    log_f.write("----------------------\n")

failed_job_items = []
estimated_total = 0.0
estimated_input_tokens = 0
estimated_output_tokens = 0

if failed:
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
                failed_jobs = [
                    j for j in jobs
                    if (j.get("conclusion") or "").lower()
                    in ("failure", "cancelled", "timed_out", "startup_failure")
                ]

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
                            if use_ai_summary:
                                tok_result = estimate_tokens_and_cost_for_condensed_log(condensed_log)
                                if tok_result:
                                    inp, out, est = tok_result
                                    estimated_input_tokens += inp
                                    estimated_output_tokens += out
                                    estimated_total += est
                            failed_job_items.append({
                                "wn": wn, "url": url, "created": created, "updated": updated,
                                "conclusion": conclusion, "run_number": run_number,
                                "jname": jname, "jconcl": jconcl, "jstarted": jstarted,
                                "original_size": original_size, "condensed_size": condensed_size,
                                "condensed_log": condensed_log,
                            })
                        else:
                            failed_job_items.append({
                                "wn": wn, "url": url, "created": created, "updated": updated,
                                "conclusion": conclusion, "run_number": run_number,
                                "jname": jname, "jconcl": jconcl, "jstarted": jstarted,
                                "original_size": 0, "condensed_size": 0, "condensed_log": None,
                            })
        except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
            pass

n_jobs = sum(1 for it in failed_job_items if it.get("condensed_log") and len(it["condensed_log"]) >= 50)

# Build plan
plan = {
    "branch": branch,
    "timestamp": timestamp,
    "summary_file": summary_file,
    "log_file": log_file_path,
    "passed": passed,
    "failed": failed,
    "pending": pending,
    "failed_job_items": failed_job_items,
    "estimated_cost": round(estimated_total, 4),
    "estimated_input_tokens": estimated_input_tokens,
    "estimated_output_tokens": estimated_output_tokens,
    "n_jobs": n_jobs,
    "use_ai_summary": use_ai_summary,
}

from datetime import datetime
ts_obj = datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S")
plan_name = f"ci_status_plan_{ts_obj.strftime('%Y%m%d_%H%M%S')}.json"
plan_path = os.path.join("/tmp", plan_name)

with open(plan_path, "w") as f:
    json.dump(plan, f, indent=2)

with open(log_file_path, "a") as log_f:
    log_f.write("\n--- Dry Run Estimation ---\n")
    log_f.write(f"Estimated tokens: {estimated_input_tokens} in + {estimated_output_tokens} out for {n_jobs} job(s)\n")
    log_f.write(f"Estimated cost: ${estimated_total:.4f} for {n_jobs} job(s)\n")
    log_f.write(f"Plan saved to: {plan_path}\n")
    log_f.write("--- End Dry Run ---\n")

print(plan_path)
PY
)

echo "Python exit code: $?" >> "$LOG_FILE"

# Extract plan path from Python output (last line)
PLAN_PATH=$(echo "$PLAN_FILE" | tail -1)

if [[ -f "$PLAN_PATH" ]]; then
  ESTIMATED_COST=$(jq -r '.estimated_cost' "$PLAN_PATH")
  N_JOBS=$(jq -r '.n_jobs' "$PLAN_PATH")
  USE_AI=$(jq -r '.use_ai_summary' "$PLAN_PATH")

  if [[ "$USE_AI" == "true" ]] && [[ "$N_JOBS" -gt 0 ]]; then
    EST_IN=$(jq -r '.estimated_input_tokens // 0' "$PLAN_PATH")
    EST_OUT=$(jq -r '.estimated_output_tokens // 0' "$PLAN_PATH")
    echo ""
    echo "Estimated tokens: $EST_IN input + $EST_OUT output for $N_JOBS job(s)"
    echo "Estimated Groq API cost: \$$ESTIMATED_COST for $N_JOBS job(s)."
  else
    echo ""
    echo "No AI summarization needed (no failed jobs or GROQ_API_KEY not set)."
  fi

  echo ""
  echo "✅ Dry run complete: $BRANCH"
  echo "   Plan: $PLAN_PATH"
  echo "   Log: $LOG_FILE"
  echo ""
  echo "Run ./devtools/_internal/ci-status/ci-status-execute.sh to execute with the saved plan."
else
  echo "❌ Plan file was not created."
  exit 1
fi
