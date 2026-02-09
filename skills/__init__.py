"""
Skills package.

This is a lightweight registry used by the automatic skill extraction pipeline
(`skill_extractor.py`). The original repo historically had a richer skill
library; the minimal version here keeps imports stable and is sufficient for
tests and basic usage.
"""

from .skill_registry import (  # noqa: F401
    SkillRegistry,
    compose_skills,
    decompose_task,
    find_similar_skills,
    get_skill,
    list_skills,
    register_skill,
    retrieve_skill,
)

__all__ = [
    "SkillRegistry",
    "register_skill",
    "get_skill",
    "list_skills",
    "find_similar_skills",
    "retrieve_skill",
    "compose_skills",
    "decompose_task",
]

