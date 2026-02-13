"""
Scout Middle Manager — Parses 70B brief outputs and gates context compression.

BriefParser: handles real-world 70B output variations.
MiddleManagerGate: Tier 1 freshness → Tier 2 70B compress + parse → Tier 3 confidence
threshold. Retry up to 3 attempts; escalate to raw TLDRs on failure.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Literal, Optional, Protocol

from vivarium.scout.audit import AuditLog
from vivarium.scout.raw_briefs import store_raw_brief
from vivarium.scout.deps import SymbolRef


class _DummyDepsGraph:
    """Minimal deps graph when none provided — hydrate_facts uses empty nodes."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.nodes: dict = {}


logger = logging.getLogger(__name__)

# Guard 3: Prevent context explosion (cap expanded context size)
MAX_EXPANDED_CONTEXT = 40_000  # 10K tokens hard limit (~4 chars/token)

# Base confidence prompt — critical_symbols_list injected at runtime (TICKET-48e)
_CONFIDENCE_PROMPT_TEMPLATE = """You are a codebase analyst. Answer based ONLY on provided context.

REQUIRED OUTPUT FORMAT (STRICT — NO DEVIATIONS):
confidence_score: X.XX
<analysis paragraph>
[GAP] <gap description> OR None identified — verified coverage of N symbols

RULES:
- confidence_score MUST be a float between 0.00 and 1.00
- confidence_score MUST reflect ONLY what's in context (no guessing)
- If ANY critical symbol missing → confidence ≤ 0.70
- If context truncated → confidence ≤ 0.65
- If all symbols present AND context complete → confidence ≥ 0.80
- NEVER say "I think" or "probably" — state confidence numerically ONLY

{critical_symbols_block}
"""

GROQ_70B_MODEL = "llama-3.3-70b-versatile"
DEFAULT_CONFIDENCE_THRESHOLD = 0.75
MAX_RETRY_ATTEMPTS = 3


def _build_confidence_prompt(question: str, query_symbols: Optional[List[Any]]) -> str:
    """TICKET-48e: Build prompt with critical symbols for stabilization."""
    critical: set[str] = set()
    # From query_symbols (paths and symbols)
    if query_symbols:
        for ref in query_symbols[:15]:
            s = str(ref)
            if "::" in s:
                path_part, sym = s.split("::", 1)
                if sym:
                    critical.add(sym)
                critical.add(path_part.split("/")[-1].replace(".py", ""))
            else:
                critical.add(str(ref))
    # From question (CamelCase, UPPER_SNAKE)
    for m in re.finditer(r"[A-Z][a-z]+(?:[A-Z][a-z]+)*|[A-Z][A-Z0-9_]{2,}", question):
        critical.add(m.group(0))
    if critical:
        lines = "\n".join(f"- {s}" for s in sorted(critical)[:20])
        block = f"CRITICAL SYMBOLS FOR THIS QUERY:\n{lines}\n"
    else:
        block = ""
    return _CONFIDENCE_PROMPT_TEMPLATE.format(critical_symbols_block=block)


class BriefParseError(Exception):
    """Raised when parsing 70B brief output fails or violates constraints."""

    pass


@dataclass
class BriefParseResult:
    """Parsed result from a 70B confidence-extraction output."""

    confidence_score: float
    analysis: str
    gaps: List[str] = field(default_factory=list)
    has_gaps_declaration: bool = False
    suspicious: bool = False


class BriefParser:
    """
    Parses raw 70B brief outputs from Intern A's confidence extraction prompt.

    Handles real-world quirks: extra newlines, whitespace, [GAP] variants,
    "None identified" variants. Rejects confidence >1.0. Flags outputs
    missing both [GAP] and "None identified" as suspicious.
    """

    # Allow newlines and arbitrary whitespace between label and value
    CONFIDENCE_RE = re.compile(
        r"confidence_score\s*:\s*([\d.]+)",
        re.IGNORECASE | re.DOTALL,
    )

    def _parse_confidence(self, text: str) -> tuple[float, int]:
        """
        Robust confidence extraction — multiple formats.
        Returns (score, analysis_start_pos). Failsafe: (0.0, 0) triggers escalation.
        """
        # Format 1: Structured (preferred)
        match = re.search(r"confidence_score\s*[:=]\s*([\d.]+)", text, re.IGNORECASE)
        if match:
            score = float(match.group(1))
            return score, match.end()

        # Format 2: Natural language ("I'm 84% confident")
        match = re.search(
            r"(?:i'm|i am|confidence)\s*(?:about\s*)?(\d{1,3})\s*%?(?:\s*confident)?",
            text,
            re.IGNORECASE,
        )
        if match:
            pct = float(match.group(1))
            score = pct / 100.0
            return score, match.end()

        # Format 3: Decimal without label ("0.84")
        match = re.search(r"(?<!\w)(0\.\d{2,})(?!\d)", text)
        if match:
            score = float(match.group(1))
            return score, match.end()

        # FAILSAFE: Return 0.0 (triggers escalation — safe default)
        snippet = text[:200].replace("\n", " ").strip()
        logger.warning("Confidence parse failed. Raw snippet: '%s...'", snippet)
        return 0.0, 0

    # [GAP] followed by optional whitespace and content (with or without trailing punctuation)
    GAP_RE = re.compile(r"\[GAP\]\s*(.+?)(?=\[GAP\]|None identified|$)", re.IGNORECASE | re.DOTALL)

    # "None identified" with optional em-dash and verified coverage, or justification suffix
    NONE_IDENTIFIED_RE = re.compile(
        r"None\s+identified\s*(?:—|–|-)\s*verified\s+coverage\s+of\s+(\d+)\s+symbols",
        re.IGNORECASE,
    )
    NONE_IDENTIFIED_LOOSE_RE = re.compile(
        r"None\s+identified",
        re.IGNORECASE,
    )

    def parse(self, raw: str) -> BriefParseResult:
        """
        Parse raw 70B output. Raises BriefParseError on invalid confidence.

        Args:
            raw: Raw output from Groq 70B (confidence extraction prompt).

        Returns:
            BriefParseResult with confidence_score, analysis, gaps, flags.

        Raises:
            BriefParseError: If confidence_score missing, unparseable, or >1.0.
        """
        text = (raw or "").strip()
        if not text:
            raise BriefParseError("Empty output")

        # 1. Extract confidence_score (robust: structured, natural language, decimal)
        score, analysis_start = self._parse_confidence(text)

        if score > 1.0:
            raise BriefParseError("hallucinated calibration")

        score = min(1.0, max(0.0, score))  # clamp to [0, 1] for valid range

        # 2. Extract [GAP] items
        gaps = []
        for g in self.GAP_RE.finditer(text):
            content = g.group(1).strip()
            if content:
                gaps.append(content)

        # 3. Check for "None identified" (strict or loose)
        has_none_identified = bool(self.NONE_IDENTIFIED_RE.search(text)) or bool(
            self.NONE_IDENTIFIED_LOOSE_RE.search(text)
        )
        has_gap = len(gaps) > 0
        has_gaps_declaration = has_gap or has_none_identified

        # 4. Suspicious: missing BOTH [GAP] AND "None identified"
        suspicious = not has_gaps_declaration

        # 5. Analysis: everything between confidence line and first [GAP]/None identified
        analysis = self._extract_analysis(text, analysis_start)

        return BriefParseResult(
            confidence_score=score,
            analysis=analysis,
            gaps=gaps,
            has_gaps_declaration=has_gaps_declaration,
            suspicious=suspicious,
        )

    def _extract_analysis(self, text: str, analysis_start: int) -> str:
        """Extract analysis text (between confidence line and gaps section)."""
        start = analysis_start
        end = len(text)
        gap_pos = text.find("[GAP]", start)
        none_m = self.NONE_IDENTIFIED_LOOSE_RE.search(text[start:])
        none_pos = start + none_m.start() if none_m else end + 1
        if gap_pos >= start:
            end = min(end, gap_pos)
        if none_pos <= len(text):
            end = min(end, none_pos)
        return text[start:end].strip()


# --- Gate integration ---


class GateDecisionProtocol(Protocol):
    """Protocol for gate decisions — type hints for big_brain integration."""

    decision: Literal["pass", "reject", "escalate"]
    content: str
    confidence: Optional[float]
    gaps: List[str]
    source: Literal["compressed", "raw_tldr", "raw_facts"]
    suspicious: bool
    attempt: int


@dataclass
class GateDecision:
    """Decision from MiddleManagerGate — pass (compressed), escalate (raw facts), or reject."""

    decision: Literal["pass", "reject", "escalate"]
    content: str
    confidence: Optional[float] = None
    gaps: List[str] = field(default_factory=list)
    source: Literal["compressed", "raw_tldr", "raw_facts"] = "compressed"
    suspicious: bool = False
    attempt: int = 0
    has_gaps_declaration: bool = False  # True if gaps declared or "None identified"
    expanded_symbols: List[str] = field(default_factory=list)  # path::symbol for TICKET-27 whimsy
    initial_confidence: Optional[float] = None  # before expansion, for whimsy delta
    cost_usd: float = 0.0  # TICKET-40: Actual gate cost (70B calls), for whimsy integrity


class MiddleManagerGate:
    """
    Gates context compression for big_brain integration.

    Tier 1: deterministic freshness (deps.graph invalidated_at)
    Tier 2: compress via 70B + parse via BriefParser
    Tier 3: confidence threshold (0.75 conservative)
    Retry: max 3 attempts → escalate to raw TLDRs
    """

    # Guard 1: Regex to extract path::symbol from gap text (e.g. "impact on resident_memory.py::serialize")
    _SYMBOL_FROM_GAP_RE = re.compile(r"(\S+\.py)::(\w+)")

    def __init__(
        self,
        *,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        max_attempts: int = MAX_RETRY_ATTEMPTS,
        groq_client: Optional[Callable[..., Any]] = None,
        audit: Optional[AuditLog] = None,
    ):
        self.confidence_threshold = confidence_threshold
        self.max_attempts = max_attempts
        self._groq_client = groq_client
        self._audit = audit or AuditLog()
        self._parser = BriefParser()

    def _extract_symbols_from_gaps(self, gaps: List[str]) -> List[SymbolRef]:
        """Extract SymbolRef from gap text. Guard 1: early exit if no gaps."""
        if not gaps:
            return []  # EARLY EXIT — no gaps, no expansion
        symbols: List[SymbolRef] = []
        for gap in gaps:
            for m in self._SYMBOL_FROM_GAP_RE.finditer(gap):
                try:
                    path_str, symbol_name = m.group(1), m.group(2)
                    ref = SymbolRef(Path(path_str), symbol_name)
                    symbols.append(ref)
                except (ValueError, IndexError):
                    continue
        return list(set(symbols))

    def _validate_doc_freshness(self, doc_path: Path, source_path: Path) -> bool:
        """
        Reject docs with stale or missing fact checksums.

        TICKET-42: Deterministic foundation — docs must have FACT_CHECKSUM
        matching current AST. If missing or mismatch, treat as stale.
        """
        if not doc_path.exists():
            return False
        content = doc_path.read_text(encoding="utf-8", errors="replace")

        match = re.search(r"<!-- FACT_CHECKSUM: ([a-f0-9]{64}) -->", content)
        if not match:
            logger.warning("No FACT_CHECKSUM in %s — treating as stale", doc_path)
            return False

        embedded_checksum = match.group(1)

        try:
            from vivarium.scout.doc_sync.ast_facts import ASTFactExtractor

            current_facts = ASTFactExtractor().extract(source_path)
            if embedded_checksum != current_facts.checksum():
                logger.warning("Checksum mismatch: %s stale (AST changed)", doc_path)
                return False
        except Exception as e:
            logger.warning("Could not validate doc freshness for %s: %s", doc_path, e)
            return False

        return True

    def _load_docs_for_symbols(
        self, symbols: List[SymbolRef], repo_root: Path
    ) -> str:
        """
        DEPRECATED (TICKET-43): Prose is not truth. Use hydrate_facts() for structured facts.

        Kept for legacy expansion path when gate receives raw_tldr_context (synthesis).
        """
        seen: set = set()
        parts: List[str] = []
        for ref in symbols:
            key = str(ref.path)
            if key in seen:
                continue
            seen.add(key)
            full_path = (repo_root / ref.path).resolve()
            if not full_path.exists():
                continue
            file_parts: List[str] = []
            docs_dir = full_path.parent / ".docs"
            for suffix in (".tldr.md", ".deep.md"):
                doc_path = docs_dir / f"{full_path.name}{suffix}"
                if doc_path.exists():
                    if not self._validate_doc_freshness(doc_path, full_path):
                        file_parts.append(
                            "[GAP] Documentation stale — AST changed since last doc sync"
                        )
                    else:
                        try:
                            file_parts.append(
                                doc_path.read_text(encoding="utf-8", errors="replace")
                            )
                        except OSError:
                            pass
            if not file_parts:
                try:
                    rel = full_path.relative_to(repo_root)
                    central = repo_root / "docs" / "livingDoc" / rel.parent
                    for suffix in (".tldr.md", ".deep.md"):
                        doc_path = central / f"{full_path.name}{suffix}"
                        if doc_path.exists():
                            if not self._validate_doc_freshness(doc_path, full_path):
                                file_parts.append(
                                    "[GAP] Documentation stale — AST changed since last doc sync"
                                )
                            else:
                                try:
                                    file_parts.append(
                                        doc_path.read_text(
                                            encoding="utf-8", errors="replace"
                                        )
                                    )
                                except OSError:
                                    pass
                except ValueError:
                    pass
            if file_parts:
                parts.append(f"## {ref.path} (expanded)\n\n" + "\n\n".join(file_parts))
        return "\n\n---\n\n".join(parts) if parts else ""

    async def validate_and_compress(
        self,
        question: str,
        facts: Optional[Any] = None,
        *,
        raw_tldr_context: Optional[str] = None,
        deps_graph: Optional[Any] = None,
        query_symbols: Optional[List[Any]] = None,
        repo_root: Optional[Path] = None,
        expansion_depth: int = 1,
    ) -> GateDecision:
        """
        Validate and compress context. Returns GateDecision for big_brain consumption.

        TICKET-43: Consumes ModuleFacts (structured) — never prose. Prose flows one way: out.
        Tier 1: If deps_graph provided, check freshness (invalidated_at).
        Tier 2: Call 70B to compress; parse with BriefParser.
        Tier 3: Require confidence >= threshold; retry up to max_attempts.
        Expansion: If low confidence + gaps, fetch more facts via hydrate_facts.
        Escalation: After max failures, return raw facts (to_prompt).
        """
        # Resolve repo_root from deps_graph if not provided
        _repo_root = repo_root
        if _repo_root is None and deps_graph is not None:
            _repo_root = getattr(deps_graph, "repo_root", None)

        # TICKET-43: Build context from facts (structured) or raw_tldr (synthesis path)
        if facts is not None and hasattr(facts, "to_prompt"):
            current_context = facts.to_prompt()
            use_facts = True
        else:
            current_context = (raw_tldr_context or "").strip()
            use_facts = False

        # Tier 1: deterministic freshness (Guard 2: safe merge for deps)
        _query_symbols = query_symbols
        if deps_graph is not None and _query_symbols:
            nodes = deps_graph.get_context_package(_query_symbols)
            trust = deps_graph.get_trust_metadata(nodes)
            if trust.get("invalidation_cascade_triggered") and trust.get("stale_ratio", 0) > 0.5:
                logger.debug("Tier 1: high stale ratio — escalating to raw")
                self._audit.log(
                    "gate_compress",
                    reason="stale_cascade",
                    confidence=0,
                    gaps=[],
                    config={"stale_ratio": trust.get("stale_ratio")},
                )
                return GateDecision(
                    decision="escalate",
                    content=current_context,
                    source="raw_facts" if use_facts else "raw_tldr",
                    attempt=0,
                )

        # Tier 2 + 3: compress via 70B, parse, check confidence
        if not current_context.strip():
            logger.warning("Gate received empty context — 70B will return 0.00 → escalation")
        last_error: Optional[str] = None
        attempt = 0
        expanded_symbols: List[str] = []
        initial_confidence: Optional[float] = None
        total_gate_cost: float = 0.0  # TICKET-40: Accumulate 70B cost for whimsy

        while attempt < self.max_attempts:
            attempt += 1
            # Guard 3: truncate context to prevent explosion
            truncated = current_context[:MAX_EXPANDED_CONTEXT]
            if len(current_context) > MAX_EXPANDED_CONTEXT:
                logger.warning("Expanded context too large — truncating")
                current_context = truncated

            confidence_prompt = _build_confidence_prompt(question, _query_symbols)
            full_prompt = f"""{confidence_prompt}

---
CONTEXT:
{current_context[:28000]}

---
QUESTION: {question}

---
YOUR RESPONSE (must include confidence_score and gaps/verified):"""

            raw_brief_path: Optional[Any] = None
            try:
                raw, cost_usd = await self._call_70b(full_prompt)
                total_gate_cost += cost_usd

                # TICKET-8: Store raw 70B output for calibration (no parse/filter)
                raw_brief_path = store_raw_brief(raw)
                config = {
                    "gaps": [],
                    "suspicious": False,
                    "attempt": attempt,
                }
                if raw_brief_path:
                    config["raw_brief_path"] = str(raw_brief_path)

                parsed = self._parser.parse(raw)
                config["gaps"] = parsed.gaps
                config["suspicious"] = parsed.suspicious

                # Audit: confidence/gap instrumentation + cost + raw_brief (TICKET-8)
                self._audit.log(
                    "gate_compress",
                    cost=cost_usd,
                    confidence=int(parsed.confidence_score * 100),
                    model=GROQ_70B_MODEL,
                    config=config,
                    raw_brief_path=str(raw_brief_path) if raw_brief_path else None,
                )

                # Tier 3: confidence threshold
                if (
                    parsed.confidence_score >= self.confidence_threshold
                    and not parsed.suspicious
                ):
                    return GateDecision(
                        decision="pass",
                        content=parsed.analysis,
                        confidence=parsed.confidence_score,
                        gaps=parsed.gaps,
                        source="compressed",
                        suspicious=False,
                        attempt=attempt,
                        has_gaps_declaration=parsed.has_gaps_declaration,
                        expanded_symbols=expanded_symbols,
                        initial_confidence=initial_confidence,
                        cost_usd=total_gate_cost,
                    )

                last_error = (
                    f"confidence {parsed.confidence_score} < {self.confidence_threshold}"
                    if parsed.confidence_score < self.confidence_threshold
                    else "suspicious (missing gaps declaration)"
                )

                # Bounded expansion: one deterministic step when low confidence + gaps
                if expansion_depth > 0 and parsed.gaps and _repo_root and use_facts:
                    symbols_to_expand = self._extract_symbols_from_gaps(parsed.gaps)
                    if symbols_to_expand:
                        expanded_symbols.extend(str(ref) for ref in symbols_to_expand)
                        initial_confidence = parsed.confidence_score
                        # Guard 2: Prevent symbol list mutation bug
                        new_symbols = (
                            _query_symbols + symbols_to_expand
                            if _query_symbols
                            else symbols_to_expand
                        )
                        _query_symbols = new_symbols
                        # TICKET-43: Load more FACTS (never prose)
                        from vivarium.scout.context import hydrate_facts

                        extra_facts = await hydrate_facts(
                            symbols_to_expand,
                            deps_graph or _DummyDepsGraph(_repo_root),
                            _repo_root,
                            max_facts=30,
                            max_depth=1,
                        )
                        if extra_facts.symbols:
                            extra = extra_facts.to_prompt(max_chars=8000)
                            expanded_context = current_context + "\n\n---\n\n" + extra
                            if len(expanded_context) > MAX_EXPANDED_CONTEXT:
                                logger.warning("Expanded context too large — truncating")
                                expanded_context = expanded_context[:MAX_EXPANDED_CONTEXT]
                            current_context = expanded_context
                            expansion_depth -= 1
                            logger.info(
                                "Gate: confidence %.2f → expand (%d symbols) → retry",
                                parsed.confidence_score,
                                len(symbols_to_expand),
                            )
                            continue  # retry with expanded context
                elif expansion_depth > 0 and parsed.gaps and _repo_root and not use_facts:
                    # Legacy: prose expansion (deprecated)
                    symbols_to_expand = self._extract_symbols_from_gaps(parsed.gaps)
                    if symbols_to_expand:
                        expanded_symbols.extend(str(ref) for ref in symbols_to_expand)
                        initial_confidence = parsed.confidence_score
                        new_symbols = (
                            _query_symbols + symbols_to_expand
                            if _query_symbols
                            else symbols_to_expand
                        )
                        _query_symbols = new_symbols
                        extra = self._load_docs_for_symbols(symbols_to_expand, _repo_root)
                        if extra:
                            expanded_context = current_context + "\n\n---\n\n" + extra
                            if len(expanded_context) > MAX_EXPANDED_CONTEXT:
                                logger.warning("Expanded context too large — truncating")
                                expanded_context = expanded_context[:MAX_EXPANDED_CONTEXT]
                            current_context = expanded_context
                            expansion_depth -= 1
                            logger.info(
                                "Gate: confidence %.2f → expand (%d symbols) → retry",
                                parsed.confidence_score,
                                len(symbols_to_expand),
                            )
                            continue

            except BriefParseError as e:
                last_error = str(e)
                parse_fail_config = {"attempt": attempt, "error": last_error}
                if raw_brief_path:
                    parse_fail_config["raw_brief_path"] = str(raw_brief_path)
                self._audit.log(
                    "gate_compress",
                    reason="parse_fail",
                    config=parse_fail_config,
                )
            except Exception as e:
                last_error = str(e)
                logger.warning("Gate 70B call failed (attempt %d): %s", attempt, e)
                self._audit.log(
                    "gate_compress",
                    reason="api_error",
                    config={"attempt": attempt, "error": last_error},
                )

        # Escalation: raw facts or raw TLDR fallback
        logger.info("Gate: max attempts reached, escalating to raw")
        self._audit.log(
            "gate_escalate",
            reason="max_retries",
            config={"last_error": last_error, "attempts": self.max_attempts},
        )
        return GateDecision(
            decision="escalate",
            content=current_context,
            source="raw_facts" if use_facts else "raw_tldr",
            attempt=self.max_attempts,
            expanded_symbols=expanded_symbols,
            cost_usd=total_gate_cost,
        )

    async def _call_70b(self, prompt: str) -> tuple[str, float]:
        """Call Groq 70B. Returns (content, cost_usd). Uses injected client if provided."""
        if self._groq_client:
            resp = await self._groq_client(
                prompt,
                model=GROQ_70B_MODEL,
                system="You output structured responses. Always include confidence_score and gaps.",
                max_tokens=1024,
            )
            content = getattr(resp, "content", str(resp)).strip()
            cost = getattr(resp, "cost_usd", 0.0) or 0.0
            return content, cost

        from vivarium.scout.llm import call_groq_async

        resp = await call_groq_async(
            prompt,
            model=GROQ_70B_MODEL,
            system="You output structured responses. Always include confidence_score and gaps.",
            max_tokens=1024,
        )
        return resp.content.strip(), resp.cost_usd
# Scout: truth-preserving funnel — shipped Feb 13 2026
