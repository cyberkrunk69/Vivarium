"""
Tool-First Router - Route tasks to tools before LLM calls.

Philosophy: "Every LLM call is a failure to have built the right tool."

Routing hierarchy:
1. Exact tool match -> execute directly (FREE)
2. High-confidence semantic match (>=0.8) -> execute (FREE)
3. Composable components -> assemble + execute (CHEAP)
4. Fast LLM routing decision -> select pattern (CHEAP)
5. Full LLM generation -> create + store tool (EXPENSIVE)
"""

import json
import time
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple

# Import skill registry for semantic search
from skills.skill_registry import SkillRegistry, retrieve_skill, compose_skills, get_skill

# Import Groq for fast routing decisions
try:
    from groq_client import get_groq_engine
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


@dataclass
class ToolRouteResult:
    """Result from tool routing decision."""
    tool: Optional[Dict[str, Any]]  # Tool definition if found
    route: str  # "exact", "semantic", "composed", "llm_routed", "generate"
    cost: Optional[float]  # Estimated cost in USD
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def found(self) -> bool:
        """Whether a tool was found."""
        return self.tool is not None


class ToolRouter:
    """
    Tool-First routing for task execution.

    Checks tools before making expensive LLM calls.
    Stores successful tool executions for future reuse.
    """

    # Common task patterns that map to actual tool names in tool_store.json
    TASK_PATTERNS = {
        # Testing
        r"add.*test|test.*coverage": "add_test_coverage",

        # File operations
        r"(read|load).*json": "read_json_safe",
        r"(write|save).*json": "write_json_safe",
        r"(parse|extract).*json": "read_json_safe",
        r"list.*python.*file|find.*\.py": "list_python_files",
        r"glob|find.*file": "glob_files",
        r"resolve.*path": "resolve_path",
        r"file.*extension|get.*ext": "get_file_extension",
        r"count.*line": "count_lines",
        r"find.*replace|replace.*in.*file": "find_replace_in_file",

        # Code analysis
        r"validate.*syntax|check.*syntax|syntax.*valid": "validate_python_syntax",
        r"extract.*function": "extract_function",
        r"extract.*import": "extract_imports",

        # Utilities
        r"(config|constant|import)": "import_config_constants",
        r"(duplicate|dedup|extract|migrate).*util": "migrate_to_utils",
        r"setup.*log|create.*log|init.*log": "setup_logger",
        r"run.*command|execute.*command|shell": "run_command",
        r"hash.*file|file.*hash|checksum": "file_hash",
        r"hash|compute.*hash|md5|sha": "compute_hash",
        r"base64.*encode|encode.*base64": "base64_encode",
        r"base64.*decode|decode.*base64": "base64_decode",
        r"env.*var|environment|get.*env": "get_env",
        r"merge.*dict|combine.*dict": "merge_dicts",
        r"retry|backoff|retry.*fail": "retry_with_backoff",
        r"dedup.*list|unique|remove.*duplicate": "deduplicate_list",
        r"chunk|split.*list|batch": "chunk_list",
        r"flatten": "flatten_list",
        r"nested.*dict|safe.*get|dict.*get": "safe_dict_get",
        r"truncate|shorten.*string": "truncate_string",
        r"format.*time|timestamp": "format_timestamp",
        r"parse.*time|parse.*date": "parse_timestamp",
        r"regex.*extract|extract.*regex": "regex_extract",
        r"regex.*find|find.*all|findall": "regex_find_all",
        r"try.*except|error.*handl|safe.*call": "safe_try_except",
    }

    def __init__(self, tool_store_path: str = "tool_store.json"):
        self.tool_store_path = Path(tool_store_path)
        self.tool_store = self._load_store()
        self.skill_registry = SkillRegistry()
        self._groq_engine = None

        # Metrics
        self.route_counts = {
            "exact": 0,
            "semantic": 0,
            "composed": 0,
            "llm_routed": 0,
            "generate": 0
        }
        self.total_routes = 0
        self.total_cost_saved = 0.0

    def _load_store(self) -> Dict[str, Any]:
        """Load tool store from disk."""
        if self.tool_store_path.exists():
            try:
                with open(self.tool_store_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def _save_store(self):
        """Save tool store to disk."""
        try:
            with open(self.tool_store_path, 'w', encoding='utf-8') as f:
                json.dump(self.tool_store, f, indent=2)
        except IOError as e:
            print(f"[TOOL ROUTER] Warning: Could not save tool store: {e}")

    def _get_groq_engine(self):
        """Lazy-load Groq engine for routing decisions."""
        if self._groq_engine is None and GROQ_AVAILABLE:
            try:
                self._groq_engine = get_groq_engine()
            except (ValueError, ImportError):
                # Groq not configured - fall back to pattern matching only
                self._groq_engine = None
        return self._groq_engine

    def route(self, task: str, context: Dict[str, Any] = None) -> ToolRouteResult:
        """
        Tool-First routing hierarchy.

        Args:
            task: Task description
            context: Additional context (workspace, etc.)

        Returns:
            ToolRouteResult with tool if found, or route="generate" if LLM needed
        """
        context = context or {}
        self.total_routes += 1

        # Level 1: Exact match in tool store
        tool = self._exact_match(task)
        if tool:
            self.route_counts["exact"] += 1
            self.total_cost_saved += 0.01  # Estimated LLM cost saved
            return ToolRouteResult(
                tool=tool,
                route="exact",
                cost=0,
                confidence=1.0,
                metadata={"match_type": "exact_name"}
            )

        # Level 2: High-confidence semantic match (>=0.8)
        tool, score = self._semantic_match(task, threshold=0.8)
        if tool:
            self.route_counts["semantic"] += 1
            self.total_cost_saved += 0.01
            return ToolRouteResult(
                tool=tool,
                route="semantic",
                cost=0,
                confidence=score,
                metadata={"similarity_score": score}
            )

        # Level 3: Composable components
        components = self._find_components(task)
        if components and len(components) >= 2:
            assembled = self._assemble_tools(components, task)
            if assembled:
                self.route_counts["composed"] += 1
                self.total_cost_saved += 0.008
                return ToolRouteResult(
                    tool=assembled,
                    route="composed",
                    cost=0.001,  # Small cost for assembly logic
                    confidence=0.7,
                    metadata={"components": components}
                )

        # Level 4: Fast LLM routing (Groq - ultra cheap)
        pattern = self._llm_route_decision(task)
        if pattern and pattern != "NONE":
            tool = self._get_pattern_tool(pattern)
            if tool:
                self.route_counts["llm_routed"] += 1
                self.total_cost_saved += 0.005
                return ToolRouteResult(
                    tool=tool,
                    route="llm_routed",
                    cost=0.0001,  # Groq fast model cost
                    confidence=0.6,
                    metadata={"pattern": pattern}
                )

        # Level 5: Full generation required
        self.route_counts["generate"] += 1
        return ToolRouteResult(
            tool=None,
            route="generate",
            cost=None,  # Unknown - full LLM generation
            confidence=0.0,
            metadata={"reason": "no_tool_match"}
        )

    def _exact_match(self, task: str) -> Optional[Dict[str, Any]]:
        """Check for exact tool name match in task."""
        task_lower = task.lower()

        # Check tool store
        for tool_name, tool_data in self.tool_store.items():
            if tool_name.lower() in task_lower:
                return tool_data

        # Check skill registry
        for skill_name in self.skill_registry.list_skills():
            if skill_name.lower() in task_lower:
                skill = self.skill_registry.get_skill(skill_name)
                if skill:
                    return skill

        return None

    def _semantic_match(self, task: str, threshold: float = 0.8) -> Tuple[Optional[Dict], float]:
        """Find high-confidence semantic match."""
        # Use skill registry's embedding-based search
        similar_skills = self.skill_registry.find_similar_skills(task, top_k=1)

        if similar_skills:
            skill_name, score = similar_skills[0]
            if score >= threshold:
                skill = self.skill_registry.get_skill(skill_name)
                return skill, score

        # Also check tool store descriptions
        best_match = None
        best_score = 0.0

        for tool_name, tool_data in self.tool_store.items():
            desc = tool_data.get("description", "")
            score = self._simple_similarity(task, desc)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = tool_data

        return best_match, best_score

    def _simple_similarity(self, text1: str, text2: str) -> float:
        """Simple word overlap similarity (fallback when no embeddings)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0

    def _find_components(self, task: str) -> List[str]:
        """Find multiple skill components that could be composed."""
        return self.skill_registry.decompose_task(task)

    def _assemble_tools(self, components: List[str], task: str) -> Optional[Dict[str, Any]]:
        """Assemble multiple tools into one."""
        return compose_skills(components)

    def _llm_route_decision(self, task: str) -> Optional[str]:
        """Use fast LLM as logic gate to select tool pattern."""
        # First try pattern matching (FREE)
        task_lower = task.lower()
        for pattern, tool_name in self.TASK_PATTERNS.items():
            if re.search(pattern, task_lower, re.IGNORECASE):
                return tool_name

        # Try Groq for ambiguous cases (ultra cheap) - graceful fallback if unavailable
        try:
            engine = self._get_groq_engine()
            if not engine:
                return None

            patterns_list = list(self.TASK_PATTERNS.values())
            prompt = f"""Task: {task}

Available tool patterns: {', '.join(patterns_list)}

Which pattern handles this? Reply with ONLY the pattern name, or NONE."""

            result = engine.execute(
                prompt=prompt,
                model="groq/compound-mini",  # Fast, cheap
                max_tokens=20
            )
            if result.get("returncode") == 0:
                return result.get("result", "").strip()
        except Exception:
            # Groq unavailable - fall back to pattern matching only
            pass

        return None

    def _get_pattern_tool(self, pattern: str) -> Optional[Dict[str, Any]]:
        """Get tool definition for a pattern name."""
        # Check skill registry first
        skill = get_skill(pattern)
        if skill:
            return skill

        # Check tool store
        return self.tool_store.get(pattern)

    def _list_patterns(self) -> str:
        """List available tool patterns."""
        patterns = list(self.TASK_PATTERNS.values())
        patterns.extend(self.skill_registry.list_skills())
        patterns.extend(self.tool_store.keys())
        return ", ".join(set(patterns))

    def record_tool_success(self, tool_name: str, success: bool, latency_ms: float):
        """Update tool metrics after execution."""
        tool = self.tool_store.get(tool_name)
        if not tool:
            # Tool might be from skill registry, skip
            return

        # Rolling average for success rate
        tool["times_used"] = tool.get("times_used", 0) + 1
        times = tool["times_used"]

        old_rate = tool.get("success_rate", 1.0)
        tool["success_rate"] = (old_rate * (times - 1) + (1 if success else 0)) / times

        old_latency = tool.get("avg_latency_ms", 0)
        tool["avg_latency_ms"] = (old_latency * (times - 1) + latency_ms) / times

        tool["last_used"] = datetime.now().isoformat()
        self._save_store()

    def store_new_tool(
        self,
        name: str,
        code: str,
        description: str,
        preconditions: List[str] = None,
        postconditions: List[str] = None,
        source_session: str = None
    ):
        """Store newly created tool for future reuse."""
        self.tool_store[name] = {
            "name": name,
            "code": code,
            "description": description,
            "preconditions": preconditions or [],
            "postconditions": postconditions or [],
            "success_rate": 1.0,  # Optimistic start
            "avg_latency_ms": 0,
            "times_used": 0,
            "created_from": source_session,
            "created_at": datetime.now().isoformat(),
            "last_used": None
        }
        self._save_store()

        # Also register with skill_registry for semantic search
        self.skill_registry.register_skill(
            name, code, description,
            preconditions, postconditions
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        return {
            "total_routes": self.total_routes,
            "route_counts": self.route_counts,
            "tool_hit_rate": (
                (self.total_routes - self.route_counts["generate"]) / self.total_routes
                if self.total_routes > 0 else 0.0
            ),
            "total_cost_saved": self.total_cost_saved,
            "tool_store_size": len(self.tool_store),
            "skill_registry_size": len(self.skill_registry.list_skills())
        }


# Global instance
_router: Optional[ToolRouter] = None


def get_router() -> ToolRouter:
    """Get or create global ToolRouter instance."""
    global _router
    if _router is None:
        _router = ToolRouter()
    return _router


def route_task(task: str, context: Dict[str, Any] = None) -> ToolRouteResult:
    """Convenience function to route a task."""
    return get_router().route(task, context)


if __name__ == "__main__":
    # Quick test
    router = ToolRouter()

    test_tasks = [
        "Add test coverage for the user module",
        "Fix the authentication bug in login",
        "Refactor the database connection code",
        "Create a new validation function",
        "Implement the payment processing feature",
    ]

    print("Testing Tool Router...")
    print("=" * 60)

    for task in test_tasks:
        result = router.route(task)
        print(f"\nTask: {task}")
        print(f"  Route: {result.route}")
        print(f"  Found: {result.found}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Cost: ${result.cost or 'N/A'}")

    print("\n" + "=" * 60)
    print(f"Stats: {router.get_stats()}")
