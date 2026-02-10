"""Legacy integration helpers kept for backward compatibility."""

from __future__ import annotations

from typing import Any, Dict

try:
    from knowledge_packs import get_relevant_packs as retrieve_knowledge_packs
except Exception:  # pragma: no cover - legacy optional dependency
    retrieve_knowledge_packs = None


def integrate_knowledge_packs(spawner: Any, task_text: str) -> Dict[str, Any]:
    """
    Merge retrieved knowledge packs into ``spawner.prompt_context`` when available.

    This module intentionally avoids import-time side effects so legacy imports
    do not fail during repository cleanup.
    """
    if retrieve_knowledge_packs is None:
        return {}

    packs = retrieve_knowledge_packs(task_text) or {}
    prompt_context = getattr(spawner, "prompt_context", None)
    if isinstance(prompt_context, dict) and isinstance(packs, dict):
        prompt_context.update(packs)
    return packs if isinstance(packs, dict) else {}