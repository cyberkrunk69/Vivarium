"""
Skills package.

This is a lightweight registry used by the automatic skill extraction pipeline
(`skill_extractor.py`). The original repo historically had a richer skill
library; the minimal version here keeps imports stable and is sufficient for
tests and basic usage.
"""

from .skill_registry import register_skill, get_skill, list_skills  # noqa: F401

__all__ = ["register_skill", "get_skill", "list_skills"]

