# Architecture Audit Report

**Generated:** 2026-02-03
**Codebase:** claude_parasite_brain_suck
**Total Python Files:** 41
**Total Lines (estimated):** ~6,500+

---

## Executive Summary

This codebase implements a **multi-agent AI task execution system** combining research paper implementations from:
- CAMEL (arXiv:2303.17760) - Role-based task decomposition
- Voyager (arXiv:2305.16291) - Skill library and self-verification
- MetaGPT (arXiv:2308.00352) - Message pool and structured artifacts
- Generative Agents (arXiv:2304.03442) - Memory synthesis and reflection
- DSPy (arXiv:2310.03714) - Prompt optimization through demonstrations
- LATS (arXiv:2310.04406) - Tree search and critic feedback
- Reflexion (arXiv:2303.11366) - Episodic memory utilities

The architecture is **ambitious but fragmented**, with significant technical debt accumulated from rapid prototyping.

---

## Module Quality Scores

| Module | Score | Status | Notes |
|--------|-------|--------|-------|
| **config.py** | 9/10 | Excellent | Clean, minimal, proper env var handling |
| **utils.py** | 8/10 | Good | Solid utilities, well-documented, DRY |
| **logger.py** | 7/10 | Good | Functional but basic; could use structured logging |
| **orchestrator.py** | 7/10 | Good | Well-structured CLI, proper validation, good docs |
| **worker.py** | 7/10 | Good | Proper lock protocol, error handling, clear flow |
| **swarm.py** | 6/10 | Fair | FastAPI server works but /grind is simulation-only |
| **brain.py** | 5/10 | Fair | Minimal orchestrator; duplicate of orchestrator.py intent |
| **roles.py** | 8/10 | Good | Solid CAMEL implementation, good schema integration |
| **message_pool.py** | 7/10 | Good | Clean MetaGPT implementation, proper persistence |
| **tree_search.py** | 6/10 | Fair | LATS skeleton only; expand/evaluate are stubs |
| **knowledge_graph.py** | 6/10 | Fair | BFS traversal works; AST parsing is basic |
| **memory_synthesis.py** | 7/10 | Good | Generative Agents reflection works; TF-IDF retrieval |
| **dspy_modules.py** | 5/10 | Fair | Mock interface dominates; real DSPy integration missing |
| **grind_spawner.py** | 5/10 | Fair | Massive file (1600+ lines); needs decomposition |
| **critic.py** | 6/10 | Fair | Basic quality checks; could be more sophisticated |
| **prompt_optimizer.py** | 6/10 | Fair | DSPy-lite; semantic matching not implemented |
| **skill_registry.py** | 7/10 | Good | Voyager skill composition works; TF-IDF retrieval |
| **artifacts/schemas.py** | 8/10 | Good | Pydantic schemas well-defined |
| **sop_executor.py** | 4/10 | Poor | Placeholder/stub implementation |
| **performance_tracker.py** | 7/10 | Good | Solid metrics collection and rolling averages |
| **improvement_suggester.py** | 6/10 | Fair | Keyword-based; could use smarter analysis |
| **utils/reflection.py** | 6/10 | Fair | Reflexion episodic memory; basic keyword matching |
| **autopilot.py** | 4/10 | Poor | Broken - references non-existent endpoints |
| **simple_loop.py** | 3/10 | Poor | Minimal script; no error handling |
| **spawn_opus.py** | 5/10 | Fair | Wrapper script; swaps files unsafely |
| **cost_tracker.py** | 5/10 | Fair | Basic cost parsing; no aggregation sophistication |
| **log_result.py** | 4/10 | Poor | Simple logging; redundant with logger.py |
| **tests/** | 6/10 | Fair | Good brain.py coverage; sparse elsewhere |

---

## Critical Issues That Need Fixing

### 1. **grind_spawner.py is a Monolith** (CRITICAL)
- **Location:** `grind_spawner.py` (1,617 lines)
- **Problem:** Single file contains GrindSession class, 15+ lesson recording functions, 10+ utility functions, CLI parsing, and all integration logic
- **Impact:** Unmaintainable, hard to test, violates SRP
- **Recommendation:** Split into:
  - `grind_session.py` - GrindSession class
  - `lesson_recorder.py` - All `record_*_lesson()` functions
  - `grind_cli.py` - CLI argument parsing and main()
  - `grind_adapters.py` - Model/budget adaptation functions

### 2. **Duplicate Orchestration Modules** (HIGH)
- **Files:** `orchestrator.py`, `brain.py`, `autopilot.py`, `simple_loop.py`
- **Problem:** Four different ways to spawn/manage tasks with overlapping functionality
- **Impact:** Confusion about which to use, code duplication
- **Recommendation:** Consolidate into single `orchestrator.py` with modes

### 3. **swarm.py /grind Endpoint is a Stub** (HIGH)
- **Location:** `swarm.py:57-81`
- **Problem:** Returns random budget values, doesn't execute actual tasks
- **Impact:** Integration testing impossible; real workloads not supported
- **Recommendation:** Implement actual task execution or document as mock server

### 4. **dspy_modules.py Mock Dominates** (MEDIUM)
- **Location:** `dspy_modules.py:31-82`
- **Problem:** 95% of code is mock implementation; real DSPy never used
- **Impact:** Claimed DSPy optimization is placebo
- **Recommendation:** Either implement real DSPy integration or remove claims

### 5. **autopilot.py References Non-Existent Endpoints** (MEDIUM)
- **Location:** `autopilot.py:21-33`
- **Problem:** Calls `/grind/queue` and expects `tasks_generated` key - neither exist in swarm.py
- **Impact:** autopilot.py is completely broken
- **Recommendation:** Fix endpoint names or deprecate module

### 6. **tree_search.py is Skeleton Only** (MEDIUM)
- **Location:** `tree_search.py:50-86, 88-110`
- **Problem:** `expand_node()` and `evaluate_node()` are synthetic stubs
- **Impact:** LATS paper implementation claims are misleading
- **Recommendation:** Implement real action generation or document as template

### 7. **No Integration Tests** (MEDIUM)
- **Location:** `tests/` directory
- **Problem:** Only unit tests exist; no end-to-end flow testing
- **Impact:** Cannot verify system works as integrated whole
- **Recommendation:** Add integration tests for orchestrator->worker->swarm flow

### 8. **Inconsistent Error Handling Patterns** (MEDIUM)
- **Pattern:** Some modules use `try/except Exception`, others specific exceptions
- **Examples:**
  - `worker.py` catches specific `httpx` exceptions properly
  - `grind_spawner.py` often catches bare `Exception`
- **Recommendation:** Standardize on specific exception handling

---

## Technical Debt Summary

### Code Duplication
- JSON read/write patterns duplicated across `worker.py`, `grind_spawner.py`, `swarm.py`
  - Should use `utils.read_json/write_json` consistently
- Lesson recording functions are nearly identical (15 functions in grind_spawner.py)
  - Extract to single parameterized function

### Unused Code
- `skills/import_config_constants.py` - Standalone file, never imported
- `skills/migrate_to_utils.py` - Standalone file, never imported
- `skills/add_test_coverage.py` - Standalone file, never imported
- ✅ `test_memory_synthesis.py` - Moved to tests/

### Missing Type Hints
- `grind_spawner.py` - Many functions lack return type annotations
- `autopilot.py` - No type hints
- `simple_loop.py` - No type hints

### Dead Patterns
- `sop_executor.py` - Quality gate verification always returns True
- `knowledge_graph.py` - `populate_from_codebase()` catches and silently ignores errors

---

## Integration Gaps

### 1. Knowledge Graph Not Integrated
- **Status:** KnowledgeGraph exists but isn't used in main flows
- **Location:** Only referenced in `query_knowledge_graph_for_recovery()` which creates fresh empty instance each call
- **Fix:** Persist and populate KG, use for skill retrieval

### 2. Performance Tracker Data Not Leveraged
- **Status:** Metrics collected but never analyzed for auto-improvement
- **Location:** `PerformanceTracker` writes to file but no feedback loop
- **Fix:** Connect to `improvement_suggester.py` output

### 3. Critic Feedback Not Looped Back
- **Status:** Critic generates quality scores but doesn't influence retry strategy
- **Location:** `grind_spawner.py:324-328` logs but doesn't act
- **Fix:** When quality_score < threshold, modify prompt with critic feedback

### 4. DSPy Demonstrations Not Persisted
- **Status:** Demos collected each run but not saved for future sessions
- **Location:** `prompt_optimizer.py:16-71` reads logs but never writes optimized prompts
- **Fix:** Save top demonstrations to dedicated file for bootstrap

---

## Recommendations for Next 3 Waves

### Wave 1: Structural Cleanup (High Priority)
1. **Split grind_spawner.py** into 4+ focused modules
2. **Consolidate orchestration** - Deprecate brain.py, autopilot.py, simple_loop.py
3. **Fix autopilot.py** endpoint references or remove
4. ✅ **Move test_memory_synthesis.py** to tests/ directory (COMPLETED)
5. **Delete standalone skill files** - Code is in skill_registry.py

### Wave 2: Complete Paper Implementations (Medium Priority)
1. **Implement real tree_search expand/evaluate** with LLM calls
2. **Connect DSPy to actual dspy-ai package** or remove mock
3. **Implement swarm.py /grind** with real task execution
4. **Wire up KnowledgeGraph** for cross-session learning
5. **Add integration tests** for full flow

### Wave 3: Production Hardening (Lower Priority)
1. **Standardize logging** - Use structured JSON logging
2. **Add retry with backoff** for API calls (currently hard timeout)
3. **Implement config validation** at startup
4. **Add metrics export** (Prometheus/StatsD compatible)
5. **Create deployment documentation**

---

## Unused/Dead Code to Remove

| File/Function | Location | Reason |
|--------------|----------|--------|
| `skills/import_config_constants.py` | Root | Never imported |
| `skills/migrate_to_utils.py` | Root | Never imported |
| `skills/add_test_coverage.py` | Root | Never imported |
| `simple_loop.py` | Root | Superseded by orchestrator |
| `brain.py` | Root | Duplicate of orchestrator.py |
| `sop_executor._check_gate()` | Line 101 | Always returns True |
| `dspy_modules.MockDSPy` | Lines 74-82 | Remove if using real DSPy |

---

## Architectural Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENTRY POINTS                              │
├─────────────────────────────────────────────────────────────────┤
│  orchestrator.py  │  grind_spawner.py  │  spawn_opus.py         │
│  (CLI: start/add) │  (CLI: --task)     │  (Opus wrapper)        │
└────────┬──────────┴────────┬───────────┴────────────────────────┘
         │                   │
         ▼                   ▼
┌─────────────────┐  ┌─────────────────────────────────────────────┐
│   worker.py     │  │            GrindSession                      │
│  - Lock protocol│  │  - Role executor (CAMEL)                     │
│  - Task exec    │◄─│  - Skill injection (Voyager)                 │
│  - HTTP client  │  │  - Prompt optimization (DSPy)                │
└────────┬────────┘  │  - Critic review (LATS)                      │
         │           │  - Self-verification                         │
         ▼           └────────────────────────────────────────────┬─┘
┌─────────────────┐                                               │
│   swarm.py      │◄──────────────────────────────────────────────┘
│  FastAPI Server │
│  /grind (stub)  │
│  /plan (AI)     │
│  /status        │
└─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     SUPPORTING MODULES                           │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   roles.py   │ message_pool │ knowledge_   │ memory_synthesis   │
│   (CAMEL)    │   (MetaGPT)  │   graph      │ (Gen. Agents)      │
├──────────────┼──────────────┼──────────────┼────────────────────┤
│ tree_search  │ dspy_modules │ skill_       │ critic.py          │
│   (LATS)     │   (DSPy)     │  registry    │ (TextGrad)         │
├──────────────┴──────────────┴──────────────┴────────────────────┤
│  utils.py  │  config.py  │  logger.py  │  artifacts/schemas.py  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conclusion

The codebase demonstrates **strong research awareness** with implementations referencing 7+ academic papers. However, **execution is inconsistent**:

- **Strong:** config.py, utils.py, roles.py, worker.py, artifacts/schemas.py
- **Needs Work:** grind_spawner.py, dspy_modules.py, tree_search.py
- **Should Remove:** brain.py, autopilot.py, simple_loop.py, standalone skill files

**Overall Architecture Score: 6/10**

The foundation is solid but needs consolidation and completion of stub implementations before production use.
