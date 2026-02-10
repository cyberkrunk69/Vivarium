# Performance and Growth Evidence (Logs Only)

Date: 2026-02-10

This document lists only verifiable, hard evidence pulled from:
- Vivarium logs/history (`/workspace`)
- AutoHive logs/history (`/workspace/autohive`)

No roadmap claims or marketing text are used as evidence.

---

## 1) Vivarium: performance evidence from logs

### 1.1 Current API audit log (runtime events)
Source: `/workspace/api_audit.log`

Direct log lines:
- `2026-02-03T22:42:10.526871` API success with model `llama-3.3-70b-versatile`, `input_tokens=30049`, `cost=0.01775893`
- `2026-02-03T22:42:12.872934` API success with model `llama-3.3-70b-versatile`, `input_tokens=30049`, `cost=0.01777552`
- `2026-02-03T22:42:15.023214` API success with model `llama-3.3-70b-versatile`, `input_tokens=30049`, `cost=0.01777868`
- `2026-02-03T22:42:15.023457` budget event `BUDGET_EXCEEDED` with `remaining=0.01912455`, `requested=0.026945`

Computed summary (from these same log lines):
- Total API events: 7
- API successes: 4
- Total successful-call cost: `0.05331729`
- Total successful-call tokens: `90203` input, `177` output

### 1.2 Verification quality signal
Source: `/workspace/tool_operations.json`

Direct log evidence:
- Verification event at `2026-02-03T09:28:34.352538` reports
  - `"hallucination_detected": true`
  - `"discrepancy_count": 1`

Computed summary:
- Verification events: 8
- Hallucination detections: 1 (12.5%)

### 1.3 Historical performance logs preserved in git history
Source commit: `5b6a0b6`
Files:
- `structured_logs.jsonl`
- `performance_history.json`

Computed from log contents at that commit:
- `structured_logs.jsonl`
  - Total entries: 385
  - Session starts: 225
  - Session completions: 153
  - Completion success rate: 86.93%
  - Elapsed time (completed sessions): avg 86.962s, median 70.441s, min 11.972s, max 374.406s
  - Peak start burst: 10 sessions started in the same second (`2026-02-03T05:53:55`)
- `performance_history.json`
  - Sessions recorded: 45
  - Success rate: 82.22%
  - Duration: avg 102.313s, median 94.079s, min 12.401s, max 374.406s
  - Quality score: avg 0.9673 (min 0.0, max 1.0)
  - First 10 quality avg: 0.858
  - Last 10 quality avg: 0.995
  - Quality change (first 10 -> last 10): +15.97%

---

## 2) Vivarium: growth evidence from git logs

Source: `git log --shortstat` on `/workspace`

Hard evidence:
- Total commits: 134
- Date span: `2026-02-03` to `2026-02-10`
- Commits per day:
  - 2026-02-03: 17
  - 2026-02-04: 1
  - 2026-02-05: 7
  - 2026-02-07: 2
  - 2026-02-08: 64
  - 2026-02-09: 39
  - 2026-02-10: 4
- Aggregate churn totals from commit shortstats:
  - Files changed (sum): 5700
  - Insertions (sum): 600517
  - Deletions (sum): 216484
  - Net lines: +384033

Largest growth commits by insertion count:
- `5b6a0b6` (2026-02-04): `3300 files`, `+455283/-0`
- `4239726` (2026-02-03): `301 files`, `+66523/-9816`
- `d9908f6` (2026-02-03): `107 files`, `+23831/-0`

---

## 3) AutoHive: performance evidence from logs

### 3.1 Session report log
Source: `/workspace/autohive/session_reports.json`

Computed from log entries:
- Total reports: 87
- Time range: `2026-02-01 05:12:30` -> `2026-02-02 00:49:27` (span: 70617 seconds)
- Reports with positive findings: 55
- Reports with zero findings: 32
- Peak report throughput: 8 reports in one minute (`2026-02-01 21:22`)

Direct log examples:
- Entry with explicit failure summary: `"Swarm failed with 5 out of 5 tasks."` (timestamp `2026-02-01 21:30:20`)
- Entry with explicit cost text: `"Total cost: $0.000000"` (timestamp `2026-02-01 20:35:24`)

### 3.2 Runtime capacity snapshot
Source: `/workspace/autohive/status.json`

Logged state:
- `helpers: 10`
- `workers: 5`
- `division_of_labor.initiative: 3`
- `division_of_labor.quest: 2`

---

## 4) AutoHive: growth evidence from git logs

Source: `git log origin/main --shortstat` on `/workspace/autohive`

Hard evidence:
- Total commits on `origin/main`: 30
- Date span: `2026-01-31` to `2026-02-02`
- Commits per day:
  - 2026-01-31: 3
  - 2026-02-01: 25
  - 2026-02-02: 2
- Aggregate shortstat totals:
  - Files changed (sum): 1396
  - Insertions (sum): 630461
  - Deletions (sum): 597586
  - Net lines: +32875

Largest growth commits by insertion count:
- `d59a08d` (2026-02-02): `707 files`, `+614044/-633`
- `6d7606b` (2026-02-01): `8 files`, `+4195/-44`
- `36e0d42` (2026-01-31): `12 files`, `+3500/-0`

Largest contraction commit:
- `5253000` (2026-02-02): `615 files`, `+4/-596455`

---

## 5) Repro commands

Vivarium current logs:
```bash
python3 - <<'PY'
import json
from pathlib import Path
rows=[json.loads(l) for l in Path('/workspace/api_audit.log').read_text().splitlines() if l.strip()]
print('events', len(rows))
print('success', sum(1 for r in rows if r.get('event')=='API_CALL_SUCCESS'))
print('success_cost_total', sum(r.get('cost',0.0) for r in rows if r.get('event')=='API_CALL_SUCCESS'))
PY
```

Vivarium historical logs:
```bash
git -C /workspace show 5b6a0b6:structured_logs.jsonl
git -C /workspace show 5b6a0b6:performance_history.json
```

Vivarium growth:
```bash
git -C /workspace log --date=short --pretty=format:'%ad' | sort | uniq -c
git -C /workspace log --shortstat --pretty=format:'%h|%ad|%s' --date=iso
```

AutoHive logs:
```bash
python3 - <<'PY'
import json
from pathlib import Path
data=json.loads(Path('/workspace/autohive/session_reports.json').read_text())
print('reports', len(data))
PY
```

AutoHive growth:
```bash
git -C /workspace/autohive log origin/main --date=short --pretty=format:'%ad' | sort | uniq -c
git -C /workspace/autohive log origin/main --shortstat --pretty=format:'%h|%ad|%s' --date=iso
```

---

## 6) Requested lens only: self-learning, speed gains, cost/task reduction

### 6.1 Self-learning: what is verifiably supported

**Vivarium (historical log @ `5b6a0b6:performance_history.json`)**
- 45/45 sessions contain a `lessons_learned` field.
- Frequent recurring learned outcomes are logged, e.g.:
  - `PASS: Exit code 0, found 4 success indicators` (9 occurrences)
  - `PASS: Exit code 0, found 5 success indicators` (9 occurrences)
  - `FAIL: exit code 1, no files modified` (7 occurrences)
- Quality trend in same file:
  - first 10 sessions average quality = `0.858`
  - last 10 sessions average quality = `0.995`
  - change = `+15.97%`

**AutoHive**
- `session_reports.json` provides iterative, timestamped reporting (87 reports),
  but does not provide a structured quality score time-series suitable for a
  robust learning-rate claim.

### 6.2 Speed gains: what is verifiably supported

**No clean, stable speed-gain claim is supported across available logs.**

Observed (Vivarium historical):
- `performance_history.json` duration trend (chronological):
  - first 10 avg = `122.805s`
  - last 10 avg = `145.757s`
  - this is slower, not faster.
- `structured_logs.jsonl` completed-session elapsed trend:
  - first 10 avg = `80.123s`
  - last 10 avg = `46.958s`
  - however success rate in the same windows drops from `100%` to `20%`.

Because elapsed-time and success trend in opposite directions, the logs do not
support a trustworthy headline like "the system got faster" without caveats.

### 6.3 Cost per task reduction: what is verifiably supported

**No before/after per-task cost reduction claim is supported across available logs.**

- Vivarium `api_audit.log` has only 4 successful calls with cost fields:
  - total cost = `0.05331729`
  - average cost per successful call = `0.01332932`
  - useful as a point estimate, not a reduction trend.
- Vivarium `performance_history.json` does not contain a cost field.
- AutoHive `session_reports.json` includes occasional free-text cost mentions
  (for example `"Total cost: $0.000000"`), but no structured per-task cost
  series for trend analysis.
