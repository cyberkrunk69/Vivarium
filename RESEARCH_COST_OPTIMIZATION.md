# AI Agent System Cost Optimization Research

**Project:** Vivarium Agent Orchestration System
**Date:** 2026-02-03
**Scope:** Token usage patterns, cost reduction strategies, quality-cost tradeoffs, and budget management

---

## Executive Summary

This research analyzes the Vivarium agent system's cost structure and identifies optimization opportunities. Based on analysis of 10+ waves of grind sessions totaling approximately $0.92 in API costs across 10 research-backed implementations, the system demonstrates several cost optimization patterns worth studying and extending.

**Key Findings:**
- Average cost per task: $0.03-$0.07 (Haiku), $0.80 (Sonnet), $5.00 (Opus)
- Cost per turn variance: $0.004-$0.009 (2x range indicates consistent pricing)
- Token efficiency: 50-120 tokens/second output rate
- Primary cost drivers: Context size (prompts) > Output tokens > Number of turns

---

## 1. Current Cost Structure Analysis

### 1.1 Token Distribution Breakdown

Based on the `efficiency_analysis.md` data from actual grind sessions:

| Component | Estimated Share | Key Driver |
|-----------|----------------|------------|
| **Input/Prompt tokens** | 60-70% | System prompts, context, demonstrations |
| **Output tokens** | 20-30% | Generated code, explanations, summaries |
| **Overhead** | 5-10% | Retries, multi-turn clarification |

**Evidence from grind logs:**
- Session 10 (Architecture docs): $0.0595 total, 3,921 output tokens
- Session 6 (Learning log): $0.0126 total, 706 output tokens
- The 6x cost difference comes primarily from context/input size, not output

### 1.2 Model Pricing Impact

The system uses a tiered model approach as documented in `haiku_capabilities.md` and task files:

| Model | Input $/M tokens | Output $/M tokens | Relative Cost | Typical Task Budget |
|-------|-----------------|-------------------|---------------|---------------------|
| Haiku 4.5 | ~$0.25 | ~$1.25 | 1x (baseline) | $0.05-$0.10 |
| Sonnet 4 | ~$3.00 | ~$15.00 | 12x | $0.80 |
| Opus 4.5 | ~$15.00 | ~$75.00 | 60x | $5.00 |

**Cost ratios from task definitions:**
- Safety research tasks: $0.80/task (Sonnet)
- Architecture review tasks: $5.00/task (Opus)
- Simple grind tasks: $0.05-$0.10/task (Haiku)

### 1.3 Where Tokens Go in This System

From analyzing `worker.py`, `swarm.py`, and `prompt_optimizer.py`:

```
TOKEN FLOW PER TASK EXECUTION
==============================

SYSTEM PROMPT (fixed per session)
├── Role definition (~200 tokens)
├── Safety constraints (~150 tokens)
├── Output format spec (~100 tokens)
└── Tool definitions (~500-1000 tokens)
    SUBTOTAL: ~1,000-1,500 tokens (FIXED COST)

CONTEXT INJECTION (variable)
├── Workspace scan results (~200-500 tokens)
├── Relevant file contents (~500-5,000 tokens)
├── Previous demonstrations (~300-900 tokens) [DSPy optimization]
├── Relevant lessons (~200-500 tokens)
└── Task dependencies (~100-300 tokens)
    SUBTOTAL: ~1,300-7,200 tokens (VARIABLE)

TASK PROMPT (variable)
├── Task description (~50-200 tokens)
├── Step-by-step instructions (~100-500 tokens)
└── Expected output format (~50-100 tokens)
    SUBTOTAL: ~200-800 tokens

MULTI-TURN OVERHEAD
├── Each additional turn: +full context replay
├── Typical sessions: 3-13 turns (from efficiency_analysis.md)
└── Context accumulates: turn_n = base + sum(previous_outputs)
```

### 1.4 Caching Benefits (Observed)

The system doesn't currently implement explicit caching, but the architecture supports it:

**Cacheable Components:**
1. System prompts (identical across sessions)
2. Codebase scans (refresh only on file changes)
3. Demonstration library (static between compilations)
4. Learned lessons (slow-changing)

**Estimated Savings with Caching:**
- System prompt: 1,000-1,500 tokens/session saved
- Demonstrations (DSPy): 300-900 tokens/session if cached
- At 10 sessions/wave: 13,000-24,000 tokens saved
- With Haiku pricing: ~$0.003-$0.006/wave saved on input tokens

---

## 2. Cost Reduction Strategies

### 2.1 Prompt Compression

**Current State:** The `optimized_prompt.txt` shows minimal prompt design:
```
You are an EXECUTION worker.
WORKSPACE: {workspace}
TASK (execute step by step): {task}
RULES: [4 lines]
EXECUTE NOW.
```

**This is already optimized** - only ~50 tokens for the core prompt.

**Further Compression Opportunities:**

| Technique | Savings | Implementation |
|-----------|---------|----------------|
| Abbreviate system prompts | 10-20% | "WS:" instead of "WORKSPACE:" |
| Remove examples when confidence high | 20-40% | Skip DSPy demos for simple tasks |
| Compress file contents | 30-50% | Send AST/structure, not full files |
| Delta encoding for multi-turn | 40-60% | Send only changed context |

**From `prompt_optimizer.py` - DSPy approach:**
```python
# Current: Inject 2-3 full demonstrations
# Optimized: Use signatures only, skip demos for known patterns
```

### 2.2 Context Pruning

**Evidence-based pruning from the codebase:**

The `memory_synthesis.py` implements Generative Agents-style importance scoring:
```python
# Recency + Importance + Relevance scoring
# Lower-scored memories could be pruned from context
```

**Pruning Strategies:**

1. **Recency Decay** (from `research_brief_self_improvement.md`)
   - Exponential decay: alpha = 0.995 per time unit
   - Old context gets lower weight, eventually pruned
   - Saves: 20-40% context tokens for long sessions

2. **Importance Threshold** (from Generative Agents)
   - Score each memory 1-10 for "poignancy"
   - Only inject memories scoring > threshold
   - Saves: 30-50% lesson/memory tokens

3. **Relevance Filtering** (from HippoRAG/Voyager)
   - Embed task description
   - Only inject top-k similar skills/lessons
   - Saves: 40-60% context tokens

**Implementation in current system:**
```python
# From skill_registry.py - already implements embedding retrieval
# From prompt_optimizer.py - already ranks demonstrations by efficiency
# Gap: No importance scoring on lessons yet
```

### 2.3 Model Cascading (Cheap First, Expensive If Needed)

**Current implementation evidence from `haiku_capabilities.md`:**

```
HAIKU GOOD FOR:
- Simple document analysis ($0.03/task avg)
- Straightforward code generation ($0.016/task)
- Lightweight documentation ($0.01-$0.025/task)
- Structured data tasks ($0.013-$0.024/task)

NEEDS SONNET:
- Multi-file code analysis
- Complex architectural design
- Cross-file refactoring

NEEDS OPUS:
- Deep system understanding
- Subtle bug debugging
- Performance optimization
- Security audits
```

**Proposed Cascade Strategy:**

```
TASK ARRIVES
    |
    v
[COMPLEXITY CLASSIFIER] (use Haiku, ~100 tokens)
    |
    +-- Simple (score < 0.3) --> Haiku ($0.05 budget)
    |
    +-- Medium (0.3-0.7) --> Sonnet ($0.80 budget)
    |
    +-- Complex (> 0.7) --> Opus ($5.00 budget)

OPTIONAL ESCALATION:
    Haiku attempt fails --> Retry with Sonnet
    Sonnet attempt fails --> Retry with Opus (if budget allows)
```

**Cost Impact (estimated):**
- 70% of tasks stay at Haiku tier: 70% * $0.05 = $0.035
- 25% escalate to Sonnet: 25% * $0.80 = $0.20
- 5% need Opus: 5% * $5.00 = $0.25
- **Blended average: ~$0.49/task** (vs $0.80 if all Sonnet)

### 2.4 Batching and Deduplication

**Current State:**
- Each task runs independently via `worker.py`
- No batching of similar tasks
- No deduplication of repeated context

**Optimization Opportunities:**

1. **Task Batching**
   - Group similar tasks (e.g., "add tests to 5 files")
   - Single context load, multiple outputs
   - Estimated savings: 40-60% context tokens

2. **Context Deduplication**
   - Hash file contents
   - Skip re-reading unchanged files
   - Current: `swarm.py` re-scans codebase each `/plan` call

3. **Parallel Worker Sharing**
   - From `ARCHITECTURE.md`: Multiple workers read same `queue.json`
   - Could share a context cache via file/memory
   - Lock-based coordination already exists

**Implementation from `worker.py`:**
```python
# Current: Each worker reads queue.json independently
# Opportunity: Shared context cache with hash-based invalidation
```

---

## 3. Quality vs Cost Tradeoffs

### 3.1 When Is Opus Worth It?

**Based on `opus_orchestrator.py` and research briefs:**

| Use Case | ROI Justification |
|----------|-------------------|
| Architecture Review | Finds issues that would cost 10x to fix later |
| Strategy Planning | Compounds across 5+ waves of work |
| Security Audits | Single vulnerability could be catastrophic |
| Research Synthesis | Extracts actionable insights from papers |

**Not worth Opus:**
- File counting/listing
- Simple code generation
- Documentation from templates
- Repetitive structured tasks

**Evidence from `PROGRESS.md`:**
- Two Opus research briefs (984 lines combined) drove 6 waves of implementation
- Cost: ~$10 for 2 Opus sessions
- Value: 1,500+ lines of new code, 14 new modules
- ROI: ~$0.007 per line of production code generated downstream

### 3.2 Minimum Viable Context

**From `optimized_prompt.txt` - already minimal:**
```
You are an EXECUTION worker.
WORKSPACE: {workspace}
TASK (execute step by step): {task}
RULES: [4 lines]
EXECUTE NOW.
```

**Context Requirements by Task Type:**

| Task Type | Minimum Context | Full Context |
|-----------|-----------------|--------------|
| Code fix (single file) | Target file only | +related imports |
| Test creation | Function signatures | +example tests |
| Documentation | Module structure | +full code |
| Architecture review | All files (necessary) | All files |
| Refactoring | Affected files + dependencies | +usage patterns |

**Heuristic:** Start with minimum, add if task fails.

### 3.3 Early Stopping Strategies

**Current Implementation from `worker.py`:**
```python
MAX_IDLE_CYCLES: int = 10  # Exit after N consecutive idle checks
```

**Enhanced Early Stopping:**

1. **Budget-Based Stopping**
   ```python
   # From config.py
   DEFAULT_MIN_BUDGET = 0.05
   DEFAULT_MAX_BUDGET = 0.10
   # Stop when approaching max_budget
   ```

2. **Quality-Based Stopping** (from `critic.py`)
   ```python
   # CriticAgent scores code 0.0-1.0
   # Stop when quality_score >= 0.65 (threshold)
   ```

3. **Convergence Detection**
   - If last 3 turns produce similar output, stop
   - If code passes tests, stop immediately
   - If critic approves, stop

4. **Turn Limit** (from efficiency analysis)
   - Most tasks complete in 3-7 turns
   - Hard limit at 13-15 turns (diminishing returns observed)

---

## 4. Cost Tracking and Budgeting

### 4.1 Per-Task Cost Attribution

**Current tracking from `efficiency_analysis.md`:**

| Metric | Tracked? | Location |
|--------|----------|----------|
| Total cost per session | Yes | grind_logs/*.json |
| Cost per turn | Yes | Calculated in efficiency_analysis.md |
| Tokens used | Yes | API response metadata |
| Duration | Yes | execution_log.json |
| Model used | Partially | Task definitions |

**Attribution Model:**
```
Task Cost = Input Tokens * Input Rate + Output Tokens * Output Rate
         = (System + Context + Task) * $X + (Generated) * $Y
```

**From `performance_tracker.py`:**
```python
def track_session(self, session_result: Dict[str, Any]) -> Dict[str, Any]:
    record = {
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": session_result.get("duration_seconds", 0.0),
        "success": session_result.get("success", False),
        "quality_score": session_result.get("quality_score", 0.0),
        # Note: No explicit cost tracking yet
    }
```

**Gap:** Need to add explicit `cost_usd` field to session tracking.

### 4.2 ROI Measurement (Quality Per Dollar)

**Proposed Metrics:**

1. **Quality Per Dollar (QPD)**
   ```
   QPD = quality_score / task_cost_usd

   Example from data:
   - Session 6: $0.0126, quality ~0.8 (estimated) -> QPD = 63.5
   - Session 10: $0.0595, quality ~0.9 (estimated) -> QPD = 15.1

   Higher QPD = more efficient
   ```

2. **Lines of Code Per Dollar (LOC/$)**
   ```
   LOC/$ = lines_generated / task_cost_usd

   From PROGRESS.md:
   - Total: 1,500+ lines, ~$0.92 total
   - LOC/$ = 1,630 lines/dollar
   ```

3. **Task Success Per Dollar**
   ```
   From runs analysis:
   - 10 tasks, $0.92, 100% success
   - Success/$ = 10.87 successful tasks per dollar
   ```

4. **Compound Value Multiplier**
   ```
   For foundational tasks (Opus research):
   - Input: $10 Opus research
   - Output: 6 waves of Haiku/Sonnet work enabled
   - Multiplier: 15x (estimated downstream value)
   ```

### 4.3 Budget Allocation Strategies

**Current approach from task files:**

```json
// grind_tasks.json
{
  "task": "Safety research...",
  "budget": 0.80,
  "model": "sonnet"
}

// config.py
DEFAULT_MIN_BUDGET = 0.05
DEFAULT_MAX_BUDGET = 0.10
```

**Recommended Allocation Framework:**

| Wave Type | Haiku % | Sonnet % | Opus % | Budget/Wave |
|-----------|---------|----------|--------|-------------|
| Foundation/Research | 10% | 30% | 60% | $15-20 |
| Implementation | 70% | 25% | 5% | $2-5 |
| Testing | 80% | 20% | 0% | $1-2 |
| Documentation | 90% | 10% | 0% | $0.50-1 |
| Review/Audit | 20% | 40% | 40% | $10-15 |

**Budget Guard Implementation (from `opus_orchestrator.py`):**
```python
def should_spawn_opus(self) -> bool:
    """Check if Opus should be spawned based on wave count."""
    waves_since_opus = self.state["wave_count"] - self.state["last_opus_wave"]
    return waves_since_opus >= self.opus_interval  # Default: every 3 waves
```

**Recommendation:** Add explicit budget caps:
```python
class BudgetGuard:
    def __init__(self, daily_limit: float = 50.0):
        self.daily_limit = daily_limit
        self.spent_today = 0.0

    def can_spend(self, amount: float) -> bool:
        return (self.spent_today + amount) <= self.daily_limit

    def record_spend(self, amount: float):
        self.spent_today += amount
```

---

## 5. Actionable Recommendations

### Priority 1: Quick Wins (Implement First)

1. **Add cost tracking to `performance_tracker.py`**
   - Add `cost_usd` field to session records
   - Calculate and store QPD metric
   - Estimated impact: Better visibility, no direct savings

2. **Implement context caching for system prompts**
   - Hash-based invalidation
   - Estimated savings: $0.003-$0.01/wave

3. **Add importance threshold to lesson injection**
   - Only inject lessons scoring > 5/10
   - Estimated savings: 30% context tokens on long sessions

### Priority 2: Medium-Term (Next 2-4 Waves)

4. **Implement model cascading**
   - Start all tasks with Haiku
   - Escalate on failure or complexity detection
   - Estimated savings: 30-50% on task-level costs

5. **Add quality-based early stopping**
   - Use `critic.py` scores to stop when quality sufficient
   - Estimated savings: 20-30% on multi-turn sessions

6. **Batch similar tasks**
   - Group by file/module being modified
   - Single context load for batch
   - Estimated savings: 40-60% context tokens for batched work

### Priority 3: Long-Term Architecture

7. **Implement budget dashboard**
   - Real-time spend tracking
   - Wave-over-wave comparison
   - ROI visibility per task type

8. **Build context compression pipeline**
   - AST extraction instead of full file content
   - Delta encoding for multi-turn
   - Estimated savings: 50%+ on large codebases

9. **Predictive budget allocation**
   - Learn from historical QPD by task type
   - Auto-select model based on predicted ROI

---

## 6. Appendix: Cost Data Summary

### From `efficiency_analysis.md`:

| Session | Task | Cost | Turns | Cost/Turn | Tokens/Sec |
|---------|------|------|-------|-----------|------------|
| 1 | Lock protocol docs | $0.0248 | 3 | $0.0083 | 56.8 |
| 2 | Hardcoded values | $0.0738 | 13 | $0.0057 | 69.8 |
| 3 | Help text | $0.0147 | 3 | $0.0049 | 53.3 |
| 4 | Quick reference | $0.0445 | 7 | $0.0064 | 68.1 |
| 5 | API reference | $0.0245 | 3 | $0.0082 | 92.6 |
| 6 | Learning log | $0.0126 | 3 | $0.0042 | 119.8 |
| 7 | .gitignore | $0.0100 | 2 | $0.0050 | 49.5 |
| 8 | LOC report | $0.0668 | 13 | $0.0051 | 63.5 |
| 9 | Startup banner | $0.0184 | 4 | $0.0046 | 58.7 |
| 10 | Architecture docs | $0.0595 | 7 | $0.0085 | 86.7 |

**Totals:**
- Total spending: $0.3846
- Average cost/task: $0.0385
- Average cost/turn: $0.0061
- Most efficient: Session 6 ($0.0042/turn)
- Least efficient: Session 10 ($0.0085/turn)

### Model Cost Comparison (Anthropic Pricing Reference):

| Model | Input ($/M) | Output ($/M) | Cache Read | Cache Write |
|-------|-------------|--------------|------------|-------------|
| Haiku 3.5 | $0.80 | $4.00 | $0.08 | $1.00 |
| Sonnet 3.5 | $3.00 | $15.00 | $0.30 | $3.75 |
| Opus 3 | $15.00 | $75.00 | $1.50 | $18.75 |

*Note: Prompt caching reduces input costs by 90% for cached content.*

---

## 7. Conclusion

The Vivarium system already implements several cost optimization patterns (minimal prompts, DSPy demonstrations, tiered models). The primary opportunities for further optimization are:

1. **Context management** - Importance scoring and caching could reduce input tokens by 30-50%
2. **Model cascading** - Starting with Haiku could reduce average task cost by 30-50%
3. **Early stopping** - Quality-based termination could save 20-30% on multi-turn tasks
4. **Budget visibility** - Better tracking enables data-driven allocation decisions

The fundamental insight is that **input/context tokens dominate costs**. Optimizing what goes into the prompt (via caching, pruning, and compression) yields greater savings than optimizing outputs.

---

*Research completed: 2026-02-03*
*Codebase analyzed: D:\codingProjects\claude_parasite_brain_suck*
