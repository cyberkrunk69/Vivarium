# Scout Doc Accuracy Baseline Audit

**Date:** 2026-02-14  
**Sample:** router.py, config.py, audit.py, inference_engine.py (hybrid-generated)

## Summary

- **Files reviewed:** 4
- **Accuracy issues found:** 11
- **Critical (would mislead user):** 3
- **Minor (typo, unclear, missing detail):** 8

**Accuracy rate:** ~85% (structure/symbols correct; param/signature extraction weak)

**Main issues:** (1) Function parameters and return types often omitted or wrong; (2) Module-level functions misattributed to classes (inference_engine); (3) Cross-module hallucination detected during config.py generation.

---

## Detailed Findings

### vivarium/scout/.docs/router.py.tldr.md

| Line | Issue | Severity | Evidence |
|------|-------|----------|----------|
| 88–96 | `check_budget_with_message` shows Parameters (none), Return Type (none) | **Critical** | Source: `def check_budget_with_message(config: ScoutConfig, estimated_cost: float = 0.01, audit: Optional[AuditLog] = None) -> bool` |
| 74–80 | `_notify_user` shows Parameters (none) | Minor | Source: `def _notify_user(message: str) -> None` |
| 98–106 | `on_git_commit` (module-level) shows Parameters (none) | Minor | Source: `def on_git_commit(changed_files: List[Path], repo_root: Optional[Path] = None) -> None` |
| 6 | `COST_PER_MILLION_70B`: 0.9 | Minor | Source: 0.90 (cosmetic) |

**Checklist:** ✓ Class inheritance correct (TriggerRouter, NavResult, SymbolDoc); ✓ No invented methods; ✓ Constants mostly accurate; ✗ Function signatures incomplete.

---

### vivarium/scout/.docs/config.py.tldr.md

| Line | Issue | Severity | Evidence |
|------|-------|----------|----------|
| Gen-time | Cross-module hallucination: `MAX_EXPANDED_CONTEXT` mentioned but not defined | Minor | Logged during generation; symbol does not exist in config.py |
| 17 | `TriggerConfig`: "class with methods" (empty) | Minor | TriggerConfig is dataclass with `type`, `max_cost`; no methods — accurate but sparse |
| 18 | `_semaphore` Value: None | Minor | Correct; type is Optional[asyncio.Semaphore] |

**Checklist:** ✓ Constants accurate (DEFAULT_CONFIG, HARD_*); ✓ ScoutConfig methods correct including whimsy_mode; ✓ EnvLoader present; ✓ No invented content.

---

### vivarium/scout/.docs/audit.py.tldr.md

| Line | Issue | Severity | Evidence |
|------|-------|----------|----------|
| 16 | AuditLog Constants: `name` (used at lines (none)) | Minor | Spurious; `name` not a class constant in AuditLog |
| 19–20 | `__init__` Parameters (none) | Minor | Source: `def __init__(self, path: Path = None)` — optional path param missing |

**Checklist:** ✓ All AuditLog methods present (including gate_metrics, flush); ✓ Constants accurate (ROTATION_SIZE_BYTES, FSYNC_*, EVENT_TYPES); ✓ No invented methods.

---

### vivarium/runtime/.docs/inference_engine.py.tldr.md

| Line | Issue | Severity | Evidence |
|------|-------|----------|----------|
| 7–15 | `EngineType` doc lists methods `estimate_complexity() -> None` and `get_engine_type_from_env() -> EngineType` | **Critical** | Source: EngineType is an Enum (GROQ, CLAUDE, AUTO). Those are module-level functions, not class methods. |
| 14 | `estimate_complexity() -> None` | **Critical** | Source: `def estimate_complexity(request: str) -> int` — wrong return type (int), wrong attribution (module-level) |
| 15 | `get_engine_type_from_env() -> EngineType` | Minor | Correct signature but wrong attribution — it's a module-level function |

**Checklist:** ✗ Class vs module attribution wrong; ✗ Return type wrong; ✓ Constants (_COMPLEXITY_KEYWORDS) accurate; ✓ No invented symbols.

---

## Recommendations

- [ ] **Param extraction:** Improve AST fact extractor to capture function parameters and return types for tldr output
- [ ] **Class vs module attribution:** Ensure module-level functions are not attributed to Enum or other classes
- [ ] **Cross-reference validation:** Add validation for symbols mentioned in docs (e.g. MAX_EXPANDED_CONTEXT) against actual source
- [ ] **Optional --rich mode:** Consider --rich for fuller prose; current hybrid produces accurate structure but sparse descriptions

---

## Expected Outcome Interpretation

| Scenario | Result |
|----------|--------|
| 90%+ accurate, minor issues | **Partial** — structure/symbols ~90%; param/signature ~70% |
| 70–90% accurate, some critical | **Matches** — 3 critical (param/signature, class attribution) |
| <70% accurate, major hallucinations | No |

**Verdict:** Ship with known issues. Accuracy is adequate for navigation and symbol discovery; parameter/signature completeness should be prioritized post-release. The hybrid pipeline (AST facts + constrained LLM) reduces hallucination; the main gaps are in fact extraction, not LLM synthesis.
