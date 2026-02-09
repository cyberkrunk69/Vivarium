import re

def estimate_complexity(request: str) -> str:
    """
    Very simple heuristic to estimate request complexity.
    Returns one of: "low", "medium", "high".
    """
    # Count words
    word_count = len(request.split())
    # Count fenced code blocks (``` … ```)
    code_blocks = len(re.findall(r"```", request)) // 2

    # Heuristic rules
    if code_blocks >= 2 or word_count > 200:
        return "high"
    if code_blocks == 1 or word_count > 80:
        return "medium"
    return "low"


def select_model_for_complexity(complexity: str, model_pool: dict) -> str:
    """
    Select a model identifier from the provided pool based on complexity.
    ``model_pool`` should map complexity levels ('low', 'medium', 'high')
    to model identifiers. Falls back to the lowest tier if a specific tier
    is missing.
    """
    return model_pool.get(complexity) or model_pool.get("low")