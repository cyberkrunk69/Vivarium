# Strategic Roadmap: Waves 14-18

## Executive Summary

After 13 waves and 77+ worker sessions, the system has built a solid foundation of research-backed capabilities. The next phase focuses on **compounding improvements** - capabilities that enable other capabilities to work better.

---

## Current State Assessment

### What's Working Well

| Capability | Implementation | Quality |
|------------|---------------|---------|
| **Knowledge Graph** | `knowledge_graph.py` - Full typed nodes/edges, auto-persistence | ✅ Complete |
| **Skill Registry** | `skills/skill_registry.py` - TF-IDF embeddings, semantic retrieval | ✅ Complete |
| **Context Builder** | `context_builder.py` - Unified retrieval interface | ✅ Complete |
| **Prompt Optimizer** | `prompt_optimizer.py` - DSPy demo collection/injection | ✅ Complete |
| **Role Decomposition** | `roles.py` - CAMEL-based task routing | ✅ Complete |
| **Critic System** | `critic.py` - Automated code review | ✅ Complete |
| **Tree Search** | `tree_search.py` - LATS exploration | ✅ Complete |
| **Memory Synthesis** | `memory_synthesis.py` - Reflection hierarchy | ✅ Complete |
| **Failure Patterns** | `failure_patterns.py` - Error categorization | ✅ Complete |

### Key Metrics
- **100% success rate** across 10 Wave 12 sessions
- **223+ learned lessons** accumulated
- **15,794 lines** of code
- **$0.92** average cost per 10-session wave

---

## Gap Analysis: What's Missing

### Critical Gaps (High Impact, Blocking Progress)

1. **No Real LLM Integration for Intelligence**
   - Current: Critic uses regex/heuristics, not actual model calls
   - Missing: API calls to Claude for semantic code review
   - Impact: Quality assessments are shallow

2. **No Active Learning Loop**
   - Current: Skills/lessons recorded but not actively used to guide decisions
   - Missing: Feedback from outcomes → updated retrieval weights
   - Impact: System doesn't learn what works

3. **No Multi-Path Exploration in Production**
   - Current: Tree search implemented but not wired to grind_spawner
   - Missing: Actually explore 2-3 approaches and pick best
   - Impact: Single-path execution misses better solutions

4. **No Automated Testing of Generated Code**
   - Current: Critic checks syntax/patterns, no runtime verification
   - Missing: Run pytest on generated modules
   - Impact: Broken code gets committed

### Moderate Gaps (Would Improve Efficiency)

5. **Query Expansion Not Fully Utilized**
   - `query_expander.py` exists but not integrated into main retrieval
   - Synonym expansion would improve skill/lesson matching

6. **No Priority Queue for Tasks**
   - Tasks processed in order given, not by importance/urgency
   - Could use importance scores to prioritize

7. **No Cost-Benefit Analysis per Task**
   - Don't track which task types are most expensive vs valuable
   - Could optimize budget allocation

### Nice-to-Have Gaps

8. **No External API Integration**
   - Can't fetch live docs, check stack overflow, etc.
   - Would help with current library versions

9. **No Persistent Worker State**
   - Each worker starts fresh
   - Could share learned context between workers

---

## Prioritized Roadmap: Waves 14-18

### Wave 14: Active Learning Loop (Foundation for Everything)

**Why First**: Without real feedback loops, all other improvements have no signal to learn from.

| Task # | Description | Enables |
|--------|-------------|---------|
| 14.1 | **Outcome Tracking** - Record success/failure per task type, track what worked | Wave 15-18 decisions |
| 14.2 | **Retrieval Feedback** - When a skill/lesson helped, boost its weight | Better retrieval |
| 14.3 | **Negative Examples** - Record what didn't work as anti-patterns | Avoid repeated failures |
| 14.4 | **A/B Testing Framework** - Compare two approaches, record winner | Strategy selection |
| 14.5 | **Metrics Dashboard Update** - Visualize learning curves | Human insight |

### Wave 15: Production Tree Search

**Why Second**: Multiple paths → better solutions → more data for learning loop.

| Task # | Description | Enables |
|--------|-------------|---------|
| 15.1 | **Wire tree_search to grind_spawner** - Actually use multi-path | Solution diversity |
| 15.2 | **Parallel Path Execution** - Run 2-3 strategies concurrently | Speed |
| 15.3 | **Path Scoring Integration** - Use critic to pick best path | Quality |
| 15.4 | **Path Outcome Feedback** - Feed results to Wave 14 learning loop | Continuous improvement |
| 15.5 | **Configurable Exploration** - Budget-based path count | Cost control |

### Wave 16: Autonomous Testing

**Why Third**: Validated code → higher quality → better demos for DSPy.

| Task # | Description | Enables |
|--------|-------------|---------|
| 16.1 | **Auto-generate Tests** - Create pytest tests for new code | Validation |
| 16.2 | **Run Tests Before Commit** - Block if tests fail | Quality gate |
| 16.3 | **Test Failure → Retry** - If tests fail, iterate | Self-correction |
| 16.4 | **Test Coverage Tracking** - Measure what's covered | Prioritization |
| 16.5 | **Test as Verification Signal** - Pass/fail feeds learning loop | Better feedback |

### Wave 17: Smart Retrieval

**Why Fourth**: Better context → better prompts → better code.

| Task # | Description | Enables |
|--------|-------------|---------|
| 17.1 | **Integrate Query Expander** - Use synonyms in skill/lesson retrieval | Better matches |
| 17.2 | **Re-ranking with Outcomes** - Boost skills that led to success | Quality |
| 17.3 | **Contextual Lesson Selection** - Match lesson category to task type | Relevance |
| 17.4 | **Cross-Session Knowledge** - Share learnings between workers | Collective intelligence |
| 17.5 | **Retrieval Ablation** - Test with/without each context type | Optimization |

### Wave 18: Self-Curriculum

**Why Fifth**: System designs its own improvement tasks.

| Task # | Description | Enables |
|--------|-------------|---------|
| 18.1 | **Identify Weak Spots** - Analyze failure patterns, find what needs work | Targeted improvement |
| 18.2 | **Generate Training Tasks** - Create tasks to practice weak areas | Skill building |
| 18.3 | **Difficulty Progression** - Start easy, increase complexity | Learning curve |
| 18.4 | **Self-Evaluation** - Track improvement on generated tasks | Progress measurement |
| 18.5 | **Task Generation Loop** - New tasks from new failures | Continuous curriculum |

---

## Task Definitions for grind_tasks.json

```json
[
  {
    "wave": 14,
    "tasks": [
      {
        "task": "OUTCOME TRACKING: Implement task outcome recording\n\n1. Create outcome_tracker.py with:\n   - record_outcome(task_id, result, success, metrics)\n   - get_success_rate_by_task_type()\n   - get_most_effective_strategies()\n2. Store outcomes in outcomes.json with:\n   - task_description, result, duration, cost, success boolean\n   - retrieval_context (what skills/lessons were used)\n   - code_quality_score from critic\n3. Integrate into grind_spawner.py post-run hook",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "RETRIEVAL FEEDBACK: Implement retrieval weight boosting\n\n1. Add to context_builder.py:\n   - record_retrieval_feedback(item_id, was_helpful: bool)\n   - apply_feedback_weights() on retrieval scores\n2. Store feedback in retrieval_feedback.json\n3. Modify find_similar_skills() to apply boost factors\n4. Integrate into grind_spawner post-run to record what helped",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "NEGATIVE EXAMPLES: Implement anti-pattern recording\n\n1. Add to failure_patterns.py:\n   - record_anti_pattern(description, code_example, why_bad)\n   - get_anti_patterns_for_task(task_description)\n2. Inject anti-patterns into prompts as 'DO NOT do this'\n3. Store in anti_patterns.json with:\n   - pattern, bad_code, explanation, frequency",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "A/B TESTING: Implement approach comparison framework\n\n1. Create ab_testing.py with:\n   - create_experiment(name, variants: List[str])\n   - record_variant_result(experiment, variant, outcome)\n   - get_winning_variant(experiment)\n2. Store experiments in experiments.json\n3. Add --experiment flag to grind_spawner for A/B runs",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "LEARNING DASHBOARD: Update progress_server.py with learning curves\n\n1. Add /api/learning endpoint with:\n   - success_rate_over_time\n   - quality_score_trend\n   - most_improved_task_types\n   - retrieval_feedback_stats\n2. Add learning curves visualization to /dad dashboard\n3. Pull data from outcomes.json and retrieval_feedback.json",
        "budget": 0.40,
        "model": "sonnet"
      }
    ]
  },
  {
    "wave": 15,
    "tasks": [
      {
        "task": "TREE SEARCH WIRING: Connect tree_search.py to grind_spawner\n\n1. In grind_spawner.py, add --tree-search flag\n2. When enabled, use TreeSearch.expand_node() to generate 2-3 strategies\n3. Run each strategy as a separate execution\n4. Use critic to score each result\n5. Select best and use for final output",
        "budget": 0.60,
        "model": "sonnet"
      },
      {
        "task": "PARALLEL PATHS: Execute multiple strategies concurrently\n\n1. Modify tree search integration to use ThreadPoolExecutor\n2. Run 2-3 path variations in parallel\n3. Collect all results, score with critic\n4. Return best path result\n5. Add --max-paths argument (default: 2)",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "PATH SCORING: Integrate critic for path selection\n\n1. After parallel execution, run critic.review() on each result\n2. Rank paths by quality_score\n3. Log path comparison to outcomes.json\n4. Return highest-scoring path",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "PATH FEEDBACK: Feed path outcomes to learning loop\n\n1. Record which strategy variant won for each task type\n2. Store in strategy_outcomes.json\n3. Use to inform future expand_node() priorities\n4. Boost strategies that consistently win",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "EXPLORATION CONFIG: Add budget-based path control\n\n1. Add exploration_budget to config.py\n2. If budget low: single path\n3. If budget medium: 2 paths\n4. If budget high: 3 paths\n5. Document in PROGRESS.md",
        "budget": 0.30,
        "model": "sonnet"
      }
    ]
  },
  {
    "wave": 16,
    "tasks": [
      {
        "task": "AUTO TEST GEN: Generate pytest tests for new code\n\n1. Create test_generator.py with:\n   - generate_tests_for_file(filepath) -> test code\n   - Template: test happy path, test edge cases, test error handling\n2. Use existing code patterns from tests/ as examples\n3. Output to tests/test_<module>.py",
        "budget": 0.60,
        "model": "sonnet"
      },
      {
        "task": "TEST GATE: Block commits if tests fail\n\n1. Add run_tests() function to grind_spawner.py\n2. After code generation, run pytest on relevant tests\n3. If tests fail, retry task with failure feedback\n4. Max 2 retries before marking as failed",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "TEST RETRY: Iterate on test failures\n\n1. Capture pytest output on failure\n2. Inject failure message into retry prompt\n3. Track retry count in session metadata\n4. Record retry patterns in failure_patterns.json",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "TEST COVERAGE: Track and report coverage\n\n1. Run pytest --cov after each wave\n2. Store coverage % in metrics.json\n3. Add coverage trend to dashboard\n4. Flag modules with <50% coverage",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "TEST SIGNAL: Feed test results to learning loop\n\n1. Record pass/fail as outcome signal\n2. Skills that produce passing code get boosted\n3. Track test_pass_rate per skill in skill_registry",
        "budget": 0.40,
        "model": "sonnet"
      }
    ]
  },
  {
    "wave": 17,
    "tasks": [
      {
        "task": "QUERY EXPANSION: Integrate query_expander into retrieval\n\n1. In context_builder.py, use QueryExpander.expand(query)\n2. Search with all expanded terms\n3. Merge results, dedupe, re-rank by combined score\n4. Add toggle for expansion on/off",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "OUTCOME RERANKING: Boost skills by success history\n\n1. Load outcomes.json in skill_registry\n2. Calculate success_rate per skill\n3. Multiply similarity score by success_boost factor\n4. Higher success = higher ranking",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "CONTEXTUAL LESSONS: Match lesson category to task type\n\n1. In context_builder.add_lessons(), filter by task_category\n2. If task contains 'test', prioritize testing lessons\n3. If task contains 'refactor', prioritize code_quality lessons\n4. Add category_weight parameter",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "CROSS-SESSION: Share learnings between workers\n\n1. Use message_pool for real-time lesson sharing\n2. Worker publishes new lesson → others can retrieve\n3. Add lesson_sync() to grind_spawner startup\n4. Dedupe by lesson ID",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "RETRIEVAL ABLATION: Test context contribution\n\n1. Create ablation_test.py\n2. Run same task with: no context, skills only, lessons only, full context\n3. Compare quality scores\n4. Report which context types help most",
        "budget": 0.50,
        "model": "sonnet"
      }
    ]
  },
  {
    "wave": 18,
    "tasks": [
      {
        "task": "WEAK SPOT ANALYSIS: Identify areas needing improvement\n\n1. Create curriculum_generator.py\n2. Analyze failure_patterns.json for common failures\n3. Analyze outcomes.json for low-success task types\n4. Output: prioritized list of weak areas",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "TRAINING TASK GEN: Create practice tasks for weak areas\n\n1. For each weak area, generate 2-3 targeted practice tasks\n2. Template: 'Fix the following [weak_area] issue: [example]'\n3. Store in training_tasks.json\n4. Add --training flag to run practice tasks",
        "budget": 0.50,
        "model": "sonnet"
      },
      {
        "task": "DIFFICULTY PROGRESSION: Implement graduated complexity\n\n1. Tag tasks with difficulty: easy, medium, hard\n2. Start workers on easy tasks in weak areas\n3. Promote to harder tasks after 3 successes\n4. Track progression in worker_progress.json",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "SELF EVALUATION: Measure improvement on training tasks\n\n1. Before training: record baseline success rate\n2. After training: re-run evaluation tasks\n3. Calculate improvement delta\n4. Report in training_report.md",
        "budget": 0.40,
        "model": "sonnet"
      },
      {
        "task": "CURRICULUM LOOP: Continuous task generation from failures\n\n1. After each wave, run weak_spot_analysis()\n2. Generate new training tasks for new failures\n3. Queue for next training session\n4. Loop: fail → train → improve → repeat",
        "budget": 0.50,
        "model": "sonnet"
      }
    ]
  }
]
```

---

## Compound Effect Analysis

```
Wave 14 (Learning Loop)
    ↓ enables
Wave 15 (Tree Search) → generates more outcomes → feeds back to →
    ↓ enables
Wave 16 (Testing) → validates outcomes → higher quality feedback to →
    ↓ enables
Wave 17 (Smart Retrieval) → better context → better code → more positive outcomes to →
    ↓ enables
Wave 18 (Self-Curriculum) → targets weaknesses → rapid improvement loop
```

Each wave builds on the previous. Wave 14 is foundational - without outcome tracking, we can't learn. Wave 15-16 generate better data. Wave 17-18 use that data intelligently.

---

## Success Metrics

| Wave | Success Criteria |
|------|------------------|
| 14 | outcomes.json populated with 50+ records, retrieval_feedback showing boosted items |
| 15 | Tree search running on 50% of tasks, path comparison logs showing selection |
| 16 | All new code has generated tests, test_pass_rate > 80% |
| 17 | Retrieval recall improved (measure with held-out test set) |
| 18 | Self-generated tasks completed, improvement delta > 10% |

---

## Handoff to CODER

**Summary**: Created comprehensive 5-wave strategic roadmap focusing on compound improvements. Wave 14 (Active Learning Loop) is foundational and enables all subsequent waves.

**Ready Artifacts**:
- `strategy_wave13.md` - This document
- Task definitions ready to copy to `grind_tasks.json`

**Blockers**: None identified.

**Recommendation**: Start with Wave 14 tasks immediately - the learning loop is the foundation for measuring all future improvements.
