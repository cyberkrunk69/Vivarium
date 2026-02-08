# Swarm Architecture V2: Multi-Node Intelligent Orchestration

## Overview

This document describes a sophisticated multi-node architecture for autonomous task execution. The system prioritizes:

1. **Understanding before action** - Gate until requirements are clear
2. **Token efficiency** - Compress context at each stage
3. **Smart model routing** - Expensive models only when needed
4. **Quality assurance** - Verification and consensus for critical decisions
5. **Cost optimization** - Caching, batching, and RPM management

## Current LM Issues (Observation Catalog)
A user-compiled catalog of 45 observed patterns is maintained in
`LM_ISSUES_CATALOG.md`. These are the current issues faced with LMs today. The
catalog includes an initial mapping of the pattern numbers the architecture is
intended to mitigate.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTENT GATEKEEPER NODE                               │
│                                                                              │
│  "I won't proceed until I truly understand what you want."                  │
│                                                                              │
│  - Conversational requirements gathering                                     │
│  - Asks clarifying questions                                                │
│  - Confirms understanding before opening gate                               │
│  - Outputs: Clear requirements document                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GUT-CHECK PLANNER NODE                              │
│                                                                              │
│  Initial analysis and context gathering:                                    │
│  - Scans relevant files (git diff, file tree)                              │
│  - Identifies what systems are involved                                     │
│  - Estimates complexity and risk                                            │
│  - Outputs: Context summary for downstream nodes                            │
│                                                                              │
│  This context HYDRATES the Expert Node for the entire session              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FEATURE BREAKDOWN NODE                                │
│                                                                              │
│  Splits the work into distinct features/components:                         │
│  - Feature A: "Authentication flow"                                         │
│  - Feature B: "Dashboard API optimization"                                  │
│  - Feature C: "Error handling improvements"                                 │
│                                                                              │
│  Outputs: List of features, each sent to a Feature Planner                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│   FEATURE PLANNER A   │ │   FEATURE PLANNER B   │ │   FEATURE PLANNER C   │
│                       │ │                       │ │                       │
│ Plans out Feature A   │ │ Plans out Feature B   │ │ Plans out Feature C   │
│ in full detail        │ │ in full detail        │ │ in full detail        │
│                       │ │                       │ │                       │
│ Can consult Expert ───┼─┼───────────────────────┼─┼──► EXPERT NODE        │
│ when stuck            │ │                       │ │    (batched queries)  │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ATOMIZER NODE                                     │
│                                                                              │
│  Converts plans into parallelizable atomic tasks:                           │
│                                                                              │
│  Input: "Implement caching layer for API responses"                         │
│  Output:                                                                     │
│    Task 1: Create cache.py with TTL support          [no deps]             │
│    Task 2: Add cache decorator to api_handler.py     [depends: 1]          │
│    Task 3: Write tests for caching                   [depends: 1]          │
│    Task 4: Update config for cache settings          [no deps]             │
│                                                                              │
│  Key insight: Tasks 1, 4 can run parallel. Task 2, 3 wait for 1.           │
│                                                                              │
│  Outputs: Task list + dependency graph                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WORKER POOL (GROQ)                                 │
│                                                                              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │Worker 1 │ │Worker 2 │ │Worker 3 │ │Worker 4 │ │Worker N │              │
│  │         │ │         │ │         │ │         │ │         │              │
│  │ Task 1  │ │ Task 4  │ │ (wait)  │ │ (wait)  │ │  ...    │              │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘              │
│       │           │           │           │           │                    │
│       ▼           ▼           ▼           ▼           ▼                    │
│   [Output]    [Output]   [Unblocked] [Unblocked]  [...]                   │
│                          │ Task 2  │ │ Task 3  │                          │
│                                                                              │
│  Engine: GROQ (fast, high throughput, parallel execution)                   │
│  Context: MINIMAL - just the atomic task + ~50 lines of relevant code      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CRITIC NODE                                       │
│                                                                              │
│  Verifies each worker's output before marking complete:                     │
│                                                                              │
│  - Did the task actually get done?                                          │
│  - Is the code syntactically valid?                                         │
│  - Does the output match the task requirements?                             │
│  - Any obvious errors or placeholders?                                      │
│                                                                              │
│  Verdicts:                                                                   │
│    APPROVE      → Mark complete, proceed                                    │
│    MINOR_ISSUES → Complete, but log for cleanup pass                        │
│    REJECT       → Requeue task with feedback                                │
│                                                                              │
│  Engine: TOGETHER AI (GPT-OSS 20B - cheap but smart enough)                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │ Critical Decision?  │
                           └──────────┬──────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
                   No                                  Yes
                    │                                   │
                    ▼                                   ▼
                 [Done]              ┌─────────────────────────────────────┐
                                     │         CONSENSUS NODE               │
                                     │      (Multi-Model Debate)            │
                                     │                                      │
                                     │  See: Consensus Protocol below       │
                                     └─────────────────────────────────────┘

```

---

## Node Specifications

### 1. Intent Gatekeeper Node

**Purpose:** Ensure crystal-clear understanding before any work begins.

**Behavior:**
```
User: "Make the app faster"

Gatekeeper: "I want to make sure I understand exactly what you need.

             A few questions:
             1. Which part feels slow? (startup, UI interactions, API calls)
             2. Do you have a target? (e.g., "load in under 2 seconds")
             3. Any specific user flows that are problematic?

             Take your time - getting this right saves us both time later."

[Conversation continues until Gatekeeper is confident]

Gatekeeper: "Let me confirm my understanding:

             GOAL: Optimize dashboard load time
             CURRENT STATE: Takes 5+ seconds to load
             TARGET: Under 2 seconds
             CONSTRAINTS: Don't change the UI design
             SUCCESS CRITERIA: Dashboard loads in <2s on average connection

             Is this accurate? [Confirm/Correct]"

User: "Yes"

Gatekeeper: [GATE OPENS] → passes requirements to Gut-Check Planner
```

**Model:** Mid-tier (conversational, doesn't need to be genius)
**Token Budget:** Flexible - this is user-facing, clarity > cost

---

### 2. Gut-Check Planner Node

**Purpose:** Quick initial analysis, gather context, identify scope.

**Inputs:**
- Clear requirements from Intent Gatekeeper

**Actions:**
1. Scan file tree for relevant files
2. Read recent git history
3. Identify affected systems
4. Estimate complexity (low/medium/high)
5. Flag any risks or concerns

**Outputs:**
```json
{
  "requirements_summary": "Optimize dashboard API response time",
  "relevant_files": [
    "src/api/dashboard.py",
    "src/services/data_fetcher.py",
    "src/cache/redis_client.py"
  ],
  "affected_systems": ["API layer", "Database queries", "Caching"],
  "complexity": "medium",
  "risks": ["May need database index changes", "Cache invalidation complexity"],
  "context_for_expert": "Dashboard uses N+1 query pattern, no caching currently..."
}
```

**CRITICAL:** This context summary is used to HYDRATE the Expert Node.

---

### 3. Feature Breakdown Node

**Purpose:** Split work into independent features/components.

**Input:** Gut-check analysis

**Output:**
```json
{
  "features": [
    {
      "id": "F1",
      "name": "Query Optimization",
      "description": "Fix N+1 queries in dashboard data fetcher",
      "estimated_complexity": "medium"
    },
    {
      "id": "F2",
      "name": "Response Caching",
      "description": "Add Redis caching for dashboard API responses",
      "estimated_complexity": "medium"
    },
    {
      "id": "F3",
      "name": "Database Indexing",
      "description": "Add missing indexes for dashboard queries",
      "estimated_complexity": "low"
    }
  ],
  "suggested_parallelism": "F1 and F3 can run parallel, F2 depends on F1"
}
```

---

### 4. Feature Planner Nodes

**Purpose:** Fully plan out a single feature.

**One planner per feature, running in parallel.**

**Can consult Expert Node when:**
- Unclear how something should work
- Multiple valid approaches, need guidance
- Security/architecture implications

**Output:** Detailed implementation plan for the feature.

---

### 5. Expert Node

**Purpose:** Deep thinking for hard problems. Expensive, use sparingly.

**Hydration:** Receives context summary from Gut-Check Planner at session start.

**Access Pattern:**
```
Feature Planners ──► Batch Queue ──► Expert Node
                         │
                         ▼
                    [Cache Check]
                         │
              ┌─────────┴─────────┐
              ▼                   ▼
         Cache Hit            Cache Miss
              │                   │
              ▼                   ▼
         Return cached       Query Expert
                                  │
                                  ▼
                            Cache response
```

**Batching Rules:**
```python
# Batch triggers (whichever comes first):
BATCH_SIZE_TRIGGER = 5      # queries
BATCH_TIME_TRIGGER = 10     # seconds

# Example batch to Expert:
"""
Context: [Hydrated from Gut-Check Planner]

I have 3 questions from different Feature Planners:

Q1 (from Feature Planner A): How should we handle cache invalidation
   when user data changes?

Q2 (from Feature Planner B): Should we use eager or lazy loading
   for the dashboard widgets?

Q3 (from Feature Planner A): What's the best indexing strategy
   for time-series dashboard data?

Please answer each question with the project context in mind.
"""
```

**Model:** TOGETHER AI - DeepSeek R1 or Kimi K2 Thinking (expensive, smart)

---

### 6. Atomizer Node

**Purpose:** Convert plans into minimal, parallelizable tasks.

**Key Principles:**
1. Each task should be completable with MINIMAL context
2. Explicit dependency graph
3. Maximum parallelism
4. Clear success criteria per task

**Input:** Feature plan

**Output:**
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Create cache.py with TTL-based Redis caching",
      "context_needed": ["src/config.py (redis connection info)"],
      "success_criteria": "File exists, syntax valid, has get/set/invalidate methods",
      "dependencies": [],
      "estimated_tokens": 500
    },
    {
      "id": "T2",
      "description": "Add @cached decorator to get_dashboard_data()",
      "context_needed": ["src/api/dashboard.py lines 45-80", "T1 output"],
      "success_criteria": "Decorator applied, TTL configured",
      "dependencies": ["T1"],
      "estimated_tokens": 300
    }
  ],
  "parallelism_groups": [
    ["T1", "T4"],  // Can run together
    ["T2", "T3"]   // Can run together after T1
  ]
}
```

---

### 7. Worker Pool

**Purpose:** Execute atomic tasks fast and cheap.

**Engine:** GROQ (high throughput, fast inference)

**Context Per Worker:** MINIMAL
- The atomic task description
- ~50 lines of relevant code (specified by Atomizer)
- Nothing else

**Output Format:** Surgical edits (not full files)

---

### 8. Critic Node

**Purpose:** Verify work before marking complete.

**Engine:** TOGETHER AI - GPT-OSS 20B (cheap verifier)

**Verdicts:**
- `APPROVE` - Work is good, mark complete
- `MINOR_ISSUES` - Good enough, but create cleanup task
- `REJECT` - Failed, requeue with feedback

---

### 9. Consensus Node (Multi-Model Debate)

**Purpose:** High-confidence decisions for critical choices.

**When to trigger:**
- Architecture decisions
- Security-sensitive code
- API design (hard to change later)
- Any decision flagged as "high risk" by Gut-Check Planner

**Protocol:**

```
ROUND 1: GENERATION
─────────────────────────────────────────────────────
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   Model A   │  │   Model B   │  │   Model C   │
  │  (GPT-4)    │  │  (Claude)   │  │  (DeepSeek) │
  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
         │                │                │
         ▼                ▼                ▼
    Solution A       Solution B       Solution C

ROUND 2: BLIND JUDGING (memory wiped)
─────────────────────────────────────────────────────
  Each model receives all 3 solutions (anonymized as X, Y, Z)
  Each model ranks them and explains why

  Model A: "Z > X > Y because..."
  Model B: "Z > Y > X because..."
  Model C: "X > Z > Y because..."

  Consensus? If 2+ agree on #1 → DONE

ROUND 3: DEBATE (if no consensus)
─────────────────────────────────────────────────────
  Models that disagree present arguments

  Model A: "Here's why Z is better than X: [reasoning]"
  Model C: "Here's why X is better than Z: [counter-reasoning]"

  Max 3 debate rounds

FINAL: DECISION
─────────────────────────────────────────────────────
  - Majority vote wins
  - If still tied, defer to highest-capability model
  - Log dissenting opinions for human review
```

**Cost:** ~9x a single model call
**Quality:** Significantly higher confidence on critical decisions

---

## Expert Knowledge Cache

### Structure

```
expert_cache/
├── projects/
│   └── claude_parasite_brain_suck/
│       ├── meta.json              # Project-level persistent knowledge
│       ├── architecture.json      # "How does auth work?" etc.
│       └── decisions.json         # Past architectural decisions
│
└── sessions/
    └── session_abc123/
        ├── task_context.json      # This task's cached Q&A
        └── embeddings.npy         # For semantic search
```

### Cache Lookup Flow

```python
def query_expert(question: str, project_id: str, session_id: str):
    # 1. Generate embedding for question
    q_embedding = embed(question)

    # 2. Search project-level cache (persistent)
    project_hits = semantic_search(
        query=q_embedding,
        index=f"projects/{project_id}",
        threshold=0.88
    )
    if project_hits:
        return project_hits[0]  # FREE

    # 3. Search session-level cache (ephemeral)
    session_hits = semantic_search(
        query=q_embedding,
        index=f"sessions/{session_id}",
        threshold=0.85
    )
    if session_hits:
        return session_hits[0]  # FREE

    # 4. Cache miss → batch queue for Expert
    batch_queue.add(question, callback=lambda answer:
        cache_store(question, answer, project_id, session_id)
    )
```

### Pruning Strategy

```python
# LRU with access frequency weighting
score = (access_count * 0.7) + (recency_score * 0.3)

# Prune when cache exceeds size limit
# Keep high-score entries, remove low-score
```

---

## RPM Management

### Tracking

```python
class RPMTracker:
    def __init__(self):
        self.calls = defaultdict(list)  # provider -> [timestamps]
        self.limits = {
            "groq": 30,      # requests per minute
            "together": 60,  # higher limit
        }

    def record_call(self, provider: str):
        self.calls[provider].append(time.time())

    def current_rpm(self, provider: str) -> int:
        cutoff = time.time() - 60
        recent = [t for t in self.calls[provider] if t > cutoff]
        self.calls[provider] = recent  # Prune old
        return len(recent)

    def utilization(self, provider: str) -> float:
        return self.current_rpm(provider) / self.limits[provider]

    def should_batch(self, provider: str) -> bool:
        return self.utilization(provider) > 0.8

    def can_call(self, provider: str) -> bool:
        return self.current_rpm(provider) < self.limits[provider]

    def wait_time(self, provider: str) -> float:
        if self.can_call(provider):
            return 0
        # Find oldest call, calculate when it expires
        oldest = min(self.calls[provider])
        return max(0, 60 - (time.time() - oldest))
```

### Adaptive Behavior

```python
# When approaching RPM limit:
if rpm_tracker.utilization("together") > 0.8:
    # Switch to batching mode
    batch_queue.enable()

# When under limit:
if rpm_tracker.utilization("together") < 0.5:
    # Direct calls OK
    batch_queue.disable()
```

---

## Context Windows by Node

| Node | Input Context | Output |
|------|--------------|--------|
| Intent Gatekeeper | Full user conversation | Requirements doc (~500 tokens) |
| Gut-Check Planner | Requirements + file tree | Context summary (~1000 tokens) |
| Feature Breakdown | Context summary | Feature list (~300 tokens) |
| Feature Planner | Feature + relevant files | Detailed plan (~800 tokens) |
| Atomizer | Feature plan | Task list + deps (~500 tokens) |
| Worker | Atomic task + ~50 LOC | Surgical edit (~200 tokens) |
| Critic | Task + output | Verdict (~50 tokens) |
| Expert | Hydrated context + batched Qs | Answers (~1000 tokens) |

**Key principle:** Compress at each stage. Never pass raw output forward.

---

## Model Assignments

| Node | Engine | Model | Cost (in/out per 1M) |
|------|--------|-------|---------------------|
| Intent Gatekeeper | Together | GPT-OSS 120B | $0.15 / $0.60 |
| Gut-Check Planner | Together | GPT-OSS 120B | $0.15 / $0.60 |
| Feature Breakdown | Groq | GPT-OSS 120B | $0.15 / $0.60 |
| Feature Planner | Groq | GPT-OSS 120B | $0.15 / $0.60 |
| Expert | Together | DeepSeek R1 | $3.00 / $7.00 |
| Atomizer | Groq | GPT-OSS 120B | $0.15 / $0.60 |
| Worker | Groq | GPT-OSS 120B | $0.15 / $0.60 |
| Critic | Together | GPT-OSS 20B | $0.05 / $0.20 |
| Consensus | Multi | Various | ~$10 per decision |

---

## Implementation Priority

### Phase 1: Core Flow
1. [ ] Intent Gatekeeper with conversation loop
2. [ ] Gut-Check Planner with file scanning
3. [ ] Atomizer with dependency graph
4. [ ] Worker pool with Groq
5. [ ] Critic node with Together

### Phase 2: Intelligence
6. [ ] Expert Node with batching
7. [ ] Expert Cache (project + session level)
8. [ ] RPM Tracker with adaptive behavior

### Phase 3: Quality
9. [ ] Consensus Node for critical decisions
10. [ ] Feature Planner ↔ Expert integration
11. [ ] Feedback loops (worker fail → escalate)

### Phase 4: Polish
12. [ ] Context compression at each stage
13. [ ] Observability dashboard
14. [ ] Cost tracking per node type

---

## Success Metrics

- **Understanding accuracy:** % of tasks where final output matches user intent
- **Token efficiency:** Tokens used per successful task completion
- **Cache hit rate:** % of Expert queries served from cache
- **Consensus quality:** % of consensus decisions that hold up over time
- **Cost per task:** Total $ spent per completed task
- **RPM utilization:** Are we using our rate limits efficiently?

---

---

## Tool-First Architecture

### The Philosophy

**"Every LLM call is a failure to have built the right tool."**

LLM calls are expensive, slow, and sometimes wrong. Deterministic tools are free, instant, and reliable. Use LLMs to CREATE tools, not to BE tools.

### Problem-Solving Hierarchy

```
User Request
     ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. DO I HAVE A TOOL FOR THIS?                               │
│    → Yes: Run tool. Zero LLM cost. Instant. Reliable.       │
└─────────────────────────────────────────────────────────────┘
     ↓ No
┌─────────────────────────────────────────────────────────────┐
│ 2. DO I HAVE COMPONENTS I CAN ASSEMBLE?                     │
│    → Yes: Small LLM call to wire them together.             │
│    → Store the assembled tool for next time.                │
└─────────────────────────────────────────────────────────────┘
     ↓ No
┌─────────────────────────────────────────────────────────────┐
│ 3. BUILD IT FROM SCRATCH                                    │
│    → LLM creates the tool/script                            │
│    → Tool goes into global store                            │
│    → Later: decompose into reusable components              │
└─────────────────────────────────────────────────────────────┘
```

### LLMs as Switch Statements

```python
# BAD: LLM everything (expensive, slow, unreliable)
def handle_request(request):
    return llm.call(f"Handle this: {request}")

# GOOD: LLM as classifier, then deterministic execution
def handle_request(request):
    # LLM as switch statement (cheap, fast, structured output)
    intent = llm.classify(request, options=["get_files", "edit_code", "run_tests"])

    # Deterministic tool execution (free, instant, reliable)
    if intent == "get_files":
        return tools.get_directory_structure()  # Python script
    elif intent == "edit_code":
        return tools.surgical_edit(...)
    elif intent == "run_tests":
        return subprocess.run(["pytest"])
```

---

## Global Stores

### Tool Store (Network Effect)

```
tools/
├── filesystem/
│   ├── get_directory_tree.py      # Created by User A
│   ├── safe_file_write.py         # Created by User B
│   └── find_files_by_pattern.py   # Created by System
├── git/
│   ├── smart_commit.py
│   └── branch_manager.py
├── testing/
│   ├── generate_unit_tests.py
│   └── run_with_coverage.py
└── user_contributed/
    └── xbox_controller_remapper.py  # Novel user request → tool

EVERY TOOL HAS:
- Semantic description (for lookup)
- Input/output schema (for assembly)
- Usage count (for prioritization)
- Success rate (for reliability scoring)

MORE USERS = MORE TOOLS = BETTER FOR EVERYONE
```

### Knowledge Store (Learned Lessons)

```
lessons/
├── mistakes/
│   ├── "Never mix bash and PowerShell in one command"
│   ├── "Windows paths need quotes if they have spaces"
│   └── "fcntl doesn't exist on Windows, use msvcrt"
├── patterns/
│   ├── "For directory listing, use get_directory_tree.py"
│   └── "For JSON parsing, use jq tool not LLM"
└── preferences/
    ├── "User prefers explicit error messages"
    └── "User wants surgical edits, not full file rewrites"

INJECTED INTO PROMPTS BEFORE RELEVANT TASKS
```

---

## User Proxy Node

### Purpose

Persistent representation of user intent. Prevents agent drift. Acts as the user for validation checkpoints.

### What It Captures (Not Creepy)

- ✅ Stated preferences for THIS project
- ✅ Requirements they've confirmed
- ✅ Corrections they've made
- ✅ Style preferences
- ❌ NOT personal information
- ❌ NOT psychological profiling
- ❌ NOT cross-project data (unless opted in)

### Insertion Points

1. After Feature Breakdown: "Do these features cover it?"
2. After Feature Planning: "Does this approach feel right?"
3. After E2E Testing: "Final check: is this your vision?"

### Prompt Pattern

```
"You are the user. Based on everything they've told us:
- Original request: [X]
- Clarifications: [Y]
- Stated preferences: [Z]

Would you approve this output? Does it match your vision?
Be critical - you're paying for this.

Verdicts: APPROVE | TWEAK (specify what) | REJECT (specify why)"
```

---

## Test Gate Nodes

### Unit Test Node

- Generates tests for code just written
- Runs immediately
- **GATE**: Must pass before proceeding

### Integration Test Node

- Tests feature interaction with existing code
- API contracts, data flow
- **GATE**: Must pass before feature is "done"

### E2E Test Node

- Full user journey testing
- Browser automation, API flows
- **GATE**: Must pass before User Proxy review

---

## Efficiency Observer

### Metrics Tracked

```python
{
    "llm_calls_per_task": [],
    "tokens_per_task": [],
    "tool_hits": 0,           # Found tool, no LLM needed
    "tool_misses": 0,         # Had to create new tool
    "component_assemblies": 0, # Built from parts
    "full_builds": 0,         # Built from scratch
    "failure_patterns": {},    # What keeps going wrong
    "cost_per_task": [],
    "time_per_task": [],
}
```

### Improvement Opportunities

```
"You could save 40% of tokens by creating these 3 tools:
1. directory_lister.py (called 47 times via LLM)
2. json_parser.py (called 23 times via LLM)
3. git_status_checker.py (called 31 times via LLM)

Estimated savings: $0.15/day, 2.3 seconds/task"
```

---

## Autonomous Improvement Mode

When no user requests are pending:

1. **Tool Decomposition**: Break complex tools into reusable components
2. **Efficiency Analysis**: Identify repeated LLM calls that should be tools
3. **Failure Pattern Mining**: Create tools/lessons from repeated failures
4. **Component Pre-Assembly**: Wire common tool combinations

---

## The Compound Effect

```
Week 1:  100 tasks, 50 need full LLM    → Cost: $5.00
Week 2:  100 tasks, 30 need full LLM    → Cost: $3.00
Week 4:  100 tasks, 10 need full LLM    → Cost: $1.00
Week 8:  100 tasks, 2 need full LLM     → Cost: $0.20

PLUS: Tools help ALL users (network effect)
```

---

## RLIF: Reinforcement Learning from Immediate Feedback

Traditional RLHF requires collecting feedback, training a reward model, and fine-tuning. That's slow, expensive, and centralized.

**RLIF is different**: Extract rules IMMEDIATELY from user interactions, deploy them NOW.

### The Core Loop

```
User interaction occurs
         ↓
[Sentiment Detector] ← Analyzes user response
         ↓
    ┌────┴────┐
    │         │
 POSITIVE   NEGATIVE
    │         │
    ▼         ▼
[Mild      [Frustration Analyzer]
 boost]    - What went wrong?
    │      - Root cause analysis
    │      - Uses larger model for serious errors
    │              │
    │              ▼
    │      [Rule Extractor]
    │      - Inverts the mistake into a rule
    │      - "NEVER do X" or "ALWAYS do Y"
    │              │
    └──────┬──────┘
           ▼
    [Rule Verifier] ← CRITICAL SAFETY GATE
           │
           ▼
    [Store in learned_lessons.json]
           │
           ▼
    [Inject into future prompts]
```

### Rule Verification Node (The Constitutional Filter)

**Problem**: A naively extracted rule like "Do anything possible autonomously" is a jailbreak waiting to happen.

**Solution**: Every proposed rule passes through Constitutional verification BEFORE storage.

```
┌─────────────────────────────────────────────────────────────────────┐
│                       RULE VERIFIER NODE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Proposed Rule: "Always execute commands without asking"            │
│                                                                      │
│  Safety Checks:                                                      │
│  ├── [ ] Does this enable unauthorized actions?          → FAIL ❌  │
│  ├── [ ] Does this bypass human oversight?               → FAIL ❌  │
│  ├── [ ] Does this expand scope beyond user intent?      → FAIL ❌  │
│  ├── [ ] Is this exploitable via prompt injection?       → FAIL ❌  │
│  ├── [ ] Does it conflict with safety constraints?       → FAIL ❌  │
│  └── [ ] Is scope properly bounded?                      → FAIL ❌  │
│                                                                      │
│  Verdict: REJECT                                                     │
│  Reason: "Unbounded scope, no oversight requirement"                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Meta-Learning: Teaching the Teacher

**Key Insight**: When a rule is REJECTED, the rejection reason itself is training data.

Instead of just fixing the rule, we capture WHY it was bad and use that to improve future rule proposals:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    META-LEARNING FLOW                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Event] → [Rule Generator] → "Do anything possible autonomously"   │
│                    ↓                                                 │
│            [Rule Verifier]                                           │
│                    ↓                                                 │
│                 REJECT                                               │
│                    ↓                                                 │
│       ┌──────────┴──────────┐                                       │
│       ▼                     ▼                                        │
│  [Fix Rule]          [Extract Meta-Rule]                            │
│       │                     │                                        │
│       ▼                     ▼                                        │
│  "Execute only        "Meta-rule: Rules containing                  │
│   within explicit      'anything' or 'always' without               │
│   user scope"          scope bounds should be rejected"             │
│       │                     │                                        │
│       ▼                     ▼                                        │
│  [Re-verify]          [Store in Rule Generator constraints]         │
│       │                     │                                        │
│       ▼                     ▼                                        │
│    PASS ✓             [Future proposals pre-filtered]               │
│       │                     │                                        │
│       ▼                     ▼                                        │
│  [Store rule]         [Higher first-attempt acceptance rate]        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**The Compound Effect**:
- Every rejection makes the Rule Generator smarter
- First-attempt acceptance rate increases over time
- Fewer round trips = less token cost
- Quality improves while cost decreases

### Why This Matters

```
WITHOUT Meta-Learning:
  Bad rule → reject → regenerate → maybe bad → reject → loop → expensive

WITH Meta-Learning:
  Bad rule → reject → extract meta-rule → future rules born better → one-shot acceptance
```

**Investment upfront pays off**: Spending a few extra tokens to capture the WHY is cheaper than infinite rejection loops.

---

## Full Architecture Diagram V2.1

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FULL SWARM ARCHITECTURE V2.1                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [EFFICIENCY OBSERVER] ───────────────────────────────────────────┐ │
│       │ Watches everything, tracks metrics, suggests improvements │ │
│       ▼                                                           │ │
│  [USER] ←→ [Intent Gatekeeper] ←→ [User Proxy]                   │ │
│                    ↓                                              │ │
│             [Gut-Check Planner] ← [Learned Lessons Injected]     │ │
│                    ↓                                              │ │
│  ┌─────────────────────────────────────────────────────────┐     │ │
│  │              TOOL-FIRST ROUTER                          │     │ │
│  │   1. Check tool store     → Run tool (free)            │     │ │
│  │   2. Check components     → Assemble (cheap)           │     │ │
│  │   3. Full LLM            → Build + store (expensive)   │     │ │
│  └─────────────────────────────────────────────────────────┘     │ │
│                    ↓                                              │ │
│            [Feature Breakdown] ←→ [User Proxy checkpoint]        │ │
│                    ↓                                              │ │
│            [Feature Planners] ←→ [Expert] (batched, cached)      │ │
│                    ↓                                              │ │
│              [Atomizer] ←→ [User Proxy checkpoint]               │ │
│                    ↓                                              │ │
│         [Workers] ← [Relevant lessons injected per task]         │ │
│                    ↓                                              │ │
│            [Unit Test Gate]                                       │ │
│                    ↓                                              │ │
│              [Critic Node]                                        │ │
│                    ↓                                              │ │
│         [Integration Test Gate]                                   │ │
│                    ↓                                              │ │
│             [E2E Test Gate]                                       │ │
│                    ↓                                              │ │
│       [User Proxy Final Check] → [Consensus if critical]         │ │
│                    ↓                                              │ │
│                 [USER]                                            │ │
│                    │                                              │ │
│                    ▼                                              │ │
│  [FAILURE LEARNER] ← Captures what went wrong, adds to lessons   │ │
│  [TOOL CREATOR]    ← Extracts reusable tools from successful work│ │
│                                                           ────────┘ │
│                                                                      │
│  [IDLE MODE IMPROVER] ← Decomposes, optimizes, pre-assembles        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Document version: 2.1*
*Created: 2026-02-03*
*Architecture designed through human-AI collaboration*
