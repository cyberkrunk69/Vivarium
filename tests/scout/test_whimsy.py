"""
TICKET-20/21: Whimsy formatter tests.

TICKET-21: Phrase banks + hash rotation. Tests use fixed query for determinism.
"""

from __future__ import annotations

import pytest

from vivarium.scout.middle_manager import GateDecision
from vivarium.scout.ui.whimsy import WhimsyFormatter
from vivarium.scout.ui.whimsy_data import DEFAULT_PHRASE_BANKS


class TestWhimsyFormatter:
    """Cave man CEO metaphors. TICKET-21: phrase bank variety."""

    def test_format_pass_with_gaps(self):
        """Pass with gaps → role says verb, gap prefix, Bright Spark."""
        d = GateDecision(
            decision="pass",
            content="analysis",
            confidence=0.84,
            gaps=["JavaScript adapters"],
            source="compressed",
            attempt=1,
        )
        out = WhimsyFormatter.format_gate_decision(d, query="test")
        roles = DEFAULT_PHRASE_BANKS["roles"]["gatekeeper"]
        assert any(r in out for r in roles), f"Expected one of {roles} in {out}"
        assert "says:" in out
        assert "84% sure" in out
        assert "JavaScript adapters" in out
        assert "Bright Spark" in out
        gap_prefixes = DEFAULT_PHRASE_BANKS["gap_prefixes"]
        assert any(p in out for p in gap_prefixes), f"Expected gap prefix in {out}"

    def test_format_pass_no_gaps(self):
        """Pass with no gaps → No gaps!"""
        d = GateDecision(
            decision="pass",
            content="analysis",
            confidence=0.92,
            gaps=[],
            source="compressed",
            attempt=1,
        )
        out = WhimsyFormatter.format_gate_decision(d, query="test")
        assert "No gaps!" in out
        assert "92% sure" in out

    def test_format_escalate_stale(self):
        """Escalate attempt=0 → stale reason, boss role."""
        d = GateDecision(
            decision="escalate",
            content="raw",
            source="raw_tldr",
            attempt=0,
        )
        out = WhimsyFormatter.format_gate_decision(d, query="test")
        stale_reasons = DEFAULT_PHRASE_BANKS["escalate_reasons"]["stale"]
        assert any(r in out for r in stale_reasons), f"Expected stale reason in {out}"
        boss_roles = DEFAULT_PHRASE_BANKS["roles"]["boss"]
        assert any(r in out for r in boss_roles), f"Expected boss role in {out}"

    def test_format_escalate_low_confidence(self):
        """Escalate attempt>0 → low confidence reason."""
        d = GateDecision(
            decision="escalate",
            content="raw",
            confidence=0.62,
            source="raw_tldr",
            attempt=3,
        )
        out = WhimsyFormatter.format_gate_decision(d, query="test")
        reasons = DEFAULT_PHRASE_BANKS["escalate_reasons"]["low_confidence"]
        assert any(r in out for r in reasons), f"Expected low_confidence reason in {out}"
        assert "62%" in out

    def test_plain_text_fallback(self):
        """use_emoji=False → no emojis."""
        d = GateDecision(
            decision="pass",
            content="x",
            confidence=0.8,
            gaps=[],
            source="compressed",
            attempt=1,
        )
        out = WhimsyFormatter.format_gate_decision(d, use_emoji=False, query="test")
        assert "🚪" not in out
        assert "😎" not in out
        assert "[Gate]" in out
        roles = DEFAULT_PHRASE_BANKS["roles"]["gatekeeper"]
        assert any(r in out for r in roles), f"Expected one of {roles} in {out}"

    def test_deterministic_same_query(self):
        """Same query = same whimsy (reproducible logs)."""
        d = GateDecision(
            decision="pass",
            content="x",
            confidence=0.8,
            gaps=[],
            source="compressed",
            attempt=1,
        )
        out1 = WhimsyFormatter.format_gate_decision(d, query="change prompts")
        out2 = WhimsyFormatter.format_gate_decision(d, query="change prompts")
        assert out1 == out2

    def test_variety_across_queries(self):
        """Different queries → different phrase picks (when hash differs)."""
        d = GateDecision(
            decision="pass",
            content="x",
            confidence=0.8,
            gaps=[],
            source="compressed",
            attempt=1,
        )
        outputs = [
            WhimsyFormatter.format_gate_decision(d, query=f"query {i}")
            for i in range(5)
        ]
        # With 5 variants per slot, 5 different queries should yield some variety
        unique = len(set(outputs))
        assert unique > 1, f"Expected variety across queries, got identical: {outputs[0][:80]}..."

    def test_user_override_respected(self, monkeypatch):
        """User phrase bank override via ~/.scout/whimsy.yaml."""
        custom = {
            "roles": {
                "gatekeeper": ["Syntax Sheriff"],
            },
        }

        def mock_load():
            return custom

        monkeypatch.setattr(
            "vivarium.scout.ui.whimsy.load_user_phrase_bank",
            mock_load,
        )
        d = GateDecision(
            decision="pass",
            content="x",
            confidence=0.8,
            gaps=[],
            source="compressed",
            attempt=1,
        )
        out = WhimsyFormatter.format_gate_decision(d, query="test")
        assert "Syntax Sheriff" in out
        assert "says:" in out
