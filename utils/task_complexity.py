import re
from typing import List, Dict, Any, Optional


FILE_PATTERN = re.compile(
    r"(?P<file>[\w./-]+\.(py|js|ts|tsx|jsx|md|json|yaml|yml|toml|ini|sh|sql|css|html))",
    re.IGNORECASE,
)


def extract_file_names(task_description: str) -> List[str]:
    if not task_description:
        return []
    return list({match.group("file") for match in FILE_PATTERN.finditer(task_description)})


def analyze_task_complexity(
    task_description: str,
    file_names: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Compute a normalized complexity score (0.0 – 1.0) with richer signals.
    Returns analysis + recommended model tier + suggested budget multiplier.
    """
    description = task_description or ""
    description_lower = description.lower()
    metadata = metadata or {}

    # ----- signal: word count (longer tasks are usually more complex) -----
    words = len(re.findall(r"\w+", description))
    word_score = min(words / 250.0, 1.0) * 0.25

    # ----- signal: high vs low complexity verbs -----
    high_complexity_keywords = {
        "create", "implement", "design", "architecture", "build",
        "refactor", "migrate", "optimize", "integrate", "orchestrate",
    }
    low_complexity_keywords = {"fix", "update", "add", "rename", "tweak", "typo"}
    high_hits = sum(kw in description_lower for kw in high_complexity_keywords)
    low_hits = sum(kw in description_lower for kw in low_complexity_keywords)
    verb_score = min(high_hits * 0.06, 0.30) - min(low_hits * 0.04, 0.18)

    # ----- signal: explicit steps / multi-part instructions -----
    step_hits = len(re.findall(r"^\s*(\d+\.|-|\*)\s+", description, re.MULTILINE))
    step_score = min(step_hits / 6.0, 1.0) * 0.15

    # ----- signal: file references -----
    files = file_names or extract_file_names(description)
    file_score = min(len(files) / 8.0, 1.0) * 0.20

    # ----- signal: research / architecture references -----
    paper_patterns = [
        r"arxiv\.org/abs/\d{4}\.\d{4,5}",
        r"doi:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+",
        r"\b(resnet|transformer|gpt|bert|vgg|cnn|rnn|llm|rlhf)\b",
    ]
    ref_hits = sum(bool(re.search(pat, description, re.I)) for pat in paper_patterns)
    ref_score = min(ref_hits * 0.08, 0.20)

    # ----- signal: risk categories -----
    risk_keywords = {"security", "auth", "encryption", "payment", "infra", "prod", "performance"}
    risk_hits = sum(kw in description_lower for kw in risk_keywords)
    risk_score = min(risk_hits * 0.06, 0.18)

    # ----- signal: ambiguity / uncertainty -----
    ambiguity_keywords = {"tbd", "maybe", "unknown", "not sure", "unclear"}
    ambiguity_hits = sum(kw in description_lower for kw in ambiguity_keywords)
    ambiguity_score = min(ambiguity_hits * 0.05, 0.10)

    # ----- signal: code blocks (usually implies deeper work) -----
    code_block_hits = description.count("```")
    code_block_score = min(code_block_hits / 2.0, 1.0) * 0.06

    # ----- signal: dependencies -----
    dep_count = len(metadata.get("depends_on", [])) if isinstance(metadata.get("depends_on"), list) else 0
    dependency_score = min(dep_count * 0.05, 0.15)

    raw_score = (
        word_score
        + verb_score
        + step_score
        + file_score
        + ref_score
        + risk_score
        + ambiguity_score
        + code_block_score
        + dependency_score
    )
    complexity_score = max(0.0, min(1.0, raw_score))

    if complexity_score < 0.30:
        band = "low"
        tier = "low"
        budget_multiplier = 0.9
    elif complexity_score < 0.60:
        band = "medium"
        tier = "medium"
        budget_multiplier = 1.1
    elif complexity_score < 0.80:
        band = "high"
        tier = "high"
        budget_multiplier = 1.4
    else:
        band = "critical"
        tier = "max"
        budget_multiplier = 1.7

    return {
        "complexity_score": round(complexity_score, 3),
        "complexity_band": band,
        "suggested_model_tier": tier,
        "suggested_budget_multiplier": budget_multiplier,
        "analysis": {
            "word_count": words,
            "word_count_signal": round(word_score, 3),
            "high_complexity_signals": round(min(high_hits * 0.06, 0.30), 3),
            "low_complexity_signals": round(min(low_hits * 0.04, 0.18), 3),
            "step_signals": round(step_score, 3),
            "file_reference_signals": round(file_score, 3),
            "paper_reference_signals": round(ref_score, 3),
            "risk_signals": round(risk_score, 3),
            "ambiguity_signals": round(ambiguity_score, 3),
            "code_block_signals": round(code_block_score, 3),
            "dependency_signals": round(dependency_score, 3),
            "file_names": files,
        },
    }


def compute_complexity(task_description: str, file_names: List[str]) -> float:
    """Backward-compatible helper returning just the score."""
    return analyze_task_complexity(task_description, file_names).get("complexity_score", 0.0)


__all__ = ["analyze_task_complexity", "compute_complexity", "extract_file_names"]