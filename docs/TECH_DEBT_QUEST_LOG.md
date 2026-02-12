# Technical Debt Quest Log

Last updated: 2026-02-12  
Scope: full-repo debt inventory (runtime, control panel, CI, tests, docs, workflows)

This log is intentionally quest-oriented so each item can be broken down later.
Ordering is highest severity/impact first.

## Severity rubric

- **P0 Critical**: security/data integrity/runtime correctness risks that can break trust or lose/corrupt state
- **P1 High**: major delivery/reliability bottlenecks that meaningfully slow progress
- **P2 Medium**: maintainability/performance drags and workflow friction
- **P3 Low**: cleanup/consistency items

---

## Priority index (global order)

| Rank | Quest ID | Severity | Category | Title |
| --- | --- | --- | --- | --- |
| 1 | QUEST-001 | P0 | Runtime Correctness | Repair broken identity manager contract in enrichment |
| 2 | QUEST-002 | P0 | Data Integrity | Add transactional, locked state writes for queue and ledgers |
| 3 | QUEST-003 | P0 | Quality/Safety | Remove fail-open execution review path |
| 4 | QUEST-004 | P0 | Security | Fix path containment checks (startswith path bug) |
| 5 | QUEST-005 | P0 | Security | Stop trusting `X-Forwarded-For` by default |
| 6 | QUEST-006 | P1 | CI/CD | Repair broken lint/type-check workflow |
| 7 | QUEST-007 | P1 | Architecture | Decompose `swarm_enrichment.py` monolith |
| 8 | QUEST-008 | P1 | Architecture | Decompose inline control-panel frontend template |
| 9 | QUEST-009 | P1 | Performance | Replace full-file log scans with real tail/indexing |
| 10 | QUEST-010 | P1 | Security | Harden UI asset loading (CSP + local assets/SRI) |
| 11 | QUEST-011 | P1 | Testing | Expand coverage for untested high-risk identity/economy paths |
| 12 | QUEST-012 | P1 | Reliability | Reduce broad `except/pass` swallowing in critical paths |
| 13 | QUEST-013 | P2 | Architecture | Decouple blueprints from `control_panel_app` internals |
| 14 | QUEST-014 | P2 | Cleanup | Remove or archive disabled spawner subsystem code |
| 15 | QUEST-015 | P2 | Docs | Replace stale cross-project install docs |
| 16 | QUEST-016 | P2 | Docs | Reconcile Python version/support drift across docs/workflows |
| 17 | QUEST-017 | P2 | Repo Hygiene | Remove generated coverage artifact from source tree |
| 18 | QUEST-018 | P2 | Workflow | Remove stale branch-specific workflow triggers |
| 19 | QUEST-019 | P2 | Security Model | Align policy enforcement between safety layers |
| 20 | QUEST-020 | P2 | Runtime Correctness | Fix `task_verifier` correctness gaps and TODO stub |
| 21 | QUEST-021 | P2 | Safety Tooling | Fix checkpoint filename collision risk |
| 22 | QUEST-022 | P2 | Operability | Persist budget/rate-limiter state across restarts |
| 23 | QUEST-023 | P2 | Testing | Tighten permissive tests and quality thresholds |
| 24 | QUEST-024 | P3 | Cleanup | Remove/replace unused `cost_tracker` singleton |
| 25 | QUEST-025 | P3 | Maintainability | Deduplicate repeated helper utilities |
| 26 | QUEST-026 | P3 | Dependency Mgmt | Add reproducible dependency locking policy |

---

## Category: Runtime Correctness and Data Integrity

### QUEST-001 (P0) - Repair broken identity manager contract in enrichment
- **Impact**: identity mutation/respec/profile flows can silently fail or return degraded behavior.
- **Evidence**:
  - `vivarium/runtime/swarm_enrichment.py:5257, 5379, 6460, 6538` and other sites import `from swarm_identity import get_identity_manager`.
  - Repo search shows no `swarm_identity.py` and no `get_identity_manager` definition.
- **Why this is debt**: key identity APIs rely on a missing module and then often fail-soft in broad exception handlers.
- **Definition of done**:
  1. Replace all `swarm_identity` imports with a canonical in-repo identity service/module.
  2. Add integration tests for `respec_identity`, `change_self_attrs`, `get_profile`, and profile facet mutation.
  3. Remove fail-soft fallback for missing identity manager in these paths.

### QUEST-002 (P0) - Add transactional, locked state writes for queue and ledgers
- **Impact**: multi-worker race conditions can lose tasks, duplicate state transitions, and corrupt JSON.
- **Evidence**:
  - Worker writes queue in multiple places: `worker_runtime.py:1166, 1622, 3299`.
  - UI routes also write queue: `control_panel/blueprints/queue/routes.py:99, 140, 165`.
  - Generic writer is non-atomic and unlocked: `vivarium/utils/__init__.py:20-24`.
  - File locking appears only in enrichment wind-down path: `swarm_enrichment.py:1283-1294`.
- **Definition of done**:
  1. Introduce shared file-lock + atomic write utility (`tempfile + fsync + replace`).
  2. Apply to queue, identity locks, reward ledgers, one-time task ledgers.
  3. Add concurrency tests with parallel worker/control-panel updates.

### QUEST-003 (P0) - Remove fail-open execution review path
- **Impact**: verifier outages/errors can approve outputs without review.
- **Evidence**:
  - Worker initialization warns review will fail open: `worker_runtime.py:270`.
  - Runtime review explicitly fails open: `worker_runtime.py:2383`.
  - Fallback suggestion confirms acceptance without critic: `worker_runtime.py:2385`.
- **Definition of done**:
  1. On verifier unavailable/error, default to `pending_review` (human approval required).
  2. Emit explicit degraded-mode event metrics.
  3. Add regression tests for verifier failure/unavailable cases.

### QUEST-004 (P0) - Fix path containment checks (startswith bug)
- **Impact**: path checks can be bypassed by prefix collisions.
- **Evidence**:
  - Artifact viewer uses string prefix check: `control_panel/blueprints/artifacts/routes.py:30`.
- **Definition of done**:
  1. Replace string prefix checks with `Path.is_relative_to` style logic.
  2. Add tests for prefix-collision paths (e.g. `/.../mutable2/...`).
  3. Audit all file-view/read endpoints for similar containment checks.

### QUEST-020 (P2) - Fix `task_verifier` correctness gaps and TODO stub
- **Impact**: unreliable verification telemetry and incomplete critic implementation.
- **Evidence**:
  - LLM verification is TODO: `task_verifier.py:145`.
  - `VerificationTracker` timestamp stores path string instead of timestamp: `task_verifier.py:180`.
  - Bare exception swallowing in verifier I/O: `task_verifier.py:158, 220, 235`.
- **Definition of done**:
  1. Correct timestamp field to real UTC timestamp.
  2. Implement or explicitly remove `verify_with_llm` stub with contract.
  3. Replace bare exceptions with typed exceptions + structured error reporting.

---

## Category: Security and Trust Boundaries

### QUEST-005 (P0) - Stop trusting `X-Forwarded-For` by default
- **Impact**: localhost-only checks can be bypassed in proxied deployments.
- **Evidence**:
  - Control panel host source trusts `X-Forwarded-For`: `control_panel/middleware.py:23-26`.
  - API host source trusts `x-forwarded-for`: `swarm_api.py:257-259`.
  - Test currently allows remote addr + spoofed XFF localhost: `tests/control_panel/test_api_coverage.py:127-129`.
- **Definition of done**:
  1. Trust forwarded headers only behind explicit trusted-proxy config.
  2. Default to socket peer address.
  3. Add negative tests for spoofed XFF.

### QUEST-010 (P1) - Harden UI asset loading (CSP + local assets/SRI)
- **Impact**: supply-chain and offline reliability risk on control panel frontend.
- **Evidence**:
  - External CDN JS loaded directly: `control_panel/frontend_template.py:8`.
  - Security headers omit CSP: `control_panel/middleware.py:40-45`.
- **Definition of done**:
  1. Serve JS locally or enforce SRI + pinned version.
  2. Add strict Content-Security-Policy header.
  3. Validate UI still works in network-isolated mode.

### QUEST-019 (P2) - Align policy enforcement between safety layers
- **Impact**: policy semantics differ by context and can drift.
- **Evidence**:
  - `SecureAPIWrapper` constitutional restrictions are LAN-only: `secure_api_wrapper.py:150-156`.
  - `swarm_api` constructs wrapper with admin context: `swarm_api.py:166-170`.
- **Definition of done**:
  1. Define explicit shared policy contract for admin/system calls.
  2. Add tests for policy parity across `SafetyGateway` and `SecureAPIWrapper`.
  3. Document intended deltas (if any) and enforce via tests.

### QUEST-008B (P2) - Re-evaluate local command surface and read scope
- **Impact**: unnecessary command surface increases policy complexity and blast radius.
- **Evidence**:
  - Allowlist includes `ls`, `cat`, `rg`: `swarm_api.py:77-83`.
  - Local command output truncation is ad-hoc: `swarm_api.py:659`.
- **Definition of done**:
  1. Reassess allowed commands to minimum viable set.
  2. Add structured read APIs in place of shell file-read commands where possible.
  3. Add exhaustive policy tests for bypass attempts.

---

## Category: CI/CD and Test Quality

### QUEST-006 (P1) - Repair broken lint/type-check workflow
- **Impact**: static checks are unreliable or not running where needed.
- **Evidence**:
  - Lint installs missing file: `.github/workflows/lint.yml:21` (`requirements-dev.txt` not present in repo root).
  - Lint points mypy at non-existent `src`: `.github/workflows/lint.yml:27`.
  - Lint only triggers on `main`: `.github/workflows/lint.yml:5-7`.
- **Definition of done**:
  1. Fix dependency file references and mypy target paths.
  2. Align workflow trigger branches with active development flow.
  3. Add workflow self-check to fail on missing dependency files.

### QUEST-011 (P1) - Expand coverage for untested high-risk identity/economy paths
- **Impact**: critical identity/economy functionality can regress silently.
- **Evidence**:
  - Existing enrichment tests cover only a subset (`tests/test_runtime_phase0_phase1.py:226, 255, 327` instantiate `EnrichmentSystem` for limited scenarios).
  - No tests cover broken `swarm_identity` integration surfaces (`respec_identity` / `change_self_attrs` contract paths).
- **Definition of done**:
  1. Add integration tests for identity mutation/respec/profile APIs.
  2. Add failure-mode tests for corrupted JSON/state and concurrent access.
  3. Gate CI on these test suites.

### QUEST-023 (P2) - Tighten permissive test/coverage thresholds
- **Impact**: CI can pass despite significant quality regressions.
- **Evidence**:
  - Control panel coverage threshold is low: `.github/workflows/control-panel.yml:63` (`--cov-fail-under=50`).
  - Test explicitly allows 500 response as acceptable: `tests/control_panel/test_api_coverage.py:157`.
- **Definition of done**:
  1. Raise coverage thresholds incrementally with an agreed target.
  2. Remove acceptance of 500 for normal malformed-input handling.
  3. Add negative tests for security and concurrency regressions.

---

## Category: Architecture and Maintainability

### QUEST-007 (P1) - Decompose `swarm_enrichment.py` monolith
- **Impact**: extreme change risk, poor reviewability, and hidden regressions.
- **Evidence**:
  - File size is extreme: `vivarium/runtime/swarm_enrichment.py` has `7456` lines.
  - High exception/pass density in the same file (multiple swallow points surfaced by scan).
- **Definition of done**:
  1. Split by domain (`tokens`, `journals`, `bounties`, `identity_mutation`, `social`).
  2. Introduce clear interfaces and typed return contracts.
  3. Add per-domain tests and ownership boundaries.

### QUEST-008 (P1) - Decompose inline control-panel frontend template
- **Impact**: UI is hard to evolve/test and tightly coupled to backend Python.
- **Evidence**:
  - Template file size is very high: `control_panel/frontend_template.py` has `4860` lines.
  - Rendered as raw string in route: `control_panel/blueprints/root/routes.py:13`.
- **Definition of done**:
  1. Move HTML/CSS/JS into static/template assets.
  2. Add frontend build/lint/test pipeline (even lightweight).
  3. Keep Python route layer focused on API and view composition.

### QUEST-013 (P2) - Decouple blueprints from `control_panel_app` internals
- **Impact**: fragile imports, implicit contracts, and hard refactors.
- **Evidence**:
  - Blueprints import private helpers from app module:
    - `blueprints/worker/routes.py:11`
    - `blueprints/spawner/routes.py:17`
    - `blueprints/queue/routes.py:17`
    - `blueprints/rollback/routes.py:139`
- **Definition of done**:
  1. Extract shared services into dedicated modules.
  2. Remove blueprint dependence on private app internals.
  3. Enforce module boundaries with import tests.

### QUEST-014 (P2) - Remove or archive disabled spawner subsystem code
- **Impact**: dead code and cognitive overhead.
- **Evidence**:
  - Spawner endpoints are disabled with 410 responses:
    - `blueprints/spawner/routes.py:152-199`.
  - Module still contains substantial status/process helper logic (`spawner/routes.py:36-137`).
- **Definition of done**:
  1. Either fully remove disabled subsystem code or re-enable behind tested feature flag.
  2. Keep only one supported orchestration path in active tree.

### QUEST-012 (P1) - Reduce broad `except/pass` swallowing in critical paths
- **Impact**: silent failures, hard incident diagnosis, and latent data corruption.
- **Evidence**:
  - High concentration in worker and enrichment (scan count highlights):
    - `worker_runtime.py` multiple broad catches.
    - `swarm_enrichment.py` multiple broad catches and `pass` paths.
  - Example in halt/budget logic swallows parsing errors: `worker_runtime.py:865-889`.
- **Definition of done**:
  1. Replace broad catches with typed exceptions.
  2. Log structured error metadata at all state mutation boundaries.
  3. Add tests for error paths currently swallowed.

### QUEST-025 (P3) - Deduplicate repeated helper utilities
- **Impact**: drift and inconsistent behavior between modules.
- **Evidence**:
  - Repeated helper patterns (`_parse_csv_items`, `_fresh_hybrid_seed`, `_read_jsonl_tail`) across app and blueprints.
- **Definition of done**:
  1. Consolidate shared helpers into utility modules with tests.
  2. Remove duplicate implementations.

---

## Category: Performance and Operability

### QUEST-009 (P1) - Replace full-file log scans with true tail/indexing
- **Impact**: log endpoints become O(file_size) and degrade over time.
- **Evidence**:
  - `_read_jsonl_tail` reads file from start every call: `control_panel_app.py:1290-1299`.
  - `/api/logs/recent` repeatedly invokes this on multiple logs: `blueprints/logs/routes.py:45-47`.
- **Definition of done**:
  1. Implement byte-offset tail reads or indexed tail helper.
  2. Cache/stream recent entries with bounded memory.
  3. Add load tests for large logs.

### QUEST-019B (P2) - Bound raw log endpoint payloads
- **Impact**: memory spikes and latency from full-file responses.
- **Evidence**:
  - `/api/logs/raw` returns entire file content: `blueprints/logs/routes.py:99-102`.
- **Definition of done**:
  1. Add pagination/byte limits.
  2. Add optional compressed/download mode.
  3. Protect endpoint with explicit size guardrails.

### QUEST-022 (P2) - Persist budget/rate limiter state across restarts
- **Impact**: process restarts can reset API budget/rate state unexpectedly.
- **Evidence**:
  - `BudgetEnforcer` and `RateLimiter` are in-memory only: `secure_api_wrapper.py:68-71`, `97-101`.
- **Definition of done**:
  1. Persist usage windows/budget state to durable storage.
  2. Define restart semantics explicitly.
  3. Add restart-resilience tests.

---

## Category: Docs, Workflows, and Repo Hygiene

### QUEST-015 (P2) - Replace stale cross-project install docs
- **Impact**: onboarding confusion and operational mistakes.
- **Evidence**:
  - Install doc references another project name and entrypoint: `docs/INSTALL_GUIDE.md:3-6`, `53`, `86`, `102`.
  - Referenced installer/model files not present in repo (`install_windows.bat`, `install_linux.sh`, `models.txt`, `default_characters/`).
- **Definition of done**:
  1. Rewrite install guide for current Vivarium runtime.
  2. Remove non-existent references.
  3. Add doc validation checks for referenced paths.

### QUEST-016 (P2) - Reconcile Python version/support drift
- **Impact**: environment inconsistency and avoidable setup failures.
- **Evidence**:
  - README says Python 3.11+: `README.md:185`.
  - Technical doc says Python 3.10+: `docs/README_TECHNICAL.md:268`.
  - Workflow matrix includes 3.10/3.11/3.12: `.github/workflows/control-panel.yml:23`.
- **Definition of done**:
  1. Set one canonical supported range.
  2. Update docs and CI matrices to match.

### QUEST-017 (P2) - Remove generated coverage artifact from source tree
- **Impact**: noisy diffs and stale test telemetry in repo history.
- **Evidence**:
  - Generated coverage file tracked: `tests/control_panel/coverage.json`.
- **Definition of done**:
  1. Remove tracked generated coverage artifact.
  2. Add ignore rules for future generated coverage JSON artifacts.

### QUEST-018 (P2) - Remove stale branch-specific workflow triggers
- **Impact**: workflow policy drift and unpredictable CI behavior.
- **Evidence**:
  - Control-panel workflow includes historical branch name: `.github/workflows/control-panel.yml:5` (`slay9kDragon`).
- **Definition of done**:
  1. Align workflow triggers to current branch policy.
  2. Remove historical one-off branch entries.

### QUEST-026 (P3) - Add reproducible dependency locking policy
- **Impact**: non-deterministic environments and upgrade surprises.
- **Evidence**:
  - Requirements are broadly unpinned and no lockfile/pyproject-based lock is present.
- **Definition of done**:
  1. Adopt lockfile strategy (`pip-tools`, `uv`, or equivalent).
  2. Define upgrade cadence and security patch workflow.

---

## Category: Targeted correctness cleanups

### QUEST-021 (P2) - Fix checkpoint filename collision risk
- **Impact**: rollback snapshots can overwrite each other for same basename files in different dirs.
- **Evidence**:
  - Backup uses `filepath.name` only: `safety_validator.py:157`.
- **Definition of done**:
  1. Preserve relative path structure in checkpoint backup.
  2. Add test for duplicate basenames in different directories.

### QUEST-024 (P3) - Remove or replace unused `cost_tracker` singleton
- **Impact**: misleading API and maintenance drag.
- **Evidence**:
  - Module claims thread safety but mutation has no lock: `utils/cost_tracker.py:9-10`, `30-39`.
  - No in-repo usage found for `CostTracker` / `cost_tracker`.
- **Definition of done**:
  1. Delete if unused, or integrate with real call sites and thread safety.
  2. Add tests if retained.

---

## Recommended execution waves

1. **Wave 1 (P0 first)**: QUEST-001 through QUEST-005.
2. **Wave 2 (P1 reliability)**: QUEST-006 through QUEST-012.
3. **Wave 3 (P2/P3 cleanup and scaling)**: remaining quests.

If you want, next pass can convert this directly into issue-ready tickets with estimated effort, owner domain, and dependency graph.

