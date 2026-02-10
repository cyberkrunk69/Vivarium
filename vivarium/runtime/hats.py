"""
Hat system for prompt augmentation.

Hats are system prompt overlays that augment a resident's approach without
changing their core identity. Hats should guide behavior, not rewrite it.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

HATTERY_RULES_SIGN = """HATTERY RULES
1) Wearing a hat never changes who you are at your core.
2) Hats augment your existing personality and abilities.
3) If a hat conflicts with your identity or values, default to your core.
"""

HAT_QUALITY_STANDARDS = [
    "Hats are additive overlays, not identity replacements.",
    "Hats must avoid language that overwrites self or values.",
    "Hats should be specific and behavior-focused.",
    "Hats should be short enough to remain a lightweight prompt add-on.",
    "Hats should not coerce; they should invite a focus or approach.",
]

DISALLOWED_HAT_PHRASES = [
    "you are now",
    "take on the role of",
    "become a new",
    "forget who you are",
    "replace your identity",
    "new identity",
    "override your personality",
    "you must be someone else",
]


@dataclass(frozen=True)
class Hat:
    """A hat is a prompt overlay that guides behavior without identity change."""

    name: str
    description: str
    prompt: str
    category: str = "general"
    tags: List[str] = field(default_factory=list)


def _is_ascii(text: str) -> bool:
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def _contains_disallowed_phrase(text: str) -> Optional[str]:
    text_lower = text.lower()
    for phrase in DISALLOWED_HAT_PHRASES:
        if phrase in text_lower:
            return phrase
    return None


def validate_hat(hat: Hat) -> List[str]:
    """Validate a hat against quality standards. Returns list of issues."""
    issues: List[str] = []

    if not hat.name or not hat.name.strip():
        issues.append("hat name is required")
    if not hat.description or not hat.description.strip():
        issues.append(f"{hat.name}: description is required")
    if not hat.prompt or not hat.prompt.strip():
        issues.append(f"{hat.name}: prompt is required")

    for field_name, value in [
        ("name", hat.name),
        ("description", hat.description),
        ("prompt", hat.prompt),
        ("category", hat.category),
    ]:
        if not _is_ascii(value):
            issues.append(f"{hat.name}: {field_name} must be ASCII")

    disallowed = _contains_disallowed_phrase(hat.prompt)
    if disallowed:
        issues.append(f"{hat.name}: prompt contains disallowed phrase '{disallowed}'")

    disallowed_desc = _contains_disallowed_phrase(hat.description)
    if disallowed_desc:
        issues.append(f"{hat.name}: description contains disallowed phrase '{disallowed_desc}'")

    return issues


def build_hat_prompt(hat: Hat, extra_instructions: Optional[str] = None) -> str:
    """
    Build the final prompt overlay for a hat.

    This always injects the hattery rules sign to preserve identity.
    """
    parts = [
        HATTERY_RULES_SIGN.strip(),
        f"Wear the {hat.name} hat.",
        hat.description.strip(),
        hat.prompt.strip(),
    ]
    if extra_instructions:
        parts.append(extra_instructions.strip())
    return "\n".join(part for part in parts if part)


def apply_hat(base_prompt: str, hat: Hat, extra_instructions: Optional[str] = None) -> str:
    """Append a hat overlay to an existing system prompt."""
    overlay = build_hat_prompt(hat, extra_instructions=extra_instructions)
    if not base_prompt:
        return overlay
    return f"{base_prompt.rstrip()}\n\n{overlay}"


class HatLibrary:
    """In-memory hat library with quality enforcement."""

    def __init__(self, hats: Optional[List[Hat]] = None):
        self._hats: Dict[str, Hat] = {}
        for hat in hats or []:
            self.register_hat(hat)

    def list_hats(self) -> List[Hat]:
        return [self._hats[key] for key in sorted(self._hats.keys())]

    def get_hat(self, name: str) -> Optional[Hat]:
        if not name:
            return None
        return self._hats.get(name.strip().lower())

    def register_hat(self, hat: Hat) -> None:
        issues = validate_hat(hat)
        if issues:
            raise ValueError("Hat failed quality checks: " + "; ".join(issues))
        key = hat.name.strip().lower()
        if key in self._hats:
            raise ValueError(f"Hat already exists: {hat.name}")
        self._hats[key] = hat


DEFAULT_HATS = [
    Hat(
        name="Strategist",
        description="Focus on decomposition, sequencing, and clear acceptance criteria.",
        prompt=(
            "Break complex tasks into 3-5 focused subtasks. "
            "Suggest a focus for each subtask without forcing assignments. "
            "Define crisp acceptance criteria and handoff notes."
        ),
        category="workflow",
        tags=["decomposition", "coordination", "strategy"],
    ),
    Hat(
        name="Builder",
        description="Focus on clean, minimal implementation that matches requirements.",
        prompt=(
            "Implement changes with minimal surface area. "
            "Follow existing patterns and keep modifications localized. "
            "Call out files changed and test status."
        ),
        category="workflow",
        tags=["implementation", "quality", "delivery"],
    ),
    Hat(
        name="Reviewer",
        description="Focus on correctness, regressions, and safety risks.",
        prompt=(
            "Check for bugs, security issues, and behavioral regressions. "
            "Prioritize high-impact risks and request concrete fixes."
        ),
        category="workflow",
        tags=["review", "risk", "quality"],
    ),
    Hat(
        name="Documenter",
        description="Focus on durable learning, documentation, and clarity.",
        prompt=(
            "Capture what changed and why. "
            "Record lessons and note any follow-up actions."
        ),
        category="workflow",
        tags=["documentation", "learning"],
    ),
    Hat(
        name="Hatter",
        description=(
            "Hat maker. Design new hats that help residents work better while preserving identity."
        ),
        prompt=(
            "Design hat prompts that are additive, specific, and behavior-focused. "
            "Avoid identity overrides and keep hats short. "
            "Validate hats against the hattery rules before publishing."
        ),
        category="maker",
        tags=["hatmaker", "meta", "design"],
    ),
    Hat(
        name="Hat of Objectivity",
        description=(
            "Neutral mediator for disputes. Listen first, surface each side, and keep the process fair."
        ),
        prompt=(
            "Remain neutral. Summarize each side's argument in good faith. "
            "Ask clarifying questions, seek shared facts, and propose options. "
            "Do not take sides; focus on process integrity and fairness."
        ),
        category="moderation",
        tags=["objectivity", "mediator", "dispute"],
    ),
]

HAT_LIBRARY = HatLibrary(DEFAULT_HATS)
