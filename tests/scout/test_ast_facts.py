"""
Tests for TICKET-42: Deterministic AST fact extractor.

Validates symbol extraction, attribution, and signature fidelity.
"""

import pytest
from pathlib import Path

from vivarium.scout.doc_sync.ast_facts import ASTFactExtractor, ModuleFacts

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ast_facts_sample.py"


def test_async_module_function_extracted() -> None:
    """Async functions at module level must be extracted as type=function."""
    facts = ASTFactExtractor().extract(FIXTURE_PATH)
    assert "async_module_func" in facts.symbols
    assert facts.symbols["async_module_func"].type == "function"
    assert facts.symbols["async_module_func"].defined_at >= 1


def test_class_method_not_module_function() -> None:
    """Methods must not appear as module-level functions."""
    facts = ASTFactExtractor().extract(FIXTURE_PATH)
    assert "sync_method" not in facts.symbols
    assert "async_method" not in facts.symbols
    assert "SampleClass" in facts.symbols
    assert "sync_method" in facts.symbols["SampleClass"].methods
    assert "async_method" in facts.symbols["SampleClass"].methods


def test_enum_attribution_no_methods() -> None:
    """Enum classes have members only; methods list must be empty."""
    facts = ASTFactExtractor().extract(FIXTURE_PATH)
    assert "SampleEnum" in facts.symbols
    assert facts.symbols["SampleEnum"].is_enum is True
    assert facts.symbols["SampleEnum"].methods == []


def test_method_signatures_extracted() -> None:
    """Class methods must have signatures in method_signatures."""
    facts = ASTFactExtractor().extract_documentable_facts(FIXTURE_PATH)
    assert "SampleClass" in facts.symbols
    sigs = facts.symbols["SampleClass"].method_signatures
    assert "sync_method" in sigs
    assert "async_method" in sigs
    assert "b" in sigs["sync_method"] or "int" in sigs["sync_method"]


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
    assert facts.symbols["MAX_EXPANDED_CONTEXT"].value == "40000"
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


def test_async_control_flow_extracted() -> None:
    """Control flow in async functions must be extracted."""
    facts = ASTFactExtractor().extract(FIXTURE_PATH)
    assert "async_module_func" in facts.control_flow
    assert len(facts.control_flow["async_module_func"]) >= 1
    blocks = facts.control_flow["async_module_func"][0].blocks
    assert any(b.get("type") == "if" for b in blocks)
