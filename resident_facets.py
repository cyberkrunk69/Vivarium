"""
Resident facet decomposition (voluntary, identity-preserving).

Facets are optional focus modes, not hard assignments. A single resident can
split into temporary shards to cover subtasks while retaining a shared sense
of self.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResidentShard:
    resident_id: str
    identity_id: str
    shard_id: str
    focus: str
    note: str = ""


@dataclass
class FacetSuggestion:
    name: str
    description: str


@dataclass
class ResidentSubtask:
    subtask_id: str
    description: str
    suggested_focus: Optional[str] = None
    resident_id: Optional[str] = None
    identity_id: Optional[str] = None
    shard_id: Optional[str] = None
    voluntary: bool = True


@dataclass
class ResidentPlan:
    task: str
    resident_id: str
    identity_id: str
    subtasks: List[ResidentSubtask] = field(default_factory=list)
    shard_plan: List[ResidentShard] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


DEFAULT_FACETS = [
    FacetSuggestion("strategy", "Clarify intent, risks, and success criteria."),
    FacetSuggestion("build", "Implement changes with minimal disruption."),
    FacetSuggestion("review", "Validate outputs and catch regressions."),
    FacetSuggestion("document", "Summarize outcomes and record lessons."),
]


def suggest_facets(task: str) -> List[FacetSuggestion]:
    task_lower = task.lower()
    facets = []
    if any(word in task_lower for word in ["plan", "design", "strategy", "architecture"]):
        facets.append(DEFAULT_FACETS[0])
    if any(word in task_lower for word in ["build", "implement", "code", "fix", "refactor"]):
        facets.append(DEFAULT_FACETS[1])
    if any(word in task_lower for word in ["review", "audit", "verify", "test"]):
        facets.append(DEFAULT_FACETS[2])
    if any(word in task_lower for word in ["doc", "document", "summarize", "write"]):
        facets.append(DEFAULT_FACETS[3])
    return facets or DEFAULT_FACETS[:2]


def split_resident(resident_id: str, identity_id: str, focuses: List[str]) -> List[ResidentShard]:
    shards = []
    for focus in focuses:
        shards.append(
            ResidentShard(
                resident_id=resident_id,
                identity_id=identity_id,
                shard_id=f"shard_{uuid.uuid4().hex[:6]}",
                focus=focus,
            )
        )
    return shards


def _split_task_sentences(task: str, max_parts: int) -> List[str]:
    parts = re.split(r"[\\n;]+|\\band\\b|\\bthen\\b", task, flags=re.IGNORECASE)
    cleaned = [p.strip() for p in parts if p.strip()]
    if not cleaned:
        return [task.strip()]
    return cleaned[:max_parts]


def decompose_task(
    task: str,
    resident_id: str,
    identity_id: str,
    max_subtasks: int = 3,
) -> ResidentPlan:
    fragments = _split_task_sentences(task, max_subtasks)
    facets = suggest_facets(task)
    shard_focuses = [f.name for f in facets[: len(fragments)]]
    shards = split_resident(resident_id, identity_id, shard_focuses)

    subtasks: List[ResidentSubtask] = []
    for idx, fragment in enumerate(fragments, start=1):
        shard = shards[min(idx - 1, len(shards) - 1)]
        subtasks.append(
            ResidentSubtask(
                subtask_id=f"subtask_{idx:02d}",
                description=fragment,
                suggested_focus=shard.focus,
                resident_id=resident_id,
                identity_id=identity_id,
                shard_id=shard.shard_id,
                voluntary=True,
            )
        )

    return ResidentPlan(
        task=task,
        resident_id=resident_id,
        identity_id=identity_id,
        subtasks=subtasks,
        shard_plan=shards,
        notes=[
            "Facets are suggestions only.",
            "All subtasks remain voluntary and identity-preserving.",
        ],
    )
