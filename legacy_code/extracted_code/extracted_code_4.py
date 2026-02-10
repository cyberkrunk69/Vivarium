"""
rlif_integration.py
-------------------
Convenient façade used by the main grind spawner to feed user responses
into the RLIF pipeline.
"""

from .rlif_detector import detect_sentiment, Sentiment
from .rlif_analyzer import analyze_issue
from .rlif_rules import add_rule


def _format_rule_from_negative(user_text: str, analysis: str) -> str:
    """
    Very simple heuristic to turn a negative interaction into a rule.
    In a real system this would be more sophisticated.
    """
    # Example heuristics:
    #   - If the user mentions "overwrite", suggest a version‑check rule.
    #   - If the user mentions "PowerShell" vs "Bash", suggest platform rule.
    lowered = user_text.lower()

    if "overwrite" in lowered:
        return "Before overwriting folders, compare versions first."
    if "powershell" in lowered and "bash" in lowered:
        return "Use PowerShell for Windows, not Unix commands in Bash tool."
    if "delete" in lowered:
        return "Never blindly delete without checking."

    # Generic fallback using the analyzer output.
    return f"NEVER do the following: {analysis}"


def process_user_interaction(user_response: str) -> None:
    """
    Entry point called by the main loop after each user reply.

    Parameters
    ----------
    user_response: str
        The raw text returned by the user.
    """
    sentiment = detect_sentiment(user_response)

    if sentiment != Sentiment.NEGATIVE:
        # Positive / neutral feedback does not generate a rule right now.
        return

    # Negative sentiment – run deeper analysis.
    cause = analyze_issue(user_response)

    # Extract a rule from the cause / original text.
    rule = _format_rule_from_negative(user_response, cause)

    # Persist the rule immediately.
    add_rule(rule)