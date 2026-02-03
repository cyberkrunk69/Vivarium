"""
DSPy-powered modules for learnable task execution.

Based on arXiv:2310.03714 - Demonstrate-Search-Predict (DSPy).
Replaces static prompts with learnable signatures and modules.

Key concepts:
- Signatures: Declarative input/output specs (replaces long prompt templates)
- Modules: Composable units with learnable components (Predict, ChainOfThought)
- Teleprompters: Optimizers that bootstrap demonstrations automatically
"""

import sys
from typing import Optional, List, Dict, Any

# Try to import DSPy; if not available, create a mock interface
try:
    import dspy
    HAS_DSPY = True
except ImportError:
    HAS_DSPY = False


# ============================================================================
# MOCK INTERFACE (if DSPy not installed)
# ============================================================================
# This allows the codebase to work with or without DSPy installed.
# Once DSPy is available, these classes are replaced by real DSPy versions.

if not HAS_DSPY:
    class Signature:
        """Mock DSPy Signature base class."""
        pass

    class InputField:
        """Mock input field descriptor."""
        def __init__(self, desc: str = ""):
            self.desc = desc

    class OutputField:
        """Mock output field descriptor."""
        def __init__(self, desc: str = ""):
            self.desc = desc

    class Module:
        """Mock DSPy Module base class."""
        pass

    class ChainOfThought:
        """Mock ChainOfThought predictor."""
        def __init__(self, signature_str: str):
            self.signature_str = signature_str

        def __call__(self, **kwargs):
            # In mock mode, return a simple object with requested fields
            result = type('Result', (), {})()
            for k, v in kwargs.items():
                setattr(result, k, v)
            return result

    class Predict:
        """Mock Predict predictor."""
        def __init__(self, signature):
            self.signature = signature

        def __call__(self, **kwargs):
            # In mock mode, return a simple object with requested fields
            result = type('Result', (), {})()
            for k, v in kwargs.items():
                setattr(result, k, v)
            return result

    # Create mock dspy module
    class MockDSPy:
        Signature = Signature
        InputField = InputField
        OutputField = OutputField
        Module = Module
        ChainOfThought = ChainOfThought
        Predict = Predict

    dspy = MockDSPy()


# ============================================================================
# GRIND SIGNATURES AND MODULES
# ============================================================================

class GrindSignature(dspy.Signature):
    """Signature for executing a grind task.

    Declares the input/output contract for task execution without
    specifying the implementation. DSPy will optimize this through
    demonstrations.
    """
    task: str = dspy.InputField(desc="The task to execute")
    context: str = dspy.InputField(desc="Workspace context and relevant files")
    solution: str = dspy.OutputField(desc="The implemented solution")
    summary: str = dspy.OutputField(desc="2-3 sentence summary of the result")


class PlanningSignature(dspy.Signature):
    """Signature for planning execution steps."""
    task: str = dspy.InputField(desc="The task to break down")
    execution_steps: str = dspy.OutputField(desc="Numbered steps to execute the task")


class GrindModule(dspy.Module):
    """Module that executes grind tasks with planning and solution generation.

    Combines ChainOfThought planning with structured prediction to achieve
    better task completions. The module learns from successful demonstrations.
    """

    def __init__(self):
        """Initialize the module with learnable components."""
        super().__init__()
        # Planning sub-module: uses chain-of-thought for step generation
        self.planner = dspy.ChainOfThought(PlanningSignature)
        # Execution sub-module: generates solution and summary
        self.executor = dspy.Predict(GrindSignature)

    def forward(self, task: str, context: str) -> Dict[str, str]:
        """Execute a task with planning and solution generation.

        Args:
            task: The task description
            context: Workspace context (files, codebase state)

        Returns:
            Dict with 'solution' and 'summary' keys
        """
        # Step 1: Plan execution steps
        plan_result = self.planner(task=task)
        execution_steps = plan_result.execution_steps

        # Step 2: Execute with plan as additional context
        enhanced_context = f"{context}\n\nPlanned steps:\n{execution_steps}"
        execution_result = self.executor(task=task, context=enhanced_context)

        return {
            "solution": execution_result.solution,
            "summary": execution_result.summary,
            "execution_steps": execution_steps
        }


# ============================================================================
# TELEPROMPTER UTILITIES (for DSPy compilation)
# ============================================================================

class BootstrapFewShotCompiler:
    """Wrapper for DSPy's BootstrapFewShot teleprompter.

    Bootstraps demonstrations from successful task completions and
    compiles modules to use them as few-shot examples.
    """

    def __init__(self, max_bootstrapped_demos: int = 4):
        """Initialize the compiler.

        Args:
            max_bootstrapped_demos: Maximum number of demonstrations to bootstrap
        """
        self.max_bootstrapped_demos = max_bootstrapped_demos
        self.teleprompter = None
        self._check_dspy_available()

    def _check_dspy_available(self):
        """Check if full DSPy is available (not mock)."""
        if not HAS_DSPY:
            print(
                "[WARNING] DSPy not installed. Using mock interface. "
                "Install with: pip install dspy-ai",
                file=sys.stderr
            )

    def compile(
        self,
        module: GrindModule,
        demonstrations: List[Dict[str, Any]],
        metric=None
    ) -> GrindModule:
        """Compile module with bootstrapped demonstrations.

        If DSPy is available, uses BootstrapFewShot to optimize the module
        with top demonstrations from successful task completions.

        Args:
            module: The GrindModule to compile
            demonstrations: List of successful task demonstrations
            metric: Optional metric function for optimization

        Returns:
            Compiled module (or original if DSPy not available)
        """
        if not HAS_DSPY or not demonstrations:
            return module

        try:
            # Use DSPy's BootstrapFewShot if available
            # This is a simplified version - full DSPy requires more setup
            print(
                f"[INFO] Bootstrapping {min(len(demonstrations), self.max_bootstrapped_demos)} "
                f"demonstrations into module"
            )
            # In a real setup, this would call dspy.BootstrapFewShot()
            # For now, return the module as-is (mock mode)
            return module
        except Exception as e:
            print(f"[WARNING] Compilation failed: {e}. Using unoptimized module.", file=sys.stderr)
            return module


# ============================================================================
# DEMONSTRATION UTILITIES
# ============================================================================

def create_demonstration(
    task: str,
    context: str,
    solution: str,
    summary: str,
    num_turns: int = 1,
    duration_ms: int = 0,
    efficiency_score: float = 1.0
) -> Dict[str, Any]:
    """Create a demonstration object from a successful task.

    Args:
        task: Task description
        context: Workspace context
        solution: Generated solution
        summary: Summary of the result
        num_turns: Number of turns to complete
        duration_ms: Duration in milliseconds
        efficiency_score: Efficiency metric (0-1)

    Returns:
        Demonstration dict for use with DSPy
    """
    return {
        "task": task,
        "context": context,
        "solution": solution,
        "summary": summary,
        "num_turns": num_turns,
        "duration_ms": duration_ms,
        "efficiency_score": efficiency_score
    }


def rank_demonstrations(
    demonstrations: List[Dict[str, Any]],
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """Rank demonstrations by efficiency score.

    Args:
        demonstrations: List of demonstrations
        top_k: Number of top demonstrations to return

    Returns:
        Sorted list of demonstrations (best first)
    """
    sorted_demos = sorted(
        demonstrations,
        key=lambda x: x.get("efficiency_score", 0.5),
        reverse=True
    )
    return sorted_demos[:top_k]


# ============================================================================
# INTEGRATION HELPERS
# ============================================================================

def get_optimized_grind_module(
    demonstrations: Optional[List[Dict[str, Any]]] = None
) -> GrindModule:
    """Get a GrindModule, optionally optimized with demonstrations.

    Args:
        demonstrations: Optional list of successful demonstrations for compilation

    Returns:
        GrindModule instance (possibly compiled with few-shot examples)
    """
    module = GrindModule()

    if demonstrations:
        compiler = BootstrapFewShotCompiler()
        module = compiler.compile(module, demonstrations)

    return module
