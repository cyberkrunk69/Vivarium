# Strategy Document: Waves 12-16

## Current State Assessment

### Capabilities Built (11 Waves Completed)

| Category | Module | Status | Paper Source |
|----------|--------|--------|--------------|
| Memory Synthesis | `memory_synthesis.py` | Complete | Generative Agents |
| Prompt Optimization | `prompt_optimizer.py` | Complete | DSPy |
| Skill Registry | `skills/skill_registry.py` | Complete | Voyager |
| Role Decomposition | `roles.py` | Complete | CAMEL |
| SOP Execution | `sop_executor.py` | Complete | MetaGPT |
| Episodic Memory | `utils/reflection.py` | Complete | Reflexion |
| Tree Search | `tree_search.py` | **Partial** | LATS |
| Critic System | `critic.py` | Complete | LATS/TextGrad |
| Knowledge Graph | `knowledge_graph.py` | **Partial** | HippoRAG |
| Performance Tracking | `performance_tracker.py` | Complete | Custom |
| Improvement Suggester | `improvement_suggester.py` | Complete | Custom |
| Message Pool | `message_pool.py` | Complete | MetaGPT |
| Lesson Recording | `lesson_recorder.py` | Complete | Custom |

### Key Metrics
- **Total sessions**: 16+ across 11 waves
- **Success rate**: 100% (no failures)
- **Code reduction**: 33% (grind_spawner 1617→1073 LOC)
- **Dead code removed**: 300+ LOC (brain.py, autopilot.py, simple_loop.py)
- **Total API cost**: ~$0.92

---

## Gap Analysis: What's Missing?

### Critical Gaps (High Impact, Blocking Other Features)

1. **Tree Search Not Fully Wired**
   - `tree_search.py` has `expand_node()` and `evaluate_node()` but they're stubs
   - No integration with grind_spawner's main execution loop
   - **Impact**: Can't explore alternative solutions, stuck with first attempt

2. **Knowledge Graph Disconnected**
   - `knowledge_graph.py` exists but not wired to retrieval pipeline
   - No automatic population during grind sessions
   - **Impact**: Can't leverage concept relationships for better context

3. **Critic Feedback Loop Incomplete**
   - `critic.py` can score code but results aren't fed back to retry
   - No automatic iteration on low-quality output
   - **Impact**: First-draft code accepted without refinement

4. **DSPy Demonstrations Not Persistent**
   - Demonstrations collected but may not persist between sessions
   - No automatic curation of best examples
   - **Impact**: 25-65% DSPy improvement not fully realized

### Secondary Gaps (Important, Not Blocking)

5. **No Embedding-Based Retrieval**
   - Skill/lesson retrieval still keyword-based
   - Semantic similarity would improve context injection
   - **Impact**: Suboptimal context selection

6. **Integration Tests Missing**
   - Unit tests exist but no end-to-end validation
   - **Impact**: Regressions not caught early

7. **Self-Curriculum Not Started**
   - AI can't design its own training tasks
   - **Impact**: Human bottleneck for task generation

8. **Tool Creation Not Started**
   - AI can't create new tools for itself
   - **Impact**: Limited to predefined capabilities

---

## Prioritized Roadmap: Waves 12-16

### Wave 12: Complete the Feedback Loops
**Theme**: Close open feedback circuits so improvements compound

| Task | Why | Enables |
|------|-----|---------|
| Wire critic.py into retry loop | Low-quality code gets refined | Higher quality first-time outputs |
| Persist DSPy demonstrations to JSON | Best examples survive sessions | Consistent 25-65% improvement |
| Wire performance_tracker → improvement_suggester | Automatic insight generation | Self-directed improvement |

### Wave 13: Knowledge Infrastructure
**Theme**: Build semantic retrieval foundation

| Task | Why | Enables |
|------|-----|---------|
| Implement embedding-based skill retrieval | Better context = better outputs | Smarter skill injection |
| Wire knowledge_graph to main flow | Concept relationships available | Richer context understanding |
| Add KG auto-population during sessions | Graph grows automatically | Compounding knowledge |

### Wave 14: Multi-Path Exploration
**Theme**: Don't accept first solution

| Task | Why | Enables |
|------|-----|---------|
| Implement real tree_search expand/evaluate | Multiple solution branches | Better solution selection |
| Add beam search with critic scoring | Keep top-N candidates | Robust to local minima |
| Integration tests for tree search | Ensure exploration works | Reliable experimentation |

### Wave 15: Self-Directed Learning
**Theme**: AI chooses what to learn

| Task | Why | Enables |
|------|-----|---------|
| Implement self-curriculum generation | AI designs own training tasks | Removes human bottleneck |
| Meta-learning from lesson patterns | AI learns how to learn | Faster improvement velocity |
| Automatic task decomposition tuning | Better complexity splitting | More efficient execution |

### Wave 16: Tool Creation & Emergence
**Theme**: AI extends its own capabilities

| Task | Why | Enables |
|------|-----|---------|
| Tool creation framework | AI can write new tools | Unbounded capability growth |
| Skill composition engine | Combine simple → complex | Emergent behaviors |
| Multi-task parallel execution | Work on N improvements at once | Higher throughput |

---

## Task Definitions (Ready for grind_tasks.json)

### Wave 12 Tasks

```json
[
  {
    "task": "FEEDBACK LOOP: Critic Retry Integration\n\nWire critic.py into grind_spawner's execution loop:\n\n1. After worker completes, call critic.review() on output\n2. If quality_score < 0.7, inject feedback and retry (max 2 retries)\n3. Log quality scores to performance_tracker\n\nEdit grind_spawner.py to add retry logic. Test with intentionally bad output.",
    "budget": 1.0,
    "model": "sonnet"
  },
  {
    "task": "PERSISTENCE: DSPy Demonstration Storage\n\nAdd demonstration persistence to prompt_optimizer.py:\n\n1. Add save_demonstrations(filepath) method\n2. Add load_demonstrations(filepath) method  \n3. Auto-save after collecting new demos\n4. Auto-load at startup\n\nUse JSON format matching existing schema.",
    "budget": 1.0,
    "model": "sonnet"
  },
  {
    "task": "INTEGRATION: Performance → Improvement Loop\n\nWire performance_tracker.py to improvement_suggester.py:\n\n1. After each wave, call suggester.generate_full_report(tracker)\n2. Save report to improvement_reports/wave_N.json\n3. Feed top suggestion into next wave's task selection\n\nEdit grind_spawner.py to add post-wave analysis.",
    "budget": 1.0,
    "model": "sonnet"
  }
]
```

### Wave 13 Tasks

```json
[
  {
    "task": "EMBEDDINGS: Semantic Skill Retrieval\n\nAdd embedding-based retrieval to skill_registry.py:\n\n1. Add compute_embedding(text) using simple TF-IDF or hash\n2. Add find_similar_skills(query, top_k=3) method\n3. Replace keyword matching with cosine similarity\n\nNote: Use lightweight embeddings (no external API calls).",
    "budget": 1.0,
    "model": "sonnet"
  },
  {
    "task": "KNOWLEDGE GRAPH: Wire to Main Flow\n\nIntegrate knowledge_graph.py into grind_spawner.py:\n\n1. Load/initialize KG at startup\n2. Call kg.populate_from_codebase() once per wave\n3. In prompt building, inject kg.query_related(task_category) context\n4. Save KG state after wave\n\nEdit grind_spawner.py to add KG integration.",
    "budget": 1.5,
    "model": "sonnet"
  },
  {
    "task": "KNOWLEDGE GRAPH: Session Auto-Population\n\nExtend knowledge_graph.py to capture session learnings:\n\n1. Add add_lesson_node(lesson_dict) method\n2. Add link_lesson_to_concepts(lesson_id) method\n3. Call after each successful task completion\n\nTest with sample lessons from learned_lessons.json.",
    "budget": 1.0,
    "model": "sonnet"
  }
]
```

### Wave 14 Tasks

```json
[
  {
    "task": "TREE SEARCH: Implement Real Expansion\n\nFix tree_search.py expand_node() to generate actual branches:\n\n1. Given a node, generate 2-3 alternative approaches\n2. Each child node has different prompt/strategy\n3. Use simple heuristics, not LLM calls for generation\n\nReplace TODO stubs with real implementation.",
    "budget": 1.5,
    "model": "sonnet"
  },
  {
    "task": "TREE SEARCH: Implement Real Evaluation\n\nFix tree_search.py evaluate_node() to score solutions:\n\n1. Call critic.review() on node's output\n2. Return quality_score as evaluation\n3. Cache evaluations to avoid re-computation\n\nWire to critic.py for scoring.",
    "budget": 1.0,
    "model": "sonnet"
  },
  {
    "task": "TREE SEARCH: Beam Search with Critic\n\nAdd beam search to tree_search.py:\n\n1. Add beam_search(root, beam_width=3, max_depth=3)\n2. Keep top beam_width nodes at each level\n3. Use UCB score for selection\n4. Return best path\n\nTest with synthetic tree.",
    "budget": 1.5,
    "model": "sonnet"
  },
  {
    "task": "INTEGRATION TESTS: Tree Search Flow\n\nAdd tests/test_tree_search_integration.py:\n\n1. Test expand → evaluate → select cycle\n2. Test beam search with mock critic\n3. Test run_tree_search end-to-end\n\nEnsure exploration actually improves output selection.",
    "budget": 1.0,
    "model": "sonnet"
  }
]
```

### Wave 15 Tasks

```json
[
  {
    "task": "SELF-CURRICULUM: Task Generator\n\nCreate curriculum_generator.py:\n\n1. Analyze learned_lessons.json for weak areas (low success categories)\n2. Generate training tasks targeting weak areas\n3. Output tasks in grind_tasks.json format\n\nClass: CurriculumGenerator with generate_tasks(n=5) method.",
    "budget": 1.5,
    "model": "sonnet"
  },
  {
    "task": "META-LEARNING: Pattern Extractor\n\nCreate meta_learner.py:\n\n1. Analyze improvement_reports/ for patterns\n2. Identify which improvement strategies worked\n3. Update learned_lessons.json with meta-lessons\n\nFocus on: what makes a task succeed vs fail?",
    "budget": 1.5,
    "model": "sonnet"
  },
  {
    "task": "ADAPTIVE: Complexity Tuning\n\nAdd adaptive complexity to roles.py:\n\n1. Track PLANNER accuracy (did decomposition match actual work?)\n2. Adjust simple/complex threshold based on history\n3. Log threshold changes to performance_tracker\n\nStart with threshold=2, adjust ±0.5 based on feedback.",
    "budget": 1.0,
    "model": "sonnet"
  }
]
```

### Wave 16 Tasks

```json
[
  {
    "task": "TOOL CREATION: Framework\n\nCreate tool_factory.py:\n\n1. Define ToolSpec dataclass (name, description, parameters, implementation)\n2. Add generate_tool(capability_description) method\n3. Add register_tool(tool_spec) to make available\n4. Persist tools to tools/custom/\n\nAI can now create tools for itself.",
    "budget": 2.0,
    "model": "sonnet"
  },
  {
    "task": "SKILL COMPOSITION: Engine\n\nExtend skill_registry.py with composition:\n\n1. Add compose_skills(skill_ids: List[str]) method\n2. Generate combined skill from primitives\n3. Add dependency resolution\n4. Register composed skill\n\nEnable simple → complex skill building.",
    "budget": 1.5,
    "model": "sonnet"
  },
  {
    "task": "MULTI-TASK: Parallel Execution\n\nExtend grind_spawner.py for multi-task:\n\n1. Add spawn_parallel_workers(tasks: List[Dict], max_concurrent=3)\n2. Track all workers in shared state\n3. Aggregate results and lessons\n4. Handle partial failures gracefully\n\nEnable working on N improvements simultaneously.",
    "budget": 2.0,
    "model": "sonnet"
  }
]
```

---

## Compound Improvement Analysis

### Dependency Graph

```
Wave 12 (Feedback Loops)
    ↓
Wave 13 (Knowledge Infrastructure) ← enables semantic retrieval
    ↓
Wave 14 (Multi-Path Exploration) ← uses knowledge + critic
    ↓
Wave 15 (Self-Directed Learning) ← uses patterns from exploration
    ↓
Wave 16 (Tool Creation) ← self-directed learning identifies needed tools
```

### Key Enablers

1. **Critic retry loop (Wave 12)** → Every subsequent wave produces higher quality code
2. **Knowledge graph (Wave 13)** → Every subsequent wave has richer context
3. **Tree search (Wave 14)** → Exploration beats single-path execution
4. **Self-curriculum (Wave 15)** → Removes human bottleneck for task generation
5. **Tool creation (Wave 16)** → Unbounded capability growth

### Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Embedding quality | Use TF-IDF first, upgrade later |
| Tree search explosion | Limit beam width and depth |
| Self-curriculum drift | Human review of generated tasks |
| Tool creation bugs | Sandbox new tools, critic review |

---

## Success Metrics for Waves 12-16

| Wave | Success Criteria |
|------|------------------|
| 12 | Critic retry reduces avg quality score gap by 20% |
| 13 | KG queries return relevant context in 80% of cases |
| 14 | Tree search finds better solution than first attempt in 30% of tasks |
| 15 | Self-generated curriculum tasks have 70% success rate |
| 16 | AI creates 1+ useful tool autonomously |

---

*Generated: 2026-02-03*
*Author: PLANNER role (Wave 11 Strategic Planning)*
