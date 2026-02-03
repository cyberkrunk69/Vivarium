# UI/UX Audit Report

**Project:** claude_parasite_brain_suck
**Date:** 2026-02-03
**Auditor:** Claude Opus 4.5 (automated audit)

---

## Executive Summary

This audit reviews all user-facing CLI scripts in the project. **38 issues** were identified across 8 files, categorized by severity:

- **Critical:** 2 issues
- **High:** 9 issues
- **Medium:** 16 issues
- **Low:** 11 issues

---

## Issues by File

### 1. brain.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 1 | Medium | No version info available | argparse setup (line 69) | Add `parser.add_argument('--version', action='version', version='%(prog)s 1.0')` |
| 2 | Low | Raw JSON output not formatted for humans | `health()` line 31 | Use `json.dumps(resp.json(), indent=2)` or tabular format |
| 3 | Medium | No error handling feedback for connection refused | `grind()` line 64 | Distinguish between connection errors and API errors: "Cannot connect to swarm at {BASE_URL}. Is it running?" |
| 4 | Low | Help text for `--budget` doesn't mention default | line 74 | Change to `help="Budget in dollars (default: $0.10)"` |
| 5 | Medium | Missing example usage in help | argparse | Add `epilog="Example: python brain.py grind --budget 0.25"` |

### 2. orchestrator.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 6 | High | Manual argument parsing is error-prone | lines 179-214 | Use argparse for consistent help/error handling |
| 7 | Medium | No help flag support (-h/--help) | CLI | Switch to argparse which provides this automatically |
| 8 | Medium | Cryptic error when `add` missing args | line 191 | Add: "Usage: python orchestrator.py add <id> <type> [--min X] [--max X] [--intensity X]" |
| 9 | Low | Doc block printed on invalid command is not formatted well | line 181 | Print a cleaner usage summary instead of raw docstring |
| 10 | Medium | Worker stderr output truncated to 200 chars without indication | line 94 | Add "...(truncated)" if stderr was longer |
| 11 | Low | "Active locks" output doesn't explain what locks mean | lines 125-130 | Add context: "Active locks indicate tasks currently being processed" |
| 12 | Medium | No confirmation before `clear` command | line 211 | Add prompt: "This will delete all tasks and logs. Continue? [y/N]" |

### 3. worker.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 13 | High | Manual argument parsing inconsistent with other scripts | lines 333-349 | Use argparse for consistency across tools |
| 14 | Medium | Worker ID format is cryptic (`worker_<hex>`) | line 28 | Consider human-readable names like `worker_1`, `worker_2` or add a prefix |
| 15 | Low | "No tasks available, waiting..." shows count but no ETA | line 308 | Add: "Will exit after 20 seconds of inactivity" |
| 16 | Low | Exit message shows "iterations" but it executed "tasks" | line 311 | Rename to "Executed {iterations} tasks" for clarity (already correct) |
| 17 | Medium | No explanation of what "deps" means in usage | line 346 | Change to: "python worker.py add <id> <instruction> [dependency_ids,comma,separated]" |

### 4. autopilot.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 18 | High | Skips step [3] in output (goes [1], [2], [4]) | lines 18, 29, 42 | Fix numbering or explain what step 3 is/was |
| 19 | Medium | "AUTOPILOT ENGAGED" message is vague | line 47 | Add: "This will continuously run /plan then /grind/queue in a loop" |
| 20 | Low | No progress indicator during long API calls | lines 20, 31 | Add "Waiting..." or spinner during 120s/300s timeouts |
| 21 | High | SLEEP_BETWEEN_CYCLES=0 means no pause, but message says "Sleeping 0s" | line 55 | Skip message entirely when sleep is 0, or clarify "No delay between cycles" |
| 22 | Low | "ERROR:" prefix but no explanation of what failed | lines 25, 38 | Add context: "Failed to generate plan:" or "Failed to execute tasks:" |
| 23 | Medium | No CLI arguments - hardcoded WORKERS=3 not used | lines 9, 49 | Either remove unused variable or add CLI args |

### 5. simple_loop.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 24 | Critical | No way to stop gracefully - Ctrl+C produces ugly traceback | lines 6-22 | Wrap in try/except KeyboardInterrupt with clean exit message |
| 25 | High | No startup banner or instructions | entire file | Add header like "Simple grind loop started. Press Ctrl+C to stop." |
| 26 | Medium | "Improvements: N/A" is confusing when key doesn't exist | line 17 | Better: "No improvements reported" or omit line |
| 27 | Low | Fixed 5-second interval with no ability to configure | line 22 | Add CLI arg or print "Next cycle in 5s..." |
| 28 | Low | Cost shown with 4 decimal places may be excessive | line 18 | Use 2 decimal places: `${cost:.2f}` |

### 6. grind_spawner.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 29 | Medium | Task display truncated to 50 chars with "..." even if shorter | line 190 | Only add "..." if actually truncated: `t['task'][:50] + ('...' if len(t['task']) > 50 else '')` |
| 30 | Low | "Workers" label in banner but they're called "sessions" everywhere else | line 185 | Rename to "Sessions: {len(tasks)}" for consistency |
| 31 | High | Error message for missing --delegate file doesn't show full path | line 157 | Show absolute path: `f"ERROR: --delegate requires {TASKS_FILE.absolute()}"` |
| 32 | Medium | "GRIND SPAWNER - DELEGATION MODE" shown even in single-task mode | line 183 | Make banner dynamic: "SINGLE TASK MODE" vs "DELEGATION MODE" |
| 33 | Low | "Respawning in 2s..." could be more informative | line 135 | Add run count: "Run #{self.runs} complete. Respawning in 2s..." |
| 34 | High | Timeout message says "600s" but most users think in minutes | line 120 | Change to: "timed out after 10 minutes" |

### 7. swarm.py

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 35 | Critical | TOGETHER_API_KEY error returns HTTP 500 with technical message | lines 54-55 | Return 503 Service Unavailable with user-friendly message: "Planning service unavailable. Set TOGETHER_API_KEY environment variable." |
| 36 | Medium | `/plan` response uses different key than `/grind/queue` expects | line 67 | Response says `tasks_created` but explore agent report says `tasks_generated` - inconsistent |
| 37 | Low | No startup message when running directly | line 235 | Add: `print(f"Black Swarm API starting on http://127.0.0.1:8420")` before uvicorn.run() |

### 8. launch.bat

| # | Severity | Issue | Location | Suggested Fix |
|---|----------|-------|----------|---------------|
| 38 | High | No explanation of what --dangerously-skip-permissions does | line 3 | Add comment or echo: "Starting Claude with full permissions (use with caution)" |

---

## Summary by Category

### Missing Help Text
- orchestrator.py: No -h/--help flag
- worker.py: No -h/--help flag
- simple_loop.py: No help at all
- autopilot.py: No help or CLI args

### Inconsistent Argument Parsing
- brain.py uses argparse
- grind_spawner.py uses argparse
- orchestrator.py uses manual sys.argv parsing
- worker.py uses manual sys.argv parsing
- simple_loop.py has no arguments
- autopilot.py has no arguments

### Confusing/Missing Error Messages
- Connection errors show raw exceptions
- Missing API key errors are not user-friendly
- Truncation not indicated when output is cut off

### Accessibility Issues
- No color coding for errors vs success
- No progress indicators for long operations
- Raw JSON dumps instead of formatted output

---

## Recommendations

1. **Standardize CLI parsing**: Use argparse across all scripts for consistent --help and error handling
2. **Add graceful shutdown**: Handle Ctrl+C cleanly in all loop-based scripts
3. **Improve error messages**: Add context and suggested fixes to error messages
4. **Add progress feedback**: Show spinners or status during long API calls
5. **Consistent terminology**: Pick "workers" or "sessions" and use it everywhere
6. **Fix autopilot step numbering**: Step [3] is missing in output
7. **Add startup banners**: Tell users what the script does and how to stop it
