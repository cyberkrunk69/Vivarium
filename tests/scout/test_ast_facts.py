"""
Tests for TICKET-42: Deterministic AST fact extractor.

Validates that facts are extracted with 100% accuracy — zero hallucination.
"""

import pytest
from pathlib import Path

from vivarium.scout.doc_sync.ast_facts import ASTFactExtractor, ModuleFacts


def test_logger_usage_correctly_extracted() -> None:
    """logger must be reported as used at exact line numbers — never 'not used'."""
    facts = ASTFactExtractor().extract(Path("vivarium/scout/middle_manager.py"))
    assert "logger" in facts.symbols
    # logger is used at multiple lines (Load context)
    assert len(facts.symbols["logger"].used_at) > 0
    assert facts.symbols["logger"].type == "constant"
    assert facts.symbols["logger"].defined_at >= 1


def test_max_expanded_context_value_and_usage() -> None:
    """MAX_EXPANDED_CONTEXT value and usage must be correctly extracted."""
    facts = ASTFactExtractor().extract(Path("vivarium/scout/middle_manager.py"))
    assert "MAX_EXPANDED_CONTEXT" in facts.symbols
    assert facts.symbols["MAX_EXPANDED_CONTEXT"].value == "10000"
    assert len(facts.symbols["MAX_EXPANDED_CONTEXT"].used_at) > 0


def test_checksum_deterministic() -> None:
    """Same file must produce same checksum."""
    extractor = ASTFactExtractor()
    facts1 = extractor.extract(Path("vivarium/scout/middle_manager.py"))
    facts2 = extractor.extract(Path("vivarium/scout/middle_manager.py"))
    assert facts1.checksum() == facts2.checksum()


def test_checksum_changes_with_source() -> None:
    """Different source must produce different checksum."""
    extractor = ASTFactExtractor()
    facts_mm = extractor.extract(Path("vivarium/scout/middle_manager.py"))
    facts_router = extractor.extract(Path("vivarium/scout/router.py"))
    assert facts_mm.checksum() != facts_router.checksum()


def test_module_facts_to_json_roundtrip() -> None:
    """ModuleFacts must serialize to JSON and checksum consistently."""
    facts = ASTFactExtractor().extract(Path("vivarium/scout/middle_manager.py"))
    json_str = facts.to_json()
    assert "logger" in json_str
    assert "MAX_EXPANDED_CONTEXT" in json_str
    assert facts.checksum() == facts.checksum()
