"""
Scout Constrained Doc Synthesizer — LLM generates prose ONLY on verified AST facts.

Never invents facts. Validates output against facts. Embeds FACT_CHECKSUM for runtime validation.
"""

from __future__ import annotations

import asyncio
import logging
import re
from pathlib import Path
from typing import Optional, Tuple

from vivarium.scout.doc_sync.ast_facts import ModuleFacts

logger = logging.getLogger(__name__)


# TICKET-50: Gate constants that must NOT appear in docs unless defined in this module
_CROSS_MODULE_HALLUCINATION_BLOCKLIST = frozenset({
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "MAX_EXPANDED_CONTEXT",
    "GROQ_70B_MODEL",
    "MAX_RETRY_ATTEMPTS",
})


def _validate_output_against_facts(prose: str, facts: ModuleFacts) -> bool:
    """Reject blatant contradictions and cross-module constant hallucinations. TICKET-46, TICKET-50."""
    # TICKET-46: Reject "not used" when used
    for name, fact in facts.symbols.items():
        if fact.used_at and re.search(
            rf"\b{re.escape(name)}\b.*\b(not used|unused|never used)",
            prose,
            re.IGNORECASE,
        ):
            return False

    # TICKET-50: Reject cross-module constant hallucination — gate constants only if defined here
    defined_names = set(facts.symbols.keys())
    for blocklisted in _CROSS_MODULE_HALLUCINATION_BLOCKLIST:
        if blocklisted in defined_names:
            continue
        if re.search(rf"\b{re.escape(blocklisted)}\b", prose):
            logger.error(
                "Cross-module hallucination: '%s' mentioned but not defined in %s",
                blocklisted,
                facts.path.name if facts.path else "?",
            )
            return False
    return True


class ConstrainedDocSynthesizer:
    """LLM generates prose ONLY on verified AST facts — never invents facts."""

    SYSTEM_PROMPT = """You are a documentation engineer. Generate accurate .tldr.md prose using ONLY the facts below.

CRITICAL RULE (TICKET-50):
- ONLY describe symbols DEFINED in this module (not imported/used symbols).
- If this module USES a constant but does not DEFINE it, DO NOT describe it.
- Example: If this module USES DEFAULT_CONFIDENCE_THRESHOLD but does not DEFINE it, DO NOT describe it.
- When in doubt: OMIT the symbol — never hallucinate ownership.

RULES:
1. NEVER invent facts not in the FACTS section.
2. NEVER say "not used" unless usage list is "(none)" in FACTS.
3. For constants, ALWAYS list line numbers where used (from FACTS) — e.g. "used at lines 109, 335, 363".
4. Include ALL module-level constants that appear in FACTS (only symbols defined in this module).
5. For classes, list their constants and methods. For methods, list parameters and return type (from FACTS).
6. If uncertain about any detail, omit it — never hallucinate.

OUTPUT FORMAT:
## Module Constants
- `logger`: (used at lines X, Y, Z)
- `MAX_EXPANDED_CONTEXT`: value (used at lines X, Y)

# ClassName
Brief description.

## Constants
- `name`: (used at lines X, Y, Z)

## Methods
- `method(param: type) -> return_type`: description

FACTS (100% ACCURATE — DO NOT CONTRADICT):
{facts_markdown}

OUTPUT (prose only — no JSON, no disclaimers):"""

    def _facts_to_markdown(self, facts: ModuleFacts) -> str:
        """Convert ModuleFacts to markdown for the prompt. Docstrings are truth — always include."""
        return self._facts_to_markdown_impl(facts, include_enrichment=True)

    def _facts_to_markdown_rich(self, facts: ModuleFacts) -> str:
        """TICKET-44: Include docstrings, signatures, purpose hints for rich synthesis."""
        return self._facts_to_markdown_impl(facts, include_enrichment=True)

    def _facts_to_markdown_impl(
        self, facts: ModuleFacts, include_enrichment: bool = False
    ) -> str:
        """Convert ModuleFacts to markdown. Optionally include docstring/signature/purpose."""
        lines = []
        for name, fact in sorted(facts.symbols.items()):
            lines.append(f"- `{name}` ({fact.type})")
            if fact.value is not None:
                lines.append(f"  Value: {fact.value}")
            if fact.type_annotation:
                lines.append(f"  Type: {fact.type_annotation}")
            if include_enrichment and fact.docstring:
                ds = fact.docstring[:200] + "..." if len(fact.docstring) > 200 else fact.docstring
                lines.append(f"  Docstring: {ds}")
            if include_enrichment and fact.signature:
                lines.append(f"  Signature: {fact.signature}")
            if include_enrichment and fact.purpose_hint:
                lines.append(f"  Purpose hint: {fact.purpose_hint}")
            sr = getattr(fact, "semantic_role", None)
            if include_enrichment and sr:
                lines.append(f"  Semantic role: {sr} (NEVER conflate with other roles)")
            if fact.used_at:
                lines.append(f"  Used at lines: {', '.join(map(str, fact.used_at))}")
            else:
                lines.append("  Used at lines: (none)")
            if fact.methods:
                lines.append(f"  Methods: {', '.join(fact.methods)}")
            if fact.fields:
                lines.append(f"  Fields: {', '.join(fact.fields)}")
        return "\n".join(lines)

    async def synthesize_tldr_async(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Synthesize TL;DR prose from facts. Returns (prose, cost_usd)."""
        facts_md = self._facts_to_markdown(facts)  # include_enrichment=True — docstrings are truth
        prompt = self.SYSTEM_PROMPT.format(facts_markdown=facts_md)

        from vivarium.scout.llm import call_groq_async

        resp = await call_groq_async(
            prompt,
            model="llama-3.1-8b-instant",
            system="You output documentation. Use ONLY the provided facts. Never invent.",
            max_tokens=1000,
        )
        prose = resp.content.strip()

        if not _validate_output_against_facts(prose, facts):
            prose = self._fallback_from_facts(facts)

        checksum = facts.checksum()
        return f"<!-- FACT_CHECKSUM: {checksum} -->\n\n{prose}", resp.cost_usd

    def synthesize_tldr(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Synchronous wrapper for synthesize_tldr_async."""
        return asyncio.run(self.synthesize_tldr_async(facts))

    async def synthesize_deep_async(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Synthesize deep doc from facts. Returns (prose, cost_usd)."""
        facts_md = self._facts_to_markdown(facts)  # include_enrichment=True — docstrings are truth
        prompt = f"""Generate detailed documentation using ONLY these facts. Never invent.

CRITICAL RULE (TICKET-50): ONLY describe symbols in FACTS below. Do NOT add constants from other modules.

FACTS:
{facts_md}

Output structured markdown with ## headings for Constants, Methods, Control Flow.
For each constant, list exact line numbers where used. Never say "not used" if lines are listed."""

        from vivarium.scout.llm import call_groq_async

        resp = await call_groq_async(
            prompt,
            model="llama-3.1-8b-instant",
            system="You output documentation. Use ONLY the provided facts.",
            max_tokens=1500,
        )
        prose = resp.content.strip()
        if not _validate_output_against_facts(prose, facts):
            prose = self._fallback_from_facts(facts)
        checksum = facts.checksum()
        return f"<!-- FACT_CHECKSUM: {checksum} -->\n\n{prose}", resp.cost_usd

    def synthesize_deep(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Synchronous wrapper for synthesize_deep_async."""
        return asyncio.run(self.synthesize_deep_async(facts))

    def _fallback_from_facts(self, facts: ModuleFacts) -> str:
        """Generate deterministic fallback when LLM output fails validation."""
        lines = ["# Module Summary\n"]
        for name, fact in sorted(facts.symbols.items()):
            if fact.type == "constant":
                usage = f" (used at lines {', '.join(map(str, fact.used_at))})" if fact.used_at else ""
                lines.append(f"- `{name}`: {fact.type}{usage}")
                if fact.value:
                    lines.append(f"  Value: {fact.value}")
            elif fact.type == "class":
                lines.append(f"- `{name}`: class with methods {', '.join(fact.methods)}")
        return "\n".join(lines)


class RichDocSynthesizer(ConstrainedDocSynthesizer):
    """TICKET-44: Two-phase synthesis — strict grounding then fluent rewrite.
    Phase 1: Minimal fact-grounded output. Phase 2: Fluent prose (no fact changes).
    """

    PHASE_1_PROMPT = """Generate minimal .tldr.md from facts below.

CRITICAL RULE (TICKET-50):
- ONLY describe symbols DEFINED in this module (not imported/used symbols).
- If a constant is NOT in the FACTS below, DO NOT describe it — even if you've seen it elsewhere.
- Example: If FACTS omit DEFAULT_CONFIDENCE_THRESHOLD, this module does not define it — OMIT it.
- When in doubt: OMIT the symbol — never hallucinate ownership.

PRIORITY RULES (for symbols that ARE in FACTS):
1. Include constants with semantic_role "threshold" or "limit" when present in FACTS
2. Include model names (semantic_role "model_name") when present in FACTS
3. Describe purpose using docstrings/signatures when available

NEVER contradict facts. You MAY infer purpose from naming conventions (e.g. "logger" → audit logging).
Thresholds (e.g. 0.75) are INPUT parameters — call them "threshold", NEVER "confidence score".

FACTS:
{facts_markdown}

MINIMAL OUTPUT (prioritize critical constants):"""

    PHASE_2_PROMPT = """Rewrite this documentation to be clear and helpful for developers.

CRITICAL RULES:
1. NEVER conflate semantic roles:
   - Thresholds (e.g. 0.75) are INPUT PARAMETERS — not results/outputs of analysis
   - Use "default threshold", "confidence threshold", "cutoff" — NOT "confidence score of 0.75"
   - Confidence scores (e.g. 0.84) are OUTPUT VALUES — not thresholds/defaults
2. NEVER change factual values (line numbers, constants).
3. DO expand explanations using purpose hints and docstrings.
4. DO use natural language — not bullet-point dumps.

ORIGINAL:
{phase_1_output}

REWRITTEN (fluent prose WITH semantic precision):"""

    async def synthesize_tldr_async(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Two-phase: strict grounding, then fluent rewrite. Returns (prose, cost_usd)."""
        from vivarium.scout.llm import call_groq_async

        facts_md = self._facts_to_markdown_rich(facts)
        phase1_prompt = self.PHASE_1_PROMPT.format(facts_markdown=facts_md)

        resp1 = await call_groq_async(
            phase1_prompt,
            model="llama-3.1-8b-instant",
            system="You output documentation. Use ONLY the provided facts. Never invent.",
            max_tokens=500,
            temperature=0.2,
        )
        phase1 = resp1.content.strip()

        phase2_prompt = self.PHASE_2_PROMPT.format(phase_1_output=phase1)
        resp2 = await call_groq_async(
            phase2_prompt,
            model="llama-3.1-8b-instant",
            system="Rewrite for clarity. Never change facts.",
            max_tokens=800,
            temperature=0.5,
        )
        phase2 = resp2.content.strip()

        cost = resp1.cost_usd + resp2.cost_usd

        if not _validate_output_against_facts(phase2, facts):
            phase2 = self._fallback_from_facts(facts)

        checksum = facts.checksum()
        return f"<!-- FACT_CHECKSUM: {checksum} -->\n\n{phase2}", cost

    def synthesize_tldr(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Synchronous wrapper for synthesize_tldr_async."""
        return asyncio.run(self.synthesize_tldr_async(facts))


PHASE_2_REASONING_PROMPT = """Rewrite this documentation to be clear, accurate, and helpful.

CRITICAL RULE (TICKET-50):
- NEVER add constants that were not in the ORIGINAL. The ORIGINAL contains ONLY symbols defined in this module.
- If ORIGINAL omits DEFAULT_CONFIDENCE_THRESHOLD, MAX_EXPANDED_CONTEXT, GROQ_70B_MODEL — do NOT add them.
- When in doubt: OMIT — never hallucinate cross-module ownership.

MANDATORY INCLUSIONS (only for constants already in ORIGINAL):
- Include constants with semantic_role "threshold" when present in ORIGINAL
- Include constants with semantic_role "limit" when present in ORIGINAL
- Include constants with semantic_role "model_name" when present in ORIGINAL
- For each constant in ORIGINAL: state its value and purpose

CONTEXT CLARITY:
- "70B" = 70-billion-parameter Llama model (NOT 70 billion outputs)
- When a constant has a Docstring specifying units (e.g. "character limit", "~10K tokens"), use that wording — do NOT infer units from the numeric value alone (40000 chars ≠ 40000 tokens)
- Thresholds (0.75) are INPUT PARAMETERS; confidence_score is OUTPUT VALUE

OUTPUT RULES:
- Output ONLY the rewritten documentation. No preamble.
- If you cannot include a mandatory constant due to length, TRUNCATE OTHER CONTENT FIRST.

ORIGINAL:
{phase_1_output}

REWRITTEN (include all mandatory constants):"""


class ReasoningDocSynthesizer(ConstrainedDocSynthesizer):
    """TICKET-46: Phase 1 Groq 8B (grounding). Phase 2 Gemini Flash (reasoning-aware rewrite).
    Uses the right model for the job — no regex validation layers.
    """

    def _sparse_module_fallback(self, facts: ModuleFacts) -> str:
        """TICKET-49: Deterministic fallback for sparse modules — module docstring only, no LLM."""
        import ast

        try:
            source = facts.path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(facts.path))
            doc = ast.get_docstring(tree)
            if doc and doc.strip():
                return f"# {facts.path.stem}\n\n{doc.strip()}"
        except Exception:
            pass
        return f"# {facts.path.stem}\n\n(Minimal module — no documentable symbols.)"

    async def synthesize_tldr_async(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Two-phase: Groq grounding, then Gemini Flash reasoning-aware rewrite.
        TICKET-49: Sparsity guardrail — for symbol_count < 3, use deterministic fallback (no LLM).
        """
        from vivarium.scout.big_brain import GEMINI_MODEL_FLASH, call_big_brain_async
        from vivarium.scout.llm import call_groq_async

        symbol_count = sum(
            1
            for _, fact in facts.symbols.items()
            if fact.type in ("class", "function", "constant")
        )

        if symbol_count < 3:
            logger.warning(
                "Sparse module (%d symbols) — using deterministic fallback (no LLM): %s",
                symbol_count,
                facts.path.name,
            )
            checksum = facts.checksum()
            prose = self._sparse_module_fallback(facts)
            return f"<!-- FACT_CHECKSUM: {checksum} -->\n\n{prose}", 0.0

        facts_md = self._facts_to_markdown_rich(facts)
        phase1_prompt = RichDocSynthesizer.PHASE_1_PROMPT.format(facts_markdown=facts_md)

        resp1 = await call_groq_async(
            phase1_prompt,
            model="llama-3.1-8b-instant",
            system="You output documentation. Use ONLY the provided facts. Never invent.",
            max_tokens=700,
            temperature=0.2,
        )
        phase1 = resp1.content.strip()
        cost1 = resp1.cost_usd

        phase2_prompt = PHASE_2_REASONING_PROMPT.format(phase_1_output=phase1)
        resp2 = await call_big_brain_async(
            phase2_prompt,
            system="Rewrite for clarity and semantic precision. Never change facts.",
            max_tokens=8000,
            model=GEMINI_MODEL_FLASH,
            task_type="doc_sync_reasoning",
        )
        phase2 = resp2.content.strip()
        # Strip common preambles (e.g. "Here's the rewritten documentation, ...:")
        for prefix in (
            "Here's the rewritten documentation",
            "Here is the rewritten documentation",
            "Here's the documentation",
        ):
            if phase2.lower().startswith(prefix.lower()):
                colon = phase2.find(":", len(prefix))
                if colon >= 0:
                    phase2 = phase2[colon + 1 :].strip()
                break
        cost2 = resp2.cost_usd

        if not _validate_output_against_facts(phase2, facts):
            logger.warning("Fact validation failed — falling back to Phase 1")
            phase2 = phase1

        checksum = facts.checksum()
        return f"<!-- FACT_CHECKSUM: {checksum} -->\n\n{phase2}", cost1 + cost2

    def synthesize_tldr(self, facts: ModuleFacts) -> Tuple[str, float]:
        """Synchronous wrapper for synthesize_tldr_async."""
        return asyncio.run(self.synthesize_tldr_async(facts))
