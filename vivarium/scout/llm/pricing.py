"""
TICKET-40: Real Cost Estimation Engine — Hardcoded 2026 MVP rates.

Source: pricepertoken.com, aipricing.org, llm-stats.com, groq.com (Feb 2026).
"""

from __future__ import annotations

# Per-million-token costs (USD), February 2026
# Google API uses gemini-2.5-pro / gemini-2.5-flash (no -002 suffix)
PRICING = {
    # Galaxy Brain (Gemini 2.5 Pro) — deep reasoning
    "gemini-2.5-pro": {
        "input_per_million": 1.25,
        "output_per_million": 10.00,
        "nickname": "galaxy_brain",
    },
    # Bright Spark (Gemini 2.5 Flash) — fast synthesis
    "gemini-2.5-flash": {
        "input_per_million": 0.30,
        "output_per_million": 2.50,
        "nickname": "bright_spark",
    },
    # Middle Manager (Groq 70B) — compression + confidence
    "llama-3.3-70b-versatile": {
        "input_per_million": 0.59,
        "output_per_million": 0.79,
        "nickname": "middle_manager",
    },
    # Router/Formatter (Groq 8B) — intent parsing + formatting
    "llama-3.1-8b-instant": {
        "input_per_million": 0.05,
        "output_per_million": 0.08,
        "nickname": "router",
    },
    # Aliases (API may return -002 suffix)
    "gemini-2.5-pro-002": {"input_per_million": 1.25, "output_per_million": 10.0, "nickname": "galaxy_brain"},
    "gemini-2.5-flash-002": {"input_per_million": 0.30, "output_per_million": 2.50, "nickname": "bright_spark"},
    "gemini-2.0-flash": {"input_per_million": 0.10, "output_per_million": 0.40, "nickname": "bright_spark"},
    "gemini-3-flash-preview": {"input_per_million": 0.15, "output_per_million": 0.60, "nickname": "bright_spark"},
}


def estimate_cost_usd(
    model_id: str, input_tokens: int, output_tokens: int
) -> float:
    """Estimate actual USD cost from token counts + hardcoded 2026 pricing."""
    pricing = PRICING.get(
        model_id, PRICING["llama-3.1-8b-instant"]
    )  # Fallback to 8B
    return (
        (input_tokens / 1_000_000) * pricing["input_per_million"]
        + (output_tokens / 1_000_000) * pricing["output_per_million"]
    )
