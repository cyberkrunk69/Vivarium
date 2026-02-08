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

## Next milestones (grounded, not speculative)
- Require file verification before scoring a session as "success".
- Normalize log fields for provenance (workspace_root, commit_sha, dry_run).
- Reduce blocked writes by clarifying protected file rules and sandbox policy.
