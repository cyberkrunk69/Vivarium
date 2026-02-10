"""
Inference engine utilities (safe-by-default).

This keeps the historical public surface area used by tests while runtime
execution remains on the canonical worker/swarm path.
"""

from __future__ import annotations

import os
import re
from enum import Enum
from typing import List


class EngineType(Enum):
    """Available inference backends."""

    GROQ = "groq"
    CLAUDE = "claude"
    AUTO = "auto"


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
    Return a numeric complexity score. Higher scores -> more demanding request.

    Scoring factors:
    - Base score = token count // 10
    - +2 for each recognized complexity keyword present
    - +5 if request length > 800 characters
    """

    score = _token_count(request) // 10

    lowered = request.lower()
    for keyword in _COMPLEXITY_KEYWORDS:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lowered):
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
