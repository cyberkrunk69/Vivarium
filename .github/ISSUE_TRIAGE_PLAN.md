# Issue Triage and Priority Plan (2026-02-15)

This file is the source-of-truth triage order for open hardening work while API write access is unavailable from integration tokens.

## Priority Order

### P0 (blockers / governance)

1. **#93** Scout hardening execution checklist (tracker)
2. **#89** Harden doc-generation invariant (`[GAP]` must never ship in docs)
3. **#90** Improve module-scoped query targeting and truth validation

### P1 (high-value reliability)

4. **#88** Reconcile `devtools/README.md` command surface with real launchers
5. **#86** Improve hourly budget exhaustion UX in ship/commit flows

### P1 (verify-and-close candidates)

These appear complete based on current repo behavior and should be verified, then closed:

- **#85** Hook installer/template drift
- **#87** CI smoke checks for wrappers/hooks
- **#91** `scout-doc-sync repair` success exit code semantics
- **#92** CLI entrypoint drift (`cli.py` vs `cli/main.py`)

## Current Gaps Not Yet Represented as Issues

1. Ruleset hardening gap:
   - `require_code_owner_review` is still disabled in active ruleset.
   - Push/update restrictions are not yet confirmed owner-only.
2. Lint debt strategy:
   - Global repo still has large formatting debt.
   - CI now enforces changed-file lint/type checks as an incremental ratchet.

## Automation

Use `./devtools/triage-issues.sh` to apply labels and optional close operations once running from a token with issue write permissions.
