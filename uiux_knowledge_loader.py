"""
UI/UX Knowledge Loader - Integrates scraped UI/UX knowledge into the swarm.

Loads knowledge from the stripper/knowledge/uiux directory and makes it
available for context injection during task execution.

Knowledge categories:
- accessibility: ARIA, WCAG, a11y best practices
- animation_motion: Animation patterns, transitions
- component_libraries: Radix, shadcn, Headless UI
- css_styling: CSS best practices, MDN references
- data_visualization: Chart patterns, D3 concepts
- design_systems: Material, Apple HIG, Fluent
- forms_patterns: Form validation, input patterns
- navigation_patterns: Routing, menus, breadcrumbs
- ux_research: Nielsen Norman, Laws of UX
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re


@dataclass
class KnowledgeChunk:
    """A piece of knowledge with metadata."""
    id: str
    category: str
    source: str
    title: str
    content: str
    url: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class UIUXKnowledgeLoader:
    """
    Loads and retrieves UI/UX knowledge for context injection.

    Supports:
    - Keyword-based retrieval
    - Category filtering
    - Relevance scoring
    """

    # Default path to scraped knowledge
    DEFAULT_KNOWLEDGE_PATH = Path("D:/codingProjects/stripper/knowledge/uiux")

    # Category priorities for different task types
    CATEGORY_PRIORITIES = {
        "accessibility": ["accessibility", "component_libraries", "forms_patterns"],
        "component": ["component_libraries", "design_systems", "css_styling"],
        "animation": ["animation_motion", "css_styling", "performance"],
        "form": ["forms_patterns", "accessibility", "component_libraries"],
        "navigation": ["navigation_patterns", "component_libraries", "ux_research"],
        "chart": ["data_visualization", "css_styling", "component_libraries"],
        "modal": ["modals_overlays", "component_libraries", "accessibility"],
        "table": ["tables_datagrids", "component_libraries", "accessibility"],
        "style": ["css_styling", "design_systems", "animation_motion"],
        "ux": ["ux_research", "accessibility", "forms_patterns"],
    }

    def __init__(self, knowledge_path: Optional[Path] = None):
        """
        Initialize knowledge loader.

        Args:
            knowledge_path: Path to UI/UX knowledge directory.
                          Defaults to stripper/knowledge/uiux
        """
        self.knowledge_path = knowledge_path or self.DEFAULT_KNOWLEDGE_PATH
        self.index: Dict[str, Any] = {}
        self.chunks: Dict[str, KnowledgeChunk] = {}
        self._loaded = False

    def load(self) -> bool:
        """
        Load the knowledge index.

        Returns:
            True if loaded successfully
        """
        if self._loaded:
            return True

        index_path = self.knowledge_path / "index.json"
        if not index_path.exists():
            print(f"[UIUX] Knowledge index not found: {index_path}")
            return False

        try:
            with open(index_path, "r", encoding="utf-8") as f:
                self.index = json.load(f)
            self._loaded = True
            print(f"[UIUX] Loaded knowledge index with {len(self.index.get('documents', []))} documents")
            return True
        except Exception as e:
            print(f"[UIUX] Failed to load index: {e}")
            return False

    def get_categories(self) -> List[str]:
        """Get list of available knowledge categories."""
        if not self._loaded:
            self.load()

        categories = set()
        for doc in self.index.get("documents", []):
            if "category" in doc:
                categories.add(doc["category"])
        return sorted(categories)

    def _score_relevance(self, doc: Dict, keywords: List[str]) -> float:
        """
        Score document relevance to keywords.

        Args:
            doc: Document metadata
            keywords: Search keywords

        Returns:
            Relevance score (0.0 - 1.0)
        """
        score = 0.0
        title = doc.get("title", "").lower()
        category = doc.get("category", "").lower()
        source = doc.get("source", "").lower()

        for keyword in keywords:
            kw = keyword.lower()
            # Title match is strongest
            if kw in title:
                score += 0.5
            # Category match
            if kw in category:
                score += 0.3
            # Source match
            if kw in source:
                score += 0.2

        return min(score, 1.0)

    def _extract_keywords(self, task: str) -> List[str]:
        """Extract keywords from task description."""
        # Common UI/UX terms to look for
        ui_terms = [
            "button", "input", "form", "modal", "dialog", "dropdown",
            "menu", "navigation", "nav", "header", "footer", "sidebar",
            "table", "grid", "list", "card", "accordion", "tab",
            "tooltip", "popover", "toast", "notification", "alert",
            "checkbox", "radio", "select", "slider", "switch", "toggle",
            "icon", "image", "avatar", "badge", "chip", "tag",
            "progress", "spinner", "loading", "skeleton",
            "chart", "graph", "visualization",
            "animation", "transition", "motion",
            "responsive", "mobile", "desktop",
            "accessibility", "a11y", "aria", "wcag",
            "color", "theme", "dark", "light",
            "spacing", "layout", "flex", "grid",
            "typography", "font", "text",
        ]

        task_lower = task.lower()
        found_keywords = []

        for term in ui_terms:
            if term in task_lower:
                found_keywords.append(term)

        # Also extract any capitalized words (likely component names)
        words = re.findall(r'\b[A-Z][a-z]+\b', task)
        found_keywords.extend([w.lower() for w in words])

        return list(set(found_keywords))

    def _detect_task_type(self, task: str) -> str:
        """Detect the primary task type for category prioritization."""
        task_lower = task.lower()

        if any(t in task_lower for t in ["accessible", "a11y", "aria", "screen reader", "wcag"]):
            return "accessibility"
        if any(t in task_lower for t in ["animate", "transition", "motion", "fade", "slide"]):
            return "animation"
        if any(t in task_lower for t in ["form", "input", "validation", "submit"]):
            return "form"
        if any(t in task_lower for t in ["nav", "menu", "route", "link", "breadcrumb"]):
            return "navigation"
        if any(t in task_lower for t in ["chart", "graph", "plot", "visualization"]):
            return "chart"
        if any(t in task_lower for t in ["modal", "dialog", "overlay", "popup"]):
            return "modal"
        if any(t in task_lower for t in ["table", "grid", "datagrid", "column"]):
            return "table"
        if any(t in task_lower for t in ["style", "css", "theme", "color"]):
            return "style"
        if any(t in task_lower for t in ["user experience", "ux", "usability"]):
            return "ux"

        return "component"  # Default

    def retrieve(
        self,
        task: str,
        top_k: int = 5,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge for a task.

        Args:
            task: Task description
            top_k: Maximum number of documents to return
            categories: Optional category filter

        Returns:
            List of relevant document metadata with content paths
        """
        if not self._loaded:
            self.load()

        if not self.index.get("documents"):
            return []

        # Extract keywords and detect task type
        keywords = self._extract_keywords(task)
        task_type = self._detect_task_type(task)

        # Get priority categories for this task type
        priority_categories = self.CATEGORY_PRIORITIES.get(task_type, [])

        # Score all documents
        scored_docs = []
        for doc in self.index.get("documents", []):
            # Skip if category filter doesn't match
            if categories and doc.get("category") not in categories:
                continue

            # Calculate relevance score
            score = self._score_relevance(doc, keywords)

            # Boost score for priority categories
            doc_category = doc.get("category", "")
            if doc_category in priority_categories:
                boost = 0.3 * (len(priority_categories) - priority_categories.index(doc_category)) / len(priority_categories)
                score += boost

            if score > 0:
                scored_docs.append((score, doc))

        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        # Return top_k
        return [doc for _, doc in scored_docs[:top_k]]

    def get_content(self, doc: Dict[str, Any]) -> Optional[str]:
        """
        Load the actual content of a document.

        Args:
            doc: Document metadata from retrieve()

        Returns:
            Document content as string, or None if not found
        """
        # Try markdown file first
        md_path = doc.get("markdown_path")
        if md_path:
            full_path = self.knowledge_path / md_path
            if full_path.exists():
                try:
                    return full_path.read_text(encoding="utf-8")
                except Exception:
                    pass

        # Fall back to JSON
        json_path = doc.get("json_path")
        if json_path:
            full_path = self.knowledge_path / json_path
            if full_path.exists():
                try:
                    data = json.loads(full_path.read_text(encoding="utf-8"))
                    return data.get("content", data.get("text", str(data)))
                except Exception:
                    pass

        return None

    def build_context(
        self,
        task: str,
        max_tokens: int = 4000,
        top_k: int = 5
    ) -> str:
        """
        Build a context string for injection into prompts.

        Args:
            task: Task description
            max_tokens: Approximate max tokens (uses char estimate)
            top_k: Max documents to include

        Returns:
            Formatted context string
        """
        docs = self.retrieve(task, top_k=top_k)

        if not docs:
            return ""

        context_parts = [
            "=" * 60,
            "UI/UX KNOWLEDGE CONTEXT",
            "=" * 60,
            ""
        ]

        char_budget = max_tokens * 4  # Rough estimate
        chars_used = 0

        for doc in docs:
            title = doc.get("title", "Unknown")
            category = doc.get("category", "unknown")
            source = doc.get("source", "unknown")

            header = f"### {title}\nCategory: {category} | Source: {source}\n\n"

            # Load content
            content = self.get_content(doc)
            if not content:
                continue

            # Truncate if needed
            remaining = char_budget - chars_used - len(header) - 100
            if remaining <= 0:
                break

            if len(content) > remaining:
                content = content[:remaining] + "\n...(truncated)"

            context_parts.append(header)
            context_parts.append(content)
            context_parts.append("")
            chars_used += len(header) + len(content)

        context_parts.append("=" * 60)
        return "\n".join(context_parts)


# Global instance
_uiux_loader: Optional[UIUXKnowledgeLoader] = None


def get_uiux_loader() -> UIUXKnowledgeLoader:
    """Get or create the global UI/UX knowledge loader."""
    global _uiux_loader
    if _uiux_loader is None:
        _uiux_loader = UIUXKnowledgeLoader()
    return _uiux_loader


def retrieve_uiux_knowledge(task: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve UI/UX knowledge.

    Args:
        task: Task description
        top_k: Max documents

    Returns:
        List of relevant document metadata
    """
    loader = get_uiux_loader()
    return loader.retrieve(task, top_k=top_k)


def build_uiux_context(task: str, max_tokens: int = 4000) -> str:
    """
    Convenience function to build UI/UX context for prompt injection.

    Args:
        task: Task description
        max_tokens: Approximate token budget

    Returns:
        Formatted context string
    """
    loader = get_uiux_loader()
    return loader.build_context(task, max_tokens=max_tokens)


if __name__ == "__main__":
    # Test the loader
    loader = UIUXKnowledgeLoader()
    loader.load()

    print(f"Categories: {loader.get_categories()}")
    print()

    # Test retrieval
    test_task = "Create an accessible dropdown menu with keyboard navigation"
    docs = loader.retrieve(test_task, top_k=3)

    print(f"Task: {test_task}")
    print(f"Found {len(docs)} relevant documents:")
    for doc in docs:
        print(f"  - {doc.get('title')} ({doc.get('category')})")

    print()
    print("Building context...")
    context = loader.build_context(test_task, max_tokens=2000)
    print(f"Context length: {len(context)} chars")
    print(context[:500] + "...")
