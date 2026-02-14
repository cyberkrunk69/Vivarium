"""
Scout LLM client — Groq API for navigation.

Pluggable for testing; uses GROQ_API_KEY from env or runtime config.
TICKET-40: Uses real cost estimation from pricing module.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from vivarium.scout.config import get_global_semaphore
from vivarium.scout.llm.pricing import estimate_cost_usd

logger = logging.getLogger(__name__)

# Fallback model when rate-limited on 70b
FALLBACK_8B_MODEL = "llama-3.1-8b-instant"

# Explicit models only—no groq/compound (agentic tasks, unpredictable pricing)
SUPPORTED_MODELS = {
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768",
}


@dataclass
class NavResponse:
    """Raw LLM response for navigation."""

    content: str
    cost_usd: float
    model: str
    input_tokens: int
    output_tokens: int


def _get_groq_api_key() -> Optional[str]:
    """Get Groq API key from env or runtime config."""
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    try:
        from vivarium.runtime import config as runtime_config

        return runtime_config.get_groq_api_key()
    except ImportError:
        return None


async def call_groq_async(
    prompt: str,
    model: str = "llama-3.1-8b-instant",
    system: Optional[str] = None,
    max_tokens: int = 500,
    temperature: Optional[float] = None,
    llm_client: Optional[Callable] = None,
) -> NavResponse:
    """
    Call Groq API for navigation. Uses llm_client if provided (for testing).
    """
    if llm_client:
        return await llm_client(prompt, model=model, system=system, max_tokens=max_tokens)

    if model not in SUPPORTED_MODELS:
        raise ValueError(
            f"Unsupported model: {model}. Use explicit models, not groq/compound."
        )

    api_key = _get_groq_api_key()
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY missing. Set it in .env or environment."
        )

    try:
        import httpx
    except ImportError:
        raise RuntimeError("httpx required for scout-nav. Install with: pip install httpx")

    url = os.environ.get("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature if temperature is not None else 0.1,
        "max_tokens": max_tokens,
    }

    async def _do_request(use_model: str):
        p = {**payload, "model": use_model}
        async with httpx.AsyncClient(timeout=30.0) as client:
            return await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=p,
            )

    resp = None
    last_error = None
    current_model = model

    for attempt in range(4):
        async with get_global_semaphore():
            resp = await _do_request(current_model)

        if resp.status_code != 429:
            if resp.status_code >= 400:
                try:
                    body = resp.json()
                    err_msg = body.get("error", {}).get("message", resp.text[:200])
                except Exception:
                    err_msg = resp.text[:200] if resp.text else str(resp.status_code)
                raise RuntimeError(f"Groq API {resp.status_code}: {err_msg}")
            resp.raise_for_status()
            break

        # 429: retry with backoff
        retry_after = resp.headers.get("Retry-After", "2")
        try:
            delay = int(retry_after)
        except ValueError:
            delay = 2

        if attempt == 0:
            logger.warning("Rate limited (429), retrying after %ds", delay)
            await asyncio.sleep(delay)
        elif "70b" in current_model.lower():
            current_model = FALLBACK_8B_MODEL
            logger.warning("Rate limited—switching to %s", current_model)
            await asyncio.sleep(delay)
        else:
            logger.warning("Rate limited on 8b, retrying after 5s")
            await asyncio.sleep(5)

        last_error = httpx.HTTPStatusError("429 Too Many Requests", request=resp.request, response=resp)

    if resp is None or resp.status_code != 200:
        if last_error:
            raise last_error
        raise RuntimeError("Request failed after retries")

    data = resp.json()

    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})
    content = msg.get("content", "").strip()

    usage = data.get("usage", {})
    # Groq Chat Completions uses prompt_tokens/completion_tokens (OpenAI format).
    # Responses API uses input_tokens/output_tokens. Support both.
    input_t = int(
        usage.get("prompt_tokens")
        or usage.get("input_tokens")
        or 0
    )
    output_t = int(
        usage.get("completion_tokens")
        or usage.get("output_tokens")
        or 0
    )

    cost = estimate_cost_usd(current_model, input_t, output_t)
    # If cost is 0 but we received content, the API was called (e.g. usage omitted).
    # Use a small epsilon so the audit log distinguishes "call made" from "no call".
    if cost == 0.0 and content:
        cost = 1e-7  # ~$0.0000001 — call was made, cost below precision or not reported

    return NavResponse(
        content=content,
        cost_usd=cost,
        model=current_model,
        input_tokens=input_t,
        output_tokens=output_t,
    )
