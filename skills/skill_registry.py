"""
Skill registry with compatibility APIs for tool-first routing.

This module intentionally keeps both:
1) lightweight module-level helper functions, and
2) a richer `SkillRegistry` class expected by historical call sites.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
import math
import re
from typing import Dict, List, Optional, Sequence, Tuple

_TOKEN_RE = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]+")


@dataclass(frozen=True)
class Skill:
    name: str
    code: str
    description: str = ""
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


_REGISTRY: Dict[str, Skill] = {}
_BOOTSTRAPPED_DEFAULTS = False


_DEFAULT_SKILLS: Tuple[Dict[str, object], ...] = (
    {
        "name": "add_test_coverage",
        "description": "Generate focused pytest tests for changed behavior.",
        "code": (
            "def add_test_coverage(target_module: str) -> str:\n"
            "    return f\"Add pytest cases for {target_module} edge cases and failures.\""
        ),
        "keywords": ["pytest", "test", "coverage", "regression"],
    },
    {
        "name": "read_json_safe",
        "description": "Read JSON from disk with clear error handling.",
        "code": (
            "import json\n"
            "from pathlib import Path\n\n"
            "def read_json_safe(path: str):\n"
            "    p = Path(path)\n"
            "    return json.loads(p.read_text(encoding='utf-8'))"
        ),
        "keywords": ["json", "read", "parse"],
    },
    {
        "name": "write_json_safe",
        "description": "Write JSON to disk with stable formatting.",
        "code": (
            "import json\n"
            "from pathlib import Path\n\n"
            "def write_json_safe(path: str, data) -> None:\n"
            "    p = Path(path)\n"
            "    p.write_text(json.dumps(data, indent=2), encoding='utf-8')"
        ),
        "keywords": ["json", "write", "save"],
    },
    {
        "name": "validate_python_syntax",
        "description": "Validate Python source code compiles cleanly.",
        "code": (
            "def validate_python_syntax(source: str) -> bool:\n"
            "    compile(source, '<skill>', 'exec')\n"
            "    return True"
        ),
        "keywords": ["python", "syntax", "validate", "compile"],
    },
    {
        "name": "run_command",
        "description": "Execute a shell command and return status/output.",
        "code": (
            "import subprocess\n\n"
            "def run_command(command: str):\n"
            "    proc = subprocess.run(command, shell=True, capture_output=True, text=True)\n"
            "    return {'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}"
        ),
        "keywords": ["shell", "command", "execute"],
    },
    {
        "name": "safe_dict_get",
        "description": "Read nested dictionary values safely.",
        "code": (
            "def safe_dict_get(data: dict, path, default=None):\n"
            "    cur = data\n"
            "    for key in path:\n"
            "        if not isinstance(cur, dict) or key not in cur:\n"
            "            return default\n"
            "        cur = cur[key]\n"
            "    return cur"
        ),
        "keywords": ["dict", "nested", "safe", "get"],
    },
)


def _tokenize(text: str) -> List[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text or "")]


def _to_vector(text: str) -> Dict[str, float]:
    tokens = _tokenize(text)
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = float(sum(counts.values()))
    return {token: count / total for token, count in counts.items()}


def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    dot = sum(vec_a.get(token, 0.0) * vec_b.get(token, 0.0) for token in set(vec_a) & set(vec_b))
    norm_a = math.sqrt(sum(value * value for value in vec_a.values()))
    norm_b = math.sqrt(sum(value * value for value in vec_b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _skill_text(skill: Skill) -> str:
    return " ".join(
        [
            skill.name,
            skill.description,
            " ".join(skill.keywords),
            " ".join(skill.preconditions),
            " ".join(skill.postconditions),
        ]
    ).strip()


def _normalize_terms(values: Optional[Sequence[str]]) -> List[str]:
    if not values:
        return []
    return [str(value).strip() for value in values if str(value).strip()]


def _bootstrap_default_skills() -> None:
    global _BOOTSTRAPPED_DEFAULTS
    if _BOOTSTRAPPED_DEFAULTS:
        return
    for item in _DEFAULT_SKILLS:
        name = str(item["name"])
        if name in _REGISTRY:
            continue
        register_skill(
            name=name,
            code=str(item["code"]),
            description=str(item.get("description", "")),
            keywords=item.get("keywords", []),
        )
    _BOOTSTRAPPED_DEFAULTS = True


def register_skill(
    name: str,
    code: str,
    description: str = "",
    preconditions: Optional[Sequence[str]] = None,
    postconditions: Optional[Sequence[str]] = None,
    keywords: Optional[Sequence[str]] = None,
) -> None:
    """Register or overwrite a skill by name."""
    normalized_name = str(name or "").strip()
    if not normalized_name:
        raise ValueError("skill name must be non-empty")
    _REGISTRY[normalized_name] = Skill(
        name=normalized_name,
        code=str(code or ""),
        description=str(description or ""),
        preconditions=_normalize_terms(preconditions),
        postconditions=_normalize_terms(postconditions),
        keywords=_normalize_terms(keywords),
    )


def get_skill(name: str) -> Optional[Dict[str, object]]:
    """Return a skill dict or None."""
    skill = _REGISTRY.get(str(name))
    return skill.to_dict() if skill else None


def list_skills() -> List[str]:
    """List registered skill names."""
    _bootstrap_default_skills()
    return sorted(_REGISTRY.keys())


def find_similar_skills(
    query: str,
    top_k: int = 3,
    *,
    min_similarity: float = 0.0,
) -> List[Tuple[str, float]]:
    """Return `(skill_name, similarity)` tuples sorted descending."""
    _bootstrap_default_skills()
    query_vector = _to_vector(query)
    if not _REGISTRY:
        return []
    scored: List[Tuple[str, float]] = []
    for name, skill in _REGISTRY.items():
        score = _cosine_similarity(query_vector, _to_vector(_skill_text(skill)))
        if score >= min_similarity:
            scored.append((name, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[: max(0, int(top_k))]


def retrieve_skill(task_description: str, min_similarity: float = 0.18) -> Optional[Dict[str, object]]:
    """Retrieve the single best skill for a task description."""
    ranked = find_similar_skills(task_description, top_k=1, min_similarity=min_similarity)
    if ranked:
        return get_skill(ranked[0][0])

    # Fallback to direct keyword containment when similarity is very low.
    task_tokens = set(_tokenize(task_description))
    if not task_tokens:
        return None
    for name, skill in _REGISTRY.items():
        if set(_tokenize(name)) & task_tokens:
            return skill.to_dict()
        if set(_tokenize(skill.description)) & task_tokens:
            return skill.to_dict()
    return None


def compose_skills(skill_names: Sequence[str]) -> Optional[Dict[str, object]]:
    """
    Compose multiple registered skills into a combined executable tool payload.
    """
    _bootstrap_default_skills()
    deduped_names: List[str] = []
    for item in skill_names or []:
        name = str(item).strip()
        if name and name not in deduped_names:
            deduped_names.append(name)

    if not deduped_names:
        return None

    parts: List[Skill] = [skill for name in deduped_names if (skill := _REGISTRY.get(name))]
    if not parts:
        return None
    if len(parts) == 1:
        payload = parts[0].to_dict()
        payload["components"] = [parts[0].name]
        return payload

    composed_name = "composed_" + "_".join(skill.name for skill in parts[:3])
    composed_code = "\n\n".join(
        f"# --- Skill: {skill.name} ---\n{skill.code}".rstrip()
        for skill in parts
    )
    composed_description = "Composed skill pipeline: " + " -> ".join(skill.name for skill in parts)
    preconditions = [item for skill in parts for item in skill.preconditions]
    postconditions = [item for skill in parts for item in skill.postconditions]
    keywords = sorted({token for skill in parts for token in skill.keywords})
    return {
        "name": composed_name,
        "code": composed_code,
        "description": composed_description,
        "preconditions": preconditions,
        "postconditions": postconditions,
        "keywords": keywords,
        "components": [skill.name for skill in parts],
    }


def decompose_task(task_description: str, top_k: int = 3) -> List[str]:
    """Suggest component skills for task decomposition."""
    ranked = find_similar_skills(task_description, top_k=top_k, min_similarity=0.1)
    return [name for name, score in ranked if score > 0.0]


class SkillRegistry:
    """
    Backward-compatible registry wrapper used by router/intent/context modules.
    """

    def __init__(self) -> None:
        _bootstrap_default_skills()
        # Some call sites probe for this attribute before using embeddings.
        self.vectorizer = None

    def register_skill(
        self,
        name: str,
        code: str,
        description: str = "",
        preconditions: Optional[Sequence[str]] = None,
        postconditions: Optional[Sequence[str]] = None,
        keywords: Optional[Sequence[str]] = None,
    ) -> None:
        register_skill(name, code, description, preconditions, postconditions, keywords)

    def get_skill(self, name: str) -> Optional[Dict[str, object]]:
        return get_skill(name)

    def list_skills(self) -> List[str]:
        return list_skills()

    def retrieve_skill(self, task_description: str, min_similarity: float = 0.18) -> Optional[Dict[str, object]]:
        return retrieve_skill(task_description, min_similarity=min_similarity)

    def find_similar_skills(
        self,
        query: str,
        top_k: int = 3,
        log_expansion: bool = False,
    ) -> List[Tuple[str, float]]:
        # `log_expansion` is accepted for compatibility with context builder.
        _ = log_expansion
        return find_similar_skills(query, top_k=top_k, min_similarity=0.0)

    def decompose_task(self, task_description: str, top_k: int = 3) -> List[str]:
        return decompose_task(task_description, top_k=top_k)

    def compose_skills(self, skill_names: Sequence[str]) -> Optional[Dict[str, object]]:
        return compose_skills(skill_names)

    def compute_embedding(self, text: str) -> Dict[str, float]:
        return _to_vector(text)


__all__ = [
    "Skill",
    "SkillRegistry",
    "register_skill",
    "get_skill",
    "list_skills",
    "find_similar_skills",
    "retrieve_skill",
    "compose_skills",
    "decompose_task",
]

