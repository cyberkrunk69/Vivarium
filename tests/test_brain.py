"""Tests for brain.py - Minimal orchestrator for Black Swarm."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import brain


class TestGrindFunction:
    """Tests for grind() function with mocked HTTP requests."""

    @patch('brain.requests.post')
    @patch('brain.load_runs')
    @patch('brain.save_runs')
    def test_grind_success(self, mock_save, mock_load, mock_post):
        """Test successful grind with valid budget."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "completed",
            "tokens_used": 1500,
            "cost": 0.05
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        mock_load.return_value = []

        with patch('builtins.print'):
            result = brain.grind(0.10)

        assert result is not None
        assert result["status"] == "completed"
        mock_post.assert_called_once()
        mock_save.assert_called_once()

    @patch('brain.requests.post')
    def test_grind_connection_failure(self, mock_post):
        """Test grind handles connection failure gracefully."""
        mock_post.side_effect = ConnectionError("Cannot connect to swarm")

        with patch('builtins.print'):
            result = brain.grind(0.10)

        assert result is None
        mock_post.assert_called_once()

    @patch('brain.requests.post')
    def test_grind_timeout(self, mock_post):
        """Test grind handles timeout error."""
        import requests
        mock_post.side_effect = requests.Timeout("Request timeout")

        with patch('builtins.print'):
            result = brain.grind(0.10)

        assert result is None

    @patch('brain.requests.post')
    @patch('brain.load_runs')
    @patch('brain.save_runs')
    def test_grind_logs_result(self, mock_save, mock_load, mock_post):
        """Test grind logs the result to runs.json."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        mock_load.return_value = []

        with patch('builtins.print'):
            brain.grind(0.50)

        # Verify save_runs was called with updated data
        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][0]
        assert len(saved_data) == 1
        assert saved_data[0]["budget"] == 0.50
        assert saved_data[0]["status"] == 200

    @patch('brain.requests.post')
    def test_grind_http_error(self, mock_post):
        """Test grind handles HTTP error response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "Invalid budget"}
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with patch('builtins.print'):
            result = brain.grind(0.10)

        # Should still return the response even on HTTP error
        assert result is not None


class TestHealthFunction:
    """Tests for health() function."""

    @patch('brain.requests.get')
    def test_health_success(self, mock_get):
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "healthy",
            "workers": 5,
            "uptime": 3600
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch('builtins.print'):
            result = brain.health()

        assert result is not None
        assert result["status"] == "healthy"
        mock_get.assert_called_once()

    @patch('brain.requests.get')
    def test_health_connection_failure(self, mock_get):
        """Test health check handles connection failure."""
        mock_get.side_effect = ConnectionError("Cannot connect to swarm")

        with patch('builtins.print'):
            result = brain.health()

        assert result is None

    @patch('brain.requests.get')
    def test_health_timeout(self, mock_get):
        """Test health check handles timeout."""
        import requests
        mock_get.side_effect = requests.Timeout("Health check timeout")

        with patch('builtins.print'):
            result = brain.health()

        assert result is None

    @patch('brain.requests.get')
    def test_health_uses_correct_url(self, mock_get):
        """Test health check uses correct endpoint."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_get.return_value = mock_response

        with patch('builtins.print'):
            brain.health()

        # Verify correct URL and timeout
        call_args = mock_get.call_args
        assert "/health" in call_args[0][0]
        assert call_args[1]["timeout"] == 10


class TestLoadSaveRuns:
    """Tests for load_runs() and save_runs() functions."""

    def test_load_runs_file_not_found(self):
        """Test load_runs returns empty list when file doesn't exist."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = brain.load_runs()
        assert result == []

    def test_load_runs_json_decode_error(self):
        """Test load_runs returns empty list on JSON error."""
        with patch('builtins.open', mock_open(read_data="invalid json")):
            with patch('json.load', side_effect=json.JSONDecodeError("", "", 0)):
                result = brain.load_runs()
        assert result == []

    def test_load_runs_success(self):
        """Test load_runs successfully loads valid JSON."""
        test_data = [
            {"timestamp": "2026-02-03T10:00:00", "budget": 0.10},
            {"timestamp": "2026-02-03T11:00:00", "budget": 0.20}
        ]
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            with patch('json.load', return_value=test_data):
                result = brain.load_runs()
        assert len(result) == 2

    def test_save_runs_writes_json(self):
        """Test save_runs writes JSON to file."""
        test_data = [{"timestamp": "2026-02-03T10:00:00", "budget": 0.10}]

        m = mock_open()
        with patch('builtins.open', m):
            with patch('json.dump') as mock_dump:
                brain.save_runs(test_data)

        # Verify file was opened for writing
        m.assert_called_once_with(brain.RUNS_FILE, "w")
        # Verify json.dump was called with correct data
        mock_dump.assert_called_once()


class TestArgumentParsing:
    """Tests for CLI argument parsing."""

    def test_grind_command_with_default_budget(self):
        """Test grind command uses default budget."""
        test_args = ["brain.py", "grind"]
        with patch('sys.argv', test_args):
            with patch('brain.grind') as mock_grind:
                brain.main()
        mock_grind.assert_called_once_with(0.10)

    def test_grind_command_with_custom_budget(self):
        """Test grind command with custom budget argument."""
        test_args = ["brain.py", "grind", "--budget", "0.50"]
        with patch('sys.argv', test_args):
            with patch('brain.grind') as mock_grind:
                brain.main()
        mock_grind.assert_called_once_with(0.50)

    def test_health_command(self):
        """Test health command parsing and execution."""
        test_args = ["brain.py", "health"]
        with patch('sys.argv', test_args):
            with patch('brain.health') as mock_health:
                brain.main()
        mock_health.assert_called_once()

    def test_no_command_fails(self):
        """Test that missing command raises error."""
        test_args = ["brain.py"]
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                brain.main()

    def test_invalid_command_fails(self):
        """Test that invalid command raises error."""
        test_args = ["brain.py", "invalid"]
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                brain.main()

    def test_invalid_budget_format(self):
        """Test that invalid budget format raises error."""
        test_args = ["brain.py", "grind", "--budget", "not_a_number"]
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                brain.main()

    def test_negative_budget(self):
        """Test parsing allows negative budget (validation may occur elsewhere)."""
        test_args = ["brain.py", "grind", "--budget", "-0.10"]
        with patch('sys.argv', test_args):
            with patch('brain.grind') as mock_grind:
                brain.main()
        mock_grind.assert_called_once_with(-0.10)


class TestErrorHandling:
    """Tests for error handling in various scenarios."""

    @patch('brain.requests.post')
    def test_grind_generic_exception(self, mock_post):
        """Test grind handles unexpected exceptions."""
        mock_post.side_effect = Exception("Unexpected error")

        with patch('builtins.print'):
            result = brain.grind(0.10)

        assert result is None

    @patch('brain.requests.get')
    def test_health_generic_exception(self, mock_get):
        """Test health handles unexpected exceptions."""
        mock_get.side_effect = Exception("Unexpected error")

        with patch('builtins.print'):
            result = brain.health()

        assert result is None

    @patch('brain.requests.post')
    @patch('brain.load_runs')
    @patch('brain.save_runs')
    def test_grind_save_runs_failure(self, mock_save, mock_load, mock_post):
        """Test grind handles save_runs failure gracefully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        mock_load.return_value = []
        mock_save.side_effect = Exception("Write error")

        with patch('builtins.print'):
            # The outer try-except in grind will catch save_runs failure
            result = brain.grind(0.10)

        # Result is None because exception caught in outer try-except
        assert result is None

    def test_grind_with_zero_budget(self):
        """Test grind handles zero budget."""
        with patch('brain.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {"status": "ok"}
            mock_post.return_value = mock_response

            with patch('brain.load_runs', return_value=[]):
                with patch('brain.save_runs'):
                    with patch('builtins.print'):
                        result = brain.grind(0.0)

            assert result is not None


class TestConfigIntegration:
    """Tests for config module integration."""

    def test_base_url_from_config(self):
        """Test that BASE_URL is set from config."""
        # Verify BASE_URL is not None and has expected format
        assert brain.BASE_URL is not None
        assert isinstance(brain.BASE_URL, str)
        assert "localhost" in brain.BASE_URL or "127.0.0.1" in brain.BASE_URL


class TestIntegration:
    """Integration tests combining multiple components."""

    @patch('brain.requests.post')
    @patch('brain.load_runs')
    @patch('brain.save_runs')
    def test_grind_complete_flow(self, mock_save, mock_load, mock_post):
        """Test complete grind flow from CLI args to result."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "completed",
            "tokens_used": 2000,
            "cost": 0.08
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        mock_load.return_value = [{"previous": "run"}]

        test_args = ["brain.py", "grind", "--budget", "0.25"]
        with patch('sys.argv', test_args):
            with patch('builtins.print'):
                brain.main()

        # Verify post was called with correct budget
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["json"]["budget"] == 0.25

        # Verify runs were saved
        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][0]
        assert len(saved_data) == 2  # previous run + new run
