# Multi-Agent Coordination Research Brief

**Project:** Black Swarm
**Date:** 2026-02-03
**Focus:** Multi-agent coordination, prompt optimization, and planning/search strategies

---

## 1. Key Techniques from Research Papers

### 1.1 CAMEL: Role-Playing Framework (arXiv:2303.17760)

**Core Innovation:** Inception prompting for autonomous multi-agent cooperation

**Key Techniques:**
- **Role-Playing Framework**: Assigns AI assistant and AI user roles to enable autonomous task completion
- **Inception Prompting**: Uses system messages to define agent roles, goals, and constraints without continuous human intervention
- **Task Specifier Agent**: Takes a preliminary idea and generates a detailed, actionable task specification
- **Instruction-Following Loop**: AI User provides instructions, AI Assistant responds with solutions until task completion

**Communication Protocol:**
```
Mt = {(I0, S0), ..., (It, St)}  // Message history
It+1 = U(Mt)                    // User generates next instruction
St+1 = A(Mt, It+1)              // Assistant generates solution
```

**Implementation Relevance:**
- Directly applicable to `roles.py` (PLANNER, CODER, REVIEWER, DOCUMENTER)
- Addresses challenges: role flipping, repeated instructions, infinite loops

---

### 1.2 MetaGPT: SOP-Driven Multi-Agent Collaboration (arXiv:2308.00352)

**Core Innovation:** Standardized Operating Procedures (SOPs) encoded into LLM workflows

**Key Techniques:**
- **Assembly Line Paradigm**: Sequential workflow with specialized roles (Product Manager -> Architect -> Project Manager -> Engineer -> QA)
- **Structured Communication Interfaces**: Agents communicate via documents/artifacts (PRDs, design specs) NOT free-form chat
- **Publish-Subscribe Mechanism**: Shared message pool where agents publish and subscribe based on role profiles
- **Executable Feedback Loop**: Self-correction through code execution and debugging

**Critical Insight:**
> "Pure natural language communication is insufficient for complex tasks" - information degrades like telephone game

**Role Definitions:**
| Role | Responsibility | Output Artifact |
|------|---------------|-----------------|
| Product Manager | Requirements analysis | PRD with User Stories |
| Architect | System design | File lists, data structures, interfaces |
| Project Manager | Task distribution | Task assignments |
| Engineer | Implementation | Code files |
| QA Engineer | Quality assurance | Test cases |

**Implementation Relevance:**
- `grind_spawner.py` needs SOP enforcement between workers
- Add structured output validation before handoffs

---

### 1.3 DSPy: Declarative Prompt Optimization (arXiv:2310.03714)

**Core Innovation:** Replace hard-coded prompts with parameterized, self-optimizing modules

**Key Techniques:**
- **Signatures**: Declarative input/output specifications (e.g., `"question -> answer"`)
- **Modules**: Reusable components (Predict, ChainOfThought, ReAct) that can be composed
- **Teleprompters**: Optimization strategies that bootstrap demonstrations automatically
- **Compiler**: Optimizes any DSPy pipeline by simulating versions and collecting traces

**Key Abstractions:**
```python
# Signature: declares WHAT, not HOW
qa = dspy.Predict("question -> answer")

# Module: implements prompting technique
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate_answer(context=context, question=question)
```

**Optimization Results:**
- GPT-3.5: 33% -> 82% improvement without hand-crafted prompts
- llama2-13b-chat: 9% -> 47% improvement

**Implementation Relevance:**
- `prompt_optimizer.py` should adopt DSPy's signature/module pattern
- Replace trial-and-error prompting with compiled demonstrations

---

### 1.4 TextGrad: Automatic Differentiation via Text (arXiv:2406.07496)

**Core Innovation:** Backpropagate textual feedback to optimize compound AI systems

**Key Techniques:**
- **Textual Gradients**: LLM-generated feedback describing how to improve variables
- **Computation Graphs**: Model AI systems as graphs where variables are inputs/outputs
- **PyTorch-like API**: `tg.Variable`, `tg.BlackboxLLM`, `tg.TextLoss`, `tg.TGD`

**Optimization Loop:**
```
Prediction = LLM(Prompt + Question)
Evaluation = LLM(Evaluation Instruction + Prediction)
Gradient = LLM("Criticize the prompt given this evaluation")
Prompt_new = Prompt.apply_gradient(Gradient)
```

**Results:**
- LeetCode-Hard: 20% relative performance gain
- Google-Proof QA: 51% -> 55% zero-shot accuracy

**Implementation Relevance:**
- Use for iterative prompt refinement in `prompt_optimizer.py`
- Collect feedback from REVIEWER to improve CODER prompts

---

### 1.5 LATS: Language Agent Tree Search (arXiv:2310.04406)

**Core Innovation:** Unify reasoning, acting, and planning via Monte Carlo Tree Search

**Key Techniques:**
- **MCTS for LLMs**: Tree search over reasoning/action trajectories
- **LM-Powered Value Function**: `V(s) = λ * LM_score(s) + (1-λ) * self_consistency(s)`
- **Self-Reflection**: Failed trajectories generate reflections for future attempts
- **Environment Feedback**: External signals improve reasoning (unlike pure CoT/ToT)

**LATS Operations:**
1. **Selection**: UCT-based node selection (`UCT(s) = V(s) + w * sqrt(ln(N(p))/N(s))`)
2. **Expansion**: Sample n actions from LM
3. **Evaluation**: Score nodes using LM + self-consistency
4. **Simulation**: Execute until terminal state
5. **Backpropagation**: Update values along path
6. **Reflection**: Generate learnings from failed attempts

**Results:**
- HumanEval: 92.7% pass@1 (state-of-the-art with GPT-4)
- WebShop: +22.1 average score improvement with GPT-3.5

**Implementation Relevance:**
- For complex tasks, explore multiple solution paths before committing
- Store reflections in memory for future attempts

---

## 2. Recommended Role Hierarchy

Based on MetaGPT's SOP patterns and CAMEL's role-playing framework:

```
                    ┌─────────────┐
                    │   PLANNER   │  (Task Decomposition + Strategy)
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌─────────────┐          ┌─────────────┐
       │  ARCHITECT  │          │  RESEARCHER │  (Optional: Info Gathering)
       └──────┬──────┘          └──────┬──────┘
              │                        │
              ▼                        │
       ┌─────────────┐                 │
       │    CODER    │ ◄───────────────┘
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │   REVIEWER  │  (Quality Gate - Mandatory)
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │ DOCUMENTER  │  (Optional: Post-completion)
       └─────────────┘
```

**Role Responsibilities:**

| Role | Input | Output | Quality Gate |
|------|-------|--------|--------------|
| PLANNER | User request | Task breakdown, priority, dependencies | Must be reviewable plan |
| ARCHITECT | Task spec | File structure, interfaces, data flow | Design doc approval |
| CODER | Design + specific task | Code changes | Tests pass |
| REVIEWER | Code changes | Accept/Reject + feedback | Mandatory gate |
| DOCUMENTER | Completed work | Documentation updates | Completeness check |

---

## 3. Communication Protocol Between Workers

### 3.1 Message Structure (MetaGPT-inspired)

```python
@dataclass
class AgentMessage:
    sender: str           # Role name
    receiver: str         # Target role or "broadcast"
    msg_type: str         # "artifact" | "instruction" | "feedback" | "status"
    content: dict         # Structured payload
    artifacts: list       # File paths, code snippets, documents
    timestamp: float
    trace_id: str         # For tracking conversation chains
```

### 3.2 Publish-Subscribe Pattern

```python
class MessagePool:
    def publish(self, message: AgentMessage):
        """Publish to shared pool"""

    def subscribe(self, role: str, msg_types: list[str]) -> list[AgentMessage]:
        """Get relevant messages for a role"""

    def get_context(self, trace_id: str) -> list[AgentMessage]:
        """Get full conversation history for a task"""
```

### 3.3 Handoff Protocol

```
1. SENDER completes work
2. SENDER publishes artifact message with:
   - summary: what was done
   - artifacts: concrete outputs
   - blockers: any issues encountered
   - next_action: suggested next step
3. RECEIVER acknowledges receipt
4. RECEIVER validates artifacts match expected schema
5. If validation fails -> return to SENDER with feedback
6. If validation passes -> RECEIVER begins work
```

### 3.4 Structured Output Schemas (Critical for reliability)

```python
# PLANNER output schema
class PlanOutput:
    tasks: list[Task]
    dependencies: dict[str, list[str]]
    estimated_complexity: str

# CODER output schema
class CodeOutput:
    files_modified: list[str]
    changes_summary: str
    test_status: str  # "passed" | "failed" | "skipped"

# REVIEWER output schema
class ReviewOutput:
    decision: str  # "approve" | "reject" | "request_changes"
    feedback: list[str]
    blocking_issues: list[str]
```

---

## 4. Prompt Optimization Pipeline Design

### 4.1 Architecture (DSPy + TextGrad hybrid)

```
┌──────────────────────────────────────────────────────────────┐
│                    PROMPT OPTIMIZATION PIPELINE               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Collect   │───▶│  Compile    │───▶│   Deploy    │      │
│  │   Traces    │    │  Prompts    │    │   & Test    │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│        │                   │                  │              │
│        ▼                   ▼                  ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Demo      │    │  DSPy       │    │  TextGrad   │      │
│  │   Store     │    │  Telepromp  │    │  Feedback   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 Implementation Steps

**Phase 1: Trace Collection** (current `prompt_optimizer.py`)
```python
class TraceCollector:
    def record(self, signature: str, input: dict, output: dict, success: bool):
        """Store execution trace for later optimization"""

    def get_demos(self, signature: str, k: int = 5) -> list[dict]:
        """Retrieve best demonstrations for a signature"""
```

**Phase 2: DSPy Compilation**
```python
class PromptCompiler:
    def compile(self, signature: str, demos: list[dict], metric: Callable) -> str:
        """
        1. Create DSPy module from signature
        2. Bootstrap demonstrations
        3. Optimize using teleprompter
        4. Return optimized prompt template
        """
```

**Phase 3: TextGrad Refinement**
```python
class PromptRefiner:
    def refine(self, prompt: str, task: str, feedback: str) -> str:
        """
        1. Evaluate current prompt on task
        2. Generate textual gradient (criticism)
        3. Apply gradient to improve prompt
        4. Validate improvement
        """
```

### 4.3 Optimization Loop

```python
def optimize_pipeline(role: str, signature: str):
    # 1. Collect traces from production
    traces = collector.get_traces(role, signature)

    # 2. Filter for successful examples
    demos = [t for t in traces if t.success]

    # 3. DSPy compilation (bootstrap few-shot examples)
    base_prompt = compiler.compile(signature, demos, metric=task_success_rate)

    # 4. TextGrad refinement (iterative improvement)
    for _ in range(MAX_ITERATIONS):
        result = execute(base_prompt, test_task)
        feedback = reviewer.evaluate(result)
        if feedback.score >= THRESHOLD:
            break
        base_prompt = refiner.refine(base_prompt, test_task, feedback.text)

    # 5. Deploy and monitor
    deploy(role, signature, base_prompt)
```

---

## 5. Priority Order for Implementation

### Priority 1: Critical Foundation (Immediate)

1. **Structured Message Protocol**
   - Define `AgentMessage` dataclass
   - Implement `MessagePool` with publish/subscribe
   - Add message validation schemas
   - **Effort:** Medium | **Impact:** High

2. **SOP-Enforced Handoffs**
   - Add mandatory REVIEWER gate between CODER output and completion
   - Define structured output schemas for each role
   - Validate outputs before handoff
   - **Effort:** Medium | **Impact:** High

### Priority 2: Coordination Layer (Short-term)

3. **Role Hierarchy Implementation**
   - Update `roles.py` with clear responsibility chains
   - Implement dependency tracking between tasks
   - Add ARCHITECT role for complex tasks
   - **Effort:** Medium | **Impact:** Medium

4. **Trace Collection Upgrade**
   - Extend `prompt_optimizer.py` to store structured traces
   - Include success/failure signals
   - Store input/output pairs with signatures
   - **Effort:** Low | **Impact:** Medium

### Priority 3: Optimization Pipeline (Medium-term)

5. **DSPy Integration**
   - Define signatures for each role's core operations
   - Implement teleprompter for few-shot optimization
   - Add compilation step to deployment pipeline
   - **Effort:** High | **Impact:** High

6. **TextGrad Feedback Loop**
   - Collect REVIEWER feedback systematically
   - Implement gradient generation from feedback
   - Create prompt refinement loop
   - **Effort:** High | **Impact:** Medium

### Priority 4: Advanced Planning (Long-term)

7. **LATS for Complex Tasks**
   - Implement tree search for multi-step plans
   - Add value function for plan evaluation
   - Store reflections for learning from failures
   - **Effort:** Very High | **Impact:** High (for complex tasks)

---

## 6. Quick Wins (Implement Today)

1. **Add message schema validation** - prevents garbage-in-garbage-out
2. **Make REVIEWER mandatory** - catches errors before they propagate
3. **Log all inter-agent messages** - enables trace collection for optimization
4. **Define explicit signatures** - `"task_description -> code_changes"` not free-form

---

## References

- CAMEL: arXiv:2303.17760 - https://github.com/camel-ai/camel
- MetaGPT: arXiv:2308.00352 - https://github.com/geekan/MetaGPT
- DSPy: arXiv:2310.03714 - https://github.com/stanfordnlp/dspy
- TextGrad: arXiv:2406.07496 - https://github.com/zou-group/textgrad
- LATS: arXiv:2310.04406 - https://github.com/lapisrocks/LanguageAgentTreeSearch
