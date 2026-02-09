"""
Unified Inference Engine - Groq-only abstraction.

Provides a single interface for Groq inference with standardized results.
"""

from __future__ import annotations

import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List


class EngineType(Enum):
    """Available inference backends."""

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
    raw_response: Optional[Dict[str, Any]] = None


class InferenceEngine(ABC):
    """Abstract base class for inference engines."""

    @abstractmethod
    def execute(
        self,
        prompt: str,
        model: str = None,
        workspace: Path = None,
        max_tokens: int = 4096,
        timeout: int = 600,
        session_id: int = 0,
        on_activity: callable = None,
    ) -> InferenceResult:
        """Execute inference and return standardized result."""

    @abstractmethod
    def check_budget(self, budget: float) -> Tuple[bool, float]:
        """Check if within budget. Returns (within_budget, remaining)."""

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""

    @abstractmethod
    def get_available_models(self) -> Dict[str, str]:
        """Get available models with descriptions."""


class GroqEngine(InferenceEngine):
    """
    Groq API inference engine.

    Uses Groq's ultra-fast inference for Llama/GPT-OSS models.
    """

    def __init__(self):
        # Import and delegate to existing groq_client
        try:
            from groq_client import get_groq_engine, GROQ_MODELS, MODEL_ALIASES

            self._engine = get_groq_engine()
            self._models = GROQ_MODELS
            self._aliases = MODEL_ALIASES
        except ImportError as exc:
            raise RuntimeError("Groq client not available. Install: pip install groq") from exc

    def execute(
        self,
        prompt: str,
        model: str = None,
        workspace: Path = None,
        max_tokens: int = 4096,
        timeout: int = 600,
        session_id: int = 0,
        on_activity: callable = None,
    ) -> InferenceResult:
        """Execute via Groq API."""
        start_time = datetime.now()

        # Resolve model alias
        if model and model.lower() in self._aliases:
            model = self._aliases[model.lower()]
        elif model is None:
            model = "groq/compound"  # Let Groq auto-select based on complexity

        try:
            result = self._engine.execute(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                timeout=timeout,
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
                raw_response=result,
            )

        except Exception as exc:
            duration = (datetime.now() - start_time).total_seconds()
            return InferenceResult(
                success=False,
                output="",
                model=model,
                cost_usd=0.0,
                tokens_input=0,
                tokens_output=0,
                duration_seconds=duration,
                error=str(exc),
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
_groq_engine: Optional[GroqEngine] = None


def get_engine(engine_type: EngineType = EngineType.AUTO) -> InferenceEngine:
    """
    Get inference engine instance.

    Args:
        engine_type: Which engine to use. AUTO detects from environment.

    Returns:
        InferenceEngine instance
    """
    global _groq_engine

    if _groq_engine is None:
        _groq_engine = GroqEngine()
    return _groq_engine


def get_engine_type_from_env() -> EngineType:
    """Determine engine type from environment."""
    env = os.environ.get("INFERENCE_ENGINE", "").lower()
    if env == "groq":
        return EngineType.GROQ
    return EngineType.AUTO


# ------------------------------------------------------------
# Complexity estimation utilities
# ------------------------------------------------------------
_COMPLEXITY_KEYWORDS: List[str] = [
    "algorithm",
    "optimize",
    "refactor",
    "benchmark",
    "scale",
    "performance",
    "thread",
    "process",
    "async",
    "concurrency",
    "distributed",
    "pipeline",
    "sql",
    "database",
    "api",
    "authentication",
    "encryption",
    "docker",
    "kubernetes",
    "microservice",
    "cache",
    "index",
    "migration",
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
    Higher scores -> more demanding request.

    Scoring factors (simple additive model):
      * Base score = token count // 10
      * +2 for each recognized complexity keyword present
      * +5 if request length > 800 characters (likely multi-step)
    """
    score = _token_count(request) // 10

    lowered = request.lower()
    for kw in _COMPLEXITY_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", lowered):
            score += 2

    if len(request) > 800:
        score += 5

    return score


if __name__ == "__main__":
    # Quick test
    print("Testing inference engine abstraction...")
    engine = get_engine()
    print(f"Engine type: {type(engine).__name__}")
    print(f"Available models: {engine.get_available_models()}")
    print(f"Stats: {engine.get_stats()}")
