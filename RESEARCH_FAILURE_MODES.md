# Failure Modes and Recovery Patterns Research

**Research Date:** 2026-02-03
**Scope:** Analysis of failure handling in claude_parasite_brain_suck codebase
**Status:** Research Only - No Code Modifications

---

## Executive Summary

This codebase implements a sophisticated multi-layered failure handling system that spans from low-level error categorization to high-level learning from failures. The architecture demonstrates several advanced patterns from recent AI research (LATS, Voyager, Generative Agents, CAMEL) applied to failure recovery.

**Key Findings:**
- 6 distinct failure categories with structured tracking
- 4 automatic synthesis triggers based on failure events
- Multi-path execution for strategy diversification
- Circuit breaker and kill switch for cascade prevention
- Pattern-based failure prediction using historical data

---

## 1. Current Failure Handling

### 1.1 Failures Caught

The system catches and categorizes the following failure types:

| Category | Detection Method | Example Triggers |
|----------|-----------------|------------------|
| **TIMEOUT** | `subprocess.TimeoutExpired` | Session exceeds 600s limit |
| **ENCODING** | Keyword matching: "encoding", "charset", "utf", "decode", "unicode" | Unicode errors, charset mismatches |
| **IMPORT** | Keyword matching: "import", "module not found", "modulenotfounderror" | Missing dependencies |
| **SYNTAX** | Keyword matching: "syntax", "syntaxerror", "invalid syntax" | Python syntax errors |
| **RUNTIME** | Keyword matching: "error", "exception", "traceback", "failed" | General execution failures |
| **UNKNOWN** | Fallback category | Uncategorized errors |

**Implementation Location:** `grind_spawner.py:245-268` - `_categorize_error()` method

```python
def _categorize_error(self, error_type: str, error_message: str, stdout: str = "", stderr: str = "") -> str:
    """Categorize error into one of: TIMEOUT, ENCODING, IMPORT, SYNTAX, RUNTIME, UNKNOWN."""
```

### 1.2 Error Categorization Flow

```
Exception Raised
       |
       v
+------------------+
|  error_type ==   |---> Yes ---> Return "TIMEOUT"
|  "timeout"?      |
+------------------+
       | No
       v
+------------------+
| Contains encoding|---> Yes ---> Return "ENCODING"
| keywords?        |
+------------------+
       | No
       v
+------------------+
| Contains import  |---> Yes ---> Return "IMPORT"
| keywords?        |
+------------------+
       | No
       v
... (continues through categories)
       |
       v
Return "UNKNOWN"
```

### 1.3 Current Recovery Strategy

**Retry Logic in GrindSession.run_once():**
1. **Technical Retry** (max 2 attempts): On non-zero exit code, retry with same prompt
2. **Critic-Driven Retry** (max 2 attempts): If quality_score < 0.7, inject feedback and retry
3. **Failure Recording**: All failures tracked in `failure_patterns.json` for future avoidance

**Code Location:** `grind_spawner.py:419-684`

```
max_retries = 2
attempt = 0
critic_retry_count = 0

while attempt <= max_retries:
    result = subprocess.run(cmd, ...)

    if result.returncode != 0 and attempt < max_retries:
        time.sleep(3)
        attempt += 1
        continue

    if critic_quality_score < 0.7 and critic_retry_count < 2:
        # Inject improvement feedback
        current_prompt = prompt + critic_feedback_injection
        critic_retry_count += 1
        attempt += 1
        continue
```

---

## 2. Failure Taxonomy

### 2.1 Infrastructure Failures

| Failure Type | Detection | Current Handling | Gap Analysis |
|--------------|-----------|------------------|--------------|
| **API Timeout** | `subprocess.TimeoutExpired` | Catch, categorize as TIMEOUT, record pattern | No exponential backoff |
| **API Rate Limit** | Not explicitly detected | Falls to RUNTIME category | Could detect 429 responses |
| **Network Failure** | `NetworkGuard` in safety_gateway.py | Pre-execution scan for network patterns | Reactive not proactive |
| **Disk Full** | Not explicitly detected | Falls to RUNTIME or UNKNOWN | No disk space pre-check |
| **JSON Corruption** | `json.JSONDecodeError` in load functions | Return empty list, log warning | Some locations unprotected |

**Error Handling Audit Results:**
- 13 locations need additional error handling (see `error_handling_report.md`)
- 52% coverage (14/27 critical points have proper handling)

### 2.2 Logic Failures

| Failure Type | Detection | Current Handling |
|--------------|-----------|------------------|
| **Wrong Output** | `verify_grind_completion()` | Self-verification step checks for success indicators |
| **Hallucination** | CriticAgent checks | Pattern matching against codebase conventions |
| **Incomplete Implementation** | Critic `_check_logic()` | Detects empty functions with pass/... |
| **Hardcoded Values** | Critic check | Flags URLs/IPs that should be config |

**Self-Verification Implementation:**
```python
def verify_grind_completion(session_id, run_num, output, returncode):
    """
    Checks for success indicators:
    - Exit code == 0
    - Keywords: "done", "complete", "success", "finished", "created", "modified"
    - files_modified field in output JSON
    """
```

### 2.3 Integration Failures (Interface Mismatch)

**Current Detection:** Limited
- Critic checks for missing imports
- Pattern matching for logger/pathlib conventions

**Gap Analysis:**
- No type checking for function signatures
- No contract validation between components
- No schema validation for JSON messages
- No interface version tracking

**Example from Recent Test Failures:**
```
TestShowStatus.test_displays_summary:
- Expected: "Total tasks: 4"
- Actual: "Total Tasks:      4" (different formatting)
```

This represents a classic integration failure where the interface contract changed but consumers were not updated.

### 2.4 Cascade Failures

**Prevention Mechanisms:**

1. **Circuit Breaker** (`safety_killswitch.py:163-284`)
   - Cost threshold: $100.00 (configurable)
   - Failure threshold: 5 consecutive failures
   - Time window: 300 seconds for failure rate
   - Suspicious pattern detection (rm -rf, DROP DATABASE, etc.)

2. **Kill Switch** (`safety_killswitch.py:13-161`)
   - Global halt via HALT file
   - Pause/resume via PAUSE file
   - File-based coordination across processes

3. **Safety Gateway** (`safety_gateway.py`)
   - Fail-closed architecture
   - Constitutional checker
   - Workspace sandbox
   - Network guard
   - Prompt sanitizer

**Cascade Flow:**
```
Single Failure
      |
      v
+---------------------+
| Circuit Breaker     |---> Threshold exceeded ---> TRIP
| record_failure()    |
+---------------------+
      |
      v
+---------------------+
| grind_loop checks   |---> Tripped ---> STOP LOOP
| get_circuit_breaker()|
+---------------------+
      |
      v
All workers receive
circuit breaker status
via polling
```

---

## 3. Recovery Strategies

### 3.1 Retry with Same Approach

**Implementation:** `grind_spawner.py:447-452`
```python
if result.returncode != 0 and attempt < max_retries:
    print(f"... failed ... retrying... (attempt {attempt + 1}/{max_retries})")
    time.sleep(3)  # 3 second delay
    attempt += 1
    current_prompt = prompt  # Reset to original
    continue
```

**Characteristics:**
- Fixed retry count (2)
- Fixed delay (3 seconds)
- No backoff strategy
- Prompt reset to original

### 3.2 Retry with Different Approach

**Critic Feedback Loop:** `grind_spawner.py:529-556`
```python
if critic_quality_score < 0.7 and critic_retry_count < 2:
    improvement_suggestions = "\n".join(critic_review.get('feedback', []))

    critic_feedback_injection = f"""
    CRITIC FEEDBACK FOR ITERATIVE IMPROVEMENT (TextGrad)
    Previous attempt received quality score: {critic_quality_score:.2f}

    REQUIRED IMPROVEMENTS:
    {improvement_suggestions}
    """
    current_prompt = prompt + critic_feedback_injection
    critic_retry_count += 1
```

**Multi-Path Execution:** `multi_path_executor.py`
- CONSERVATIVE: 30% budget, proven approaches
- BALANCED: 50% budget, standard practices
- AGGRESSIVE: 20% budget, experimental approaches

```python
def execute_paths_parallel(self, task, executor_func):
    """Execute all paths in parallel and return best result."""
    paths = self.generate_path_variants(task)  # 3 strategies

    with ThreadPoolExecutor(max_workers=len(paths)) as executor:
        futures = {executor.submit(...): path for path in paths}
        for future in as_completed(futures):
            path = future.result()
            completed_paths.append(path)

    best_path = max(completed_paths, key=lambda p: p.quality_score)
```

### 3.3 Graceful Degradation

**Cost-Based Degradation:**
```python
if self.max_total_cost:
    total_spent = get_total_spent()
    if total_spent >= self.max_total_cost:
        print(f"WARNING: Total cost reached max")
        self.running = False
        circuit_breaker.check_cost(total_spent)
        break
```

**Model Adaptation Based on Complexity:**
```python
def adapt_model_for_complexity(base_model, complexity_score):
    if complexity_score >= 0.85:
        return "opus"
    elif complexity_score >= 0.65:
        return "opus"
    elif complexity_score >= 0.35:
        return "sonnet" if base_model == "haiku" else base_model
    return base_model
```

### 3.4 Human Escalation

**Current Mechanisms:**
1. **Kill Switch Files:** Human creates HALT or PAUSE file
2. **Audit Logging:** All safety decisions logged to `safety_audit.log`
3. **Console Output:** Warnings printed for human observation

**Missing:**
- No automated alerting system
- No notification mechanism for critical failures
- No escalation thresholds defined

---

## 4. Learning from Failures

### 4.1 Failure to Lesson Extraction

**FailurePatternDetector** (`failure_patterns.py`):

```python
def track_failure(
    self,
    task_description: str,
    error_type: str,
    error_message: str,
    task_characteristics: Dict[str, Any],
    attempted_approaches: List[str],
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Record a task failure with complete context."""

    record = {
        "id": failure_id,
        "timestamp": datetime.now().isoformat(),
        "task_description": task_description,
        "error_type": error_type,
        "error_message": error_message,
        "task_characteristics": task_characteristics,
        "attempted_approaches": attempted_approaches,
        "context": context or {},
    }
```

**Automatic Lesson Recording Triggers:**
```
TRIGGER 1: After every N sessions (default: 5)
TRIGGER 2: After any failure (immediate)
TRIGGER 3: When lesson count exceeds 50
TRIGGER 4: When importance_sum > 150 (Generative Agents threshold)
```

### 4.2 Pattern Detection for Prevention

**Similarity Matching:** `failure_patterns.py:117-202`
```python
def check_failure_patterns(
    self,
    task_description: str,
    task_characteristics: Optional[Dict[str, Any]] = None,
    similarity_threshold: float = 0.6,
    top_n: int = 3
) -> Dict[str, Any]:
    """Check if a task is similar to past failures."""

    # Score each past failure
    for failure in self.failures:
        text_sim = self._compute_task_similarity(task_description, failure["task_description"])
        char_overlap = self._check_characteristic_overlap(...)
        combined_score = (text_sim * 0.7) + (min(char_overlap / 3, 1.0) * 0.3)
```

**Warning Levels:**
- HIGH: similarity >= 0.85
- MEDIUM: similarity >= 0.75
- LOW: similarity >= 0.60

**Warning Injection:**
```python
failure_warning = self.failure_detector.generate_warning_prompt(
    self.task,
    task_characteristics={...}
)
if failure_warning:
    print(f"[Session {self.session_id}] Failure pattern warning injected")
```

### 4.3 Root Cause Analysis Automation

**Error Statistics Reporting:**
```python
def report_error_statistics() -> None:
    categories = count_error_categories()
    print(f"Total failures: {categories['total_failures']}")
    for cat in ["TIMEOUT", "ENCODING", "IMPORT", "SYNTAX", "RUNTIME", "UNKNOWN"]:
        count = categories[cat]
        if count > 0:
            pct = (count / categories["total_failures"]) * 100
            print(f"{cat}: {count} ({pct:.1f}%)")
```

**Knowledge Graph Recovery Queries:**
```python
def query_knowledge_graph_for_recovery(error_type: str, task_description: str, kg: KnowledgeGraph):
    """Query knowledge graph for recovery strategies when stuck."""

    error_node_id = f"error_{error_type.lower()}"
    related_subgraph = kg.query_related(error_node_id, depth=2)

    return {
        "related_concepts": [...],
        "recovery_strategies": [...],
        "similar_lessons": [...]
    }
```

---

## 5. Gap Analysis and Recommendations

### 5.1 Current Strengths

1. **Rich failure categorization** with 6 semantic categories
2. **Proactive failure prevention** via pattern matching on historical failures
3. **Multi-path exploration** reduces single-point-of-failure risk
4. **Circuit breaker pattern** prevents cascading failures
5. **Learning from failures** via automatic synthesis triggers

### 5.2 Identified Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| No exponential backoff | API rate limit violations | HIGH |
| Missing disk space checks | Silent failures on full disk | MEDIUM |
| No interface contract validation | Integration failures | HIGH |
| Limited alerting/notification | Delayed human response | MEDIUM |
| No structured retry policies | Inconsistent recovery behavior | MEDIUM |
| 52% error handling coverage | Potential crashes | HIGH |

### 5.3 Failure Recovery Pattern Matrix

| Failure Type | Current Recovery | Recommended Enhancement |
|--------------|------------------|------------------------|
| TIMEOUT | Retry once, record | Add timeout prediction, scale timeout based on complexity |
| ENCODING | Record, continue | Add encoding detection pre-flight |
| IMPORT | Record, continue | Add dependency resolution retry |
| SYNTAX | Record, continue | Add syntax pre-validation |
| RUNTIME | Retry 2x, critic feedback | Add contextual recovery strategies |
| UNKNOWN | Record, continue | Improve classification granularity |

---

## 6. Architecture Diagram

```
+------------------------------------------------------------------+
|                     FAILURE HANDLING ARCHITECTURE                 |
+------------------------------------------------------------------+

                        +-------------------+
                        |   Task Input      |
                        +-------------------+
                                |
                                v
+------------------------------------------------------------------+
|                    PRE-EXECUTION SAFETY                          |
|  +------------------+  +------------------+  +-----------------+ |
|  | Constitutional   |  | Workspace        |  | Network Guard   | |
|  | Checker          |  | Sandbox          |  |                 | |
|  +------------------+  +------------------+  +-----------------+ |
|  +------------------+  +------------------+                      |
|  | Prompt           |  | Failure Pattern  |                      |
|  | Sanitizer        |  | Detector         |                      |
|  +------------------+  +------------------+                      |
+------------------------------------------------------------------+
                                |
                        PASS    |    FAIL
                    +-----------+------------+
                    |                        |
                    v                        v
          +------------------+      +------------------+
          | Execute Task     |      | Block & Log      |
          +------------------+      +------------------+
                    |
                    v
          +------------------+
          | Check Result     |
          +------------------+
                    |
        +-----------+-----------+
        |           |           |
     SUCCESS     FAILURE    CRITIC<0.7
        |           |           |
        v           v           v
+-------------+ +---------+ +------------+
| Verify      | | Retry   | | Feedback   |
| Completion  | | (max 2) | | Retry      |
+-------------+ +---------+ +------------+
        |           |           |
        v           v           v
+------------------------------------------------------------------+
|                    POST-EXECUTION LEARNING                        |
|  +------------------+  +------------------+  +-----------------+ |
|  | Track Failure    |  | Record Lesson    |  | Update KG       | |
|  | Pattern          |  |                  |  |                 | |
|  +------------------+  +------------------+  +-----------------+ |
|  +------------------+  +------------------+                      |
|  | Circuit Breaker  |  | Memory           |                      |
|  | Update           |  | Synthesis        |                      |
|  +------------------+  +------------------+                      |
+------------------------------------------------------------------+
                                |
                                v
                    +-------------------+
                    | Next Session      |
                    +-------------------+
```

---

## 7. Research References

The codebase implements patterns from these papers:

1. **LATS** (arXiv:2310.04406) - Language Agent Tree Search
   - Multi-path exploration
   - Quality-based path selection
   - Critic feedback loops

2. **Voyager** (arXiv:2305.16291) - Open-Ended Embodied Agent
   - Skill library and retrieval
   - Self-verification after task completion
   - Compositional skill reuse

3. **Generative Agents** (arXiv:2304.03442) - Interactive Simulacra
   - Memory synthesis triggers
   - Importance-based reflection
   - Temporal memory pruning

4. **CAMEL** (arXiv:2303.17760) - Communicative Agents
   - Role-based task decomposition
   - Inception prompting
   - Cooperative agent patterns

5. **TextGrad** (arXiv:2406.14762)
   - Gradient of quality scores
   - Iterative refinement via feedback

---

## 8. Conclusion

The failure handling system demonstrates sophisticated patterns but has room for improvement:

**Strong Points:**
- Comprehensive failure taxonomy
- Proactive failure pattern detection
- Multi-layered safety architecture
- Learning-enabled recovery

**Areas for Enhancement:**
- Complete the 48% gap in error handling coverage
- Add exponential backoff for transient failures
- Implement interface contract validation
- Add automated alerting for critical failures
- Formalize retry policies per failure type

The system's architecture allows for incremental improvement without major structural changes.
