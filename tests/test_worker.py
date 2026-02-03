"""
Unit tests for worker.py - Lock Protocol, Task Execution, and Queue Management
"""

import json
import os
import tempfile
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# We need to import from parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import worker


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace with required structure."""
    locks_dir = tmp_path / "task_locks"
    locks_dir.mkdir()

    queue_file = tmp_path / "queue.json"
    execution_log = tmp_path / "execution_log.json"

    # Patch workspace paths
    with patch.object(worker, 'WORKSPACE', tmp_path), \
         patch.object(worker, 'QUEUE_FILE', queue_file), \
         patch.object(worker, 'LOCKS_DIR', locks_dir), \
         patch.object(worker, 'EXECUTION_LOG', execution_log):
        yield {
            'workspace': tmp_path,
            'locks_dir': locks_dir,
            'queue_file': queue_file,
            'execution_log': execution_log
        }


class TestTimestamp:
    """Tests for get_timestamp function."""

    def test_get_timestamp_returns_iso_format(self):
        """Timestamp should be ISO 8601 formatted."""
        ts = worker.get_timestamp()
        # Should be parseable as ISO format
        parsed = datetime.fromisoformat(ts)
        assert parsed is not None

    def test_get_timestamp_is_utc(self):
        """Timestamp should be in UTC timezone."""
        ts = worker.get_timestamp()
        parsed = datetime.fromisoformat(ts)
        assert parsed.tzinfo is not None


class TestEnsureDirectories:
    """Tests for ensure_directories function."""

    def test_creates_locks_dir(self, tmp_path):
        """Should create task_locks directory."""
        locks_dir = tmp_path / "task_locks"
        with patch.object(worker, 'LOCKS_DIR', locks_dir):
            worker.ensure_directories()
            assert locks_dir.exists()

    def test_idempotent(self, tmp_path):
        """Should not fail if directory already exists."""
        locks_dir = tmp_path / "task_locks"
        locks_dir.mkdir()
        with patch.object(worker, 'LOCKS_DIR', locks_dir):
            worker.ensure_directories()  # Should not raise
            assert locks_dir.exists()


class TestReadQueue:
    """Tests for read_queue function."""

    def test_returns_empty_when_no_file(self, temp_workspace):
        """Should return empty structure when queue file doesn't exist."""
        result = worker.read_queue()
        assert result == {"tasks": [], "completed": [], "failed": []}

    def test_reads_existing_queue(self, temp_workspace):
        """Should read and parse existing queue file."""
        queue_data = {
            "tasks": [{"id": "task_001", "type": "grind"}],
            "api_endpoint": "http://localhost:8420"
        }
        temp_workspace['queue_file'].write_text(json.dumps(queue_data))

        result = worker.read_queue()
        assert result["tasks"][0]["id"] == "task_001"


class TestReadWriteExecutionLog:
    """Tests for execution log read/write functions."""

    def test_read_returns_empty_when_no_file(self, temp_workspace):
        """Should return empty structure when log doesn't exist."""
        result = worker.read_execution_log()
        assert result == {"version": "1.0", "tasks": {}, "swarm_summary": {}}

    def test_write_updates_swarm_summary(self, temp_workspace):
        """Writing log should auto-calculate swarm summary."""
        log = {
            "version": "1.0",
            "tasks": {
                "task_001": {"status": "completed"},
                "task_002": {"status": "in_progress"},
                "task_003": {"status": "pending"},
                "task_004": {"status": "failed"}
            },
            "swarm_summary": {}
        }

        worker.write_execution_log(log)

        # Read back and check summary
        result = worker.read_execution_log()
        assert result["swarm_summary"]["total_tasks"] == 4
        assert result["swarm_summary"]["completed"] == 1
        assert result["swarm_summary"]["in_progress"] == 1
        assert result["swarm_summary"]["pending"] == 1
        assert result["swarm_summary"]["failed"] == 1


class TestLockPath:
    """Tests for get_lock_path function."""

    def test_returns_correct_path(self, temp_workspace):
        """Should return path in locks directory with .lock extension."""
        result = worker.get_lock_path("task_001")
        assert result == temp_workspace['locks_dir'] / "task_001.lock"


class TestIsLockStale:
    """Tests for is_lock_stale function."""

    def test_nonexistent_lock_not_stale(self, temp_workspace):
        """Non-existent lock file should not be considered stale."""
        lock_path = temp_workspace['locks_dir'] / "nonexistent.lock"
        assert worker.is_lock_stale(lock_path) is False

    def test_fresh_lock_not_stale(self, temp_workspace):
        """Recently created lock should not be stale."""
        lock_path = temp_workspace['locks_dir'] / "fresh.lock"
        lock_data = {
            "worker_id": "test_worker",
            "started_at": worker.get_timestamp(),
            "task_id": "task_001"
        }
        lock_path.write_text(json.dumps(lock_data))

        assert worker.is_lock_stale(lock_path) is False

    def test_old_lock_is_stale(self, temp_workspace):
        """Lock older than timeout should be stale."""
        lock_path = temp_workspace['locks_dir'] / "old.lock"
        old_time = datetime.now(timezone.utc) - timedelta(seconds=worker.LOCK_TIMEOUT_SECONDS + 60)
        lock_data = {
            "worker_id": "test_worker",
            "started_at": old_time.isoformat(),
            "task_id": "task_001"
        }
        lock_path.write_text(json.dumps(lock_data))

        assert worker.is_lock_stale(lock_path) is True

    def test_corrupted_lock_is_stale(self, temp_workspace):
        """Corrupted lock file should be treated as stale."""
        lock_path = temp_workspace['locks_dir'] / "corrupted.lock"
        lock_path.write_text("not valid json {{{")

        assert worker.is_lock_stale(lock_path) is True

    def test_lock_missing_started_at_is_stale(self, temp_workspace):
        """Lock without started_at field should be treated as stale."""
        lock_path = temp_workspace['locks_dir'] / "missing_field.lock"
        lock_path.write_text(json.dumps({"worker_id": "test"}))

        assert worker.is_lock_stale(lock_path) is True


class TestTryAcquireLock:
    """Tests for try_acquire_lock function."""

    def test_acquires_lock_on_free_task(self, temp_workspace):
        """Should acquire lock when no existing lock."""
        result = worker.try_acquire_lock("task_001")
        assert result is True

        lock_path = temp_workspace['locks_dir'] / "task_001.lock"
        assert lock_path.exists()

        lock_data = json.loads(lock_path.read_text())
        assert lock_data["task_id"] == "task_001"
        assert "worker_id" in lock_data
        assert "started_at" in lock_data

    def test_fails_when_task_locked(self, temp_workspace):
        """Should fail when task is already locked by another worker."""
        lock_path = temp_workspace['locks_dir'] / "task_001.lock"
        lock_data = {
            "worker_id": "other_worker",
            "started_at": worker.get_timestamp(),
            "task_id": "task_001"
        }
        lock_path.write_text(json.dumps(lock_data))

        result = worker.try_acquire_lock("task_001")
        assert result is False

    def test_acquires_stale_lock(self, temp_workspace):
        """Should acquire lock if existing lock is stale."""
        lock_path = temp_workspace['locks_dir'] / "task_001.lock"
        old_time = datetime.now(timezone.utc) - timedelta(seconds=worker.LOCK_TIMEOUT_SECONDS + 60)
        lock_data = {
            "worker_id": "dead_worker",
            "started_at": old_time.isoformat(),
            "task_id": "task_001"
        }
        lock_path.write_text(json.dumps(lock_data))

        result = worker.try_acquire_lock("task_001")
        assert result is True

        # Verify new lock has current worker
        new_lock_data = json.loads(lock_path.read_text())
        assert new_lock_data["worker_id"] == worker.WORKER_ID


class TestReleaseLock:
    """Tests for release_lock function."""

    def test_releases_existing_lock(self, temp_workspace):
        """Should remove lock file."""
        lock_path = temp_workspace['locks_dir'] / "task_001.lock"
        lock_path.write_text(json.dumps({"worker_id": "test"}))

        worker.release_lock("task_001")

        assert not lock_path.exists()

    def test_safe_on_nonexistent_lock(self, temp_workspace):
        """Should not raise if lock doesn't exist."""
        worker.release_lock("nonexistent_task")  # Should not raise


class TestCheckDependenciesComplete:
    """Tests for check_dependencies_complete function."""

    def test_no_dependencies_returns_true(self, temp_workspace):
        """Task with no dependencies should return True."""
        task = {"id": "task_001"}
        execution_log = {"tasks": {}}

        result = worker.check_dependencies_complete(task, execution_log)
        assert result is True

    def test_all_deps_completed(self, temp_workspace):
        """Should return True when all dependencies are completed."""
        task = {"id": "task_003", "depends_on": ["task_001", "task_002"]}
        execution_log = {
            "tasks": {
                "task_001": {"status": "completed"},
                "task_002": {"status": "completed"}
            }
        }

        result = worker.check_dependencies_complete(task, execution_log)
        assert result is True

    def test_some_deps_incomplete(self, temp_workspace):
        """Should return False when some dependencies not completed."""
        task = {"id": "task_003", "depends_on": ["task_001", "task_002"]}
        execution_log = {
            "tasks": {
                "task_001": {"status": "completed"},
                "task_002": {"status": "in_progress"}
            }
        }

        result = worker.check_dependencies_complete(task, execution_log)
        assert result is False

    def test_missing_dep_in_log(self, temp_workspace):
        """Should return False when dependency not in log."""
        task = {"id": "task_002", "depends_on": ["task_001"]}
        execution_log = {"tasks": {}}

        result = worker.check_dependencies_complete(task, execution_log)
        assert result is False


class TestIsTaskDone:
    """Tests for is_task_done function."""

    def test_completed_task_is_done(self, temp_workspace):
        """Completed task should return True."""
        execution_log = {"tasks": {"task_001": {"status": "completed"}}}
        assert worker.is_task_done("task_001", execution_log) is True

    def test_failed_task_is_done(self, temp_workspace):
        """Failed task should return True."""
        execution_log = {"tasks": {"task_001": {"status": "failed"}}}
        assert worker.is_task_done("task_001", execution_log) is True

    def test_in_progress_task_not_done(self, temp_workspace):
        """In progress task should return False."""
        execution_log = {"tasks": {"task_001": {"status": "in_progress"}}}
        assert worker.is_task_done("task_001", execution_log) is False

    def test_missing_task_not_done(self, temp_workspace):
        """Task not in log should return False."""
        execution_log = {"tasks": {}}
        assert worker.is_task_done("task_001", execution_log) is False


class TestExecuteTask:
    """Tests for execute_task function."""

    def test_successful_execution(self, temp_workspace):
        """Should return completed status on successful API call."""
        task = {"id": "task_001", "type": "grind", "min_budget": 0.05, "max_budget": 0.10, "intensity": "medium"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "Task completed successfully"}

        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            result = worker.execute_task(task, "http://localhost:8420")

        assert result["status"] == "completed"
        assert result["result_summary"] == "Task completed successfully"
        assert result["errors"] is None

    def test_api_error_response(self, temp_workspace):
        """Should return failed status on API error."""
        task = {"id": "task_001", "type": "grind"}

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            result = worker.execute_task(task, "http://localhost:8420")

        assert result["status"] == "failed"
        assert "500" in result["errors"]

    def test_connection_error(self, temp_workspace):
        """Should return failed status on connection error."""
        import httpx
        task = {"id": "task_001", "type": "grind"}

        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = httpx.ConnectError("Connection refused")
            result = worker.execute_task(task, "http://localhost:8420")

        assert result["status"] == "failed"
        assert "Cannot connect" in result["errors"]


class TestFindAndExecuteTask:
    """Tests for find_and_execute_task function."""

    def test_executes_available_task(self, temp_workspace):
        """Should find, lock, execute, and release task."""
        # Setup queue
        queue = {
            "tasks": [{"id": "task_001", "type": "grind"}],
            "api_endpoint": "http://localhost:8420"
        }
        temp_workspace['queue_file'].write_text(json.dumps(queue))

        # Setup empty execution log
        worker.write_execution_log({"version": "1.0", "tasks": {}, "swarm_summary": {}})

        # Mock execute_task
        with patch.object(worker, 'execute_task') as mock_execute:
            mock_execute.return_value = {"status": "completed", "result_summary": "Done", "errors": None}
            result = worker.find_and_execute_task(queue)

        assert result is True

        # Check log was updated
        log = worker.read_execution_log()
        assert log["tasks"]["task_001"]["status"] == "completed"

        # Check lock was released
        lock_path = temp_workspace['locks_dir'] / "task_001.lock"
        assert not lock_path.exists()

    def test_skips_completed_tasks(self, temp_workspace):
        """Should skip already completed tasks."""
        queue = {
            "tasks": [{"id": "task_001", "type": "grind"}],
            "api_endpoint": "http://localhost:8420"
        }

        # Mark task as completed in log
        log = {"version": "1.0", "tasks": {"task_001": {"status": "completed"}}, "swarm_summary": {}}
        worker.write_execution_log(log)

        with patch.object(worker, 'execute_task') as mock_execute:
            result = worker.find_and_execute_task(queue)

        assert result is False
        mock_execute.assert_not_called()

    def test_skips_locked_tasks(self, temp_workspace):
        """Should skip tasks locked by other workers."""
        queue = {
            "tasks": [{"id": "task_001", "type": "grind"}],
            "api_endpoint": "http://localhost:8420"
        }

        # Create lock for the task
        lock_path = temp_workspace['locks_dir'] / "task_001.lock"
        lock_path.write_text(json.dumps({
            "worker_id": "other_worker",
            "started_at": worker.get_timestamp(),
            "task_id": "task_001"
        }))

        worker.write_execution_log({"version": "1.0", "tasks": {}, "swarm_summary": {}})

        with patch.object(worker, 'execute_task') as mock_execute:
            result = worker.find_and_execute_task(queue)

        assert result is False
        mock_execute.assert_not_called()

    def test_respects_dependencies(self, temp_workspace):
        """Should skip tasks with incomplete dependencies."""
        queue = {
            "tasks": [{"id": "task_002", "type": "grind", "depends_on": ["task_001"]}],
            "api_endpoint": "http://localhost:8420"
        }

        # task_001 not completed
        worker.write_execution_log({"version": "1.0", "tasks": {}, "swarm_summary": {}})

        with patch.object(worker, 'execute_task') as mock_execute:
            result = worker.find_and_execute_task(queue)

        assert result is False
        mock_execute.assert_not_called()


class TestWorkerLoop:
    """Tests for worker_loop function."""

    def test_exits_on_max_iterations(self, temp_workspace):
        """Should exit after max_iterations."""
        queue = {
            "tasks": [
                {"id": "task_001", "type": "grind"},
                {"id": "task_002", "type": "grind"},
                {"id": "task_003", "type": "grind"}
            ],
            "api_endpoint": "http://localhost:8420"
        }
        temp_workspace['queue_file'].write_text(json.dumps(queue))
        worker.write_execution_log({"version": "1.0", "tasks": {}, "swarm_summary": {}})

        with patch.object(worker, 'execute_task') as mock_execute:
            mock_execute.return_value = {"status": "completed", "result_summary": "Done", "errors": None}
            worker.worker_loop(max_iterations=2)

        # Should have executed exactly 2 tasks
        assert mock_execute.call_count == 2

    def test_exits_on_idle(self, temp_workspace):
        """Should exit after max idle cycles with no tasks."""
        queue = {"tasks": [], "api_endpoint": "http://localhost:8420"}
        temp_workspace['queue_file'].write_text(json.dumps(queue))
        worker.write_execution_log({"version": "1.0", "tasks": {}, "swarm_summary": {}})

        with patch('time.sleep'):  # Don't actually sleep in tests
            worker.worker_loop()

        # Should exit without error


class TestAddTask:
    """Tests for add_task helper function."""

    def test_adds_task_to_queue(self, temp_workspace):
        """Should add task to queue file."""
        worker.add_task("task_001", "Run tests")

        queue = json.loads(temp_workspace['queue_file'].read_text())
        assert len(queue["tasks"]) == 1
        assert queue["tasks"][0]["id"] == "task_001"
        assert queue["tasks"][0]["atomic_instruction"] == "Run tests"

    def test_adds_task_with_dependencies(self, temp_workspace):
        """Should add task with dependencies."""
        worker.add_task("task_002", "Deploy", depends_on=["task_001"])

        queue = json.loads(temp_workspace['queue_file'].read_text())
        assert queue["tasks"][0]["depends_on"] == ["task_001"]
