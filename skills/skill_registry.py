"""
Minimal in-memory skill registry.

The repo contains code paths that import `skills.skill_registry` to register and
retrieve reusable code snippets extracted from successful sessions.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Sequence


@dataclass(frozen=True)
class Skill:
    name: str
    code: str
    description: str = ""
    preconditions: List[str] = None
    postconditions: List[str] = None

    def to_dict(self) -> Dict:
        d = asdict(self)
        # Normalize None lists
        d["preconditions"] = d["preconditions"] or []
        d["postconditions"] = d["postconditions"] or []
        return d


_REGISTRY: Dict[str, Skill] = {}


def register_skill(
    name: str,
    code: str,
    description: str = "",
    preconditions: Optional[Sequence[str]] = None,
    postconditions: Optional[Sequence[str]] = None,
) -> None:
    """Register or overwrite a skill by name."""
    _REGISTRY[name] = Skill(
        name=name,
        code=code,
        description=description,
        preconditions=list(preconditions) if preconditions else [],
        postconditions=list(postconditions) if postconditions else [],
    )


def get_skill(name: str) -> Optional[Dict]:
    """Return a skill dict or None."""
    skill = _REGISTRY.get(name)
    return skill.to_dict() if skill else None


def list_skills() -> List[str]:
    """List registered skill names."""
    return sorted(_REGISTRY.keys())

