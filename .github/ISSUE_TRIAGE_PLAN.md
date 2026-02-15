# Issue Triage and Priority Plan (2026-02-14)

This file is the source-of-truth triage order for open hardening work.

## Status (post-triage 2026-02-14)

### Closed (verified fixed in PR #97)

- **#85** Hook installer/template drift
- **#87** CI smoke checks for wrappers/hooks
- **#91** scout-doc-sync repair exit code
- **#92** CLI entrypoint drift

### P0 (blockers)

- **#93** Scout hardening execution checklist (tracker)
- **#89** Harden doc-generation invariant — **blocked:** validate-content not in CI
- **#90** Improve module-scoped query targeting (needs verification)

### P1 (high-value)

- **#88** Reconcile devtools README (needs spot-check)
- **#86** Budget exhaustion UX (check_budget_with_message exists; needs verification)

### New gap issues (to create)

1. Ruleset hygiene: single canonical ruleset
2. CI: add validate-content check
3. Scout doc fidelity regression suite
4. Lint debt strategy

## Automation

```bash
# Apply labels (no closes)
./devtools/triage-issues.sh

# Apply labels + close verified-fixed issues
./devtools/triage-issues.sh REPO --close-resolved

# Create new gap issues
./devtools/triage-issues.sh REPO --close-resolved --create-gaps
```

Full report: `docs/ISSUE_TRIAGE_REPORT_20260214.md`
