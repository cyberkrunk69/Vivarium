"""
TICKET-89: Tests for GAP/FALLBACK placeholder validation.
"""

import pytest
from pathlib import Path

from vivarium.scout.doc_generation import (
    validate_no_placeholders,
    validate_content_for_placeholders,
)


def test_validate_no_placeholders_clean():
    """Clean content returns (True, [])."""
    ok, found = validate_no_placeholders("Normal doc content.", "foo.md")
    assert ok is True
    assert found == []


def test_validate_no_placeholders_fallback():
    """[FALLBACK] is detected."""
    ok, found = validate_no_placeholders("[FALLBACK]\n\nAuto content", "foo.md")
    assert ok is False
    assert "[FALLBACK]" in found


def test_validate_no_placeholders_gap():
    """[GAP] is detected."""
    ok, found = validate_no_placeholders("Some text [GAP] more text", "bar.tldr.md")
    assert ok is False
    assert "[GAP]" in found


def test_validate_no_placeholders_placeholder():
    """[PLACEHOLDER] is detected."""
    ok, found = validate_no_placeholders("x [PLACEHOLDER] y", "baz.md")
    assert ok is False
    assert "[PLACEHOLDER]" in found


def test_validate_no_placeholders_multiple():
    """Multiple markers are all reported."""
    ok, found = validate_no_placeholders(
        "[FALLBACK] and [GAP] here",
        "multi.md",
    )
    assert ok is False
    assert "[FALLBACK]" in found
    assert "[GAP]" in found


def test_validate_content_for_placeholders(tmp_path):
    """validate_content_for_placeholders scans .tldr.md files."""
    docs = tmp_path / ".docs"
    docs.mkdir()
    clean = docs / "clean.tldr.md"
    clean.write_text("Clean content", encoding="utf-8")
    dirty = docs / "dirty.tldr.md"
    dirty.write_text("Has [GAP] here", encoding="utf-8")

    all_clean, violations = validate_content_for_placeholders(tmp_path, recursive=True)
    assert all_clean is False
    assert len(violations) == 1
    assert "dirty.tldr.md" in violations[0][0]
    assert "[GAP]" in violations[0][1]


def test_validate_content_for_placeholders_all_clean(tmp_path):
    """All clean returns (True, [])."""
    docs = tmp_path / ".docs"
    docs.mkdir()
    (docs / "a.tldr.md").write_text("Clean", encoding="utf-8")

    all_clean, violations = validate_content_for_placeholders(tmp_path, recursive=True)
    assert all_clean is True
    assert violations == []
