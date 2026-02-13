"""
Scout Big Brain — Gemini API for natural language interpretation and high-quality synthesis.

Used for: query interpretation, PR descriptions, commit messages, module-level analysis.
Supports Google Gemini (gemini-2.5-pro, gemini-3-flash-preview). Requires GEMINI_API_KEY.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional

from vivarium.scout.audit import AuditLog

logger = logging.getLogger(__name__)

# Primary big brain model: reasoning, analysis, synthesis
BIG_BRAIN_MODEL = "gemini-2.5-pro"
# Fallback when rate-limited or unavailable
BIG_BRAIN_FALLBACK = "gemini-2.0-flash"


@dataclass
class BigBrainResponse:
    """Response from big brain API."""

    content: str
    cost_usd: float
    model: str
    input_tokens: int
    output_tokens: int


def _get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from env or runtime config."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        from vivarium.runtime import config as runtime_config

        return getattr(runtime_config, "get_gemini_api_key", lambda: None)()
    except ImportError:
        return None


def _estimate_gemini_cost(model_id: str, input_tokens: int, output_tokens: int) -> float:
    """Rough cost in USD for Gemini models (per 1M tokens)."""
    # Gemini 2.5 Pro: ~$1.25/1M input, ~$5/1M output (approximate)
    # Gemini 2.0 Flash: ~$0.10/1M input, ~$0.40/1M output
    pricing = {
        "gemini-2.5-pro": {"input": 1.25, "output": 5.0},
        "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
        "gemini-3-flash-preview": {"input": 0.15, "output": 0.60},
    }
    p = pricing.get(model_id, {"input": 1.0, "output": 2.0})
    return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000


async def call_big_brain_async(
    prompt: str,
    *,
    system: Optional[str] = None,
    max_tokens: int = 2048,
    model: Optional[str] = None,
    task_type: str = "general",
    big_brain_client: Optional[Callable] = None,
) -> BigBrainResponse:
    """
    Call Gemini API for big brain tasks (query interpretation, PR synthesis, commit, analysis).

    Uses GEMINI_API_KEY. Logs to audit as "big_brain_{task_type}".
    """
    if big_brain_client:
        return await big_brain_client(
            prompt, system=system, max_tokens=max_tokens, model=model, task_type=task_type
        )

    api_key = _get_gemini_api_key()
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY missing. Set it in .env or environment for big brain tasks."
        )

    model_used = model or BIG_BRAIN_MODEL

    def _do_request(use_model: str) -> tuple[str, int, int]:
        """Sync request (google-genai may not have native async)."""
        from google import genai

        client = genai.Client(api_key=api_key)
        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        response = client.models.generate_content(
            model=use_model,
            contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=0.2,
            ),
        )
        text = (response.text or "").strip()
        usage = getattr(response, "usage_metadata", None)
        input_t = output_t = 0
        if usage:
            input_t = int(getattr(usage, "prompt_token_count", None) or getattr(usage, "input_token_count", None) or 0)
            output_t = int(getattr(usage, "candidates_token_count", None) or getattr(usage, "output_token_count", None) or 0)
        if not input_t and not output_t and text:
            input_t = max(1, len(prompt.split()) * 2)
            output_t = max(1, len(text.split()) * 2)
        return text, input_t, output_t

    try:
        text, input_t, output_t = await asyncio.to_thread(_do_request, model_used)
    except Exception as e:
        if "2.5-pro" in model_used or "gemini-2.5" in model_used:
            logger.warning("Big brain %s failed, trying fallback: %s", model_used, e)
            model_used = BIG_BRAIN_FALLBACK
            try:
                text, input_t, output_t = await asyncio.to_thread(_do_request, BIG_BRAIN_FALLBACK)
            except Exception as e2:
                raise RuntimeError(f"Big brain failed: {e2}") from e2
        else:
            raise

    cost = _estimate_gemini_cost(model_used, input_t, output_t)
    if cost == 0.0 and text:
        cost = 1e-7

    audit = AuditLog()
    audit.log(
        f"big_brain_{task_type}",
        cost=cost,
        model=model_used,
        input_t=input_t,
        output_t=output_t,
    )

    return BigBrainResponse(
        content=text,
        cost_usd=cost,
        model=model_used,
        input_tokens=input_t,
        output_tokens=output_t,
    )


def _heuristic_query_spec(natural_language: str) -> dict[str, Any]:
    """Fallback when big brain unavailable. Returns scope, include_deep, copy_to_clipboard."""
    q = natural_language.lower()
    return {
        "scope": "vivarium/scout" if "scout" in q else "vivarium",
        "include_deep": any(
            w in q for w in ("deep", "detailed", "full", "everything", "complete", "in-depth")
        ),
        "copy_to_clipboard": "no clipboard" not in q and "don't copy" not in q and "dont copy" not in q,
    }


async def interpret_query_async(natural_language: str) -> dict[str, Any]:
    """
    Use big brain to interpret natural language into a scout query spec.

    Returns dict with: scope, include_deep, copy_to_clipboard.
    Falls back to heuristics when GEMINI_API_KEY is missing.
    """
    if not _get_gemini_api_key():
        return _heuristic_query_spec(natural_language)

    prompt = f"""Interpret this natural language request into a structured scout query.

User request: "{natural_language}"

Respond with ONLY valid JSON, no markdown or explanation:
{{
  "scope": "vivarium/scout",
  "include_deep": true,
  "copy_to_clipboard": true
}}

Rules:
- scope: package path (e.g. vivarium/scout, vivarium, vivarium/runtime/auth). Default vivarium/scout for scout-related queries.
- include_deep: true if user wants "deep", "detailed", "full", "everything", "complete", "in-depth" content. Otherwise false.
- copy_to_clipboard: true unless user explicitly says not to copy or "just save" or similar."""

    response = await call_big_brain_async(
        prompt,
        system="You output only valid JSON. No markdown, no explanation.",
        max_tokens=256,
        task_type="query_interpret",
    )
    raw = response.content.strip()
    # Strip markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Big brain returned invalid JSON: %s", raw[:200])
        return _heuristic_query_spec(natural_language)
