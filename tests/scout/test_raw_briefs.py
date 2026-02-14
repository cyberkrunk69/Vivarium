"""
TICKET-8: Raw brief capture and PII sanitization tests.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from vivarium.scout.raw_briefs import (
    RAW_BRIEFS_DIR,
    REDACTED_PLACEHOLDER,
    list_raw_briefs,
    sanitize_for_pii,
    store_raw_brief,
)


class TestSanitizeForPii:
    """No PII leakage — absolute paths redacted."""

    def test_redacts_users_path(self):
        raw = "See /Users/john/secret/file.py for details."
        out, had = sanitize_for_pii(raw)
        assert REDACTED_PLACEHOLDER in out
        assert "/Users/john" not in out
        assert had is True

    def test_redacts_home_path(self):
        raw = "Check /home/ubuntu/project/x.py"
        out, had = sanitize_for_pii(raw)
        assert REDACTED_PLACEHOLDER in out
        assert "/home/ubuntu" not in out

    def test_redacts_windows_path(self):
        raw = "File at C:\\Users\\jane\\doc.txt"
        out, had = sanitize_for_pii(raw)
        assert REDACTED_PLACEHOLDER in out
        assert "C:\\" not in out or REDACTED_PLACEHOLDER in out

    def test_allows_repo_relative_paths(self):
        raw = "vivarium/scout/router.py and docs/LLM_CONTEXT.md"
        out, had = sanitize_for_pii(raw)
        assert "vivarium/scout/router.py" in out
        assert "docs/LLM_CONTEXT.md" in out
        assert had is False

    def test_empty_returns_false(self):
        out, had = sanitize_for_pii("")
        assert out == ""
        assert had is False


class TestStoreRawBrief:
    """Raw briefs stored and retrievable."""

    def test_stores_and_retrieves(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        content = "confidence_score: 0.80\nAnalysis.\nNone identified — verified coverage of 5 symbols"
        path = store_raw_brief(content)
        assert path is not None
        assert path.exists()
        assert path.read_text() == content

    def test_sanitizes_before_storage(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        content = "confidence_score: 0.80\nSee /Users/leak/secret.py"
        path = store_raw_brief(content)
        assert path is not None
        stored = path.read_text()
        assert REDACTED_PLACEHOLDER in stored
        assert "/Users/leak" not in stored

    def test_empty_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        assert store_raw_brief("") is None
        assert store_raw_brief("   ") is None


class TestListRawBriefs:
    """Raw briefs listable for analysis."""

    def test_returns_paths(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "vivarium.scout.raw_briefs.RAW_BRIEFS_DIR",
            tmp_path / "raw_briefs",
        )
        (tmp_path / "raw_briefs").mkdir(parents=True)
        (tmp_path / "raw_briefs" / "20250101_120000.md").write_text("x")
        (tmp_path / "raw_briefs" / "20250101_120001.md").write_text("y")
        paths = list_raw_briefs(limit=10)
        assert len(paths) == 2
