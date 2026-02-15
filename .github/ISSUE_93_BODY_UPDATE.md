# Scout hardening execution checklist (linked work items)

## Checklist

- [x] #84 Fix devtools Scout wrappers (find_python) — CLOSED
- [x] #85 Repair scout-autonomy hook templates — CLOSED (PR #97)
- [ ] #86 Improve scout-ship budget exhaustion UX — in progress / needs verification
- [x] #87 Add CI smoke checks — CLOSED (PR #97)
- [ ] #88 Reconcile devtools README — needs spot-check
- [ ] #89 Harden [GAP] doc invariant — **blocked:** validate-content not in CI
- [ ] #90 Module-specific query scope — needs verification
- [x] #91 Fix scout-doc-sync repair exit code — CLOSED (PR #97)
- [x] #92 Reduce CLI entrypoint drift — CLOSED (PR #97)

## New child issues

- [ ] #98 Ruleset hygiene finalization
- [ ] #99 CI: add validate-content check
- [ ] #100 Scout doc fidelity regression suite
- [ ] #101 Lint debt strategy

## Exit criteria

- Wrapper and hook smoke checks pass on fresh clone
- README command surface matches real launchers and flags
- Doc/query truth-boundary checks pass for representative non-scout modules

## Next 3 execution tasks

1. Add `scout-doc-sync validate-content` to ci.yml (unblocks #89)
2. Verify #86 with low hourly_budget; close if messaging sufficient
3. Spot-check #88 README vs launchers; close if aligned
