"""
Unit tests for BriefParser — 5 real 70B output variations.

Verifies BriefParser parses all Intern A outputs without exception,
rejects confidence >1.0, flags missing gaps as suspicious.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vivarium.scout.middle_manager import BriefParseError, BriefParser, BriefParseResult

REPO_ROOT = Path(__file__).resolve().parents[2]
INTERN_A_OUTPUT = REPO_ROOT / "test_results" / "prompts_first_person.json"

# 5 real 70B output variations (Intern A handoff)
VARIATION_1_EXTRA_NEWLINES = """confidence_score:

0.78

Changing prompts to first person would affect readability. Some prompts use "you" already.
None identified — verified coverage of 5 symbols"""

VARIATION_2_WHITESPACE = """confidence_score:   0.82
Removing the safety preflight would allow blocked tasks to execute. The gateway blocks malicious patterns.
None identified — verified coverage of 12 symbols"""

VARIATION_3_GAP_WITH_PUNCTUATION = """confidence_score: 0.65
Refactoring cycle to async/await may break callers expecting sync. [GAP] Impact on swarm_api.py.
[GAP] Caller chain not fully traced."""

VARIATION_4_GAP_WITHOUT_PUNCTUATION = """confidence_score: 0.71
First-person prompts could improve clarity. [GAP] Impact on X
[GAP] Third-party integrations unknown"""

VARIATION_5_NONE_IDENTIFIED_LOOSE = """confidence_score: 0.90
Context is sufficient. None identified (all symbols verified)."""


class TestBriefParserVariations:
    """5 real 70B output variations — all must parse without exception."""

    def test_variation_1_extra_newlines(self):
        """Extra newlines: confidence_score:\\n\\n0.78"""
        parser = BriefParser()
        r = parser.parse(VARIATION_1_EXTRA_NEWLINES)
        assert r.confidence_score == 0.78
        assert r.has_gaps_declaration is True
        assert r.suspicious is False
        assert "first person" in r.analysis.lower()

    def test_variation_2_whitespace(self):
        """Whitespace: confidence_score:   0.82"""
        parser = BriefParser()
        r = parser.parse(VARIATION_2_WHITESPACE)
        assert r.confidence_score == 0.82
        assert r.has_gaps_declaration is True
        assert r.suspicious is False

    def test_variation_3_gap_with_punctuation(self):
        """[GAP] Impact on X. (with trailing punctuation)"""
        parser = BriefParser()
        r = parser.parse(VARIATION_3_GAP_WITH_PUNCTUATION)
        assert r.confidence_score == 0.65
        assert len(r.gaps) >= 1
        assert "Impact on swarm_api.py" in r.gaps[0] or "swarm_api" in str(r.gaps)
        assert r.has_gaps_declaration is True
        assert r.suspicious is False

    def test_variation_4_gap_without_punctuation(self):
        """[GAP] Impact on X (no trailing punctuation)"""
        parser = BriefParser()
        r = parser.parse(VARIATION_4_GAP_WITHOUT_PUNCTUATION)
        assert r.confidence_score == 0.71
        assert len(r.gaps) >= 1
        assert r.has_gaps_declaration is True
        assert r.suspicious is False

    def test_variation_5_none_identified_loose(self):
        """None identified with justification suffix (no em-dash)"""
        parser = BriefParser()
        r = parser.parse(VARIATION_5_NONE_IDENTIFIED_LOOSE)
        assert r.confidence_score == 0.90
        assert r.has_gaps_declaration is True
        assert r.suspicious is False


class TestBriefParserConstraints:
    """Reject confidence >1.0, flag missing gaps as suspicious."""

    def test_rejects_confidence_gt_1(self):
        parser = BriefParser()
        with pytest.raises(BriefParseError, match="hallucinated calibration"):
            parser.parse("confidence_score: 1.05\nAnalysis.\nNone identified — verified coverage of 1 symbols")

    def test_rejects_confidence_gt_1_whitespace(self):
        parser = BriefParser()
        with pytest.raises(BriefParseError, match="hallucinated calibration"):
            parser.parse("confidence_score:  1.2\nAnalysis.\n[GAP] X")

    def test_flags_missing_gaps_as_suspicious(self):
        """Output with neither [GAP] nor 'None identified' is suspicious."""
        parser = BriefParser()
        r = parser.parse("confidence_score: 0.80\nAnalysis only. No gaps declared.")
        assert r.confidence_score == 0.80
        assert r.has_gaps_declaration is False
        assert r.suspicious is True

    def test_empty_raises(self):
        parser = BriefParser()
        with pytest.raises(BriefParseError, match="Empty output"):
            parser.parse("")

    def test_missing_confidence_returns_zero(self):
        """Unparseable confidence → failsafe 0.0 (triggers escalation, never crash)."""
        parser = BriefParser()
        r = parser.parse("No confidence here. Just text.")
        assert r.confidence_score == 0.0


def test_parse_confidence_natural_language():
    """Natural language 'I'm 84% confident' format (model drift)."""
    parser = BriefParser()
    text = "I'm 84% confident that the gate prevents hallucination"
    r = parser.parse(text)
    assert r.confidence_score == 0.84


def test_parse_confidence_structured():
    """Structured confidence_score: 0.84 format."""
    parser = BriefParser()
    text = "confidence_score: 0.84\nanalysis: MiddleManagerGate prevents hallucination by..."
    r = parser.parse(text)
    assert r.confidence_score == 0.84


class TestBriefParserInternAOutputs:
    """Parse all 3 Intern A outputs without exception (when file exists)."""

    @pytest.fixture
    def intern_a_results(self):
        if not INTERN_A_OUTPUT.exists():
            pytest.skip("Intern A output not found; run test_confidence_prompt.py first")
        data = json.loads(INTERN_A_OUTPUT.read_text(encoding="utf-8"))
        if data.get("run_status") != "pass":
            pytest.skip("Intern A run did not pass")
        return data.get("results", [])

    def test_parses_all_intern_a_outputs(self, intern_a_results):
        parser = BriefParser()
        for item in intern_a_results:
            raw = item.get("raw_output")
            if not raw:
                continue
            r = parser.parse(raw)
            assert r.confidence_score is not None
            assert 0 <= r.confidence_score <= 1.0
            # Intern A passed outputs have gaps_declared=True
            assert r.has_gaps_declaration is True
            assert r.suspicious is False
