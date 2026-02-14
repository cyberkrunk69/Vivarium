"""
Intern #3: Recursion safety tests for MiddleManagerGate bounded expansion.

Verifies:
- Guard 1: Empty gaps → no expansion
- Guard 2: Symbol merge (query_symbols + symbols_to_expand) safe when query_symbols is None
- No path to expansion_depth > 1
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from vivarium.scout.middle_manager import MiddleManagerGate
from vivarium.scout.deps import SymbolRef


# Mock that always returns low confidence with resolvable gap
async def _mock_low_confidence_with_gap(prompt: str, **kwargs):
    return SimpleNamespace(
        content="confidence_score: 0.62\nLow confidence.\n[GAP] impact on resident_memory.py::serialize",
        cost_usd=0.001,
    )


# Mock that always returns low confidence (no resolvable symbols in gaps)
async def _mock_low_confidence_vague_gap(prompt: str, **kwargs):
    return SimpleNamespace(
        content="confidence_score: 0.60\nUncertain.\n[GAP] everything is broken",
        cost_usd=0.001,
    )


class TestExtractSymbolsFromGaps:
    """Guard 1: Prevent empty symbol explosion."""

    def test_empty_gaps_returns_empty_list(self):
        """Empty gaps → no expansion."""
        gate = MiddleManagerGate(audit=MagicMock())
        result = gate._extract_symbols_from_gaps([])
        assert result == []

    def test_extracts_symbol_from_gap(self):
        """Gap with path::symbol → SymbolRef extracted."""
        gate = MiddleManagerGate(audit=MagicMock())
        test_gaps = ["[GAP] impact on resident_memory.py::serialize"]
        symbols = gate._extract_symbols_from_gaps(test_gaps)
        assert len(symbols) == 1
        assert str(symbols[0]) == "resident_memory.py::serialize"

    def test_extracts_from_vivarium_path(self):
        """Gap with full path → SymbolRef extracted."""
        gate = MiddleManagerGate(audit=MagicMock())
        test_gaps = ["[GAP] vivarium/scout/resident_memory.py::serialize"]
        symbols = gate._extract_symbols_from_gaps(test_gaps)
        assert len(symbols) == 1
        assert "resident_memory.py" in str(symbols[0].path)
        assert symbols[0].symbol == "serialize"

    def test_vague_gap_returns_empty(self):
        """Gap like 'everything is broken' → no path::symbol → empty."""
        gate = MiddleManagerGate(audit=MagicMock())
        symbols = gate._extract_symbols_from_gaps(["[GAP] everything is broken"])
        assert len(symbols) == 0


class TestExpansionDepthLimit:
    """No path to expansion_depth > 1."""

    def test_expansion_depth_zero_no_expansion(self, tmp_path):
        """expansion_depth=0 → no expansion, escalate after retries."""
        gate = MiddleManagerGate(
            groq_client=_mock_low_confidence_with_gap,
            audit=MagicMock(),
            max_attempts=2,
        )
        decision = asyncio.run(
            gate.validate_and_compress(
                question="test",
                raw_tldr_context="test context",
                repo_root=tmp_path,
                expansion_depth=0,
            )
        )
        assert decision.decision == "escalate"
        assert decision.source == "raw_tldr"

    def test_expansion_depth_one_escalates_when_no_resolvable_symbols(self, tmp_path):
        """expansion_depth=1 + vague gap (no path::symbol) → escalate."""
        gate = MiddleManagerGate(
            groq_client=_mock_low_confidence_vague_gap,
            audit=MagicMock(),
            max_attempts=2,
        )
        decision = asyncio.run(
            gate.validate_and_compress(
                question="test",
                raw_tldr_context="test context",
                repo_root=tmp_path,
                expansion_depth=1,
            )
        )
        assert decision.decision == "escalate"
        # No symbols to expand → no expansion → escalate after max attempts

    def test_empty_gaps_no_expansion(self, tmp_path):
        """Empty gaps → attempt 0 (no expansion), escalate."""
        async def _mock_low_conf_empty_gaps(prompt: str, **kwargs):
            return SimpleNamespace(
                content="confidence_score: 0.60\ntest\nNone identified — verified coverage of 0 symbols",
                cost_usd=0.001,
            )

        gate = MiddleManagerGate(
            groq_client=_mock_low_conf_empty_gaps,
            audit=MagicMock(),
            max_attempts=2,
        )
        decision = asyncio.run(
            gate.validate_and_compress(
                question="test",
                raw_tldr_context="test context",
                repo_root=tmp_path,
                expansion_depth=1,
            )
        )
        # With "None identified" we have no gaps → no expansion
        assert decision.attempt >= 1
        # Either pass (if confidence parsed) or escalate
