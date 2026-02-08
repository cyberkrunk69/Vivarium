"""
Inference engine utilities (safe-by-default).

This repo historically experimented with multiple backends. For local safety and
testability we keep the public surface area small and avoid any implicit
installation or execution of external CLIs.
"""

from __future__ import annotations

import re
import os
from enum import Enum
from typing import List


class EngineType(Enum):
    """Available inference backends."""

    GROQ = "groq"
    CLAUDE = "claude"
    AUTO = "auto"


# Simple keyword list that usually indicates higher reasoning / coding demand
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
    """Approximate token count using whitespace split."""

    return len(text.split())


def estimate_complexity(request: str) -> int:
    """
    Return a numeric complexity score. Higher scores → more demanding request.

    Scoring factors (simple additive model):
    - Base score = token count // 10
    - +2 for each recognized complexity keyword present
    - +5 if request length > 800 characters (likely multi-step)
    """

    score = _token_count(request) // 10

    lowered = request.lower()
    for kw in _COMPLEXITY_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", lowered):
            score += 2

    if len(request) > 800:
        score += 5

    return score


def get_engine_type_from_env() -> EngineType:
    """Determine engine type from INFERENCE_ENGINE environment variable."""

    env = os.environ.get("INFERENCE_ENGINE", "").strip().lower()
    if env == "groq":
        return EngineType.GROQ
    if env == "claude":
        return EngineType.CLAUDE
    return EngineType.AUTO

