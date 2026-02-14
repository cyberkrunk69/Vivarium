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
import sys
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Optional

from vivarium.scout.audit import AuditLog
from vivarium.scout.middle_manager import GateDecision, MiddleManagerGate

logger = logging.getLogger(__name__)

# Primary big brain model: reasoning, analysis, synthesis
BIG_BRAIN_MODEL = "gemini-2.5-pro"
# Fallback when rate-limited or unavailable
BIG_BRAIN_FALLBACK = "gemini-2.0-flash"

# TICKET-19: Gate-approved briefs → Flash (cheap); escalate → Pro (expensive)
GEMINI_MODEL_FLASH = "gemini-2.5-flash"  # $0.30/M input, $2.50/M output (API uses no -002 suffix)
GEMINI_MODEL_PRO = "gemini-2.5-pro"       # $1.25/M input, $10.00/M output


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
    """TICKET-40: Use real pricing from llm.pricing."""
    from vivarium.scout.llm.pricing import estimate_cost_usd

    return estimate_cost_usd(model_id, input_tokens, output_tokens)


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


async def call_big_brain_gated_async(
    question: str,
    facts: Optional[Any] = None,
    *,
    raw_tldr_context: Optional[str] = None,
    deps_graph: Optional[Any] = None,
    query_symbols: Optional[list] = None,
    task_type: str = "synthesis",
    model: Optional[str] = None,
    model_escalate: Optional[str] = None,
    big_brain_client: Optional[Callable] = None,
    gate: Optional[MiddleManagerGate] = None,
    on_decision: Optional[Callable[["GateDecision"], None]] = None,
    on_decision_async: Optional[Callable[["GateDecision"], Awaitable[None]]] = None,
) -> BigBrainResponse:
    """
    Gated path: compress context via 70B, then call Gemini.

    TICKET-43: Prefer facts (ModuleFacts) — structured truth. raw_tldr_context for synthesis path.
    TICKET-19: Route gate-approved briefs to Flash (cheap); escalate to Pro (expensive).
    """
    gate = gate or MiddleManagerGate(confidence_threshold=0.75)
    decision = await gate.validate_and_compress(
        question=question,
        facts=facts,
        raw_tldr_context=raw_tldr_context,
        deps_graph=deps_graph,
        query_symbols=query_symbols,
    )

    if on_decision:
        on_decision(decision)
    if on_decision_async:
        await on_decision_async(decision)

    # decision.content is compressed (pass) or raw (escalate)
    context_for_prompt = decision.content
    audit = getattr(gate, "_audit", None) or AuditLog()

    # TICKET-48d: Preserve gate-declared gaps in synthesis prompt
    gap_context = ""
    if decision.gaps:
        gap_context = "\n\n[GAP MARKERS FROM GATE]\n" + "\n".join(
            f"- {g}" for g in decision.gaps
        )

    prompt = f"""Context:
{context_for_prompt}
{gap_context}

---
Question: {question}

Answer based on the context above. If gaps exist above, acknowledge uncertainty where relevant."""

    # TICKET-19: ROUTING: Flash for pass, Pro for escalate
    if decision.decision == "pass":
        model_used = model or GEMINI_MODEL_FLASH
        audit.log(
            "gate_synthesis",
            model="flash",
            confidence=int((decision.confidence or 0) * 100),
        )
    else:
        model_used = model_escalate or GEMINI_MODEL_PRO
        audit.log(
            "gate_synthesis",
            model="pro",
            reason="escalate",
        )

    return await call_big_brain_async(
        prompt,
        system="You answer concisely based on the provided context.",
        max_tokens=1024,
        model=model_used,
        task_type=task_type,
        big_brain_client=big_brain_client,
    )


async def interpret_query_async(natural_language: str) -> dict[str, Any]:
    """
    Use big brain to interpret natural language into a scout query spec.

    Returns dict with: scope, include_deep, copy_to_clipboard.
    Requires GEMINI_API_KEY. Raises when big brain unavailable.
    """
    if not _get_gemini_api_key():
        raise EnvironmentError(
            "GEMINI_API_KEY required for natural language interpretation. Set it in .env"
        )
    return await _interpret_query_via_big_brain(natural_language)


async def _interpret_query_via_big_brain(natural_language: str) -> dict[str, Any]:
    """Call big brain to interpret query. Raises on failure."""
    prompt = f"""Interpret this natural language request into a structured scout query.

User request: "{natural_language}"

Respond with ONLY valid JSON, no markdown or explanation:
{{
  "scope": "vivarium/scout",
  "include_deep": true,
  "copy_to_clipboard": true
}}

- scope: package path to search (e.g. vivarium/scout, vivarium, vivarium/runtime/auth)
- include_deep: whether to include detailed/deep content vs tldr only
- copy_to_clipboard: whether to copy results to clipboard"""

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
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Big brain returned invalid JSON: {raw[:200]!r}") from e


def _extract_json_from_content(raw: str) -> dict[str, Any] | None:
    """Extract first valid JSON object from content. Returns None if none found."""
    raw = raw.strip()
    if not raw:
        return None
    # Strip markdown code blocks
    if raw.startswith("```"):
        parts = raw.split("```", 2)
        if len(parts) >= 2:
            raw = parts[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
    # Find first { and matching }
    start = raw.find("{")
    if start < 0:
        return None
    depth = 0
    for i, c in enumerate(raw[start:], start):
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(raw[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _flatten_spec(obj: dict) -> dict:
    """Flatten nested params into top-level spec for runners."""
    spec = dict(obj)
    params = spec.pop("params", None)
    if isinstance(params, dict):
        for k, v in params.items():
            spec.setdefault(k, v)
    return spec


def parse_chat_response(raw: str) -> tuple[str, Any]:
    """
    Parse big brain response. Returns ("tool", spec) or ("message", text).
    Flexible: extracts JSON from content; if no valid tool, treats as message.
    Never returns raw JSON/partial output to user.
    """
    import re

    from vivarium.scout.tools import get_valid_tool_names

    valid_tools = get_valid_tool_names()
    obj = _extract_json_from_content(raw)
    if obj is not None and isinstance(obj, dict):
        tool = obj.get("tool")
        if tool in valid_tools:
            return ("tool", _flatten_spec(obj))
        msg = obj.get("message")
        if msg is not None and isinstance(msg, str):
            return ("message", msg)
    # Salvage truncated/malformed JSON: extract tool name and scope if present
    text = raw.strip()
    if text and "tool" in text.lower():
        tm = re.search(r'"tool"\s*:\s*"(\w+)"', text, re.I)
        if tm and tm.group(1) in valid_tools:
            spec = {"tool": tm.group(1)}
            sm = re.search(r'"scope"\s*:\s*"([^"]+)"', text)
            if sm:
                spec["scope"] = sm.group(1)
            im = re.search(r'"include_deep"\s*:\s*(true|false)', text, re.I)
            if im:
                spec["include_deep"] = im.group(1).lower() == "true"
            return ("tool", spec)
    if text and ("{" in text or "```json" in text.lower()) and ("tool" in text or "params" in text):
        return ("message", None)
    return ("message", text if text else None)


def _has_tool_output(messages: list[dict]) -> bool:
    """True if conversation includes tool output (synthesis needed)."""
    for m in messages:
        if "[Tool " in str(m.get("content", "")):
            return True
    return False


def _extract_last_tool_output(messages: list[dict]) -> str:
    """TICKET-38: Extract content of most recent tool result. Bounded synthesis context."""
    import re

    for m in reversed(messages):
        content = m.get("content", "")
        if "[Tool " in content and "result]" in content:
            match = re.search(r"\[Tool \w+ result\]:\s*\n(.*)", content, re.DOTALL)
            if match and match.group(1).strip():
                return match.group(1).strip()
    return ""


def _extract_last_user_message(messages: list[dict]) -> str:
    """Last user message content."""
    for m in reversed(messages):
        if m.get("role") == "user":
            return (m.get("content") or "").strip()
    return ""


def _truncate_string_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate string to fit token cap (~4 chars/token)."""
    if not text:
        return ""
    if len(text) // 4 <= max_tokens:
        return text
    return text[: max_tokens * 4]


async def chat_turn_async(
    messages: list[dict[str, str]],
    cwd_scope: str = "vivarium",
    repo_state: dict[str, Any] | None = None,
    caveman: bool = False,
    progress_cb: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Chat turn. Uses Groq for easy work (tool selection, routing). Uses big brain
    (Gemini) only for cognitive tasks (synthesizing answer from tool output).
    """
    from vivarium.scout.llm import call_groq_async
    from vivarium.scout.tools import get_tools_minimal

    tools_minimal = get_tools_minimal()
    tools_lines = [f"- {t['name']}: {t['desc']}" for t in tools_minimal]
    tools_block = "\n".join(tools_lines)
    state = repo_state or {}
    state.setdefault("cwd_scope", cwd_scope)
    state_json = json.dumps(state, indent=2)

    conv_lines = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        label = "User" if role == "user" else "Scout"
        conv_lines.append(f"{label}: {content}")
    conv_block = "\n\n".join(conv_lines) if conv_lines else "(no prior messages)"

    # Routing: Groq has strict context limits. Chat history can be 1MB+ (full tldr outputs).
    # For routing, use only the last user message so we stay under limits.
    needs_synthesis = _has_tool_output(messages)
    if not needs_synthesis:
        last_user = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
        conv_block = f"User: {last_user}" if last_user else "(no message)"

    caveman_rule = " Use eliv. Small words. " if caveman else ""
    prompt = f"""You are Scout. You help with code, docs, and dev workflow.

Context: {state_json}

Tools (pick one):
{tools_block}

Conversation:
{conv_block}

Rules: Always pick a tool when the user asks for info, docs, tldr, or how something works. Use query for those. Never reply with a greeting when the user asked a question. Use message only for greetings (hi, hello) or when no tool fits.

Respond with: {{"tool": "name", "scope": "...", "include_deep": true/false, ...}} (flat params).
Or {{"message": "..."}} only for greetings."""

    system = "You are Scout. Use tools to gather info. Always use tldr/deep docs first; only look at raw code when docs insufficient." + caveman_rule

    # Synthesis: TICKET-38 — Gate the synthesis path. Bounded 4K context, same safety as query.
    if needs_synthesis:
        if progress_cb:
            progress_cb("Gating synthesis...")
        try:
            last_tool = _extract_last_tool_output(messages)
            last_user = _extract_last_user_message(messages)
            synthesis_context = (
                f"User: {last_user}\n\nTool output:\n{last_tool}"
                if last_user or last_tool
                else last_tool or "(no context)"
            )
            synthesis_context = _truncate_string_to_tokens(synthesis_context, 4000)

            synthesis_query = (
                "Summarize the tool output above for the user. Be concise. "
                "Acknowledge [GAP] markers when present."
            )

            on_decision_async = None
            try:
                from vivarium.scout.config import ScoutConfig
                from vivarium.scout.ui.whimsy import (
                    decision_to_whimsy_params,
                    generate_gate_whimsy,
                )

                if ScoutConfig().whimsy_mode:

                    async def _print_synthesis_whimsy(d: GateDecision) -> None:
                        cost = getattr(d, "cost_usd", 0) or (
                            0.05 if d.decision == "pass" else 0.50
                        )
                        params = decision_to_whimsy_params(d, cost)
                        line = await generate_gate_whimsy(**params)
                        print(line, file=sys.stderr)

                    on_decision_async = _print_synthesis_whimsy
            except ImportError:
                pass

            response = await call_big_brain_gated_async(
                question=synthesis_query,
                raw_tldr_context=synthesis_context,
                task_type="synthesis",
                on_decision_async=on_decision_async,
            )
            return response.content.strip()
        except Exception as e:
            logger.debug("Synthesis failed: %s", e)
            msg = str(e).split("\n")[0] if str(e) else "unknown"
            raise RuntimeError(f"Groq synthesis failed: {msg}") from e

    # Routing (no tool output yet): Groq only
    if progress_cb:
        progress_cb("Calling Groq to pick tool...")
    try:
        groq_resp = await call_groq_async(
            prompt,
            model="llama-3.1-8b-instant",
            system=system,
            max_tokens=512,
        )
        audit = AuditLog()
        audit.log(
            "chat_groq",
            cost=groq_resp.cost_usd,
            model=groq_resp.model,
            input_t=groq_resp.input_tokens,
            output_t=groq_resp.output_tokens,
        )
        return groq_resp.content.strip()
    except Exception as e:
        logger.debug("Groq routing failed: %s", e)
        msg = str(e).split("\n")[0] if str(e) else "unknown"
        raise RuntimeError(f"Groq routing failed: {msg}") from e


async def interpret_command_async(
    natural_language: str,
    cwd_scope: str = "vivarium",
) -> dict[str, Any]:
    """
    Interpret natural language into a scout tool call. Big brain picks the cheapest/fastest
    tool that satisfies the user (index=free, query=read-only, sync=expensive, nav=index-or-LLM).
    Requires GEMINI_API_KEY. Raises when big brain unavailable.
    """
    if not _get_gemini_api_key():
        raise EnvironmentError(
            "GEMINI_API_KEY required for natural language interpretation. Set it in .env"
        )
    return await _interpret_command_via_big_brain(natural_language, cwd_scope)


async def _interpret_command_via_big_brain(
    natural_language: str,
    cwd_scope: str,
) -> dict[str, Any]:
    """Call big brain to pick the right tool. Tools passed as data—no hardcoded strings."""
    from vivarium.scout.tools import get_tools, get_valid_tool_names

    tools_json = json.dumps(get_tools(), indent=2)
    valid_names = sorted(get_valid_tool_names())
    prompt = f"""Pick the best scout tool for this request. Use the cheapest/fastest tool that satisfies the user.

User request: "{natural_language}"
Context: current scope "{cwd_scope}"

Available tools (JSON):
{tools_json}

Respond with ONLY valid JSON. You MUST set "tool" to exactly one of: {valid_names}.
Include all params the tool needs: scope, include_deep, copy_to_clipboard, changed_only, task, query.
Use null for params that don't apply to the chosen tool. Prefer cheaper/faster tools."""

    response = await call_big_brain_async(
        prompt,
        system="You output only valid JSON. Pick the tool that saves the user money and time.",
        max_tokens=256,
        task_type="command_interpret",
    )
    raw = response.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    try:
        spec = json.loads(raw)
        valid = get_valid_tool_names()
        tool = spec.get("tool")
        if tool is None or tool not in valid:
            raise RuntimeError(
                f"Big brain must return valid tool. Got {tool!r}. Valid: {sorted(valid)}"
            )
        spec.setdefault("scope", cwd_scope)
        spec.setdefault("include_deep", False)
        spec.setdefault("copy_to_clipboard", True)
        spec.setdefault("changed_only", False)
        return spec
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Big brain returned invalid JSON: {raw[:200]!r}") from e


async def answer_help_async(
    repo_state: dict[str, Any],
    *,
    use_gate: bool = True,
    query: str = "",
) -> str:
    """
    User asked "what can you do". Big brain lists capabilities from tools data,
    suggests one based on repo state, you be the judge.

    When use_gate=True (default), context is compressed via MiddleManagerGate
    before Gemini. Escalation uses raw TLDRs with Pro model.
    """
    from vivarium.scout.tools import get_tools

    tools_json = json.dumps(get_tools(), indent=2)
    state_json = json.dumps(repo_state, indent=2)
    caveman = repo_state.get("caveman_mode", False)
    caveman_rule = " CAVEMAN MODE: use eliv only. Small words. No big word. Cave man understand. " if caveman else " Use eliv when you talk to user. "
    caveman_examples = """
Examples of caveman style (talk like this):
- User: "you no hardcode string! bad robot. you use big brain for that."
- User: "make so even cave man can use and understand. small word, easy meaning."
- User: "they need desc for big brain to know what tool do no?"
- Scout reply: "me do: find code, read doc, make doc, find where change, plan, see status. you have 3 file stage. me say try sync. you be judge."
""" if caveman else ""

    raw_context = f"""Available tools (JSON, each has desc and eliv):
{tools_json}

Repo state:
{state_json}
{caveman_rule}
{caveman_examples}"""

    question = "What can Scout do? List capabilities and suggest one from repo state. Plain text."

    if use_gate:
        # TICKET-27/29: 8B gate whimsy when SCOUT_WHIMSY=1; else legacy phrase banks
        on_decision = None
        on_decision_async = None
        try:
            from vivarium.scout.config import ScoutConfig
            from vivarium.scout.ui.whimsy import (
                WhimsyFormatter,
                generate_gate_whimsy,
                decision_to_whimsy_params,
            )

            if ScoutConfig().whimsy_mode:
                # TICKET-27: Fresh 8B whimsy per gate decision
                async def _print_whimsy_8b(d: GateDecision) -> None:
                    cost = getattr(d, "cost_usd", 0) or (
                        0.05 if d.decision == "pass" else 0.50
                    )
                    params = decision_to_whimsy_params(d, cost)
                    line = await generate_gate_whimsy(**params)
                    print(line, file=sys.stderr)

                on_decision_async = _print_whimsy_8b
            else:
                def _print_whimsy_legacy(d: GateDecision) -> None:
                    print(
                        WhimsyFormatter.format_gate_decision(d, query=query),
                        file=sys.stderr,
                    )

                on_decision = _print_whimsy_legacy
        except ImportError:
            pass

        response = await call_big_brain_gated_async(
            question=question,
            raw_tldr_context=raw_context,
            task_type="help",
            model_escalate=BIG_BRAIN_MODEL,
            on_decision=on_decision,
            on_decision_async=on_decision_async,
        )
    else:
        prompt = f"""The user asked what scout can do.

{raw_context}
List what you do. Suggest one from repo state. You be the judge. Plain text."""
        system = "You are scout. Caveman mode: small words only." if caveman else "You are scout. Use eliv. Suggest from repo state. Empower user."
        response = await call_big_brain_async(
            prompt,
            system=system,
            max_tokens=512,
            task_type="help",
        )
    return response.content.strip()
