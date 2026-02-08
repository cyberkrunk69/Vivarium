# TODO

## CI / Automation
- [ ] Review CI workflow coverage (lint, type check, coverage thresholds).
- [ ] Add a dedicated "scans" job so scan failures are isolated.
- [ ] Add a scheduled workflow (weekly) to run structured + workflow scans on main.

## Developer Tooling
- [ ] Add a `make scan` target (or scripts/scan_all.sh) to run both scans locally.
- [ ] Add a small wrapper (tools/scan_all.py) to run all scans and emit one report.

## Documentation
- [ ] Document scan tools and reports in QUICK_REF.md.
- [ ] Add SCANNING.md explaining when to run scans and how to interpret reports.

## Validation / Tests
- [ ] Add small fixture files and unit tests for the scan tools.

## Completed
- [x] Add PyYAML dependency for scan tools.
- [x] Add structured file scan and workflow semantic scan tools.
- [x] Wire scan hooks into pre-commit and CI.
