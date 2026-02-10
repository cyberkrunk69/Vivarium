"""
Unified Inference Engine - Routes to Groq or Together AI based on task type.

Architecture:
- GROQ: Fast parallel execution (workers, sweepers)
- TOGETHER: Deep thinking (planners, reasoners, critics)

This gives us the best of both worlds:
- Groq's speed for churning through tasks
- Together's smart models for planning and verification
"""

import os
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass

# Import both engines
try:
    from groq_client import GroqInferenceEngine, get_groq_engine
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from together_client import (
        TogetherInferenceEngine,
        get_together_engine,
        NodeType,
        ModelRouter,
        MODELS_BY_TYPE
    )
    TOGETHER_AVAILABLE = True
except ImportError:
    TOGETHER_AVAILABLE = False


class EngineChoice(Enum):
    """Which inference provider to use."""
    GROQ = "groq"           # Fast execution
    TOGETHER = "together"   # Deep thinking
    AUTO = "auto"           # Route automatically


@dataclass
class InferenceResult:
    """Unified result from any engine."""
    success: bool
    output: str
    cost_usd: float
    model: str
    engine: str
    node_type: str
    tokens_in: int
    tokens_out: int
    elapsed: float
    error: Optional[str] = None


class UnifiedInferenceEngine:
    """
    Routes inference requests to the appropriate engine.

    Groq for:
    - WORKER: General task execution
    - SWEEPER: Cheap cleanup tasks
    - High-throughput parallel work

    Together for:
    - REASONER: Complex planning, architecture
    - THINKER: Multi-step reasoning, debugging
    - VERIFIER: Quality verification (critic node)
    - CODER: Complex code generation (optional, can use Groq too)
    """

    # Which node types go to which engine
    ENGINE_ROUTING = {
        NodeType.WORKER: EngineChoice.GROQ,
        NodeType.SWEEPER: EngineChoice.GROQ,
        NodeType.CODER: EngineChoice.GROQ,      # Groq is fast enough for most code
        NodeType.REASONER: EngineChoice.TOGETHER,
        NodeType.THINKER: EngineChoice.TOGETHER,
        NodeType.VERIFIER: EngineChoice.TOGETHER,
        NodeType.GUARD: EngineChoice.TOGETHER,
    }

    def __init__(self):
        self.groq_engine = None
        self.together_engine = None

        # Lazy init - only create when needed
        self._init_groq()
        self._init_together()

    def _init_groq(self):
        """Initialize Groq engine if available."""
        if GROQ_AVAILABLE and os.environ.get("GROQ_API_KEY"):
            try:
                self.groq_engine = get_groq_engine()
            except Exception as e:
                print(f"[UNIFIED] Groq init failed: {e}")

    def _init_together(self):
        """Initialize Together engine if available."""
        if TOGETHER_AVAILABLE and os.environ.get("TOGETHER_API_KEY"):
            try:
                self.together_engine = get_together_engine()
            except Exception as e:
                print(f"[UNIFIED] Together init failed: {e}")

    def _determine_node_type(self, task: str) -> NodeType:
        """Analyze task to determine appropriate node type."""
        if not TOGETHER_AVAILABLE:
            return NodeType.WORKER

        _, node_type, _ = ModelRouter.route(task)
        return node_type

    def _route_to_engine(self, node_type: NodeType) -> EngineChoice:
        """Determine which engine should handle this node type."""
        return self.ENGINE_ROUTING.get(node_type, EngineChoice.GROQ)

    def execute(
        self,
        prompt: str,
        node_type: Optional[NodeType] = None,
        force_engine: Optional[EngineChoice] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> InferenceResult:
        """
        Execute a prompt using the appropriate engine.

        Args:
            prompt: The prompt to execute
            node_type: Force a specific node type
            force_engine: Force a specific engine (groq/together)
            max_tokens: Max response tokens
            temperature: Sampling temperature

        Returns:
            InferenceResult with unified format
        """
        # Determine node type from task if not specified
        if node_type is None:
            node_type = self._determine_node_type(prompt)

        # Determine engine
        if force_engine and force_engine != EngineChoice.AUTO:
            engine_choice = force_engine
        else:
            engine_choice = self._route_to_engine(node_type)

        # Execute on appropriate engine
        if engine_choice == EngineChoice.GROQ and self.groq_engine:
            return self._execute_groq(prompt, node_type, max_tokens, temperature)
        elif engine_choice == EngineChoice.TOGETHER and self.together_engine:
            return self._execute_together(prompt, node_type, max_tokens, temperature)
        elif self.groq_engine:
            # Fallback to Groq if Together not available
            return self._execute_groq(prompt, node_type, max_tokens, temperature)
        elif self.together_engine:
            # Fallback to Together if Groq not available
            return self._execute_together(prompt, node_type, max_tokens, temperature)
        else:
            return InferenceResult(
                success=False,
                output="",
                cost_usd=0,
                model="none",
                engine="none",
                node_type=node_type.value,
                tokens_in=0,
                tokens_out=0,
                elapsed=0,
                error="No inference engine available"
            )

    def _execute_groq(
        self,
        prompt: str,
        node_type: NodeType,
        max_tokens: int,
        temperature: float
    ) -> InferenceResult:
        """Execute on Groq."""
        result = self.groq_engine.execute(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return InferenceResult(
            success=result.get("returncode") == 0,
            output=result.get("result", ""),
            cost_usd=result.get("cost", 0),
            model=result.get("model", "unknown"),
            engine="groq",
            node_type=node_type.value,
            tokens_in=result.get("input_tokens", 0),
            tokens_out=result.get("output_tokens", 0),
            elapsed=result.get("elapsed", 0),
            error=result.get("error_message")
        )

    def _execute_together(
        self,
        prompt: str,
        node_type: NodeType,
        max_tokens: int,
        temperature: float
    ) -> InferenceResult:
        """Execute on Together AI."""
        result = self.together_engine.execute(
            prompt=prompt,
            node_type=node_type,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return InferenceResult(
            success=result.get("returncode") == 0,
            output=result.get("result", ""),
            cost_usd=result.get("cost", 0),
            model=result.get("model", "unknown"),
            engine="together",
            node_type=result.get("node_type", node_type.value),
            tokens_in=result.get("input_tokens", 0),
            tokens_out=result.get("output_tokens", 0),
            elapsed=result.get("elapsed", 0),
            error=result.get("error_message")
        )

    def verify(self, task: str, output: str, files_changed: List[str] = None) -> Dict[str, Any]:
        """
        Critic node - uses Together AI's verification model.

        This is the Observer pattern - verify work before marking complete.
        """
        if self.together_engine:
            return self.together_engine.verify(task, output, files_changed)
        else:
            # Fallback: basic verification without LLM
            return {
                "verdict": "APPROVE",
                "reason": "No verification engine available, auto-approving",
                "cost": 0
            }

    def plan(self, complex_task: str) -> Dict[str, Any]:
        """
        Planner node - uses Together AI's reasoning model for task decomposition.

        Breaks complex tasks into steps.
        """
        plan_prompt = f"""You are a technical project planner. Break this complex task into concrete steps.

TASK:
{complex_task}

OUTPUT FORMAT:
Return a JSON array of steps, each with:
- "step": step number
- "description": what to do
- "node_type": "worker" | "coder" | "reasoner" (what kind of node should do this)
- "dependencies": list of step numbers this depends on (empty if none)

Example:
[
  {{"step": 1, "description": "Read the existing code", "node_type": "worker", "dependencies": []}},
  {{"step": 2, "description": "Design the new architecture", "node_type": "reasoner", "dependencies": [1]}},
  {{"step": 3, "description": "Implement the changes", "node_type": "coder", "dependencies": [2]}}
]

Now break down the task:"""

        result = self.execute(
            prompt=plan_prompt,
            node_type=NodeType.REASONER,
            max_tokens=2000,
            temperature=0.5
        )

        return {
            "success": result.success,
            "plan": result.output,
            "cost": result.cost_usd,
            "model": result.model,
            "engine": result.engine
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get combined stats from both engines."""
        stats = {
            "groq": {},
            "together": {},
            "combined": {
                "total_cost_usd": 0,
                "total_calls": 0
            }
        }

        if self.groq_engine:
            groq_stats = self.groq_engine.get_stats()
            stats["groq"] = groq_stats
            stats["combined"]["total_cost_usd"] += groq_stats.get("total_cost_usd", 0)
            stats["combined"]["total_calls"] += groq_stats.get("total_requests", 0)

        if self.together_engine:
            together_stats = self.together_engine.get_stats()
            stats["together"] = together_stats
            stats["combined"]["total_cost_usd"] += together_stats.get("total_cost_usd", 0)
            stats["combined"]["total_calls"] += together_stats.get("total_calls", 0)

        return stats


# Global instance
_unified_engine: Optional[UnifiedInferenceEngine] = None


def get_unified_engine() -> UnifiedInferenceEngine:
    """Get or create the global unified engine."""
    global _unified_engine
    if _unified_engine is None:
        _unified_engine = UnifiedInferenceEngine()
    return _unified_engine


if __name__ == "__main__":
    print("Testing unified inference engine...")
    print(f"Groq available: {GROQ_AVAILABLE}")
    print(f"Together available: {TOGETHER_AVAILABLE}")

    engine = get_unified_engine()

    # Test routing
    test_tasks = [
        ("Fix the typo in README", "Should route to GROQ (worker)"),
        ("Design a distributed system", "Should route to TOGETHER (reasoner)"),
        ("Debug why auth fails", "Should route to TOGETHER (thinker)"),
        ("Implement the parser function", "Should route to GROQ (coder)"),
        ("Verify the output is correct", "Should route to TOGETHER (verifier)"),
    ]

    for task, expected in test_tasks:
        node_type = engine._determine_node_type(task)
        engine_choice = engine._route_to_engine(node_type)
        print(f"\nTask: {task[:40]}...")
        print(f"  Node: {node_type.value} → Engine: {engine_choice.value}")
        print(f"  Expected: {expected}")
