"""Targeted unit tests for orphaned code paths in control_panel_app.
Mocks external dependencies (db, redis, file I/O) where needed."""
from __future__ import annotations

import os
import pytest

from vivarium.runtime.control_panel_app import (
    _safe_int_env,
    _safe_float_env,
    _clamp_int,
    _parse_csv_items,
    _mask_secret,
)


class TestSafeIntEnv:
    """_safe_int_env: parse int from env with fallback."""

    def test_env_unset_returns_default(self, monkeypatch):
        monkeypatch.delenv("VIVARIUM_TEST_INT_XYZ", raising=False)
        assert _safe_int_env("VIVARIUM_TEST_INT_XYZ", 42) == 42

    def test_env_valid_int_returns_parsed(self, monkeypatch):
        monkeypatch.setenv("VIVARIUM_TEST_INT_XYZ", "999")
        assert _safe_int_env("VIVARIUM_TEST_INT_XYZ", 42) == 999

    def test_env_invalid_returns_default(self, monkeypatch):
        monkeypatch.setenv("VIVARIUM_TEST_INT_XYZ", "not_a_number")
        assert _safe_int_env("VIVARIUM_TEST_INT_XYZ", 42) == 42


class TestSafeFloatEnv:
    """_safe_float_env: parse float from env with fallback."""

    def test_env_unset_returns_default(self, monkeypatch):
        monkeypatch.delenv("VIVARIUM_TEST_FLOAT_XYZ", raising=False)
        assert _safe_float_env("VIVARIUM_TEST_FLOAT_XYZ", 3.14) == 3.14

    def test_env_valid_float_returns_parsed(self, monkeypatch):
        monkeypatch.setenv("VIVARIUM_TEST_FLOAT_XYZ", "2.718")
        assert _safe_float_env("VIVARIUM_TEST_FLOAT_XYZ", 3.14) == 2.718

    def test_env_invalid_returns_default(self, monkeypatch):
        monkeypatch.setenv("VIVARIUM_TEST_FLOAT_XYZ", "nope")
        assert _safe_float_env("VIVARIUM_TEST_FLOAT_XYZ", 3.14) == 3.14


class TestClampInt:
    """_clamp_int: clamp value to [minimum, maximum]."""

    def test_value_in_range_unchanged(self):
        assert _clamp_int(5, 1, 10) == 5

    def test_value_below_min_returns_min(self):
        assert _clamp_int(-3, 0, 10) == 0

    def test_value_above_max_returns_max(self):
        assert _clamp_int(99, 0, 10) == 10

    def test_float_input_coerced_to_int(self):
        assert _clamp_int(5.7, 1, 10) == 5


class TestParseCsvItems:
    """_parse_csv_items: parse comma-separated items with dedup and limits."""

    def test_empty_input_returns_empty_list(self):
        assert _parse_csv_items("") == []
        assert _parse_csv_items(None) == []

    def test_single_item(self):
        assert _parse_csv_items("a") == ["a"]

    def test_multiple_items_deduped(self):
        assert _parse_csv_items("a, b, a, c") == ["a", "b", "c"]

    def test_max_items_respected(self):
        result = _parse_csv_items("1,2,3,4,5,6,7,8,9,10,11", max_items=5)
        assert result == ["1", "2", "3", "4", "5"]

    def test_long_item_truncated(self):
        long_val = "x" * 3000
        result = _parse_csv_items(long_val, max_len=100)
        assert len(result) == 1
        assert len(result[0]) == 100


class TestMaskSecret:
    """_mask_secret: mask sensitive strings for display."""

    def test_short_secret_masked_as_stars(self):
        assert _mask_secret("short") == "****"
        assert _mask_secret("") == "****"

    def test_long_secret_shows_first_and_last_four(self):
        assert _mask_secret("abcdefghijklmnop") == "abcd...mnop"

    def test_none_handled(self):
        assert _mask_secret(None) == "****"
