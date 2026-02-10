# Prompt Engineering Research for AI Agents

This document analyzes prompt engineering patterns used in this codebase and explores research-backed techniques for improving AI agent performance.

---

## Table of Contents

1. [Current Prompt Patterns](#1-current-prompt-patterns)
2. [Prompt Optimization Research](#2-prompt-optimization-research)
3. [Dynamic Prompt Construction](#3-dynamic-prompt-construction)
4. [Prompt Evaluation](#4-prompt-evaluation)
5. [Research References](#5-research-references)

---

## 1. Current Prompt Patterns

### 1.1 Base Template Structure

The codebase uses a layered prompt construction approach defined in `grind_spawner.py`:

```
GRIND_PROMPT_TEMPLATE = """You are an EXECUTION worker. Follow instructions EXACTLY.

WORKSPACE: {workspace}

TASK (execute step by step):
{task}

RULES:
1. Follow the steps EXACTLY as written - no improvisation
2. Be FAST - don't over-explain, just do the work
3. If a step says "edit file X", edit it. If it says "create file Y", create it.
4. No lengthy analysis - the planning was already done
5. When done, output a 2-3 sentence summary

EXECUTE NOW.
"""
```

**Key Observations:**
- **Directive framing**: Opens with explicit role assignment ("You are an EXECUTION worker")
- **Parameter injection**: Uses Python string formatting for `{workspace}` and `{task}`
- **Numbered rules**: Provides explicit behavioral constraints
- **Action orientation**: Ends with imperative "EXECUTE NOW" to reduce verbosity

### 1.2 Role Injection via CAMEL Framework

The `roles.py` module implements CAMEL (Communicative Agents for AI Language Model Exploration) role-playing architecture (arXiv:2303.17760):

**Role Definitions:**
| Role | Description | Allowed Tools |
|------|-------------|---------------|
| PLANNER | Break complex tasks into atomic subtasks | task_analysis, decomposition, json_output |
| CODER | Implement code changes according to specifications | file_read, file_edit, bash_execute, test_run |
| REVIEWER | Validate code against requirements and quality standards | code_review, test_validate, quality_check |
| DOCUMENTER | Update documentation and record lessons learned | json_read, json_write, documentation_update |

**Inception Prompting Pattern:**
```
"You are the {ROLE}. Your job is to {DESCRIPTION}.
The PLANNER has assigned you: {subtask}
When done, hand off to {NEXT_ROLE} with:
- Summary of what you completed
- Any blockers or issues encountered
- Ready-to-review artifacts"
```

This creates a chain-of-responsibility where each role knows:
1. Its specific responsibilities
2. What task it should accomplish
3. Who receives its output next

### 1.3 Context Building Strategy

The `ContextBuilder` class (`context_builder.py`) implements a unified retrieval interface that assembles context from multiple sources:

**Context Assembly Order:**
1. **CAMEL role injection** - Role definition and inception prompt
2. **Unified context block**:
   - Skills (from Voyager skill library)
   - Lessons (from learned_lessons.json)
   - Knowledge graph context
3. **Failure warning injection** - If similar tasks have failed before
4. **DSPy few-shot examples** - Top demonstrations from successful runs
5. **Review gate injection** - Mandatory reviewer validation requirements

**Fluent API Pattern:**
```python
context_builder = ContextBuilder(workspace)
unified_context = context_builder \
    .add_skills(task, top_k=3) \
    .add_lessons(task, top_k=3) \
    .add_kg_context(task, depth=2) \
    .build(log_injection=True)
```

This modular approach enables selective context injection based on task requirements.

---

## 2. Prompt Optimization Research

### 2.1 DSPy Patterns (arXiv:2310.03714)

The codebase implements DSPy-inspired prompt optimization through `prompt_optimizer.py` and `dspy_modules.py`.

**Core DSPy Concepts:**

1. **Signatures**: Declarative input/output specifications
   ```python
   class GrindSignature(dspy.Signature):
       task: str = dspy.InputField(desc="The task to execute")
       context: str = dspy.InputField(desc="Workspace context")
       solution: str = dspy.OutputField(desc="The implemented solution")
       summary: str = dspy.OutputField(desc="2-3 sentence summary")
   ```

2. **Modules**: Composable units with learnable components
   ```python
   class GrindModule(dspy.Module):
       def __init__(self):
           self.planner = dspy.ChainOfThought(PlanningSignature)
           self.executor = dspy.Predict(GrindSignature)
   ```

3. **Teleprompters**: Bootstrap demonstrations automatically
   - Collect successful completions from `grind_logs/`
   - Rank by efficiency metrics (num_turns, duration_ms)
   - Inject top 2-3 examples into prompts

**Expected Improvement:** 25-65% over standard few-shot prompting (per DSPy paper)

### 2.2 Few-Shot vs Zero-Shot

The codebase uses a **hybrid approach**:

| Mode | When Used | Implementation |
|------|-----------|----------------|
| Zero-shot | No demonstrations available | Base `GRIND_PROMPT_TEMPLATE` only |
| Few-shot | Demonstrations exist in `grind_logs/` | `optimize_prompt()` injects examples |
| Self-bootstrapping | After each successful run | `_update_prompt_optimizer_online()` adds new demos |

**Demonstration Selection Strategy:**
```python
def get_relevant_demonstrations(task, demonstrations, top_k=3):
    # Load from file first (enables bootstrap across sessions)
    persisted_demos = load_demonstrations()
    # Simple approach: return top-k by efficiency
    return demonstrations[:top_k]
```

**Efficiency Score Calculation:**
```python
# Lower num_turns = higher score
# 4 turns = perfect (100%), 20 turns = worst (10%)
efficiency_score = max(0.1, 1.0 - (num_turns - 4) / 20.0)
```

### 2.3 Chain-of-Thought Variations

The codebase implements several CoT variants:

**1. Planning Chain-of-Thought:**
```python
# In GrindModule.forward()
plan_result = self.planner(task=task)  # ChainOfThought
execution_steps = plan_result.execution_steps
enhanced_context = f"{context}\n\nPlanned steps:\n{execution_steps}"
```

**2. Role-Based Chain:**
```
PLANNER (decompose) -> CODER (implement) -> REVIEWER (validate) -> DOCUMENTER (record)
```

**3. Adaptive Complexity Chain:**
- Low complexity (score < 0.35): Skip PLANNER, go direct to CODER
- Medium/High complexity (score >= 0.35): Full chain with PLANNER

### 2.4 Self-Consistency

The codebase implements self-consistency through:

**1. Critic Review Loop (LATS/TextGrad pattern):**
```python
if critic_quality_score < 0.7 and critic_retry_count < 2:
    # Build enhanced prompt with critic feedback
    critic_feedback_injection = f"""
    CRITIC FEEDBACK FOR ITERATIVE IMPROVEMENT (TextGrad)
    Previous attempt received quality score: {critic_quality_score:.2f}
    REQUIRED IMPROVEMENTS: {improvement_suggestions}
    """
    current_prompt = prompt + critic_feedback_injection
    critic_retry_count += 1
    # Retry with enhanced prompt
```

**2. Self-Verification (Voyager pattern):**
```python
def verify_grind_completion(session_id, run_num, output, returncode):
    success_keywords = ["done", "complete", "success", "finished", ...]
    # Check for success indicators in output
    # Verify files were actually modified
    return {"verified": True/False, "indicators": [...], "details": "..."}
```

**3. Multi-Path Execution:**
- CONSERVATIVE strategy: Careful approach
- BALANCED strategy: Standard approach
- AGGRESSIVE strategy: Fast approach
- Compare quality scores, select best path

---

## 3. Dynamic Prompt Construction

### 3.1 Adapting Prompts to Task Type

**Complexity Detection (`roles.py`):**

The `decompose_task()` function analyzes multiple signals to score task complexity (0.0-1.0):

| Signal | Weight | Examples |
|--------|--------|----------|
| Word count | 0.0-0.3 | Longer tasks = more complex |
| High-complexity keywords | +0.15 each | "create", "implement", "design", "architecture" |
| Low-complexity keywords | -0.08 each | "fix", "update", "add", "change" |
| Complexity phrases | +0.12 each | "multiple", "integrate", "coordinate" |
| File references | +0.05 each | ".py", ".js", "file" mentions |
| Paper/architecture refs | +0.10 each | "arxiv", "algorithm", "pattern" |

**Threshold Classification:**
- score < 0.35: Simple task (direct to CODER)
- score >= 0.35: Complex task (requires PLANNER)

**Model Adaptation:**
```python
def adapt_model_for_complexity(base_model, complexity_score):
    if complexity_score >= 0.85: return "opus"      # Very complex
    elif complexity_score >= 0.65: return "opus"    # High complexity
    elif complexity_score >= 0.35:
        return "sonnet" if base_model == "haiku" else base_model
    return base_model  # Simple tasks keep base model
```

**Budget Adaptation:**
```python
def adapt_budget_for_complexity(base_budget, complexity_score):
    if complexity_score >= 0.85: return base_budget * 2.0
    elif complexity_score >= 0.65: return base_budget * 1.5
    elif complexity_score >= 0.35: return base_budget * 1.2
    return base_budget
```

### 3.2 Skill Injection Patterns

**Voyager Skill Library (`skill_registry.py`):**

Skills are retrieved by semantic matching and injected into prompts:

**Retrieval Strategy (priority order):**
1. TF-IDF embedding-based cosine similarity
2. Keyword matching fallback
3. Skill composition if no single match

**Injection Format:**
```
============================================================
VOYAGER SKILL INJECTION (arXiv:2305.16291)
============================================================

RELEVANT SKILL: {skill_name}

# {skill_description}
{skill_code}

============================================================
```

**Query Expansion for Better Matching (`query_expander.py`):**
```python
TECHNICAL_SYNONYMS = {
    "error": ["exception", "failure", "bug", "issue"],
    "fix": ["repair", "resolve", "correct", "patch"],
    "test": ["testing", "verification", "validation", "coverage"],
    ...
}
```

### 3.3 Lesson Injection Patterns

**Memory Synthesis (`memory_synthesis.py`):**

Lessons are retrieved using HippoRAG-style semantic retrieval:

**Relevance Score Formula:**
```
score = importance_weight * 0.4 + embedding_similarity * 0.6
```

**Injection Format:**
```
============================================================
LEARNED LESSONS CONTEXT
============================================================

Category: {lesson_category}
Lesson: {lesson_text}
Key Insights:
  - {insight_1}
  - {insight_2}
Source: {source_citation}

============================================================
```

**Importance Scoring (Generative Agents pattern):**
- LLM-based rating 1-10 (or heuristic proxy)
- Keywords: "critical", "security", "breakthrough" = high importance
- Keywords: "check", "list", "minor" = low importance

### 3.4 Failure Warning Injection

**Failure Pattern Detection (`failure_patterns.py`):**

When a task is similar to past failures, warnings are injected:

**Similarity Computation:**
```python
# Combined score (weighted average)
text_similarity = SequenceMatcher(task1, task2).ratio()
characteristic_overlap = count_matching_characteristics()
combined_score = (text_similarity * 0.7) + (characteristic_overlap * 0.3)
```

**Warning Level Thresholds:**
- >= 0.85: HIGH warning
- >= 0.75: MEDIUM warning
- >= similarity_threshold: LOW warning

**Injection Format:**
```
WARNING  FAILURE PATTERN WARNING WARNING
Warning Level: {HIGH/MEDIUM/LOW}

Similar tasks have failed previously:
  - {error_type}: {task_description}...

Suggested Avoidance Strategies:
  * Avoid these previously failed approaches: {approaches}
  * Watch for {most_common_error} - occurred in N similar task(s)
  * Review similar failure error messages before implementing
```

---

## 4. Prompt Evaluation

### 4.1 How to Know if a Prompt is Good

The codebase uses multiple evaluation signals:

**1. CriticAgent Quality Scoring (`critic.py`):**

| Check | Severity | What It Detects |
|-------|----------|-----------------|
| Error handling | warning | External API calls without try-except |
| Imports | info | Unused imports, missing required modules |
| Syntax | critical | Mismatched brackets/braces/parens |
| Patterns | warning/info | Inconsistent logger usage, os.path vs pathlib |
| Logic | warning | Empty functions, hardcoded config values |

**Scoring Formula:**
```python
score = 1.0
score -= critical_count * 0.15
score -= warning_count * 0.05
score -= info_count * 0.02
return max(0.0, min(1.0, score))
```

**Quality Score Interpretation:**
- 0.0-0.35: Critical issues - code will fail
- 0.35-0.65: Warnings - code may work but has issues
- 0.65-0.75: Passing but lower quality
- 0.75-1.0: High quality

**2. Self-Verification (`grind_spawner.py`):**
```python
# Task passes verification if:
# 1. returncode == 0 (successful execution), AND
# 2. Has success indicators OR files were modified
if returncode == 0 and (len(indicators) > 0 or files_modified):
    verified = True
```

**3. Performance Tracking (`performance_tracker.py`):**
- Rolling average quality scores over last N sessions
- Success rate percentage
- Improvement rate calculation:
  ```python
  improvement = ((current - baseline) / abs(baseline)) * 100.0
  ```

### 4.2 A/B Testing Prompts

The codebase implements A/B testing through **Multi-Path Execution** (`multi_path_executor.py`):

**Strategy Comparison:**
```python
# Budget allocation for parallel exploration
BALANCED = 50%
CONSERVATIVE = 30%
AGGRESSIVE = 20%
```

**Comparison Result Tracking:**
```json
{
  "strategy": "BALANCED",
  "quality_score": 0.85,
  "metadata": {
    "total_elapsed": 45.2,
    "paths_explored": 3
  },
  "all_paths": [
    {"strategy": "CONSERVATIVE", "quality_score": 0.82, "success": true},
    {"strategy": "BALANCED", "quality_score": 0.85, "success": true},
    {"strategy": "AGGRESSIVE", "quality_score": 0.78, "success": true}
  ]
}
```

**Path Preference Learning:**
- Track which strategies work best for which task types
- Build historical recommendations by complexity category
- Confidence scoring based on sample size:
  ```python
  confidence = min(1.0, sqrt(sample_size / 30.0))
  ```

### 4.3 Prompt Regression Testing

The codebase supports prompt regression detection through:

**1. Demonstration Quality Tracking:**
- Demonstrations stored with efficiency scores
- New demonstrations compared against existing top performers
- Keep only top 20 demonstrations sorted by efficiency

**2. Lesson Synthesis for Pattern Detection:**
```python
# When multiple similar lessons exist, synthesize into reflections
if len(high_importance_lessons) >= threshold:
    reflection = generate_reflection(lessons_batch)
    # reflection.type = "level_1_pattern" or "level_2_principle"
```

**3. Error Category Statistics:**
```python
def count_error_categories():
    categories = {
        "TIMEOUT": 0, "ENCODING": 0, "IMPORT": 0,
        "SYNTAX": 0, "RUNTIME": 0, "UNKNOWN": 0
    }
    # Count failures by category from logs
    return categories
```

This enables detection of systemic issues like:
- Increasing TIMEOUT errors = prompts becoming too complex
- Increasing SYNTAX errors = prompts not enforcing code style
- Increasing IMPORT errors = missing dependency instructions

### 4.4 Online Learning for Prompt Improvement

**Checkpoint-Based Learning (`grind_spawner.py`):**
```python
# Every 5 turns, record online learning checkpoint
if checkpoint_counter % 5 == 0:
    learn_online(session_id, run_num, context, result, turn_count)
```

**Automatic Updates to Prompt Systems:**

1. **Prompt Optimizer Updates:**
   - Successful runs (returncode=0, self_verified=True) become new demonstrations
   - Efficiency score calculated and compared against existing demos

2. **Skill Registry Updates:**
   - High-quality runs (quality_score >= 0.9) trigger automatic skill extraction
   - Medium-quality runs (quality_score >= 0.75) matched against pattern keywords
   - New skills registered with preconditions and postconditions

3. **Failure Pattern Updates:**
   - Failed runs recorded with full context
   - Similar future tasks receive warning injections

---

## 5. Research References

### Papers Implemented in This Codebase

| Paper | arXiv | Key Concept | Implementation |
|-------|-------|-------------|----------------|
| CAMEL | 2303.17760 | Role-playing inception prompting | `roles.py` |
| DSPy | 2310.03714 | Self-bootstrapping demonstrations | `prompt_optimizer.py`, `dspy_modules.py` |
| Voyager | 2305.16291 | Skill library composition | `skill_registry.py` |
| Generative Agents | 2304.03442 | Memory synthesis, importance scoring | `memory_synthesis.py` |
| MetaGPT | 2308.00352 | Structured outputs, role subscriptions | `roles.py` (ROLE_SUBSCRIPTIONS) |
| LATS | 2310.04406 | Language agent tree search, critic | `critic.py` |
| TextGrad | 2406.14762 | Iterative refinement via feedback | `grind_spawner.py` (critic retry loop) |
| HippoRAG | - | Semantic retrieval with importance weighting | `memory_synthesis.py` |

### Additional Research Directions

**1. Constitutional AI for Prompts:**
- Already implemented in `safety_constitutional.py`
- Could be extended to evaluate prompt safety before execution

**2. Prompt Compression:**
- Not yet implemented
- Research: LLMLingua, Selective Context
- Would reduce token costs for long context prompts

**3. Prompt Caching:**
- Partial implementation via `skill_embeddings.json` cache
- Could extend to full prompt response caching

**4. Automatic Prompt Generation:**
- Current: Manual template + dynamic injection
- Research: APE (Automatic Prompt Engineer), OPRO
- Could generate optimal prompts from task descriptions

**5. Adversarial Prompt Robustness:**
- Current: Basic injection detection in `safety_sanitize.py`
- Could extend with adversarial testing suite

---

## Summary

This codebase implements a sophisticated prompt engineering architecture that combines:

1. **Layered construction**: Base template + role injection + context retrieval + failure warnings + few-shot examples
2. **Adaptive behavior**: Task complexity analysis determines model, budget, and role chain
3. **Continuous learning**: Successful runs become demonstrations, failures become warnings
4. **Multi-signal evaluation**: Critic quality scores + self-verification + performance tracking

The architecture is research-backed with implementations of CAMEL, DSPy, Voyager, Generative Agents, and LATS patterns. Future improvements could focus on prompt compression, automatic prompt generation, and adversarial robustness testing.
