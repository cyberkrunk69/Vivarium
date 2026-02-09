class ComplexityEstimator:
    """
    Simple heuristic‑based estimator for request complexity.
    Returns one of: 'low', 'medium', 'high'.
    """
    def __init__(self, thresholds: dict | None = None):
        # Default thresholds – can be tuned per deployment
        self.thresholds = thresholds or {
            "token_count": 200,   # tokens per request
            "code_blocks": 2,     # number of ``` sections
            "nested_steps": 3,    # bullet/numbered steps as a proxy for nesting
        }

    def estimate(self, request: str) -> str:
        # Basic heuristics:
        token_count = len(request.split())
        code_blocks = request.count("```")
        # Approximate step count (nested bullet or numbered lists)
        steps = request.count("\n- ") + request.count("\n1. ")

        # High complexity if any metric far exceeds its threshold
        if token_count > self.thresholds["token_count"] * 2 or code_blocks > self.thresholds["code_blocks"] * 2:
            return "high"
        # Medium complexity if any metric modestly exceeds its threshold
        if token_count > self.thresholds["token_count"] or code_blocks > self.thresholds["code_blocks"] or steps > self.thresholds["nested_steps"]:
            return "medium"
        # Otherwise consider it low complexity
        return "low"
import re
from enum import Enum, auto

class ComplexityLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class ComplexityEstimator:
    """
    Very lightweight heuristic estimator.
    - Token count (approx words) → size
    - Presence of programming keywords → higher difficulty
    - Number of question marks / bullet points → more sub‑tasks
    """

    PROGRAMMING_KEYWORDS = {
        "def ", "class ", "import ", "for ", "while ", "if ", "else:", "elif ",
        "try:", "except ", "return ", "print(", "await ", "async ", "lambda ",
    }

    @staticmethod
    def estimate(request_text: str) -> ComplexityLevel:
        # Normalise
        txt = request_text.strip().lower()

        # Rough token count (words)
        token_count = len(re.findall(r"\w+", txt))

        # Count programming keywords
        prog_hits = sum(kw in txt for kw in ComplexityEstimator.PROGRAMMING_KEYWORDS)

        # Count bullet‑style sub‑tasks (lines starting with '-', '*', or numbers)
        subtask_hits = len(re.findall(r"^\s*[-*]\s+", txt, flags=re.MULTILINE)) + \
                       len(re.findall(r"^\s*\d+\.\s+", txt, flags=re.MULTILINE))

        # Heuristic scoring
        score = 0
        if token_count > 300:
            score += 2
        elif token_count > 150:
            score += 1

        score += prog_hits * 2
        score += subtask_hits

        # Map score to level
        if score >= 6:
            return ComplexityLevel.HIGH
        elif score >= 3:
            return ComplexityLevel.MEDIUM
        else:
            return ComplexityLevel.LOW