"""
TICKET-9: Gate path vs direct path, audit events.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

# Repo root for imports
REPO_ROOT = Path(__file__).resolve().parents[2]
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from vivarium.scout.audit import AuditLog
from vivarium.scout.big_brain import (
    answer_help_async,
    call_big_brain_async,
    call_big_brain_gated_async,
)
from vivarium.scout.middle_manager import GateDecision, MiddleManagerGate


CANONICAL_ANSWER = "Scout helps with code, docs, and dev workflow. Tools: query, sync, nav. Try query for docs."


async def _mock_groq_pass(prompt: str, **kwargs):
    """Mock 70B that returns high confidence → gate pass."""
    return SimpleNamespace(
        content="confidence_score: 0.85\nScout helps with code, docs, dev workflow. Tools: query, sync, nav.\nNone identified — verified coverage of 5 symbols",
        cost_usd=0.001,
    )


async def _mock_big_brain(prompt: str, **kwargs):
    """Mock Gemini that returns canonical answer."""
    return SimpleNamespace(
        content=CANONICAL_ANSWER,
        cost_usd=0.01,
        model="gemini-2.5-pro",
        input_tokens=100,
        output_tokens=50,
    )


class TestGatePathVsDirectPath:
    """Gate path vs direct path, same query, semantically equivalent."""

    def test_gate_path_produces_response(self, tmp_path, monkeypatch):
        """Gate path returns valid response."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")
        gate = MiddleManagerGate(groq_client=_mock_groq_pass, audit=audit)

        response = asyncio.run(call_big_brain_gated_async(
            question="What can Scout do?",
            raw_tldr_context="Tools: query, sync. State: 3 files staged.",
            gate=gate,
            big_brain_client=_mock_big_brain,
        ))
        assert response.content.strip()
        assert "Scout" in response.content or "query" in response.content.lower()

    def test_direct_path_produces_response(self):
        """Direct path (no gate) returns valid response."""
        response = asyncio.run(call_big_brain_async(
            "What can Scout do? Context: Tools query, sync. Answer briefly.",
            system="You answer concisely.",
            max_tokens=128,
            big_brain_client=_mock_big_brain,
        ))
        assert response.content.strip()
        assert response.content == CANONICAL_ANSWER

    def test_gate_and_direct_semantically_equivalent(self, tmp_path, monkeypatch):
        """Same query via gate path and direct path → both return non-empty, similar."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")
        gate = MiddleManagerGate(groq_client=_mock_groq_pass, audit=audit)

        raw_context = "Tools: query (read docs), sync (generate). State: vivarium/scout."

        gate_resp = asyncio.run(call_big_brain_gated_async(
            question="What can Scout do?",
            raw_tldr_context=raw_context,
            gate=gate,
            big_brain_client=_mock_big_brain,
        ))

        direct_resp = asyncio.run(call_big_brain_async(
            f"Context: {raw_context}\n\nQuestion: What can Scout do?\nAnswer briefly.",
            system="You answer concisely.",
            max_tokens=128,
            big_brain_client=_mock_big_brain,
        ))

        assert gate_resp.content.strip()
        assert direct_resp.content.strip()
        # Semantically equivalent: same mock returns same content
        assert gate_resp.content == direct_resp.content == CANONICAL_ANSWER


class TestAuditGateEvents:
    """Audit log shows gate_compress or gate_escalate."""

    def test_gate_path_logs_gate_compress(self, tmp_path, monkeypatch):
        """Gate path (pass) logs gate_compress."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")
        gate = MiddleManagerGate(groq_client=_mock_groq_pass, audit=audit)

        asyncio.run(call_big_brain_gated_async(
            question="What?",
            raw_tldr_context="Context.",
            gate=gate,
            big_brain_client=_mock_big_brain,
        ))

        events = audit.last_events(n=20, event_type="gate_compress")
        assert len(events) >= 1

    def test_gate_escalate_logs_gate_escalate(self, tmp_path, monkeypatch):
        """Gate escalate path logs gate_escalate."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")

        async def _mock_groq_reject(prompt: str, **kwargs):
            return SimpleNamespace(
                content="confidence_score: 0.50\nLow.\n[GAP] X.",
                cost_usd=0.001,
            )

        gate = MiddleManagerGate(
            groq_client=_mock_groq_reject,
            audit=audit,
            max_attempts=2,
        )

        asyncio.run(call_big_brain_gated_async(
            question="What?",
            raw_tldr_context="Context.",
            gate=gate,
            big_brain_client=_mock_big_brain,
        ))

        escalate_events = audit.last_events(n=10, event_type="gate_escalate")
        assert len(escalate_events) >= 1


class TestTicket19FlashRouting:
    """TICKET-19: Gate pass → Flash; escalate → Pro."""

    def test_pass_uses_flash_model(self, tmp_path, monkeypatch):
        """Gate pass → synthesis uses GEMINI_MODEL_FLASH."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")
        gate = MiddleManagerGate(groq_client=_mock_groq_pass, audit=audit)

        captured_model = []

        async def _capture_model(prompt, **kwargs):
            captured_model.append(kwargs.get("model"))
            return SimpleNamespace(
                content=CANONICAL_ANSWER,
                cost_usd=0.01,
                model=kwargs.get("model", "gemini"),
                input_tokens=100,
                output_tokens=50,
            )

        response = asyncio.run(call_big_brain_gated_async(
            question="What can Scout do?",
            raw_tldr_context="Tools: query, sync.",
            gate=gate,
            big_brain_client=_capture_model,
        ))
        assert response.content.strip()
        assert len(captured_model) == 1
        assert "gemini-2.5-flash" in captured_model[0]

    def test_escalate_uses_pro_model(self, tmp_path, monkeypatch):
        """Gate escalate → synthesis uses GEMINI_MODEL_PRO."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")

        async def _mock_groq_reject(prompt: str, **kwargs):
            return SimpleNamespace(
                content="confidence_score: 0.50\nLow.\n[GAP] X.",
                cost_usd=0.001,
            )

        gate = MiddleManagerGate(
            groq_client=_mock_groq_reject,
            audit=audit,
            max_attempts=2,
        )

        captured_model = []

        async def _capture_model(prompt, **kwargs):
            captured_model.append(kwargs.get("model"))
            return SimpleNamespace(
                content=CANONICAL_ANSWER,
                cost_usd=0.01,
                model=kwargs.get("model", "gemini"),
                input_tokens=100,
                output_tokens=50,
            )

        response = asyncio.run(call_big_brain_gated_async(
            question="What?",
            raw_tldr_context="Context.",
            gate=gate,
            big_brain_client=_capture_model,
        ))
        assert response.content.strip()
        assert len(captured_model) == 1
        assert "gemini-2.5-pro" in captured_model[0]

    def test_gate_synthesis_logged_on_pass(self, tmp_path, monkeypatch):
        """gate_synthesis event logged with model=flash on pass."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")
        gate = MiddleManagerGate(groq_client=_mock_groq_pass, audit=audit)

        asyncio.run(call_big_brain_gated_async(
            question="What?",
            raw_tldr_context="Context.",
            gate=gate,
            big_brain_client=_mock_big_brain,
        ))

        events = audit.last_events(n=20, event_type="gate_synthesis")
        assert len(events) >= 1
        assert events[0].get("model") == "flash"


class TestAnswerHelpGated:
    """answer_help_async with gated and direct paths."""

    def test_answer_help_direct_path(self, monkeypatch):
        """answer_help_async with use_gate=False (direct) works."""
        async def _mock_bb(prompt, **kwargs):
            return SimpleNamespace(
                content=CANONICAL_ANSWER,
                cost_usd=0.01,
                model="gemini",
                input_tokens=0,
                output_tokens=0,
            )

        monkeypatch.setattr(
            "vivarium.scout.big_brain.call_big_brain_async",
            _mock_bb,
        )
        result = asyncio.run(answer_help_async(
            {"cwd_scope": "vivarium/scout"},
            use_gate=False,
        ))
        assert result.strip()
        assert result == CANONICAL_ANSWER

    def test_answer_help_gated_path(self, tmp_path, monkeypatch):
        """answer_help_async with use_gate=True uses gated path."""
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        audit = AuditLog(path=tmp_path / "audit.jsonl")
        async def _mock_bb(prompt, **kwargs):
            return SimpleNamespace(
                content=CANONICAL_ANSWER,
                cost_usd=0.01,
                model="gemini",
                input_tokens=0,
                output_tokens=0,
            )

        monkeypatch.setattr(
            "vivarium.scout.big_brain.call_big_brain_async",
            _mock_bb,
        )
        gate = MiddleManagerGate(groq_client=_mock_groq_pass, audit=audit)
        original = __import__("vivarium.scout.big_brain", fromlist=["call_big_brain_gated_async"]).call_big_brain_gated_async

        async def _gated_with_mock_gate(*args, **kwargs):
            kwargs["gate"] = gate
            return await original(*args, **kwargs)

        monkeypatch.setattr(
            "vivarium.scout.big_brain.call_big_brain_gated_async",
            _gated_with_mock_gate,
        )
        result = asyncio.run(answer_help_async(
            {"cwd_scope": "vivarium/scout"},
            use_gate=True,
        ))
        assert result.strip()
        assert result == CANONICAL_ANSWER
