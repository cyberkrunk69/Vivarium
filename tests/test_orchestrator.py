"""
Unit tests for orchestrator.py - Task Management and Worker Spawning
"""

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import orchestrator


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace with required structure."""
    locks_dir = tmp_path / "task_locks"
    locks_dir.mkdir()

    queue_file = tmp_path / "queue.json"
    execution_log = tmp_path / "execution_log.json"

    with patch.object(orchestrator, 'WORKSPACE', tmp_path), \
         patch.object(orchestrator, 'QUEUE_FILE', queue_file), \
         patch.object(orchestrator, 'LOCKS_DIR', locks_dir), \
         patch.object(orchestrator, 'EXECUTION_LOG', execution_log):
        yield {
            'workspace': tmp_path,
            'locks_dir': locks_dir,
            'queue_file': queue_file,
            'execution_log': execution_log
        }


class TestReadWriteJson:
    """Tests for read_json and write_json functions."""

    def test_read_json_empty_when_no_file(self, temp_workspace):
        """Should return empty dict when file doesn't exist."""
        result = orchestrator.read_json(temp_workspace['queue_file'])
        assert result == {}

    def test_read_json_parses_file(self, temp_workspace):
        """Should parse existing JSON file."""
        data = {"key": "value", "number": 42}
        temp_workspace['queue_file'].write_text(json.dumps(data))

        result = orchestrator.read_json(temp_workspace['queue_file'])
        assert result == data

    def test_write_json_creates_file(self, temp_workspace):
        """Should create file with JSON content."""
        data = {"tasks": [{"id": "task_001"}]}
        orchestrator.write_json(temp_workspace['queue_file'], data)

        content = json.loads(temp_workspace['queue_file'].read_text())
        assert content == data

    def test_write_json_pretty_formatted(self, temp_workspace):
        """Should write with indentation."""
        data = {"key": "value"}
        orchestrator.write_json(temp_workspace['queue_file'], data)

        content = temp_workspace['queue_file'].read_text()
        assert "\n" in content  # Has newlines from formatting


class TestSpawnWorker:
    """Tests for spawn_worker function."""

    def test_returns_worker_result(self, temp_workspace):
        """Should return dict with worker_id, stdout, stderr, returncode."""
        mock_result = MagicMock()
        mock_result.stdout = "Worker output"
        mock_result.stderr = ""
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            result = orchestrator.spawn_worker(5)

        assert result["worker_id"] == 5
        assert result["stdout"] == "Worker output"
        assert result["stderr"] == ""
        assert result["returncode"] == 0

    def test_captures_worker_errors(self, temp_workspace):
        """Should capture stderr from failed workers."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Error: connection refused"
        mock_result.returncode = 1

        with patch('subprocess.run', return_value=mock_result):
            result = orchestrator.spawn_worker(0)

        assert result["returncode"] == 1
        assert "Error" in result["stderr"]


class TestAddTask:
    """Tests for add_task function."""

    def test_adds_task_to_empty_queue(self, temp_workspace):
        """Should create queue and add task."""
        orchestrator.add_task("task_001", "grind")

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert len(queue["tasks"]) == 1
        assert queue["tasks"][0]["id"] == "task_001"
        assert queue["tasks"][0]["type"] == "grind"
        assert queue["api_endpoint"] == "http://127.0.0.1:8420"

    def test_adds_task_with_budget(self, temp_workspace):
        """Should set budget parameters."""
        orchestrator.add_task("task_001", "grind", min_budget=0.10, max_budget=0.20)

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        task = queue["tasks"][0]
        assert task["min_budget"] == 0.10
        assert task["max_budget"] == 0.20

    def test_adds_task_with_intensity(self, temp_workspace):
        """Should set intensity parameter."""
        orchestrator.add_task("task_001", "grind", intensity="high")

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert queue["tasks"][0]["intensity"] == "high"

    def test_adds_task_with_dependencies(self, temp_workspace):
        """Should set dependencies."""
        orchestrator.add_task("task_002", "grind", depends_on=["task_001"])

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert queue["tasks"][0]["depends_on"] == ["task_001"]

    def test_appends_to_existing_queue(self, temp_workspace):
        """Should append to existing tasks."""
        # Add first task
        orchestrator.add_task("task_001", "grind")
        # Add second task
        orchestrator.add_task("task_002", "grind")

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert len(queue["tasks"]) == 2
        assert queue["tasks"][0]["id"] == "task_001"
        assert queue["tasks"][1]["id"] == "task_002"

    def test_task_marked_parallel_safe(self, temp_workspace):
        """Tasks should be marked as parallel_safe."""
        orchestrator.add_task("task_001", "grind")

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert queue["tasks"][0]["parallel_safe"] is True


class TestClearAll:
    """Tests for clear_all function."""

    def test_clears_queue(self, temp_workspace):
        """Should reset queue to empty state."""
        # Setup with tasks
        queue = {"tasks": [{"id": "task_001"}]}
        orchestrator.write_json(temp_workspace['queue_file'], queue)

        orchestrator.clear_all()

        new_queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert new_queue["tasks"] == []
        assert new_queue["api_endpoint"] == "http://127.0.0.1:8420"

    def test_clears_execution_log(self, temp_workspace):
        """Should reset execution log."""
        log = {"tasks": {"task_001": {"status": "completed"}}}
        orchestrator.write_json(temp_workspace['execution_log'], log)

        orchestrator.clear_all()

        new_log = orchestrator.read_json(temp_workspace['execution_log'])
        assert new_log["tasks"] == {}

    def test_removes_lock_files(self, temp_workspace):
        """Should remove all lock files."""
        # Create some locks
        (temp_workspace['locks_dir'] / "task_001.lock").write_text("{}")
        (temp_workspace['locks_dir'] / "task_002.lock").write_text("{}")

        orchestrator.clear_all()

        locks = list(temp_workspace['locks_dir'].glob("*.lock"))
        assert len(locks) == 0

    def test_handles_no_locks_dir(self, temp_workspace):
        """Should not fail if locks dir doesn't exist."""
        temp_workspace['locks_dir'].rmdir()

        orchestrator.clear_all()  # Should not raise


class TestShowStatus:
    """Tests for show_status function."""

    def test_displays_summary(self, temp_workspace, capsys):
        """Should print status summary."""
        log = {
            "swarm_summary": {
                "total_tasks": 4,
                "completed": 2,
                "in_progress": 1,
                "pending": 0,
                "failed": 1
            },
            "tasks": {
                "task_001": {"status": "completed"},
                "task_002": {"status": "completed"},
                "task_003": {"status": "in_progress"},
                "task_004": {"status": "failed", "errors": "API timeout"}
            }
        }
        orchestrator.write_json(temp_workspace['execution_log'], log)
        orchestrator.write_json(temp_workspace['queue_file'], {"tasks": []})

        orchestrator.show_status()

        output = capsys.readouterr().out
        assert "Total tasks: 4" in output
        assert "Completed:   2" in output
        assert "Failed:      1" in output

    def test_shows_failed_tasks(self, temp_workspace, capsys):
        """Should list failed task errors."""
        log = {
            "swarm_summary": {"failed": 1},
            "tasks": {
                "task_001": {"status": "failed", "errors": "Connection timeout"}
            }
        }
        orchestrator.write_json(temp_workspace['execution_log'], log)
        orchestrator.write_json(temp_workspace['queue_file'], {"tasks": []})

        orchestrator.show_status()

        output = capsys.readouterr().out
        assert "Connection timeout" in output

    def test_shows_active_locks(self, temp_workspace, capsys):
        """Should list active lock files."""
        orchestrator.write_json(temp_workspace['execution_log'], {"swarm_summary": {}, "tasks": {}})
        orchestrator.write_json(temp_workspace['queue_file'], {"tasks": []})
        (temp_workspace['locks_dir'] / "task_001.lock").write_text("{}")

        orchestrator.show_status()

        output = capsys.readouterr().out
        assert "Active locks: 1" in output
        assert "task_001.lock" in output


class TestStartOrchestrator:
    """Tests for start_orchestrator function."""

    def test_creates_locks_dir(self, temp_workspace):
        """Should ensure locks directory exists."""
        temp_workspace['locks_dir'].rmdir()
        orchestrator.write_json(temp_workspace['queue_file'], {"tasks": []})

        orchestrator.start_orchestrator(num_workers=1)

        assert temp_workspace['locks_dir'].exists()

    def test_initializes_execution_log(self, temp_workspace):
        """Should create execution log if not exists."""
        orchestrator.write_json(temp_workspace['queue_file'], {"tasks": []})

        orchestrator.start_orchestrator(num_workers=1)

        log = orchestrator.read_json(temp_workspace['execution_log'])
        assert "version" in log
        assert "start_time" in log

    def test_exits_with_no_tasks(self, temp_workspace, capsys):
        """Should exit early if no tasks in queue."""
        orchestrator.write_json(temp_workspace['queue_file'], {"tasks": []})

        orchestrator.start_orchestrator(num_workers=2)

        output = capsys.readouterr().out
        assert "No tasks in queue" in output

    def test_spawns_workers(self, temp_workspace):
        """Should spawn specified number of workers."""
        orchestrator.write_json(temp_workspace['queue_file'], {
            "tasks": [{"id": "task_001"}]
        })

        # Test uses ThreadPoolExecutor instead for easier mocking
        from concurrent.futures import ThreadPoolExecutor, Future

        spawn_calls = []
        def mock_spawn(worker_id):
            spawn_calls.append(worker_id)
            return {"worker_id": worker_id, "stdout": "done", "stderr": "", "returncode": 0}

        with patch.object(orchestrator, 'spawn_worker', side_effect=mock_spawn):
            with patch('orchestrator.ProcessPoolExecutor', ThreadPoolExecutor):
                orchestrator.start_orchestrator(num_workers=3)

        # Should have spawned 3 workers
        assert len(spawn_calls) == 3


class TestQueueManagement:
    """Integration tests for queue management."""

    def test_full_queue_lifecycle(self, temp_workspace):
        """Test adding tasks, checking status, and clearing."""
        # Start empty
        assert not temp_workspace['queue_file'].exists()

        # Add tasks
        orchestrator.add_task("task_001", "grind", min_budget=0.05)
        orchestrator.add_task("task_002", "grind", depends_on=["task_001"])

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert len(queue["tasks"]) == 2

        # Clear all
        orchestrator.clear_all()

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        assert len(queue["tasks"]) == 0

    def test_task_defaults(self, temp_workspace):
        """Test that tasks get proper default values."""
        orchestrator.add_task("task_001", "grind")

        queue = orchestrator.read_json(temp_workspace['queue_file'])
        task = queue["tasks"][0]

        assert task["min_budget"] == 0.05
        assert task["max_budget"] == 0.10
        assert task["intensity"] == "medium"
        assert task["status"] == "pending"
        assert task["depends_on"] == []
        assert task["parallel_safe"] is True
