# Vivarium Development Timeline (regression/progress view)

Updated: 2026-02-08

This timeline captures the back-and-forth between regressions and progress,
grounded in logs and commit history already in this repo.

## Evidence sources
- structured_logs.jsonl
- performance_history.json
- kernel_run.log
- api_audit.log
- safety_audit.log
- tool_operations.json
- git log (commit messages)

## Regression <-> progress cycles (timestamped)
- [PROGRESS] 2026-02-03T05:44: Structured sessions start (architecture review)
  in structured_logs.jsonl.
- [PROGRESS] 2026-02-03T05:53-05:56: Feedback loop tasks run in parallel
  (structured_logs.jsonl).
- [PROGRESS] 2026-02-03T06:02: Dashboard redesign task completes
  (structured_logs.jsonl).
- [PROGRESS] 2026-02-03T06:09-06:15: Knowledge graph + retrieval tasks execute
  (structured_logs.jsonl).
- [PROGRESS] 2026-02-03T06:22:39 -> 06:22:54: Same task rerun drops from
  43.310875s to 12.959601s (performance_history.json).
- [GUARDRAIL] 2026-02-03T06:29-06:30: Safety gate blocks network and prompt
  injection patterns (safety_audit.log).
- [REGRESSION] kernel_run.log: write blocks and sensitive-file protections
  triggered during large runs (blocked writes, cautions).
- [REGRESSION] kernel_run.log: encoding errors and patch parse failures
  ("charmap" errors, invalid patch blocks).
- [REGRESSION] 2026-02-03T07:46-07:54: Safety integration attempts fail with no
  files modified (performance_history.json).
- [REGRESSION] 2026-02-03T09:28: Verification mismatch for claimed file edits
  (tool_operations.json).
- [REGRESSION] 2026-02-03T09:34-09:35: Repeated failed attempts for the
  hallucination bug with no files modified (performance_history.json).
- [REGRESSION] 2026-02-03T22:41: GROQ_API_KEY missing blocks API calls
  (api_audit.log).
- [GUARDRAIL] 2026-02-03T22:42: Budget exceeded events logged (api_audit.log).

## Bugs and failure modes observed (evidence-backed)
- Hallucination/verification gap:
  - tool_operations.json shows claimed files with no verified files.
  - performance_history.json shows repeated attempts with no files modified.
- Encoding failures during automated edits:
  - kernel_run.log contains "charmap" codec errors.
- Patch parse failures:
  - kernel_run.log reports invalid patch blocks.
- Safety integration regressions:
  - performance_history.json records failed safety wiring attempts with
    "no files modified."

## Code pushes (git log highlights)
The following are commit messages recorded in git log; included verbatim:
- cf19d90 Merge pull request #16 from cyberkrunk69/cursor/lm-issues-and-fixes-4c99
- 919d919 Add LM issues catalog and link in architecture
- 93b2f93 Update documentation branding to Vivarium
- fc63889 Rename runtime branding to Vivarium
- 22b1752 Reorganize README around Vivarium concept
- e3ba83e docs: add git hooks troubleshooting note
- 8f0ab36 Merge pull request #11 from cyberkrunk69/cursor/readme-performance-proofs-8550
- 8c530b1 Merge pull request #10 from cyberkrunk69/cursor/grind-spawner-file-missing-7c61

## Patterns worth noting
- Safety and verification gates catch regressions, but they also surface gaps
  where tasks claim success without file changes.
- Performance can improve sharply on reruns, but regressions often show up as
  blocked writes, encoding errors, or verification mismatches.
- Failures cluster around integration steps (safety wiring, file operations),
  suggesting these are the highest-friction points to stabilize.
- User-reported environment anomalies (macOS) and adversarial model behavior
  across platforms were cited as blockers; the response included large-scale
  cleanup, malware scanning, and file corruption repair during the Cursor era.
  The user also reported anomalous behavior observations after a repo download.
  Treat this as user-reported context, not verified by logs.
- Inference noted by the developer: running the swarm in an anomalous
  environment could plausibly lead to data destruction or file corruption.
  As a result, the developer prioritized tech-debt cleanup and crowd-sourced
  analysis of the anomaly.

## Claude era vs Cursor era (speed + quality comparison)
Definition used for this comparison:
- Claude era = commits before the first cursor/ PR merge
  (c5862f3 @ 2026-02-07T23:07:56-07:00).
- Cursor era = commits from that merge onward.

Output speed (commit cadence):
- Claude era: 30 commits across 5 calendar days, 114.26h span,
  avg gap 3.94h, max gap 62.31h.
  With the 10h/day assumption: ~6 commits per 10h.
- Cursor era: 54 commits across 2 calendar days, 13.62h span,
  avg gap 0.26h, max gap 3.43h.
  With the 10h/day assumption: ~27 commits per 10h.

Quality signals (evidence-backed):
- Claude era: performance_history.json (2026-02-03) shows 45 sessions,
  avg duration 102.31s, avg quality 0.97, success rate 82.22%.
  Regressions include verification mismatches, safety integration failures,
  and encoding/patch parse errors (tool_operations.json, performance_history.json,
  kernel_run.log).
- Cursor era: quality signals are primarily code/infra changes:
  core path unit/integration/e2e tests, quality gate pipeline, pruning bloat,
  Groq-only hardening (git log).
  No comparable runtime metrics after 2026-02-03 are present in
  performance_history.json.

## Timeline gaps between code changes (commit-time analysis)
Assumption: ~10 hours/day of active development since start.
Note: Commit gaps measure time between code changes, not necessarily idle time.

Largest gaps between commits (chronological commit dates):
- 62.31h gap
  - 0492a20 2026-02-05T07:49:53-06:00 Fix regex escaping in linkifyFilePaths
  - -> 7f98509 2026-02-08T04:08:18+00:00 Harden core: Groq-only API, JSONL logs, loud failures
- 28.33h gap
  - 5b6a0b6 2026-02-04T02:38:41-06:00 BACKUP: All work from Feb 3-4 before clean rollback
  - -> e6c8e41 2026-02-05T06:58:37-06:00 Control Panel v1: START/PAUSE/STOP, Budget Scaling, Chat History, Sunday Rest
- 8.89h gap
  - 75b046c 2026-02-03T10:54:15-06:00 Add /vision route for new living dashboard + multi-user LAN task
  - -> bcc798b 2026-02-03T19:47:54-06:00 Add founding memory, identity system, and rename tooling
- 5.85h gap
  - 3e623eb 2026-02-03T20:47:45-06:00 Milestone: Swarm builds its own architecture autonomously ($0.17)
  - -> 5b6a0b6 2026-02-04T02:38:41-06:00 BACKUP: All work from Feb 3-4 before clean rollback

Given the 10h/day assumption, gaps >10h likely represent extended blockers,
long-running experiments, or uncommitted work.

## Most critical time-wasting blockers (evidence-backed)
- Missing GROQ_API_KEY blocked API calls (api_audit.log 2026-02-03T22:41:31).
- Verification gap for claimed file edits (tool_operations.json 2026-02-03T09:28).
- Repeated failed attempts with no files modified (performance_history.json
  2026-02-03T09:34-09:35, hallucination bug attempts).
- Safety integration attempts failing with no file changes (performance_history.json
  2026-02-03T07:46-07:54).
- Encoding errors during automated edits (kernel_run.log "charmap" errors).
- Patch parse failures during automated edits (kernel_run.log invalid patch blocks).
- File protection blocks on sensitive targets (kernel_run.log blocked writes).

## Next milestones (grounded, not speculative)
- Require file verification before scoring a session as "success".
- Normalize log fields for provenance (workspace_root, commit_sha, dry_run).
- Reduce blocked writes by clarifying protected file rules and sandbox policy.
