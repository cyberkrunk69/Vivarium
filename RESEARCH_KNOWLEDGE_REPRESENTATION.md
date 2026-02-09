# Research: Knowledge Representation for AI Agents

## Executive Summary

This codebase implements a sophisticated multi-layered knowledge representation system for autonomous AI agents. Drawing from multiple research papers (Voyager, CAMEL, Generative Agents, HippoRAG, DSPy, LATS/TextGrad), it demonstrates practical approaches to storing, retrieving, synthesizing, and transferring knowledge across agent tasks.

---

## 1. Current Knowledge Structures

### 1.1 Knowledge Graph (knowledge_graph.py)

**Architecture:**
- **Nodes**: Typed entities with `id`, `label`, `type`, and `properties`
- **Edges**: Typed relationships connecting nodes
- **Adjacency List**: Fast neighbor lookup via `Dict[str, List[Tuple[str, EdgeType]]]`

**Node Types (NodeType Enum):**
| Type | Purpose |
|------|---------|
| CONCEPT | Abstract ideas, technical concepts |
| SKILL | Learned capabilities, classes |
| LESSON | Recorded learnings from tasks |
| FILE | Source code files in codebase |
| FUNCTION | Callable functions |
| SOLUTION_PATH | Exploration strategies |

**Edge Types (EdgeType Enum):**
| Type | Semantics |
|------|-----------|
| RELATES_TO | General conceptual link |
| IMPLEMENTS | Code implements concept |
| USES | Dependency relationship |
| DEPENDS_ON | Prerequisite relationship |
| CONTAINS | Hierarchical containment |
| EXPLORED_BY | Path explored this concept |
| RECOMMENDED_FOR | Suggested for task type |

**Key Capabilities:**
1. **Auto-population from codebase**: `populate_from_codebase()` scans Python files, extracts functions/classes, creates FILE/FUNCTION nodes with CONTAINS edges
2. **Concept extraction**: `extract_concepts()` uses regex patterns for technical terms, code patterns, quoted strings, arXiv references
3. **Subgraph queries**: `query_related(node_id, depth)` performs BFS to retrieve connected subgraphs
4. **Path-outcome linking**: `link_path_to_outcomes()` connects solution paths to quality scores and task types

**Observation:** The graph structure is well-typed but relatively shallow in practice. Most queries return nodes within 2-hop distance. The graph excels at structural relationships (file contains function) but underutilizes semantic edges.

---

### 1.2 Lessons (learned_lessons.json + memory_synthesis.py)

**Lesson Schema:**
```json
{
  "id": "lesson_001",
  "task_category": "code_analysis",
  "lesson": "Always read files before proposing changes",
  "trial_number": 1,
  "task_feedback": "Error: suggested changes to unread file content",
  "self_verification": true,
  "retrieval_cues": ["file_modification", "code_changes"],
  "timestamp": "2026-02-03",
  "importance": 4,
  "embedding": {"always": 0.166, "read": 0.166, ...}
}
```

**Key Fields:**
- `importance`: 1-10 scale (1=mundane, 10=significant)
- `embedding`: Pre-computed TF-IDF term frequencies
- `retrieval_cues`: Semantic tags for matching
- `key_insights`: List of actionable learnings
- `source`: Paper citation (e.g., "arXiv:2310.03714")

**Lesson Categories Observed:**
- `code_analysis`, `error_handling`, `planning`, `efficiency`
- `role_based_decomposition`, `memory_synthesis`, `prompt_optimization`
- `skill_composition`, `quality_assurance`, `task_classification`

**Synthesis Mechanism (MemorySynthesis):**
1. **Importance scoring**: Combines LLM rating (50%), frequency (15%), recency (20%), success (15%)
2. **Reflection generation**: Groups high-importance lessons, extracts common themes, creates higher-level insights
3. **Reflection types**: `level_1_pattern` (single category) vs `level_2_principle` (cross-category)
4. **Pruning**: Removes lessons subsumed by reflections via deduplication

**Trigger Conditions for Synthesis:**
- Every N sessions (default: 5)
- After any failure (immediate learning)
- When lesson count exceeds threshold (50)
- Explicit request via CLI flag

---

### 1.3 Skills (skills/skill_registry.py)

**Skill Schema:**
```json
{
  "name": "import_config_constants",
  "code": "# Executable Python code...",
  "description": "Centralizes configuration imports",
  "preconditions": ["config module exists", "constants defined"],
  "postconditions": ["constants imported", "no magic strings"]
}
```

**Design Principles (from Voyager arXiv:2305.16291):**
1. **Temporally Extended**: Multi-step patterns, not single actions
2. **Interpretable**: Clear pre/postconditions
3. **Compositional**: Skills combine to solve larger problems

**Built-in Skills:**
| Skill | Purpose |
|-------|---------|
| `import_config_constants` | Centralize config imports |
| `migrate_to_utils` | Extract repeated patterns to utils |
| `add_test_coverage` | Comprehensive test patterns |

**Skill Composition:**
```python
def compose_skills(skill_list):
    # Merges code, descriptions, pre/postconditions
    # Returns composite skill with merged metadata
```

**Automatic Skill Extraction (skill_registry_extraction.py):**
- Triggers when: `quality_score >= 0.9`, `returncode == 0`, `self_verified == True`
- Extracts code blocks from session output
- Registers with `learned_{task_name}` naming convention

---

## 2. Retrieval Effectiveness

### 2.1 Retrieval Methods Compared

| Method | Implementation | Strengths | Weaknesses |
|--------|---------------|-----------|------------|
| **TF-IDF** | `TfidfVectorizer(analyzer='char', ngram_range=(2,3))` | Fast, no external deps, handles typos | Misses semantic similarity |
| **Keyword Matching** | Exact/substring match on terms | Deterministic, explainable | Misses synonyms, context |
| **Graph Traversal** | BFS with depth limit | Captures relationships | Computationally expensive at scale |
| **Query Expansion** | Synonym/abbreviation mapping | Improves recall | Can reduce precision |

### 2.2 Query Expansion System (query_expander.py)

**Expansion Sources:**
1. **TECHNICAL_SYNONYMS**: `"error" -> ["exception", "failure", "bug", "issue"]`
2. **ABBREVIATIONS**: `"kg" -> "knowledge graph"`, `"dspy" -> "dspy prompt optimization"`
3. **RELATED_TERMS**: `"skill" -> ["voyager", "composition", "registry", "reuse"]`

**Expansion Process:**
```python
def expand_query(query: str) -> List[str]:
    # 1. Add original significant words (len > 2)
    # 2. Expand abbreviations
    # 3. Add synonyms
    # 4. Add related technical terms
    # 5. Extract quoted phrases (exact match)
    # 6. Extract arXiv references
    # 7. Deduplicate
```

### 2.3 Unified Context Builder (context_builder.py)

**Integration Point for All Retrieval:**
```python
builder = ContextBuilder()
builder.add_skills(query, top_k=3)    # TF-IDF + keyword fallback
builder.add_lessons(query, top_k=3)   # Importance-weighted similarity
builder.add_kg_context(query, depth=2) # Graph traversal
context = builder.build()
```

**Retrieval Scoring (HippoRAG pattern):**
```
relevance = importance_weight * 0.4 + embedding_similarity * 0.6
```

### 2.4 What Gets Retrieved vs What Should Be

**Current Retrieval Behavior:**
- **Skills**: Matches on character n-grams, favors exact term overlap
- **Lessons**: Importance-biased, recency-boosted
- **KG Concepts**: String matching on node labels

**Gaps Identified:**

1. **Semantic Understanding**: TF-IDF cannot capture "refactoring" is similar to "code cleanup" without explicit mapping

2. **Cross-domain Transfer**: A lesson about "error handling in API calls" won't match queries about "exception management in HTTP requests" without synonym expansion

3. **Negative Knowledge**: System doesn't strongly surface "don't do X" patterns from failure_patterns.json during retrieval

4. **Temporal Relevance**: Old high-importance lessons persist even when superseded by newer patterns

5. **Structural Context**: Graph knows `file:critic.py CONTAINS func:review` but retrieval doesn't use this for "find code review functions"

---

## 3. Knowledge Decay and Refresh

### 3.1 Current Decay Mechanisms

**Archival (memory_synthesis.py:archive_unused):**
```python
def archive_unused(self) -> int:
    # Archives lessons with:
    # - retrieval_count < 1
    # - older than 30 days
```

**Limitation:** Binary threshold (30 days) regardless of domain relevance.

### 3.2 Implicit Staleness Indicators

| Signal | Current Use | Gap |
|--------|-------------|-----|
| `retrieval_count` | Archival threshold | Not used in ranking |
| `timestamp` | Recency scoring (20%) | Fixed decay rate |
| Lesson supersession | Reflection pruning | Only exact duplicates |

### 3.3 What's Missing: Versioning and Evolution

**No Current Support For:**
1. **Skill versioning**: Updated skill replaces old one without history
2. **Lesson conflict resolution**: Contradictory lessons coexist
3. **Deprecation marking**: No "this pattern is obsolete" flag
4. **Confidence decay**: All lessons maintain original importance

**Potential Improvements:**

1. **Exponential Decay**: `effective_importance = base_importance * decay^(days_old / half_life)`

2. **Contradiction Detection**: Flag when new lesson contradicts existing with similar retrieval_cues

3. **Usage-based Refresh**: Successful retrieval resets "freshness clock"

4. **Semantic Versioning for Skills**: `import_config_constants@2.0` with changelog

---

## 4. Cross-Domain Transfer

### 4.1 Current Transfer Mechanisms

**4.1.1 Path Knowledge Transfer (path_knowledge_transfer.py)**

Thread-safe discovery sharing between parallel execution paths:

```python
@dataclass
class Discovery:
    path_id: str
    discovery_type: str  # 'skill', 'pattern', 'insight', 'error_solution'
    content: Any
    quality_impact: Optional[float]
    metadata: Optional[Dict[str, Any]]
```

**Transfer Statistics Tracked:**
- Total discoveries
- Contribution by path
- Quality improvements attributed to transfer

**4.1.2 Failure Pattern Transfer (failure_patterns.py)**

```python
def check_failure_patterns(task_description, task_characteristics):
    # Returns:
    # - similar_failures (similarity > 0.6)
    # - warning_level: high/medium/low/none
    # - suggested_strategies (avoid X, watch for Y)
```

**Similarity Scoring:**
```
combined_score = text_similarity * 0.7 + characteristic_overlap * 0.3
```

### 4.2 Abstraction Levels

The system operates at multiple abstraction levels:

| Level | Example | Storage |
|-------|---------|---------|
| **Concrete** | "Use `try-except` around `json.load()`" | Skills (code) |
| **Pattern** | "Always handle file I/O errors" | Lessons |
| **Principle** | "Defensive programming prevents silent failures" | Reflections (level_2) |
| **Meta** | "Patterns spanning multiple categories are more valuable" | Implicit in synthesis thresholds |

### 4.3 Meta-Knowledge (Knowledge About Knowledge)

**Explicit Meta-Knowledge:**
1. **Importance scoring rules**: Which keywords indicate high-value lessons
2. **Synthesis thresholds**: When to consolidate (sum > 150)
3. **Composition rules**: How skills combine

**Implicit Meta-Knowledge:**
1. **Query expansion mappings**: Codified domain expertise about synonyms
2. **Retrieval_cues design**: Human-curated tags for semantic matching
3. **Category taxonomy**: The `task_category` vocabulary itself

**Gap:** No mechanism to learn new meta-knowledge. The synonym mappings, importance keywords, and category taxonomy are hard-coded rather than learned from experience.

---

## 5. Research Findings and Implications

### 5.1 Strengths of Current System

1. **Multi-source Integration**: ContextBuilder unifies skills, lessons, and graph into coherent prompt context

2. **Research-grounded Design**: Clear citation trail (Voyager, CAMEL, Generative Agents) provides theoretical foundation

3. **Compositional Skills**: Voyager-inspired skill composition enables capability compounding

4. **Self-verification**: Prevents false positives in autonomous learning

5. **Failure Learning**: Dedicated failure pattern detection prevents repeat mistakes

### 5.2 Identified Limitations

1. **Semantic Gap**: TF-IDF/keyword retrieval misses conceptual similarity without extensive synonym engineering

2. **Shallow Graph Usage**: Knowledge graph stores structure but retrieval rarely exploits multi-hop reasoning

3. **Fixed Decay Rates**: No domain-specific or usage-adaptive knowledge aging

4. **No Transfer Learning**: Each lesson is independent; no mechanism to abstract patterns across domains

5. **Missing Negative Examples**: Skills are all "do this"; no "don't do this" skill type

### 5.3 Recommendations for Future Research

1. **Embedding Upgrade**: Replace TF-IDF with sentence transformers for semantic retrieval
   - Trade-off: Latency and dependency on external models

2. **Graph-Enhanced Retrieval**: Use graph structure in retrieval scoring
   - Example: Boost lessons connected to currently-active FILE nodes

3. **Adaptive Importance**: Learn importance weights from downstream task success
   - Currently: Fixed 50%/15%/20%/15% weights
   - Proposed: Meta-learn weights from retrieval->task_success correlation

4. **Contradiction Resolution**: Detect and resolve conflicting lessons
   - Method: Cluster similar lessons, flag divergent recommendations

5. **Skill Negative Space**: Add anti-patterns as first-class citizens
   - Example: `avoid_magic_strings` skill with failure examples

6. **Cross-Category Transfer**: Explicitly model concept transfer
   - Example: "Error handling in X" lessons should inform "Error handling in Y"

---

## 6. Appendix: Key Files Reference

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `knowledge_graph.py` | Graph structure and queries | `KnowledgeGraph`, `KnowledgeNode`, `KnowledgeEdge` |
| `learned_lessons.json` | Persistent lesson storage | JSON array of lesson objects |
| `memory_synthesis.py` | Lesson retrieval and synthesis | `MemorySynthesis.synthesize()`, `compute_importance()` |
| `lesson_recorder.py` | Lesson creation interface | `record_lesson()` |
| `skills/skill_registry.py` | Skill storage and retrieval | `SkillRegistry`, `find_similar_skills()` |
| `context_builder.py` | Unified retrieval interface | `ContextBuilder.build()` |
| `query_expander.py` | Query enhancement | `expand_query()` |
| `path_knowledge_transfer.py` | Cross-path sharing | `SharedPathContext`, `Discovery` |
| `failure_patterns.py` | Failure learning | `FailurePatternDetector` |

---

## 7. Conclusion

This system represents a practical implementation of agentic knowledge representation, drawing from state-of-the-art research. The multi-layered approach (graph + lessons + skills) provides complementary retrieval mechanisms, while the synthesis pipeline enables emergent higher-order patterns.

The primary limitation is the semantic gap in retrieval, addressable with embedding upgrades. The secondary limitation is the static nature of meta-knowledge, requiring human curation of synonyms and importance heuristics.

Future work should focus on:
1. Learning retrieval weights from task outcomes
2. Deeper integration of graph structure into retrieval
3. Explicit modeling of knowledge contradictions and obsolescence

---

*Research conducted: 2026-02-03*
*Codebase: claude_parasite_brain_suck*
