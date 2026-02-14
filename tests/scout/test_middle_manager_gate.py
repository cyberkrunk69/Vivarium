"""
Unit tests for MiddleManagerGate — retry escalation path.

Verifies mock 70B rejection → raw TLDR fallback after max attempts.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from vivarium.scout.middle_manager import GateDecision, MiddleManagerGate


RAW_TLDR_CONTEXT = """## module_a (tldr)
Module A does X.

## module_b (tldr)
Module B does Y."""


async def _mock_70b_reject_low_confidence(prompt: str, **kwargs):
    """Mock 70B that returns low confidence (below 0.75 threshold)."""
    return SimpleNamespace(
        content="confidence_score: 0.50\nLow confidence analysis.\n[GAP] Missing context.",
        cost_usd=0.001,
    )


async def _mock_70b_parse_error(prompt: str, **kwargs):
    """Mock 70B that returns unparseable output."""
    return SimpleNamespace(content="No confidence here. Just garbage.", cost_usd=0.001)


async def _mock_70b_suspicious(prompt: str, **kwargs):
    """Mock 70B that returns suspicious (no gaps declaration)."""
    return SimpleNamespace(
        content="confidence_score: 0.80\nAnalysis only. No gaps declared.",
        cost_usd=0.001,
    )


class TestMiddleManagerGateRetryEscalation:
    """Retry escalation: mock 70B rejection → raw TLDR fallback."""

    def test_escalates_to_raw_tldr_after_max_rejections(self, tmp_path, monkeypatch):
        """Mock 70B returns low confidence 3x → escalate to raw TLDRs."""
        from vivarium.scout.audit import AuditLog

        monkeypatch.setattr("vivarium.scout.raw_briefs.RAW_BRIEFS_DIR", tmp_path / "raw_briefs")
        gate = MiddleManagerGate(
            confidence_threshold=0.75,
            max_attempts=3,
            groq_client=_mock_70b_reject_low_confidence,
            audit=AuditLog(path=tmp_path / "audit.jsonl"),
        )
        decision = asyncio.run(gate.validate_and_compress(
            question="What does X do?",
            raw_tldr_context=RAW_TLDR_CONTEXT,
        ))
        assert decision.decision == "escalate"
        assert decision.source == "raw_tldr"
        assert decision.content == RAW_TLDR_CONTEXT
        assert decision.attempt == 3

    def test_escalates_on_parse_error_after_max_retries(self, tmp_path, monkeypatch):
        """Mock 70B returns unparseable 3x → escalate to raw TLDRs."""
        from vivarium.scout.audit import AuditLog

        monkeypatch.setattr("vivarium.scout.raw_briefs.RAW_BRIEFS_DIR", tmp_path / "raw_briefs")
        gate = MiddleManagerGate(
            max_attempts=3,
            groq_client=_mock_70b_parse_error,
            audit=AuditLog(path=tmp_path / "audit.jsonl"),
        )
        decision = asyncio.run(gate.validate_and_compress(
            question="What?",
            raw_tldr_context=RAW_TLDR_CONTEXT,
        ))
        assert decision.decision == "escalate"
        assert decision.source == "raw_tldr"
        assert decision.content == RAW_TLDR_CONTEXT

    def test_passes_on_first_acceptable_response(self, tmp_path, monkeypatch):
        """Mock 70B returns high confidence → pass on first attempt."""
        from vivarium.scout.audit import AuditLog

        monkeypatch.setattr("vivarium.scout.raw_briefs.RAW_BRIEFS_DIR", tmp_path / "raw_briefs")
        async def _mock_ok(prompt: str, **kwargs):
            return SimpleNamespace(
                content="confidence_score: 0.85\nGood analysis.\nNone identified — verified coverage of 5 symbols",
                cost_usd=0.001,
            )

        gate = MiddleManagerGate(
            groq_client=_mock_ok,
            audit=AuditLog(path=tmp_path / "audit.jsonl"),
        )
        decision = asyncio.run(gate.validate_and_compress(
            question="What?",
            raw_tldr_context=RAW_TLDR_CONTEXT,
        ))
        assert decision.decision == "pass"
        assert decision.source == "compressed"
        assert decision.confidence == 0.85
        assert "Good analysis" in decision.content
        assert decision.attempt == 1

    def test_audit_log_instrumentation(self, tmp_path, monkeypatch):
        """Audit log receives confidence/gap hooks."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = MagicMock()
        async def _mock_ok(prompt: str, **kwargs):
            return SimpleNamespace(
                content="confidence_score: 0.80\nAnalysis.\n[GAP] Missing X.",
                cost_usd=0.001,
            )

        gate = MiddleManagerGate(
            groq_client=_mock_ok,
            audit=audit,
        )
        asyncio.run(gate.validate_and_compress(
            question="What?",
            raw_tldr_context=RAW_TLDR_CONTEXT,
        ))
        audit.log.assert_called()
        calls = [c for c in audit.log.call_args_list if c[0][0] == "gate_compress"]
        assert len(calls) >= 1
        # Check confidence/gaps in config
        call_kw = calls[0][1]
        assert "config" in call_kw
        assert "gaps" in call_kw["config"] or "confidence" in call_kw


class TestRawBriefCapture:
    """TICKET-8: Raw brief stored and raw_brief_path in audit."""

    def test_gate_stores_raw_brief_on_success(self, tmp_path, monkeypatch):
        """Successful 70B response → raw brief stored, raw_brief_path in audit."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = MagicMock()
        content = "confidence_score: 0.85\nGood.\nNone identified — verified coverage of 5 symbols"
        async def _mock_ok(prompt: str, **kwargs):
            return SimpleNamespace(content=content, cost_usd=0.001)

        gate = MiddleManagerGate(groq_client=_mock_ok, audit=audit)
        asyncio.run(gate.validate_and_compress(
            question="What?",
            raw_tldr_context="## x (tldr)\nContext.",
        ))
        # Audit called with raw_brief_path
        calls = [c for c in audit.log.call_args_list if c[0][0] == "gate_compress"]
        assert len(calls) >= 1
        kw = calls[0][1]
        assert "raw_brief_path" in kw or (kw.get("config") or {}).get("raw_brief_path")
        # File stored
        raw_dir = tmp_path / "raw_briefs"
        assert raw_dir.exists()
        files = list(raw_dir.glob("*.md"))
        assert len(files) >= 1
        assert content in files[0].read_text()


class TestGateDecisionProtocol:
    """Type hints match GateDecision protocol."""

    def test_gate_decision_has_required_fields(self):
        """GateDecision implements protocol for big_brain."""
        d = GateDecision(
            decision="pass",
            content="compressed",
            confidence=0.8,
            gaps=["gap1"],
            source="compressed",
            suspicious=False,
            attempt=1,
        )
        assert d.decision in ("pass", "reject", "escalate")
        assert isinstance(d.content, str)
        assert d.confidence is None or 0 <= d.confidence <= 1
        assert isinstance(d.gaps, list)
        assert d.source in ("compressed", "raw_tldr")
