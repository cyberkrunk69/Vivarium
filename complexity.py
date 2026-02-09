import re
from typing import List

# Simple token approximation – split on whitespace.
def _token_count(text: str) -> int:
    return len(text.split())

def _code_block_count(text: str) -> int:
    # Count occurrences of triple backticks or triple tildes
    return len(re.findall(r'(```|~~~)', text))

def _bullet_list_count(text: str) -> int:
    return len(re.findall(r'^\s*[-*]\s+', text, flags=re.MULTILINE))

def _keyword_weight(text: str) -> int:
    keywords = {
        "optimize": 5,
        "refactor": 5,
        "debug": 5,
        "explain": 3,
        "design": 4,
        "implement": 6,
    }
    score = 0
    lowered = text.lower()
    for kw, w in keywords.items():
        if kw in lowered:
            score += w
    return score

def estimate_complexity(prompt: str) -> int:
    """
    Return an integer 0‑100 representing estimated difficulty.
    The algorithm is deliberately simple and fast.
    """
    score = 0
    score += min(_token_count(prompt) // 10, 30)          # token count contribution
    score += min(_code_block_count(prompt) * 10, 20)     # code blocks
    score += min(_bullet_list_count(prompt) * 5, 15)     # sub‑tasks
    score += min(_keyword_weight(prompt), 20)            # keyword weight
    return min(score, 100)