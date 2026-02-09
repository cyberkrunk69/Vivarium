import re
from typing import List

def compute_complexity(task_description: str, file_names: List[str]) -> float:
    """
    Compute a normalized complexity score (0.0 – 1.0) for a given task.
    Signals used:
      • Word count of the description
      • Presence of high‑complexity verbs (create, implement, design)
      • Presence of low‑complexity verbs (fix, update, add)
      • Number of files mentioned / involved
      • References to papers or known architectures (arXiv IDs, DOI, “ResNet”, “Transformer”, etc.)
    The raw score is scaled to 0‑1.
    """
    # ----- basic signals -----
    words = len(re.findall(r"\w+", task_description))
    word_score = min(words / 200.0, 1.0)                     # >200 words → max weight

    high_complexity_keywords = {"create", "implement", "design"}
    low_complexity_keywords  = {"fix", "update", "add"}

    description_lower = task_description.lower()
    high_hits = sum(kw in description_lower for kw in high_complexity_keywords)
    low_hits  = sum(kw in description_lower for kw in low_complexity_keywords)

    verb_score = (high_hits * 0.2 - low_hits * 0.1)         # can be negative; clamp later

    # ----- file‑related signal -----
    file_score = min(len(file_names) / 10.0, 1.0)           # >10 files → max weight

    # ----- paper / architecture references -----
    paper_patterns = [
        r"arxiv\.org/abs/\d{4}\.\d{4,5}",
        r"doi:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+",
        r"\b(resnet|transformer|gpt|bert|vgg|cnn|rnn)\b"
    ]
    ref_hits = sum(bool(re.search(pat, task_description, re.I)) for pat in paper_patterns)
    ref_score = min(ref_hits * 0.15, 0.3)                    # each hit adds a bit, max 0.3

    # ----- combine & normalize -----
    raw_score = 0.4 * word_score + 0.3 * file_score + 0.2 * ref_score + verb_score
    # clamp to [0,1]
    complexity_score = max(0.0, min(1.0, raw_score))

    return complexity_score