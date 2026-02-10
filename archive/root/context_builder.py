"""
Unified Context Builder - Single interface for all retrieval needs

Combines skill retrieval, lesson retrieval, and knowledge graph context
into one coherent context string for prompt injection.

Implements retrieval from:
- skills/skill_registry.py (Voyager skill library)
- lesson_recorder.py (learned lessons)
- knowledge_graph.py (concept relationships)
"""

import json
from pathlib import Path
from typing import List, Optional
from skills.skill_registry import SkillRegistry
from knowledge_graph import KnowledgeGraph, NodeType
from memory_synthesis import MemorySynthesis

# Optional UI/UX knowledge loader
try:
    from uiux_knowledge_loader import get_uiux_loader, UIUXKnowledgeLoader
    UIUX_AVAILABLE = True
except ImportError:
    UIUX_AVAILABLE = False


class ContextBuilder:
    """
    Unified retrieval interface for all context types.

    Usage:
        builder = ContextBuilder()
        builder.add_founding_memory()  # Identity and values foundation
        builder.add_skills(query="implement tests", top_k=3)
        builder.add_lessons(query="error handling", top_k=3)
        builder.add_kg_context(query="DSPy optimization", depth=2)
        context_string = builder.build()
    """

    def __init__(self, workspace: str = "."):
        """Initialize retrieval systems."""
        self.workspace = Path(workspace)
        self.skill_registry = SkillRegistry()
        self.kg = KnowledgeGraph(filepath=str(self.workspace / "knowledge_graph.json"))
        self.memory_synth = MemorySynthesis(lessons_file=str(self.workspace / "learned_lessons.json"))

        # Context components
        self.founding_memory = None  # Identity seed - loaded first
        self.skills_context = []
        self.lessons_context = []
        self.kg_context = []
        self.uiux_context = []

        # UI/UX knowledge loader (lazy init)
        self._uiux_loader = None

    def add_founding_memory(self) -> 'ContextBuilder':
        """
        Load the founding memory - identity seeds and core principles.

        This should be called first to establish foundational context
        that structures all subsequent learning and behavior.

        Returns:
            Self for method chaining
        """
        founding_file = self.workspace / "founding_memory.md"
        if founding_file.exists():
            try:
                self.founding_memory = founding_file.read_text(encoding='utf-8')
            except Exception as e:
                print(f"[CONTEXT] Warning: Could not load founding memory: {e}")
                self.founding_memory = None
        return self

    def add_skills(self, query: str, top_k: int = 3, log_expansion: bool = False) -> 'ContextBuilder':
        """
        Retrieve top-k relevant skills from the skill registry.

        Args:
            query: Task description for skill matching
            top_k: Number of top skills to retrieve (default: 3)
            log_expansion: Whether to log query expansion details (default: False)

        Returns:
            Self for method chaining
        """
        similar_skills = self.skill_registry.find_similar_skills(query, top_k=top_k, log_expansion=log_expansion)

        for skill_name, similarity_score in similar_skills:
            skill = self.skill_registry.get_skill(skill_name)
            if skill:
                self.skills_context.append({
                    "name": skill_name,
                    "score": similarity_score,
                    "description": skill["description"],
                    "code": skill["code"]
                })

        return self

    def add_lessons(self, query: str, top_k: int = 3, log_expansion: bool = False) -> 'ContextBuilder':
        """
        Retrieve top-k relevant lessons from learned_lessons.json.

        Args:
            query: Task description for lesson matching
            top_k: Number of top lessons to retrieve (default: 3)
            log_expansion: Whether to log query expansion details (default: False)

        Returns:
            Self for method chaining
        """
        lessons = self.memory_synth.load_all_lessons()
        similar_lessons = self.memory_synth.retrieve_relevant_lessons(query, lessons, top_k=top_k, log_expansion=log_expansion)

        for lesson in similar_lessons:
            self.lessons_context.append({
                "lesson": lesson.get("lesson", ""),
                "score": lesson.get("relevance_score", 0.0),
                "category": lesson.get("task_category", ""),
                "key_insights": lesson.get("key_insights", []),
                "source": lesson.get("source", "")
            })

        return self

    def add_uiux(self, query: str, top_k: int = 3, max_tokens: int = 2000) -> 'ContextBuilder':
        """
        Retrieve UI/UX knowledge from the scraped knowledge base.

        Args:
            query: Task description for matching
            top_k: Number of documents to retrieve (default: 3)
            max_tokens: Token budget for content (default: 2000)

        Returns:
            Self for method chaining
        """
        if not UIUX_AVAILABLE:
            return self

        if self._uiux_loader is None:
            self._uiux_loader = get_uiux_loader()
            self._uiux_loader.load()

        docs = self._uiux_loader.retrieve(query, top_k=top_k)
        for doc in docs:
            content = self._uiux_loader.get_content(doc)
            if content:
                # Truncate content if too long
                if len(content) > max_tokens * 4:
                    content = content[:max_tokens * 4] + "\n...(truncated)"

                self.uiux_context.append({
                    "title": doc.get("title", "Unknown"),
                    "category": doc.get("category", "unknown"),
                    "source": doc.get("source", "unknown"),
                    "content": content
                })

        return self

    def add_kg_context(self, query: str, depth: int = 2) -> 'ContextBuilder':
        """
        Retrieve knowledge graph context with related concepts.

        Args:
            query: Task description for concept matching
            depth: Graph traversal depth (default: 2)

        Returns:
            Self for method chaining
        """
        related_concepts = self.kg.get_related_concepts(query, max_results=5)

        for concept in related_concepts:
            # Find nodes matching this concept
            for node_id, node in self.kg.nodes.items():
                if node.label.lower() == concept.lower():
                    # Query subgraph around this concept
                    subgraph = self.kg.query_related(node_id, depth=depth)
                    self.kg_context.append({
                        "concept": concept,
                        "type": node.type.value,
                        "related_nodes": len(subgraph.get("nodes", {})),
                        "edges": len(subgraph.get("edges", []))
                    })
                    break

        return self

    def build(self, log_injection: bool = True) -> str:
        """
        Build unified context string from all retrieved components.

        Args:
            log_injection: Whether to print what context was injected (default: True)

        Returns:
            Formatted context string ready for prompt injection
        """
        sections = []

        # Founding memory section (FIRST - structures everything else)
        if self.founding_memory:
            founding_section = "============================================================\n"
            founding_section += "FOUNDING MEMORY - IDENTITY & VALUES SEED\n"
            founding_section += "============================================================\n\n"
            founding_section += self.founding_memory
            founding_section += "\n\n============================================================\n"
            sections.append(founding_section)

            if log_injection:
                print("[CONTEXT] Injected founding memory (identity seed)")

        # Skills section
        if self.skills_context:
            skills_section = "============================================================\n"
            skills_section += "VOYAGER SKILL INJECTION (arXiv:2305.16291)\n"
            skills_section += "============================================================\n\n"

            for skill in self.skills_context:
                skills_section += f"RELEVANT SKILL: {skill['name']}\n\n"
                skills_section += f"# {skill['description']}\n"
                skills_section += f"{skill['code']}\n\n"

            skills_section += "============================================================\n"
            sections.append(skills_section)

            if log_injection:
                skill_names = [s['name'] for s in self.skills_context]
                print(f"[CONTEXT] Injected {len(self.skills_context)} skills: {', '.join(skill_names)}")

        # Lessons section
        if self.lessons_context:
            lessons_section = "============================================================\n"
            lessons_section += "LEARNED LESSONS CONTEXT\n"
            lessons_section += "============================================================\n\n"

            for lesson in self.lessons_context:
                lessons_section += f"Category: {lesson['category']}\n"
                lessons_section += f"Lesson: {lesson['lesson']}\n"
                lessons_section += f"Key Insights:\n"
                for insight in lesson['key_insights']:
                    lessons_section += f"  - {insight}\n"
                lessons_section += f"Source: {lesson['source']}\n\n"

            lessons_section += "============================================================\n"
            sections.append(lessons_section)

            if log_injection:
                categories = [l['category'] for l in self.lessons_context]
                print(f"[CONTEXT] Injected {len(self.lessons_context)} lessons: {', '.join(categories)}")

        # Knowledge graph section
        if self.kg_context:
            kg_section = "============================================================\n"
            kg_section += "KNOWLEDGE GRAPH CONTEXT\n"
            kg_section += "============================================================\n"
            kg_section += "Related concepts from codebase analysis:\n\n"

            for ctx in self.kg_context:
                kg_section += f"  - {ctx['concept']} ({ctx['type']})\n"

            kg_section += "============================================================\n"
            sections.append(kg_section)

            if log_injection:
                concepts = [c['concept'] for c in self.kg_context]
                print(f"[CONTEXT] Injected {len(self.kg_context)} concepts: {', '.join(concepts)}")

        # UI/UX knowledge section
        if self.uiux_context:
            uiux_section = "============================================================\n"
            uiux_section += "UI/UX DESIGN KNOWLEDGE (scraped best practices)\n"
            uiux_section += "============================================================\n\n"

            for doc in self.uiux_context:
                uiux_section += f"### {doc['title']}\n"
                uiux_section += f"Category: {doc['category']} | Source: {doc['source']}\n\n"
                uiux_section += doc['content'][:3000]  # Limit content
                uiux_section += "\n\n"

            uiux_section += "============================================================\n"
            sections.append(uiux_section)

            if log_injection:
                titles = [d['title'][:30] for d in self.uiux_context]
                print(f"[CONTEXT] Injected {len(self.uiux_context)} UI/UX docs: {', '.join(titles)}")

        # Clear stored context after building
        self.founding_memory = None
        self.skills_context = []
        self.lessons_context = []
        self.kg_context = []
        self.uiux_context = []

        return "\n".join(sections)

    def reset(self) -> 'ContextBuilder':
        """Reset all context components.

        Returns:
            Self for method chaining
        """
        self.founding_memory = None
        self.skills_context = []
        self.lessons_context = []
        self.kg_context = []
        self.uiux_context = []
        return self

    @property
    def context_parts(self) -> List:
        """Get all context parts as a combined list."""
        return self.skills_context + self.lessons_context + self.kg_context


def build_context(
    query: str,
    workspace: str = ".",
    include_founding_memory: bool = True,
    include_skills: bool = True,
    include_lessons: bool = True,
    include_kg: bool = True,
    include_uiux: bool = False,
    top_k: int = 3
) -> str:
    """
    Convenience function to build context in one call.

    Args:
        query: Task description for retrieval
        workspace: Workspace directory path (default: current dir)
        include_founding_memory: Whether to include identity seed (default: True)
        include_skills: Whether to include skill retrieval (default: True)
        include_lessons: Whether to include lesson retrieval (default: True)
        include_kg: Whether to include KG context (default: True)
        include_uiux: Whether to include UI/UX knowledge (default: False)
        top_k: Number of top items to retrieve (default: 3)

    Returns:
        Formatted context string
    """
    builder = ContextBuilder(workspace)

    # Founding memory first - structures everything else
    if include_founding_memory:
        builder.add_founding_memory()

    if include_skills:
        builder.add_skills(query, top_k=top_k)

    if include_lessons:
        builder.add_lessons(query, top_k=top_k)

    if include_kg:
        builder.add_kg_context(query)

    if include_uiux:
        builder.add_uiux(query, top_k=top_k)

    return builder.build(log_injection=False)
