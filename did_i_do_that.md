# did_i_do_that

Catalog of odd, accidental, or unlikely changes observed across the repo.

## How to Use This Log

- Record anything that looks unlikely, accidental, or unexplained.
- Capture evidence and impact in the same entry.
- Note whether the issue is still active, mitigated, or resolved.
- Keep entries concise but complete.

---

## Index

- D-2026-02-09-01 - Root CODEOWNERS pointed to @claude-ai/team-leads (Resolved)

---

## D-2026-02-09-01 - Root CODEOWNERS pointed to @claude-ai/team-leads

### Summary

- **What**: `CODEOWNERS` at repo root contained `* @claude-ai/team-leads`.
- **First noticed**: 2026-02-09 (user report).
- **Status**: Mitigated on branch `cursor/repository-access-hardening-a505`
  (root CODEOWNERS now points to `@cyberkrunk69`).
- **Severity**: Low (no direct access granted by CODEOWNERS).

### Location

- **File**: `CODEOWNERS` (repo root)
- **Note**: GitHub prioritizes `.github/CODEOWNERS` over root `CODEOWNERS`.

### Evidence

- **Commit introducing file**: `5b6a0b6` ("BACKUP: All work from Feb 3-4...")
- **Commit author**: `cyberkrunk69` (with Claude co-author tag)
- **Content observed on `origin/master`**:
  - `# CODEOWNERS - ensure PRs get the right reviewers`
  - `* @claude-ai/team-leads`

### Likely Cause (Hypothesis)

- Template or AI-assisted insertion during the Feb 3-4 backup work.
- Team name does not match known org/repo configuration.

### Impact Analysis

- CODEOWNERS **does not grant access** to the repo.
- It can **auto-request reviews** and can **block merges** only if branch
  protection requires CODEOWNER approval.
- If `@claude-ai/team-leads` did not exist or lacked repo access, the entry would
  have been ignored.
- Because `.github/CODEOWNERS` exists, the root file may have had no effect.

### Remediation

- Root `CODEOWNERS` updated to `* @cyberkrunk69` on branch
  `cursor/repository-access-hardening-a505`.
- Optional follow-up: delete root `CODEOWNERS` entirely to avoid confusion and
  keep a single source of truth in `.github/CODEOWNERS`.

### Follow-Ups / Checks

- Confirm branch protection requires CODEOWNERS approval.
- Verify no teams named `@claude-ai/team-leads` exist in org settings.
- Consider removing root `CODEOWNERS` after merge.
