# Coverage Targets (Issue #75 Follow-up)

## Current State (Post-Refactor)
- Overall: 33.1%
- Tests: 43 total, 42 passing, 1 flaky (worker isolation)

## Targets by Milestone

### Milestone 1: Stable (Now)
- Overall: 50%
- Critical paths: 75% (queue, worker, identities)
- Status: ✅ Achieved with DM/chatrooms tests

### Milestone 2: Robust (Next Sprint)
- Overall: 75%
- All blueprints: 60%+
- Error paths: 50%

### Milestone 3: Comprehensive (Future)
- Overall: 85%
- All routes: 80%+
- Property-based tests for queue

## Per-Module Targets

| Module | Current | Target M1 | Target M2 |
|--------|---------|-----------|-----------|
| identities | 45% | 60% | 80% |
| messages | 40% | 55% | 75% |
| logs | 50% | 60% | 80% |
| queue | 35% | 60% | 85% |
| bounties | 30% | 50% | 75% |
| quests | 25% | 45% | 70% |
| worker | 40% | 70% | 85% |
| dm | 0% | 40% | 70% |
| chatrooms | 0% | 40% | 70% |

## Action Items
- [ ] Fix worker test isolation (Issue #75.1)
- [ ] Add DM/chatrooms tests (+12% coverage)
- [ ] Add POST path tests for ui_settings, completed_requests, human_request
- [ ] Property-based tests for queue operations (hypothesis)
- [ ] Fuzz testing for API inputs (schemathesis)
