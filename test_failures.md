# Test Failures Report

**Total Results:** 2 failed, 61 passed

## Failed Tests

### 1. `TestShowStatus.test_displays_summary`
- **File:** tests/test_orchestrator.py:230
- **Issue:** String matching failure in assertion
- **Expected:** "Total tasks: 4"
- **Actual Output:** "Total Tasks:      4" (capitalized "Tasks", extra spacing)
- **Root Cause:** Output formatting changed - text has uppercase "T" and multiple spaces for alignment

### 2. `TestShowStatus.test_shows_active_locks`
- **File:** tests/test_orchestrator.py:259
- **Issue:** String matching failure in assertion
- **Expected:** "Active locks: 1"
- **Actual Output:** "ACTIVE LOCKS (1)" (different format in show_status output)
- **Root Cause:** Output formatting changed - section header changed from lowercase to uppercase with count in parentheses

## Analysis

Both failures are in the `show_status()` function's output formatting. The function appears to have been refactored to use different text formatting/alignment (padding, uppercase headers), but the test assertions still expect the old format.

The actual functionality works correctly - the status is being displayed properly, just with different formatting than what the tests expect.

## Recommendation

Update test assertions in tests/test_orchestrator.py to match the new output format from the refactored show_status() function.
