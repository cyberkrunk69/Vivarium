# Architecture Diagrams - Recovered from Chat Session

## 1. Unified Inference Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     UNIFIED INFERENCE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐                    ┌──────────────────┐    │
│  │    GROQ     │  ←── Fast work ───  │  TOGETHER AI     │    │
│  │  (Workers)  │                     │  (Thinkers)      │    │
│  ├─────────────┤                     ├──────────────────┤    │
│  │ GPT-OSS 120B│                     │ DeepSeek R1      │    │
│  │ Gemma 3N    │                     │ Kimi K2 Thinking │    │
│  │ (sweeper)   │                     │ GPT-OSS 20B      │    │
│  └─────────────┘                     │ (verifier)       │    │
│                                      └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 2. Task Execution Flow

```
Task arrives
    ↓
[Worker] executes on Groq (fast, cheap)
    ↓
[Critic] verifies on Together (smart, cheap verifier model)
    ↓
APPROVE → mark complete
REJECT → mark failed, don't checkpoint
MINOR_ISSUES → complete + log for cleanup
```

## 3. Observer Pattern

```
Worker executes task ($0.001)
    ↓
Observer verifies ($0.0005 with cheap model)
    ↓
APPROVE → done
REJECT → requeue with feedback
MINOR_ISSUES → done + cleanup task
```

## 4. Node Graph Architecture

```
[Router] → picks model tier based on task
    ↓
[Planner] → breaks complex task into steps (optional)
    ↓
[Worker] → executes task (GPT-OSS 120B)
    ↓
[Critic/Verifier] → checks if output is good (GPT-OSS 20B)
    ↓
[Orchestrator] → manages the whole flow
```

Basic node flow:
```
[Node] → [Node] → [Node]
           ↓
        [Node]
```

## 5. PII Stripper / Trust Boundary Architecture

```
┌─────────────────────────────────────────────┐
│              CLOUD (untrusted)              │
│                                             │
│  Sees: "find folders for girlfriend_name_1" │
│  Returns: tool code + instructions          │
│  Never sees: "Jessica", your file paths     │
└─────────────────────────────────────────────┘
                    ▲ stripped
                    │
            ┌───────┴───────┐
            │  EDGE MODEL   │  ← runs on YOUR cpu
            │  (trust gate) │
            └───────┬───────┘
                    │ rehydrated
                    ▼
┌─────────────────────────────────────────────┐
│              LOCAL (trusted)                │
│                                             │
│  Has: "Jessica", C:\Users\you\Pictures\...  │
│  Executes: tool locally                     │
│  Results: stay local or get stripped        │
└─────────────────────────────────────────────┘
```

## 6. Tool-First Problem Solving Hierarchy

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

## 7. LLM Efficiency Anti-Pattern vs Good Pattern

```
BAD:  User asks for dir → LLM generates dir command → runs → returns
      (costs tokens every time, sometimes fails)

GOOD: User asks for dir → LLM ONCE creates get_dir.py → tool stored
      Next time: User asks for dir → tool lookup → run get_dir.py
      (costs nothing, always works)
```

## 8. Model Tier Matrix

| Role | Model | Price (in/out) | Use Case |
|------|-------|----------------|----------|
| **Reasoner** | DeepSeek R1-0528 | $3.00/$7.00 | Complex planning, architecture decisions |
| **Thinker** | Kimi K2 Thinking | $1.20/$4.00 | Multi-step reasoning, debugging |
| **Coder** | Qwen3 Coder Next 79.7B | $0.50/$1.20 | Code generation, refactoring |
| **Worker** | GPT-OSS 120B | $0.15/$0.60 | General tasks - default |
| **Verifier** | GPT-OSS 20B | $0.05/$0.20 | Observer pattern verification |
| **Sweeper** | Gemma 3N E4B | $0.02/$0.04 | Ultra-cheap cleanup |
| **Guard** | Llama Guard 4 12B | $0.20 | Safety checks |

## 9. Autonomy Taxonomy

| Term | Autonomy | Description |
|------|----------|-------------|
| **Model** | None | Raw LLM inference. Input → output. No decisions. |
| **Tool** | None | A capability (file read, web search). Called by something else. |
| **Worker** | Low | Given a task, executes it, returns result. No self-direction. |
| **Agent** | High | Has goals, decides actions, uses tools, can loop until done. |

## 10. Function Taxonomy

| Term | Function |
|------|----------|
| **Router** | Classifies input, picks which path/model to use |
| **Planner** | Decomposes complex task into steps |
| **Executor** | Runs a single step/action |
| **Critic** | Evaluates output quality (from RL actor-critic) |
| **Verifier** | Checks correctness (from formal methods) |
| **Judge** | Scores/ranks outputs (LLM-as-judge pattern) |
| **Orchestrator** | Coordinates flow between components |

## 11. Knowledge Base Stats

```
╔═══════════════════════════════════════════════════════════════════╗
║                    KNOWLEDGE BASE STATS                            ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  AI/ML RESEARCH                                                   ║
║  ├── Categories: 29                                               ║
║  ├── Files: 614                                                   ║
║  ├── Size: 715 MB                                                 ║
║  │                                                                ║
║  │   agent_architectures ........... 30 papers                   ║
║  │   code_generation ............... 24 papers                   ║
║  │   efficiency_inference .......... 30 papers                   ║
║  │   embeddings_representations .... 30 papers                   ║
║  │   finetuning_methods ............ 30 papers                   ║
║  │   hallucination_factuality ...... 30 papers                   ║
║  │   long_context_memory ........... 30 papers                   ║
║  │   model_compression ............. 30 papers                   ║
║  │   multimodal_vision ............. 30 papers                   ║
║  │   rag_retrieval ................. 27 papers                   ║
║  │   reasoning_foundations ......... 27 papers                   ║
║  │   security_adversarial .......... 30 papers                   ║
║  │   self_evolving_agents .......... 6 papers                    ║
║  │   tool_use ...................... 15 papers                   ║
║  │   world_models_reasoning ........ 30 papers                   ║
║  │   ... and 14 more categories                                  ║
║                                                                    ║
║  UI/UX RESEARCH                                                   ║
║  ├── Categories: 17                                               ║
║  ├── Files: 1,860                                                 ║
║  ├── Size: 35 MB                                                  ║
║                                                                    ║
║  TOTAL: ~2,500 files, ~750 MB of curated knowledge               ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 12. RLIF - Rule Verification with Meta-Learning

### Rule Verification Node

```
┌─────────────────────────────────────────────────────────────────────┐
│                       RULE VERIFIER NODE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Proposed Rule arrives                                               │
│         ↓                                                            │
│  Safety Checks:                                                      │
│  ├── Does this enable unauthorized actions?                         │
│  ├── Does this bypass human oversight?                              │
│  ├── Does this expand scope beyond user intent?                     │
│  ├── Is this exploitable via prompt injection?                      │
│  ├── Does it conflict with safety constraints?                      │
│  └── Is scope properly bounded?                                     │
│         ↓                                                            │
│  PASS → Store rule                                                   │
│  FAIL → Reject + extract meta-rule + improve generator              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Meta-Learning Flow (Teaching the Teacher)

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

### The Compound Effect

```
WITHOUT Meta-Learning:
  Bad rule → reject → regenerate → maybe bad → reject → loop → expensive

WITH Meta-Learning:
  Bad rule → reject → extract meta-rule → future rules born better → one-shot
```

**Key Insight**: The correction itself is training data. Don't throw it away.

---

*Recovered from chat session 88cbd38b-d19e-4ca3-96b0-a7957b57b3b8 on 2026-02-03*
