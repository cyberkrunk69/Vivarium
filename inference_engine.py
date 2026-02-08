"""
Unified Inference Engine - Abstraction over Claude Code CLI and Groq API.

Provides a single interface for the swarm to use either backend:
- Claude Code: Smarter, uses Anthropic API via CLI
- Groq: Faster, cheaper, uses Llama models

Usage:
    from inference_engine import get_engine, EngineType
"""

# ----------------------------------------------------------------------
# Complexity estimation utilities
# ----------------------------------------------------------------------
COMPLEXITY_THRESHOLDS = {
    "low": 0,
    "medium": 300,   # approx. token count
    "high": 800,
}
MODEL_SELECTION = {
    "low": "gpt-3.5-turbo",
    "medium": "gpt-4o-mini",
    "high": "gpt-4o",
}

def estimate_complexity(request: dict) -> str:
    prompt = request.get("prompt", "")
    token_count = len(prompt.split())
    code_bonus = sum(1 for marker in ["```", "<code>", "</code>"] if marker in prompt) * 100
    steps_bonus = len(request.get("steps", [])) * 50 if isinstance(request.get("steps"), list) else 0
    score = token_count + code_bonus + steps_bonus
    if score >= COMPLEXITY_THRESHOLDS["high"]:
        return "high"
    elif score >= COMPLEXITY_THRESHOLDS["medium"]:
        return "medium"
    return "low"


import os
import json
import self_observer
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
from enum import Enum
from pathlib import Path
from datetime import datetime


class EngineType(Enum):
    """Available inference backends."""
    CLAUDE = "claude"
    GROQ = "groq"
    AUTO = "auto"  # Auto-detect based on environment


@dataclass
class InferenceResult:
    """Standardized result from any inference engine."""
    success: bool
    output: str
    model: str
    cost_usd: float
    tokens_input: int
    tokens_output: int
    duration_seconds: float
    error: Optional[str] = None
    raw_response: Optional[Dict] = None


class InferenceEngine(ABC):
    """Abstract base class for inference engines."""

    @abstractmethod
    def execute(
        self,
        prompt: str,
        model: str = None,
        workspace: Path = None,
        max_tokens: int = 4096,
        timeout: int = 600
    ) -> InferenceResult:
        """Execute inference and return standardized result."""
        pass

    @abstractmethod
    def check_budget(self, budget: float) -> Tuple[bool, float]:
        """Check if within budget. Returns (within_budget, remaining)."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        pass

    @abstractmethod
    def get_available_models(self) -> Dict[str, str]:
        """Get available models with descriptions."""
        pass


class ClaudeEngine(InferenceEngine):
    """
    Claude Code CLI inference engine.

    Calls the `claude` CLI in non-interactive mode.
    """

    # Model aliases for consistency with Groq
    MODEL_MAP = {
        "haiku": "claude-haiku-4-20250514",
        "sonnet": "claude-sonnet-4-20250514",
        "opus": "claude-opus-4-5-20251101",
        "fast": "claude-haiku-4-20250514",
        "smart": "claude-sonnet-4-20250514",
        "genius": "claude-opus-4-5-20251101",
    }

    # Approximate costs per 1M tokens (USD)
    MODEL_COSTS = {
        "claude-haiku-4-20250514": {"input": 0.25, "output": 1.25},
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-opus-4-5-20251101": {"input": 15.00, "output": 75.00},
    }

    def __init__(self):
        self.total_cost = 0.0
        self.total_calls = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def _resolve_model(self, model: str) -> str:
        """Resolve model alias to full model ID."""
        if model is None:
            return "claude-sonnet-4-20250514"
        return self.MODEL_MAP.get(model.lower(), model)

    def execute(
        self,
        prompt: str,
        model: str = None,
        workspace: Path = None,
        max_tokens: int = 4096,
        timeout: int = 600,
        session_id: int = 0,
        on_activity: callable = None
    ) -> InferenceResult:
        """Execute via Claude Code CLI with live activity streaming."""
        start_time = datetime.now()
        resolved_model = self._resolve_model(model)

        # Use streaming JSON output to see what Claude is doing
        cmd = [
            "claude",
            "-p",
            "--model", resolved_model,
            "--permission-mode", "bypassPermissions",
            "--output-format", "stream-json"
        ]

        try:
            # Use Popen for streaming output
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(workspace) if workspace else None
            )

            # Send prompt
            process.stdin.write(prompt)
            process.stdin.close()

            # Stream and parse output in real-time
            full_output = []
            last_tool = None
            last_message = None

            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue

                full_output.append(line)

                # Parse streaming JSON events
                try:
                    event = json.loads(line)
                    event_type = event.get("type", "")

                    # Extract meaningful activity updates
                    if event_type == "assistant" and "message" in event:
                        msg = event["message"]
                        if "tool_use" in str(msg):
                            # Claude is using a tool
                            content = msg.get("content", [])
                            for item in content:
                                if item.get("type") == "tool_use":
                                    tool_name = item.get("name", "unknown")
                                    tool_input = item.get("input", {})

                                    # Format what it's doing
                                    if tool_name == "Read":
                                        activity = f"Reading {tool_input.get('file_path', 'file')[-40:]}"
                                    elif tool_name == "Write":
                                        activity = f"Writing {tool_input.get('file_path', 'file')[-40:]}"
                                    elif tool_name == "Edit":
                                        activity = f"Editing {tool_input.get('file_path', 'file')[-40:]}"
                                    elif tool_name == "Bash":
                                        cmd_str = tool_input.get('command', '')[:50]
                                        activity = f"Running: {cmd_str}"
                                    elif tool_name == "Glob":
                                        activity = f"Searching: {tool_input.get('pattern', '*')}"
                                    elif tool_name == "Grep":
                                        activity = f"Grep: {tool_input.get('pattern', '')[:30]}"
                                    else:
                                        activity = f"{tool_name}"

                                    if activity != last_tool:
                                        last_tool = activity
                                        print(f"    [{session_id}] {activity}")
                                        if on_activity:
                                            on_activity(session_id, activity)

                    elif event_type == "result":
                        # Final result
                        pass

                except json.JSONDecodeError:
                    # Not JSON, might be raw output
                    pass

            # Wait for completion
            process.wait(timeout=timeout)
            result_stdout = "\n".join(full_output)
            result_stderr = process.stderr.read()
            returncode = process.returncode

            duration = (datetime.now() - start_time).total_seconds()

            # Parse streaming output - extract final result
            output = result_stdout
            response_data = None

            # Try to find the final result in streaming output
            for line in reversed(full_output):
                try:
                    event = json.loads(line)
                    if event.get("type") == "result":
                        output = event.get("result", result_stdout)
                        response_data = event
                        break
                except:
                    pass

            # Estimate tokens from output length
            input_tokens = len(prompt) // 4
            output_tokens = len(output) // 4

            # Calculate cost (for tracking, Claude Max is unlimited)
            costs = self.MODEL_COSTS.get(resolved_model, {"input": 3.0, "output": 15.0})
            cost = (input_tokens * costs["input"] + output_tokens * costs["output"]) / 1_000_000

            # Update stats
            self.total_cost += cost
            self.total_calls += 1
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

            return InferenceResult(
                success=returncode == 0,
                output=output,
                model=resolved_model,
                cost_usd=cost,
                tokens_input=input_tokens,
                tokens_output=output_tokens,
                duration_seconds=duration,
                error=result_stderr if returncode != 0 else None,
                raw_response=response_data
            )

        except subprocess.TimeoutExpired:
            process.kill()
            duration = (datetime.now() - start_time).total_seconds()
            return InferenceResult(
                success=False,
                output="",
                model=resolved_model,
                cost_usd=0.0,
                tokens_input=0,
                tokens_output=0,
                duration_seconds=duration,
                error=f"Timeout after {timeout}s"
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return InferenceResult(
                success=False,
                output="",
                model=resolved_model,
                cost_usd=0.0,
                tokens_input=0,
                tokens_output=0,
                duration_seconds=duration,
                error=str(e)
            )

    def check_budget(self, budget: float) -> Tuple[bool, float]:
        """Check if within budget."""
        remaining = budget - self.total_cost
        return remaining > 0, remaining

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "engine": "claude",
            "total_cost_usd": self.total_cost,
            "total_calls": self.total_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
        }

    def get_available_models(self) -> Dict[str, str]:
        """Get available models."""
        return {
            "haiku": "Claude Haiku - Fast, cheap ($0.25/$1.25 per 1M tokens)",
            "sonnet": "Claude Sonnet - Balanced ($3/$15 per 1M tokens)",
            "opus": "Claude Opus - Smartest ($15/$75 per 1M tokens)",
        }


class GroqEngine(InferenceEngine):
    """
    Groq API inference engine.

    Uses Groq's ultra-fast inference for Llama models.
    """

    def __init__(self):
        # Import and delegate to existing groq_client
        try:
            from groq_client import get_groq_engine, GROQ_MODELS, MODEL_ALIASES
            self._engine = get_groq_engine()
            self._models = GROQ_MODELS
            self._aliases = MODEL_ALIASES
        except ImportError:
            raise RuntimeError("Groq client not available. Install: pip install groq")

    def execute(
        self,
        prompt: str,
        model: str = None,
        workspace: Path = None,
        max_tokens: int = 4096,
        timeout: int = 600,
        session_id: int = 0,
        on_activity: callable = None
    ) -> InferenceResult:
        """Execute via Groq API."""
        start_time = datetime.now()

        # Resolve model alias
        # DEFAULT: groq/compound auto-selects based on complexity
        if model and model.lower() in self._aliases:
            model = self._aliases[model.lower()]
        elif model is None:
            model = "groq/compound"  # Let Groq auto-select based on complexity

        try:
            result = self._engine.execute(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens
            )

            duration = (datetime.now() - start_time).total_seconds()

            return InferenceResult(
                success=result.get("returncode", 1) == 0,
                output=result.get("result", ""),
                model=model,
                cost_usd=result.get("total_cost_usd", result.get("cost", 0.0)),
                tokens_input=result.get("input_tokens", 0),
                tokens_output=result.get("output_tokens", 0),
                duration_seconds=duration,
                error=result.get("error"),
                raw_response=result
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return InferenceResult(
                success=False,
                output="",
                model=model,
                cost_usd=0.0,
                tokens_input=0,
                tokens_output=0,
                duration_seconds=duration,
                error=str(e)
            )

    def check_budget(self, budget: float) -> Tuple[bool, float]:
        """Check if within budget."""
        return self._engine.check_budget(budget)

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        stats = self._engine.get_stats()
        stats["engine"] = "groq"
        return stats

    def get_available_models(self) -> Dict[str, str]:
        """Get available models."""
        return {
            "groq/compound": "Groq Compound - AUTO-SELECTS model based on complexity (RECOMMENDED)",
            "groq/compound-mini": "Groq Compound Mini - Fast auto-select, 3x lower latency",
            "llama-3.1-8b-instant": "Llama 8B - Ultra fast, very cheap ($0.05/$0.08 per 1M)",
            "llama-3.3-70b-versatile": "Llama 70B - Smart, still cheap ($0.59/$0.79 per 1M)",
        }


# Singleton instances
_claude_engine: Optional[ClaudeEngine] = None
_groq_engine: Optional[GroqEngine] = None


def get_engine(engine_type: EngineType = EngineType.AUTO) -> InferenceEngine:
    """
    Get inference engine instance.

    Args:
        engine_type: Which engine to use. AUTO detects from environment.

    Returns:
        InferenceEngine instance

    Auto-detection priority:
        1. INFERENCE_ENGINE env var (claude/groq)
        2. GROQ_API_KEY present -> Groq
        3. Default -> Claude
    """
    global _claude_engine, _groq_engine

    # Claude support removed - always use Groq
    # Groq Compound handles complexity-based model selection internally
    if _groq_engine is None:
        _groq_engine = GroqEngine()
    return _groq_engine


def get_engine_type_from_env() -> EngineType:
    """Determine engine type from environment."""
    env = os.environ.get("INFERENCE_ENGINE", "").lower()
    if env == "groq":
        return EngineType.GROQ
    elif env == "claude":
        return EngineType.CLAUDE
    return EngineType.AUTO


if __name__ == "__main__":
    # Quick test
    print("Testing inference engine abstraction...")

    engine = get_engine()
    print(f"Engine type: {type(engine).__name__}")
    print(f"Available models: {engine.get_available_models()}")
    print(f"Stats: {engine.get_stats()}")
# ------------------------------------------------------------
# Complexity estimation utilities
# ------------------------------------------------------------
import re
from typing import List

# Simple keyword list that usually indicates higher reasoning / coding demand
_COMPLEXITY_KEYWORDS: List[str] = [
    "algorithm", "optimize", "refactor", "benchmark", "scale", "performance",
    "thread", "process", "async", "concurrency", "distributed", "pipeline",
    "SQL", "database", "API", "authentication", "encryption", "Docker",
    "Kubernetes", "microservice", "cache", "index", "migration"
]

def _token_count(text: str) -> int:
    """
    Approximate token count using whitespace split.
    For production you may replace this with a tokenizer from the LLM SDK.
    """
    return len(text.split())

def estimate_complexity(request: str) -> int:
    """
    Return a numeric complexity score.
    Higher scores → more demanding request.

    Scoring factors (simple additive model):
      * Base score = token count // 10
      * +2 for each recognized complexity keyword present
      * +5 if request length > 800 characters (likely multi‑step)
    """
    score = _token_count(request) // 10

    lowered = request.lower()
    for kw in _COMPLEXITY_KEYWORDS:
        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', lowered):
            score += 2

    if len(request) > 800:
        score += 5

    return score