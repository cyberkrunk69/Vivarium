# Issue Triage Report — 2026-02-14

**Branch:** chore/issue-triage-hygiene  
**Context:** PR #97 merged. Verification against current master.

## Summary

| Category | Count |
|----------|-------|
| Closed (verified fixed) | 4 |
| Kept open + relabeled | 6 |
| New issues created | 4 |

---

## Closed Now (verified against master)

### #85 Repair scout-autonomy hook templates and installer drift
- **Evidence:** `devtools/scout-autonomy` sources `utils.sh`; hooks use `find_python`; smoke test Test 4 validates hook installation.
- **Files:** `devtools/scout-autonomy`, `devtools/_internal/common/utils.sh`, `devtools/scout-smoke-test.sh`
- **PR:** #97 (commit 12f3ffb)
- **Close comment:** "Closing as completed by PR #97. Hooks source utils.sh; find_python works; smoke test validates installation. devtools/scout-autonomy enable-commit installs prepare-commit-msg; Test 4 verifies."

### #87 Add CI smoke checks for Scout wrappers and hook installation
- **Evidence:** `.github/workflows/ci.yml` runs `./devtools/scout-smoke-test.sh`; smoke test covers wrappers, find_python, hooks, module entrypoints, repair exit code.
- **Files:** `.github/workflows/ci.yml` (line 34-35), `devtools/scout-smoke-test.sh`
- **PR:** #97
- **Close comment:** "Closing as completed by PR #97. CI runs Scout Smoke Tests step (ci.yml). Smoke test covers wrappers, find_python, hooks, doc_sync repair."

### #91 Fix scout-doc-sync repair exit code when repairs succeed
- **Evidence:** `_handle_repair` returns 0 when no stale (line 397) and when repair succeeds (line 437). Smoke test Test 6 validates.
- **Files:** `vivarium/scout/cli/doc_sync.py` (lines 384-437), `devtools/scout-smoke-test.sh` (Test 6)
- **PR:** #97
- **Close comment:** "Closing as completed by PR #97. doc_sync repair returns 0 on success (no stale + repaired). Smoke test Test 6 validates."

### #92 Reduce Scout CLI entrypoint drift
- **Evidence:** `vivarium/scout/cli.py` removed; canonical entrypoint is `vivarium/scout/cli/` package; wrappers invoke `vivarium.scout.cli.*` submodules.
- **Files:** No `vivarium/scout/cli.py` (removed); `vivarium/scout/cli/` package exists
- **PR:** #97
- **Close comment:** "Closing as completed by PR #97. Legacy cli.py removed; canonical cli/ package. Wrappers use vivarium.scout.cli.* submodules."

---

## Kept Open + Relabeled

### #83 Scout hardening tracker
- **Labels:** type:tracker, priority:p0, area:scout
- **Status:** Parent tracker; remains open until child issues resolved.

### #86 Improve scout-ship error messaging for hourly budget exhaustion
- **Labels:** priority:p1, area:scout
- **Status:** `check_budget_with_message` in router.py prints explicit "Hourly budget exhausted" + remediation. May be done — needs verification with low limits.hourly_budget.
- **Note:** router.py lines 62-71 show explicit messaging. Leave open for user verification.

### #88 Reconcile devtools README Scout command surface
- **Labels:** priority:p1, area:scout
- **Status:** README lists scout-* launchers; PR #97 reconciled. Needs spot-check.
- **Note:** devtools/README.md lines 17-26 list scout-*; may be done.

### #89 Harden doc-generation invariant: [GAP] must never ship in docs
- **Labels:** priority:p0, area:scout, area:ci-quality
- **Status:** **NOT DONE.** `validate_content_for_placeholders` and `scout-doc-sync validate-content` exist, but CI does NOT run them. Acceptance: "Validation command/check exists to catch regressions" — command exists, CI check does not.
- **Gap:** Add `scout-doc-sync validate-content --target vivarium` (or similar) to ci.yml.

### #90 Improve module-specific query scope targeting
- **Labels:** priority:p0, area:scout
- **Status:** PR #97 claimed to add; needs verification. Leave open.

### #93 Scout hardening execution checklist
- **Labels:** type:tracker, priority:p0, area:scout, area:ci-quality
- **Status:** Tracker; update body with checklist (see below).

---

## New Issues Created

### A) Ruleset hygiene finalization
- **Title:** Ruleset hygiene: single canonical ruleset, remove stale/disabled confusion
- **Body:** Define single canonical ruleset; remove or document disabled/stale rules; align branch protection with policy_guard.py expectations.
- **Labels:** priority:p1, area:security-governance

### B) CI required-check alignment
- **Title:** CI: add validate-content check for [GAP]/[FALLBACK]/[PLACEHOLDER] invariant
- **Body:** scout-doc-sync validate-content exists but is not run in CI. Add step to ci.yml to fail when generated docs contain forbidden markers. Complements #89.
- **Labels:** priority:p0, area:ci-quality, area:scout

### C) Scout doc fidelity regression suite
- **Title:** Scout doc fidelity: add regression tests for enum/method/async attribution
- **Body:** Add tests (or expand test_ast_facts.py) to guard enum attribution, method_signatures extraction, async function handling. Prevents regression of AST fact extraction fidelity.
- **Labels:** priority:p2, area:scout, area:ci-quality

### D) Lint debt strategy
- **Title:** Lint debt strategy: incremental ratchet vs full reformat plan
- **Body:** CI enforces lint on changed files. Global repo has formatting debt. Document strategy: incremental ratchet (current) vs one-time full reformat. Decide and document.
- **Labels:** priority:p2, area:ci-quality

---

## Tracker #93 Updated Checklist

```markdown
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
- [ ] Ruleset hygiene finalization
- [ ] CI: add validate-content check
- [ ] Scout doc fidelity regression suite
- [ ] Lint debt strategy

## Next 3 execution tasks
1. Add `scout-doc-sync validate-content` to ci.yml (unblocks #89)
2. Verify #86 with low hourly_budget; close if messaging sufficient
3. Spot-check #88 README vs launchers; close if aligned
```

---

## Label Creation Commands

Run when gh CLI has working TLS:

```bash
gh label create "priority:p0" --description "Blocker / governance" --color "b60205"
gh label create "priority:p1" --description "High value" --color "d93f0b"
gh label create "priority:p2" --description "Lower priority" --color "fbca04"
gh label create "type:tracker" --description "Meta / checklist issue" --color "c5def5"
gh label create "area:security-governance" --description "Policy, branch rules" --color "1d76db"
gh label create "area:ci-quality" --description "CI, lint, coverage" --color "0e8a16"
gh label create "area:scout" --description "Scout devtools" --color "5319e7"
```

---

## Known Limitations

- gh CLI TLS certificate errors prevented live label/close operations from this environment.
- Run `./devtools/triage-issues.sh --close-resolved` when gh works to apply closes.
- #86, #88, #90 left open pending user verification.
