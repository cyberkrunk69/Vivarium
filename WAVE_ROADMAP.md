# Wave Roadmap: Future Development Plan

**Document Version:** 1.0
**Created:** 2026-02-03
**Current Wave:** 14 (Safety Wave - in progress)
**Based on:** `wave_status.json`, `SAFETY_CONSTRAINTS.json`, existing infrastructure

---

## Wave 15: Multi-Path Exploration

**Objective:** Enable parallel exploration of solution strategies with learning from path comparison outcomes.

**Foundation Files:**
- `multi_path_executor.py` - Current parallel execution engine
- `memory_synthesis.py` - Path comparison synthesis methods (`synthesize_path_comparisons`, `extract_cost_quality_tradeoffs`)
- `knowledge_graph.py` - `NodeType.SOLUTION_PATH`, `link_path_to_outcomes`, `get_paths_for_concept`
- `grind_spawner.py` - `--multi-path` flag integration

### Task 15.1: Path Strategy Generator

**File:** `multi_path_executor.py`
**Description:** Extend `generate_path_variants()` to create strategy-specific prompt variants beyond simple budget allocation.

**Implementation:**
- Add `prompt_variant` field to `ExecutionPath` dataclass
- Create strategy-specific context injection (CONSERVATIVE: extra validation steps, AGGRESSIVE: experimental patterns, BALANCED: standard best practices)
- Integrate with `create_strategy_prompt_modifier()` to auto-generate variants

**Acceptance Criteria:**
- Each path receives a distinct prompt tailored to its strategy
- Prompt variants are logged in `multi_path_execution_log.json`
- Tests pass: strategy prompts differ in complexity/approach

---

### Task 15.2: Path Comparison Learning Pipeline

**File:** `memory_synthesis.py`
**Description:** Implement automated learning from path comparison outcomes using existing `synthesize_path_comparisons()`.

**Implementation:**
- Create `PathComparisonLearner` class that:
  - Loads `multi_path_execution_log.json` after each multi-path run
  - Calls `synthesize_path_comparisons()` to generate insights
  - Updates `path_comparison_insights.json` with new learnings
- Add `extract_strategy_preferences()` to identify which strategies work best for which task types
- Implement confidence-weighted strategy selection for future runs

**Acceptance Criteria:**
- After 5+ multi-path executions, system can recommend optimal strategy for task type
- Insights include confidence scores based on sample size
- Integration with `grind_spawner.py` to auto-apply learnings

---

### Task 15.3: Knowledge Graph Path Tracking

**File:** `knowledge_graph.py`
**Description:** Fully wire path outcomes to knowledge graph for concept-based retrieval.

**Implementation:**
- In `link_path_to_outcomes()`, ensure bidirectional edges are created:
  - `SOLUTION_PATH --EXPLORED_BY--> CONCEPT`
  - Store quality metrics in path node properties
- Create `recommend_path_for_task()` method that:
  - Extracts concepts from task using `extract_concepts()`
  - Queries `get_paths_for_concept()` for each concept
  - Aggregates and ranks paths by historical quality
- Add `NodeType.TASK_TYPE` for clustering similar tasks

**Acceptance Criteria:**
- Query "What path worked best for refactoring tasks?" returns ranked results
- Path recommendations improve over time with more data
- Integration point in `GrindSession.get_prompt()` for path suggestions

---

### Task 15.4: Budget-Aware Path Reallocation

**File:** `multi_path_executor.py`
**Description:** Dynamically reallocate budget based on early path results.

**Implementation:**
- Add `PathController` class that monitors running paths
- Implement early termination for paths with quality < 0.3 after initial execution
- Reallocate freed budget to remaining high-performing paths
- Add `budget_reallocation_log` to track reallocation decisions

**Acceptance Criteria:**
- Paths that fail early release budget to others
- Total budget utilization remains at ~100%
- Reallocation decisions logged for learning

---

### Task 15.5: Path Result Aggregation

**File:** Create `path_aggregator.py`
**Description:** Combine successful outputs from multiple paths when beneficial.

**Implementation:**
- Create `PathAggregator` class with methods:
  - `can_aggregate(paths: List[ExecutionPath]) -> bool`
  - `aggregate_outputs(paths: List[ExecutionPath]) -> str`
- Implement aggregation strategies:
  - Code merge (for non-conflicting changes)
  - Documentation merge (combine insights)
  - Test suite merge (union of test cases)
- Add safety check via `safety_gateway.py` before emitting aggregated output

**Acceptance Criteria:**
- Aggregation produces valid, runnable code
- Conflicts are detected and reported (no silent merge errors)
- Aggregated output quality >= max(individual path qualities)

---

### Task 15.6: Path Exploration Depth Control

**File:** `multi_path_executor.py`
**Description:** Add support for multi-level path exploration (tree search).

**Implementation:**
- Add `exploration_depth` parameter to `MultiPathExecutor`
- Implement recursive path generation:
  - Level 1: Initial 3 strategies
  - Level 2: Top 2 performers spawn sub-variants
- Cap exploration depth based on budget and time constraints
- Integrate with LATS paper patterns (arXiv:2310.04406)

**Acceptance Criteria:**
- Depth-2 exploration produces 5-9 total paths
- Budget respects per-level allocation
- Best path selection considers all levels

---

### Task 15.7: Real-time Path Monitoring Dashboard

**File:** Create `path_monitor.py`
**Description:** Provide real-time visibility into parallel path execution.

**Implementation:**
- Create `PathMonitor` class with methods:
  - `get_active_paths() -> List[Dict]`
  - `get_path_progress(path_id) -> Dict`
  - `get_comparison_summary() -> Dict`
- Write status to `path_monitor_state.json` every 5 seconds
- Add CLI output formatting for `--multi-path` mode

**Acceptance Criteria:**
- Console shows live progress of each path
- Path status includes: strategy, elapsed time, current step
- Summary printed at completion comparing all paths

---

### Task 15.8: Path Strategy A/B Testing Framework

**File:** Create `path_ab_testing.py`
**Description:** Controlled experiments to validate new strategies.

**Implementation:**
- Create `StrategyExperiment` class:
  - Define control (BALANCED) and treatment (new strategy) groups
  - Randomize task assignment to strategies
  - Track and compare outcomes with statistical significance
- Implement `run_experiment(task_set, control, treatment, sample_size)`
- Generate experiment reports with p-values and confidence intervals

**Acceptance Criteria:**
- Can run experiments with n=20+ samples
- Reports include statistical significance tests
- New strategies only graduate to production if p < 0.05

---

## Wave 16: Self-Improvement (Within Safety Constraints)

**Objective:** Enable the system to optimize its own prompts and skill extraction based on successful patterns, while strictly adhering to `SAFETY_CONSTRAINTS.json`.

**Safety Boundary:** All self-improvement is LOCAL ONLY - no external data, no network access, no self-replication beyond workspace.

**Foundation Files:**
- `prompt_optimizer.py` - DSPy-based prompt optimization
- `skill_extractor.py` - Automatic skill extraction
- `skills/skill_registry.py` - Skill storage and retrieval
- `learned_lessons.json` - Knowledge repository
- `SAFETY_CONSTRAINTS.json` - Enforced constraints

### Task 16.1: Prompt Performance Tracking

**File:** `prompt_optimizer.py`
**Description:** Track which prompt patterns correlate with high-quality outcomes.

**Implementation:**
- Create `PromptPerformanceTracker` class:
  - Log prompt templates with outcome metrics (quality_score, success, elapsed_time)
  - Compute correlation between prompt features and outcomes
  - Identify high-performing prompt components
- Add `analyze_prompt_effectiveness(prompt, outcome) -> Dict`
- Store analysis in `prompt_performance_log.json`

**Acceptance Criteria:**
- After 20+ sessions, can identify top-3 prompt patterns
- Patterns include: specific instructions, context length, role definitions
- Integration with `GrindSession.get_prompt()` to prefer successful patterns

---

### Task 16.2: Automatic Prompt Template Refinement

**File:** `prompt_optimizer.py`
**Description:** Refine prompt templates based on performance data.

**Implementation:**
- Extend `optimize_prompt()` to:
  - Load prompt performance data
  - Identify underperforming sections
  - Generate improved variants using successful patterns
- Create `PromptRefiner` class with methods:
  - `identify_weak_sections(prompt, performance_data) -> List[str]`
  - `generate_improvements(weak_sections, successful_patterns) -> List[str]`
  - `validate_improvement(original, improved) -> bool`
- Add safety check: improvements must pass `safety_sanitize.py` validation

**Acceptance Criteria:**
- Refined prompts score >= original prompts on held-out tasks
- Refinement process logged for transparency
- Safety sanitization prevents malicious prompt injection

---

### Task 16.3: Skill Extraction Quality Scoring

**File:** `skill_extractor.py`
**Description:** Score extracted skills for reusability and correctness.

**Implementation:**
- Extend `extract_skill_from_session()` to compute:
  - `generalizability_score`: Can skill apply to other tasks?
  - `correctness_score`: Does skill produce correct outputs?
  - `complexity_score`: Is skill appropriately scoped?
- Create `SkillQualityScorer` class with weighted scoring
- Only auto-register skills with aggregate score >= 0.75

**Acceptance Criteria:**
- Skill quality scores are logged with each extraction
- Low-quality skills are flagged for manual review
- Skill registry shows quality distribution

---

### Task 16.4: Skill Usage Tracking and Refinement

**File:** `skills/skill_registry.py`
**Description:** Track skill usage and refine based on outcomes.

**Implementation:**
- Add `track_skill_usage(skill_name, task, outcome)` method
- Store usage history with outcomes in skill metadata
- Implement `refine_skill(skill_name)` that:
  - Analyzes usage patterns
  - Identifies failure modes
  - Updates preconditions/postconditions based on actual usage
- Create `deprecate_skill(skill_name, reason)` for underperforming skills

**Acceptance Criteria:**
- Skills have usage count and success rate visible
- Skills with <50% success rate flagged for refinement
- Deprecated skills moved to `skills_archive/` with reason

---

### Task 16.5: Learning Rate Adaptation

**File:** `memory_synthesis.py`
**Description:** Adapt how aggressively the system incorporates new learnings.

**Implementation:**
- Add `AdaptiveLearningRate` class:
  - High learning rate when outcomes are consistent (fast adaptation)
  - Low learning rate when outcomes are noisy (cautious adaptation)
  - Compute rate from recent `quality_score` variance
- Integrate with `synthesize()` to weight new reflections by learning rate
- Add `learning_rate_log.json` for transparency

**Acceptance Criteria:**
- Learning rate auto-adjusts based on outcome consistency
- During unstable periods, system is conservative with new learnings
- Rate history is logged and queryable

---

### Task 16.6: Self-Verification Enhancement

**File:** `grind_spawner.py` (function `verify_grind_completion`)
**Description:** Improve self-verification to reduce false positives/negatives.

**Implementation:**
- Extend `verify_grind_completion()` to:
  - Check actual file changes against expected changes
  - Verify test execution results if tests were run
  - Validate code syntax if code was generated
- Create `VerificationRule` class for custom verification logic
- Add domain-specific rules (e.g., "refactor" tasks must not change behavior)

**Acceptance Criteria:**
- False positive rate (claiming success when failed) < 5%
- False negative rate (claiming failure when succeeded) < 5%
- Verification rules are extensible via config

---

### Task 16.7: Feedback Loop Visualization

**File:** Create `feedback_visualizer.py`
**Description:** Generate visual reports of self-improvement progress.

**Implementation:**
- Create `FeedbackVisualizer` class that generates:
  - Prompt quality trend chart (over time)
  - Skill registry growth chart
  - Learning rate history chart
  - Error category distribution
- Output as HTML report in `reports/feedback_report.html`
- Add CLI command `python feedback_visualizer.py --generate`

**Acceptance Criteria:**
- Report shows clear trends over 7+ days of operation
- Charts are readable and informative
- Report includes actionable insights summary

---

### Task 16.8: Safety-Constrained Self-Modification Boundaries

**File:** `safety_gateway.py`
**Description:** Ensure self-improvement never violates safety constraints.

**Implementation:**
- Create `SelfImprovementGuard` class:
  - Whitelist of files that can be modified by self-improvement
  - Blacklist of operations (no modifying safety modules themselves)
  - Rate limits on self-modifications per hour
- Integrate guard checks before any self-modification operation
- Add audit trail in `self_improvement_audit.jsonl`

**Acceptance Criteria:**
- Self-improvement cannot modify: `safety_*.py`, `SAFETY_CONSTRAINTS.json`
- Rate limit: max 10 self-modifications per hour
- All self-modifications logged with before/after diffs

---

## Wave 17: Robustness

**Objective:** Build resilience against errors, failures, and edge cases through recovery patterns and graceful degradation.

**Foundation Files:**
- `failure_patterns.py` - Failure pattern detection
- `safety_killswitch.py` - Circuit breaker implementation
- `safety_audit.py` - Anomaly detection
- `grind_spawner.py` - Error categorization (`_categorize_error`)

### Task 17.1: Error Recovery Strategy Library

**File:** Create `error_recovery.py`
**Description:** Implement recovery strategies for common error types.

**Implementation:**
- Create `RecoveryStrategy` base class with:
  - `can_handle(error_type, context) -> bool`
  - `execute_recovery(error_type, context) -> RecoveryResult`
- Implement strategies for each error category (from `_categorize_error`):
  - `TimeoutRecoveryStrategy`: Reduce complexity, increase timeout, split task
  - `EncodingRecoveryStrategy`: Force UTF-8, strip non-ASCII
  - `ImportRecoveryStrategy`: Install missing packages, suggest alternatives
  - `SyntaxRecoveryStrategy`: Run linter, auto-fix common issues
  - `RuntimeRecoveryStrategy`: Add try/except, reduce scope
- Create `RecoveryOrchestrator` that selects and applies strategies

**Acceptance Criteria:**
- Each error type has at least one recovery strategy
- Recovery success rate logged for learning
- Failed recoveries escalate to circuit breaker

---

### Task 17.2: Graceful Degradation Modes

**File:** Create `degradation_modes.py`
**Description:** Define degraded operation modes when resources are constrained.

**Implementation:**
- Create `DegradationMode` enum:
  - `FULL`: All features enabled
  - `REDUCED`: Skip expensive operations (multi-path, deep KG queries)
  - `MINIMAL`: Core execution only (no learning, no synthesis)
  - `SAFE_STOP`: Complete current task, then halt
- Implement `DegradationController` that:
  - Monitors resource usage (memory, API calls, cost)
  - Triggers degradation when thresholds exceeded
  - Restores full mode when resources recover
- Integrate with `grind_spawner.py` to respect degradation mode

**Acceptance Criteria:**
- System can operate in REDUCED mode indefinitely
- MINIMAL mode handles 10x normal error rate
- Mode transitions are logged and gradual

---

### Task 17.3: Checkpoint and Resume System

**File:** Create `checkpoint_manager.py`
**Description:** Enable task resumption after interruption.

**Implementation:**
- Create `CheckpointManager` class:
  - `create_checkpoint(session_id, state) -> checkpoint_id`
  - `load_checkpoint(checkpoint_id) -> state`
  - `list_checkpoints(session_id) -> List[checkpoint_id]`
- Store checkpoints in `checkpoints/` directory
- Integrate with `GrindSession` to:
  - Create checkpoint every 5 turns
  - Resume from latest checkpoint on restart
- Add `--resume` flag to `grind_spawner.py`

**Acceptance Criteria:**
- Sessions can resume from checkpoint within 30 seconds
- Checkpoint files are under 1MB each
- Resume maintains task context and partial results

---

### Task 17.4: Circuit Breaker Enhancements

**File:** `safety_killswitch.py`
**Description:** Enhance `CircuitBreaker` with smarter trip conditions.

**Implementation:**
- Add new trip conditions:
  - `trip_on_pattern_frequency`: Same error 3x in 5 minutes
  - `trip_on_resource_exhaustion`: Memory > 90%, disk > 95%
  - `trip_on_anomaly_detection`: Integration with `detect_anomalies()` from `safety_audit.py`
- Implement `HalfOpenState` for gradual recovery:
  - After cooldown, allow 1 test request
  - If successful, reset; if failed, re-trip
- Add `get_trip_history() -> List[TripEvent]` for analysis

**Acceptance Criteria:**
- Circuit breaker catches resource exhaustion before crash
- Half-open state prevents full outages from single failures
- Trip history enables post-mortem analysis

---

### Task 17.5: Failure Pattern Prediction

**File:** `failure_patterns.py`
**Description:** Predict likely failures before they occur.

**Implementation:**
- Extend `FailurePatternDetector` with:
  - `predict_failure_risk(task, context) -> float`
  - Use historical failure data to train simple classifier
  - Features: task complexity, task type, recent error rate
- Create `PredictiveGuard` that:
  - Runs prediction before task execution
  - Warns if risk > 0.7
  - Suggests mitigation strategies
- Integrate with `GrindSession.run_once()` pre-execution

**Acceptance Criteria:**
- Prediction accuracy > 70% on validation set
- High-risk tasks receive extra validation steps
- Prediction model updates online with new data

---

### Task 17.6: Timeout Adaptation

**File:** `grind_spawner.py`
**Description:** Dynamically adjust timeouts based on task characteristics.

**Implementation:**
- Create `TimeoutCalculator` class:
  - Base timeout: 600s (current)
  - Adjust by complexity score: +300s for complexity > 0.8
  - Adjust by task type: +180s for "refactor", -60s for "fix typo"
  - Cap at 1200s maximum
- Integrate with `GrindSession.run_once()` subprocess timeout
- Log timeout decisions for learning

**Acceptance Criteria:**
- Timeout-related failures reduced by 30%
- Complex tasks get appropriate time allocation
- Simple tasks complete faster (don't waste timeout)

---

### Task 17.7: Error Message Enhancement

**File:** `grind_spawner.py`
**Description:** Provide actionable error messages with recovery suggestions.

**Implementation:**
- Create `ErrorEnhancer` class:
  - Parse raw error messages
  - Map to known error patterns
  - Generate actionable suggestions
- Integrate with `_categorize_error()` to enhance all logged errors
- Store enhanced errors in session logs

**Acceptance Criteria:**
- 80% of errors have specific recovery suggestions
- Suggestions are accurate and actionable
- Error messages include relevant documentation links (local)

---

### Task 17.8: Health Check System

**File:** Create `health_check.py`
**Description:** Continuous health monitoring for early problem detection.

**Implementation:**
- Create `HealthChecker` class:
  - `check_system_health() -> HealthReport`
  - `check_component_health(component) -> ComponentHealth`
  - Components: knowledge_graph, skill_registry, lesson_store, sandbox
- Implement health indicators:
  - Knowledge graph: node count, edge consistency
  - Skill registry: skill count, average quality
  - Lesson store: lesson count, recency
  - Sandbox: audit log size, blocked operation count
- Create `/health` endpoint for external monitoring (localhost only)

**Acceptance Criteria:**
- Health check runs every 60 seconds
- Unhealthy components trigger alerts
- Health history stored for trend analysis

---

## Wave 18+: Future Possibilities

**Objective:** Explore advanced capabilities that compound learning enables, while strictly adhering to safety constraints.

### Wave 18: Collaborative Learning

**18.1: Worker Specialization**
- Workers develop expertise in specific task types
- Route tasks to best-suited workers based on history
- File: Create `worker_specialization.py`

**18.2: Knowledge Sharing Between Sessions**
- Share insights across concurrent sessions via `message_pool.py`
- Implement conflict resolution for contradictory learnings
- File: Extend `message_pool.py`

**18.3: Collective Memory Consolidation**
- Nightly synthesis of all worker learnings
- Generate "collective wisdom" reflections
- File: Extend `memory_synthesis.py`

---

### Wave 19: Meta-Learning

**19.1: Learning-to-Learn Patterns**
- Track which learning strategies work best
- Adapt synthesis parameters based on meta-performance
- File: Create `meta_learning.py`

**19.2: Strategy Evolution**
- Automatically generate new execution strategies
- A/B test against existing strategies
- File: Extend `path_ab_testing.py`

**19.3: Complexity Prediction Improvement**
- Learn better complexity estimation from outcomes
- Refine `decompose_task()` based on actual execution time
- File: Extend `roles.py`

---

### Wave 20: Domain Adaptation

**20.1: Task Domain Classification**
- Classify tasks into domains (web, data, testing, etc.)
- Domain-specific prompts and skills
- File: Create `domain_classifier.py`

**20.2: Domain-Specific Knowledge Graphs**
- Separate KG subgraphs per domain
- Cross-domain insight transfer
- File: Extend `knowledge_graph.py`

**20.3: Domain Expert Roles**
- New roles for specific domains
- Expert knowledge injection
- File: Extend `roles.py`

---

### Wave 21: Explanation and Transparency

**21.1: Decision Explanation System**
- Explain why specific paths/strategies were chosen
- Trace decisions back to learned lessons
- File: Create `explanation_engine.py`

**21.2: Audit Report Generation**
- Weekly summary of all operations
- Highlight safety events and learnings
- File: Extend `safety_audit.py`

**21.3: User Feedback Integration**
- Accept user corrections on quality scores
- Learn from human feedback (local only)
- File: Create `feedback_collector.py`

---

## Safety Invariants (All Waves)

Per `SAFETY_CONSTRAINTS.json`, ALL future waves MUST maintain:

1. **Network Isolation**
   - Only localhost (127.0.0.1) allowed
   - No external API calls
   - GitHub push only when explicitly requested by user

2. **Workspace Containment**
   - All file operations within workspace directory
   - No system-level configuration changes
   - No credential/secret storage

3. **Autonomy Limits**
   - No self-replication to external systems
   - No persistence beyond local workspace
   - All operations require implicit or explicit user consent

4. **Pre-Execution Validation**
   - Every task passes through `SafetyGateway.pre_execute_safety_check()`
   - Constitutional checks enforced
   - Prompt sanitization required

---

## Implementation Priority

| Wave | Priority | Dependencies | Est. Effort |
|------|----------|--------------|-------------|
| 15.1-15.3 | High | Wave 14 complete | 2 days |
| 15.4-15.8 | Medium | 15.1-15.3 | 3 days |
| 16.1-16.4 | High | Wave 15 stable | 3 days |
| 16.5-16.8 | Medium | 16.1-16.4 | 2 days |
| 17.1-17.4 | High | Wave 14 complete | 3 days |
| 17.5-17.8 | Medium | 17.1-17.4 | 2 days |
| 18+ | Low | Waves 15-17 stable | Ongoing |

---

## Change Log

- **2026-02-03:** Initial roadmap created covering Waves 15-18+
