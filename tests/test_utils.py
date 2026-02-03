"""
Tests for utils.py module.
"""

import json
import pytest
from pathlib import Path
import tempfile
from datetime import datetime
from utils import read_json, write_json, get_timestamp, ensure_dir, format_error


class TestReadJson:
    """Tests for read_json function."""

    def test_read_existing_file(self):
        """Test reading an existing JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.json"
            test_data = {"key": "value", "number": 42}

            with open(test_file, "w") as f:
                json.dump(test_data, f)

            result = read_json(test_file)
            assert result == test_data

    def test_read_missing_file(self):
        """Test reading a non-existent file returns empty dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "nonexistent.json"
            result = read_json(test_file)
            assert result == {}

    def test_read_invalid_json(self):
        """Test reading a file with invalid JSON raises JSONDecodeError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "invalid.json"
            test_file.write_text("not valid json {")

            with pytest.raises(json.JSONDecodeError):
                read_json(test_file)


class TestWriteJson:
    """Tests for write_json function."""

    def test_write_creates_file(self):
        """Test that write_json creates a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "output.json"
            test_data = {"tasks": [], "completed": []}

            write_json(test_file, test_data)

            assert test_file.exists()
            with open(test_file) as f:
                result = json.load(f)
            assert result == test_data

    def test_write_creates_parent_dirs(self):
        """Test that write_json creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "deep" / "nested" / "output.json"
            test_data = {"test": "data"}

            write_json(test_file, test_data)

            assert test_file.exists()
            assert test_file.parent.exists()

    def test_write_proper_formatting(self):
        """Test that write_json uses 2-space indentation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "formatted.json"
            test_data = {"nested": {"key": "value"}}

            write_json(test_file, test_data)

            content = test_file.read_text()
            assert "  " in content  # 2-space indent


class TestGetTimestamp:
    """Tests for get_timestamp function."""

    def test_returns_iso_format(self):
        """Test that get_timestamp returns valid ISO format."""
        timestamp = get_timestamp()
        # Should be ISO 8601 format with timezone
        assert isinstance(timestamp, str)
        assert "T" in timestamp
        assert "+" in timestamp or "Z" in timestamp

    def test_timestamp_parseable(self):
        """Test that returned timestamp can be parsed back."""
        timestamp = get_timestamp()
        parsed = datetime.fromisoformat(timestamp)
        assert isinstance(parsed, datetime)

    def test_timestamp_has_timezone(self):
        """Test that timestamp includes UTC timezone."""
        timestamp = get_timestamp()
        assert "+00:00" in timestamp or "Z" in timestamp


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_creates_directory(self):
        """Test that ensure_dir creates a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "newdir"
            result = ensure_dir(test_dir)

            assert test_dir.exists()
            assert test_dir.is_dir()
            assert result == test_dir

    def test_creates_nested_dirs(self):
        """Test that ensure_dir creates nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "a" / "b" / "c"
            result = ensure_dir(test_dir)

            assert test_dir.exists()
            assert result == test_dir

    def test_idempotent(self):
        """Test that ensure_dir is idempotent (safe to call multiple times)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "testdir"

            result1 = ensure_dir(test_dir)
            result2 = ensure_dir(test_dir)
            result3 = ensure_dir(test_dir)

            assert result1 == result2 == result3
            assert test_dir.exists()


class TestFormatError:
    """Tests for format_error function."""

    def test_format_basic_exception(self):
        """Test formatting a basic exception."""
        exc = ValueError("Something went wrong")
        result = format_error(exc)
        assert result == "ValueError: Something went wrong"

    def test_format_exception_with_empty_message(self):
        """Test formatting an exception with no message."""
        exc = RuntimeError()
        result = format_error(exc)
        assert result == "RuntimeError"

    def test_format_various_exceptions(self):
        """Test formatting various exception types."""
        test_cases = [
            (KeyError("missing_key"), "KeyError: 'missing_key'"),
            (TypeError("wrong type"), "TypeError: wrong type"),
            (FileNotFoundError("file.txt"), "FileNotFoundError: file.txt"),
        ]

        for exc, expected_start in test_cases:
            result = format_error(exc)
            assert expected_start in result or result.startswith(expected_start.split(":")[0])

    def test_format_preserves_exception_info(self):
        """Test that format preserves exception type and message."""
        exc = ConnectionError("Cannot reach host")
        result = format_error(exc)

        assert "ConnectionError" in result
        assert "Cannot reach host" in result
