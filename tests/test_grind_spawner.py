"""
Tests for grind_spawner.py - CLI tool for spawning parallel Claude sessions.
Tests GrindSession initialization, prompt formatting, task loading, and subprocess mocking.
"""

import json
import pytest
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from grind_spawner import GrindSession, get_total_spent, GRIND_PROMPT_TEMPLATE


class TestGrindSessionInitialization:
    """Test GrindSession class initialization."""

    def test_init_sets_all_attributes(self):
        """Test that __init__ correctly sets all instance attributes."""
        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test/workspace"),
            task="Fix bugs"
        )

        assert session.session_id == 1
        assert session.model == "haiku"
        assert session.budget == 0.10
        assert session.workspace == Path("/test/workspace")
        assert session.task == "Fix bugs"
        assert session.runs == 0
        assert session.total_cost == 0.0
        assert session.running is True
        assert session.max_total_cost is None

    def test_init_with_max_total_cost(self):
        """Test that max_total_cost is stored when provided."""
        session = GrindSession(
            session_id=2,
            model="opus",
            budget=0.50,
            workspace=Path("/test"),
            task="Refactor code",
            max_total_cost=10.0
        )

        assert session.max_total_cost == 10.0

    def test_init_defaults_max_total_cost_to_none(self):
        """Test that max_total_cost defaults to None when not provided."""
        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task="Test task"
        )

        assert session.max_total_cost is None


class TestGetPrompt:
    """Test GrindSession.get_prompt() method."""

    def test_get_prompt_format(self):
        """Test that get_prompt() returns correctly formatted prompt."""
        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/workspace"),
            task="Add logging"
        )

        prompt = session.get_prompt()

        # Check that prompt contains expected elements
        assert "WORKSPACE:" in prompt
        assert "workspace" in prompt
        assert "TASK (execute step by step):" in prompt
        assert "Add logging" in prompt
        assert "EXECUTE NOW." in prompt

    def test_get_prompt_includes_workspace(self):
        """Test that get_prompt() includes correct workspace path."""
        workspace_path = Path("D:/some/repo")
        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=workspace_path,
            task="Task content"
        )

        prompt = session.get_prompt()
        assert f"WORKSPACE: {workspace_path}" in prompt

    def test_get_prompt_includes_task(self):
        """Test that get_prompt() includes the task description."""
        task_text = "Fix all UI bugs in the login form"
        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task=task_text
        )

        prompt = session.get_prompt()
        assert task_text in prompt

    def test_get_prompt_includes_execution_rules(self):
        """Test that prompt includes the execution rules."""
        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task="Test task"
        )

        prompt = session.get_prompt()

        # Check for key rules
        assert "Follow the steps EXACTLY" in prompt
        assert "Be FAST" in prompt
        assert "When done, output a 2-3 sentence summary" in prompt


class TestRunOnce:
    """Test GrindSession.run_once() method with mocked subprocess."""

    @patch('grind_spawner.subprocess.run')
    @patch('grind_spawner.LOGS_DIR')
    def test_run_once_success(self, mock_logs_dir, mock_subprocess_run):
        """Test successful run_once execution."""
        # Setup mocks
        mock_logs_dir.mkdir = Mock()
        mock_log_file = Mock()
        mock_logs_dir.__truediv__ = Mock(return_value=mock_log_file)

        mock_subprocess_run.return_value = Mock(
            returncode=0,
            stdout='{"result": "success"}',
            stderr=None
        )

        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task="Test task"
        )

        result = session.run_once()

        assert result["session_id"] == 1
        assert result["run"] == 1
        assert result["returncode"] == 0
        assert session.runs == 1
        mock_subprocess_run.assert_called_once()

    @patch('grind_spawner.subprocess.run')
    @patch('grind_spawner.LOGS_DIR')
    def test_run_once_increments_runs(self, mock_logs_dir, mock_subprocess_run):
        """Test that run_once increments the runs counter."""
        mock_logs_dir.mkdir = Mock()
        mock_log_file = Mock()
        mock_logs_dir.__truediv__ = Mock(return_value=mock_log_file)

        mock_subprocess_run.return_value = Mock(
            returncode=0,
            stdout='{}',
            stderr=None
        )

        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task="Task"
        )

        assert session.runs == 0
        session.run_once()
        assert session.runs == 1
        session.run_once()
        assert session.runs == 2

    @patch('grind_spawner.subprocess.run')
    @patch('grind_spawner.LOGS_DIR')
    def test_run_once_handles_timeout(self, mock_logs_dir, mock_subprocess_run):
        """Test that run_once handles subprocess timeout."""
        mock_logs_dir.mkdir = Mock()
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired("cmd", 600)

        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task="Task"
        )

        result = session.run_once()

        assert "error" in result
        assert result["error"] == "timeout"

    @patch('grind_spawner.subprocess.run')
    @patch('grind_spawner.LOGS_DIR')
    def test_run_once_handles_exception(self, mock_logs_dir, mock_subprocess_run):
        """Test that run_once handles general exceptions."""
        mock_logs_dir.mkdir = Mock()
        mock_subprocess_run.side_effect = RuntimeError("Test error")

        session = GrindSession(
            session_id=1,
            model="haiku",
            budget=0.10,
            workspace=Path("/test"),
            task="Task"
        )

        result = session.run_once()

        assert "error" in result
        assert "Test error" in result["error"]

    @patch('grind_spawner.subprocess.run')
    @patch('grind_spawner.LOGS_DIR')
    def test_run_once_builds_correct_command(self, mock_logs_dir, mock_subprocess_run):
        """Test that run_once builds the correct claude command."""
        mock_logs_dir.mkdir = Mock()
        mock_log_file = Mock()
        mock_logs_dir.__truediv__ = Mock(return_value=mock_log_file)

        mock_subprocess_run.return_value = Mock(
            returncode=0,
            stdout='{}',
            stderr=None
        )

        session = GrindSession(
            session_id=1,
            model="opus",
            budget=0.10,
            workspace=Path("/test"),
            task="Task"
        )

        session.run_once()

        # Verify subprocess was called with correct command structure
        call_args = mock_subprocess_run.call_args
        cmd = call_args[1]["cmd"] if "cmd" in call_args[1] else call_args[0][0]

        assert "claude" in cmd
        assert "-p" in cmd
        assert "--model" in cmd
        assert "opus" in cmd
        assert "--output-format" in cmd
        assert "json" in cmd


class TestTaskLoading:
    """Test task loading from grind_tasks.json."""

    def test_load_tasks_from_json(self, tmp_path):
        """Test loading tasks from a JSON file."""
        tasks_file = tmp_path / "grind_tasks.json"
        tasks_data = [
            {"task": "Task 1", "budget": 0.10, "model": "haiku"},
            {"task": "Task 2", "budget": 0.50, "model": "opus"}
        ]
        tasks_file.write_text(json.dumps(tasks_data))

        with open(tasks_file) as f:
            loaded = json.load(f)

        assert len(loaded) == 2
        assert loaded[0]["task"] == "Task 1"
        assert loaded[1]["budget"] == 0.50

    def test_task_structure_validity(self, tmp_path):
        """Test that loaded tasks have required fields."""
        tasks_file = tmp_path / "grind_tasks.json"
        tasks_data = [
            {
                "task": "Fix bugs",
                "budget": 0.25,
                "model": "sonnet",
                "workspace": "/workspace"
            }
        ]
        tasks_file.write_text(json.dumps(tasks_data))

        with open(tasks_file) as f:
            tasks = json.load(f)

        task = tasks[0]
        assert "task" in task
        assert "budget" in task
        assert "model" in task


class TestGetTotalSpent:
    """Test get_total_spent() function."""

    @patch('grind_spawner.LOGS_DIR')
    def test_get_total_spent_no_logs(self, mock_logs_dir):
        """Test get_total_spent with no log files."""
        mock_logs_dir.exists.return_value = False

        total = get_total_spent()

        assert total == 0.0

    @patch('grind_spawner.LOGS_DIR')
    def test_get_total_spent_with_cost_logs(self, mock_logs_dir):
        """Test get_total_spent with logs containing cost data."""
        mock_log1 = Mock()
        mock_log1.read_text.return_value = '{"cost": 0.10}'

        mock_log2 = Mock()
        mock_log2.read_text.return_value = '{"cost": 0.25}'

        mock_logs_dir.exists.return_value = True
        mock_logs_dir.glob.return_value = [mock_log1, mock_log2]

        total = get_total_spent()

        assert total == 0.35

    @patch('grind_spawner.LOGS_DIR')
    def test_get_total_spent_handles_invalid_json(self, mock_logs_dir):
        """Test that get_total_spent handles invalid JSON gracefully."""
        mock_log1 = Mock()
        mock_log1.read_text.return_value = 'invalid json'

        mock_logs_dir.exists.return_value = True
        mock_logs_dir.glob.return_value = [mock_log1]

        # Should not raise, just return 0.0
        total = get_total_spent()

        assert total == 0.0

    @patch('grind_spawner.LOGS_DIR')
    def test_get_total_spent_skips_logs_without_cost(self, mock_logs_dir):
        """Test that get_total_spent skips logs without cost field."""
        mock_log1 = Mock()
        mock_log1.read_text.return_value = '{"result": "success"}'

        mock_log2 = Mock()
        mock_log2.read_text.return_value = '{"cost": 0.15}'

        mock_logs_dir.exists.return_value = True
        mock_logs_dir.glob.return_value = [mock_log1, mock_log2]

        total = get_total_spent()

        assert total == 0.15


class TestGrindPromptTemplate:
    """Test the GRIND_PROMPT_TEMPLATE constant."""

    def test_template_has_required_placeholders(self):
        """Test that template has required format placeholders."""
        assert "{workspace}" in GRIND_PROMPT_TEMPLATE
        assert "{task}" in GRIND_PROMPT_TEMPLATE

    def test_template_formatting(self):
        """Test that template can be formatted with required values."""
        formatted = GRIND_PROMPT_TEMPLATE.format(
            workspace="/test",
            task="Test task"
        )

        assert "/test" in formatted
        assert "Test task" in formatted
        assert "{workspace}" not in formatted
        assert "{task}" not in formatted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
