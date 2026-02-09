# did_i_do_that

Catalog of odd, accidental, or unlikely changes observed across the repo.

## 2026-02-09 - Root CODEOWNERS pointed to @claude-ai/team-leads

- **What**: `CODEOWNERS` at repo root contained:
  - `* @claude-ai/team-leads`
- **Where found**: `CODEOWNERS` (repo root), not `.github/CODEOWNERS`.
- **When added**: commit `5b6a0b6` ("BACKUP: All work from Feb 3-4...").
- **Attribution**: commit authored by `cyberkrunk69` with a Claude co-author tag.
- **Why it is odd**: the team name does not match this org/repo setup.
- **Impact**: CODEOWNERS does **not** grant access. It only auto-requests
  reviews and can gate merges if branch protection requires CODEOWNERS review.
  GitHub also prioritizes `.github/CODEOWNERS`, so the root file may have been
  ignored entirely.
