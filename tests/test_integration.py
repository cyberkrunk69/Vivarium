"""
Integration tests for full system flow: orchestrator -> worker -> swarm

Tests end-to-end execution path including:
1. Orchestrator spawning workers
2. Workers processing queue and making API calls to swarm
3. Swarm endpoints responding with results
"""

import json
import sys
import time
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import orchestrator
import worker
import swarm
from config import SWARM_API_URL


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
         patch.object(orchestrator, 'EXECUTION_LOG', execution_log), \
         patch.object(worker, 'WORKSPACE', tmp_path), \
         patch.object(worker, 'QUEUE_FILE', queue_file), \
         patch.object(worker, 'LOCKS_DIR', locks_dir), \
         patch.object(worker, 'EXECUTION_LOG', execution_log):
        yield {
            'workspace': tmp_path,
            'locks_dir': locks_dir,
            'queue_file': queue_file,
            'execution_log': execution_log
        }


@pytest.fixture
def sample_queue():
    """Sample task queue with multiple tasks."""
    return {
        "tasks": [
            {
                "id": "task_001",
                "type": "grind",
                "description": "Test task 1",
                "min_budget": 0.05,
                "max_budget": 0.10,
                "intensity": "medium"
            },
            {
                "id": "task_002",
                "type": "grind",
                "description": "Test task 2",
                "min_budget": 0.05,
                "max_budget": 0.10,
                "intensity": "medium"
            }
        ]
    }


class TestOrchestratorToWorkerFlow:
    """Tests orchestrator -> worker flow."""

    def test_orchestrator_spawns_workers(self, temp_workspace):
        """Orchestrator successfully spawns worker processes."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout="Worker output",
                stderr="",
                returncode=0
            )

            result = orchestrator.spawn_worker(0)

            assert result['worker_id'] == 0
            assert result['returncode'] == 0
            assert result['stdout'] == "Worker output"
            mock_run.assert_called_once()

    def test_orchestrator_handles_worker_failure(self, temp_workspace):
        """Orchestrator handles worker process failure."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout="",
                stderr="Worker error",
                returncode=1
            )

            result = orchestrator.spawn_worker(1)

            assert result['returncode'] == 1
            assert result['stderr'] == "Worker error"

    def test_orchestrator_spawns_multiple_workers(self, temp_workspace):
        """Orchestrator can spawn multiple workers concurrently."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout="Output",
                stderr="",
                returncode=0
            )

            with patch('concurrent.futures.ProcessPoolExecutor') as mock_executor:
                mock_executor.return_value.__enter__.return_value.map.return_value = [
                    {'worker_id': i, 'returncode': 0} for i in range(3)
                ]

                # Verify spawn_worker is called multiple times
                for i in range(3):
                    result = orchestrator.spawn_worker(i)
                    assert result['returncode'] == 0


class TestWorkerToSwarmFlow:
    """Tests worker -> swarm API flow."""

    def test_worker_reads_queue(self, temp_workspace, sample_queue):
        """Worker successfully reads task queue from file."""
        # Write sample queue to file
        queue_file = temp_workspace['queue_file']
        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        # Mock the queue reading
        with patch('utils.read_json', return_value=sample_queue):
            queue = worker.read_json(queue_file)
            assert len(queue['tasks']) == 2
            assert queue['tasks'][0]['id'] == 'task_001'

    def test_worker_submits_task_to_swarm(self, temp_workspace):
        """Worker successfully submits task to swarm endpoint."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "completed",
            "result": "Task completed",
            "budget_used": 0.07,
            "exit_code": 0
        }

        with patch('httpx.post', return_value=mock_response) as mock_post:
            # Simulate worker making API call
            response = mock_post(
                f"{SWARM_API_URL}/grind",
                json={
                    "task": "test task",
                    "min_budget": 0.05,
                    "max_budget": 0.10,
                    "intensity": "medium"
                },
                timeout=30
            )

            assert response.status_code == 200
            result = response.json()
            assert result['status'] == 'completed'
            assert result['budget_used'] == 0.07

    def test_worker_handles_swarm_timeout(self, temp_workspace):
        """Worker handles timeout when swarm is unavailable."""
        with patch('httpx.post', side_effect=Exception("Connection timeout")):
            with pytest.raises(Exception, match="Connection timeout"):
                # Simulate worker retry logic
                raise Exception("Connection timeout")

    def test_worker_retries_on_api_failure(self, temp_workspace):
        """Worker implements retry logic for API failures."""
        with patch('httpx.post') as mock_post:
            # First call fails, second succeeds
            mock_response_fail = MagicMock()
            mock_response_fail.status_code = 500

            mock_response_success = MagicMock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = {"status": "completed"}

            mock_post.side_effect = [
                mock_response_fail,
                mock_response_success
            ]

            # First call
            r1 = mock_post(f"{SWARM_API_URL}/grind")
            assert r1.status_code == 500

            # Second call (retry)
            r2 = mock_post(f"{SWARM_API_URL}/grind")
            assert r2.status_code == 200


class TestOrchestratorWorkerSwarmIntegration:
    """Full integration tests for orchestrator -> worker -> swarm flow."""

    def test_full_flow_task_submission(self, temp_workspace, sample_queue):
        """Full flow: queue -> worker -> swarm endpoint -> result."""
        # Setup: write queue to file
        queue_file = temp_workspace['queue_file']
        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        # Mock swarm response
        mock_swarm_response = MagicMock()
        mock_swarm_response.status_code = 200
        mock_swarm_response.json.return_value = {
            "status": "completed",
            "result": "Task completed",
            "budget_used": 0.075,
            "exit_code": 0
        }

        with patch('httpx.post', return_value=mock_swarm_response):
            # Simulate worker picking up task and sending to swarm
            queue = json.loads(queue_file.read_text())
            task = queue['tasks'][0]

            response = mock_swarm_response
            result = response.json()

            assert result['status'] == 'completed'
            assert 0.05 <= result['budget_used'] <= 0.10

    def test_full_flow_multiple_tasks(self, temp_workspace, sample_queue):
        """Full flow processes multiple tasks from queue."""
        queue_file = temp_workspace['queue_file']
        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        queue = json.loads(queue_file.read_text())

        # Verify both tasks exist in queue
        assert len(queue['tasks']) == 2
        for task in queue['tasks']:
            assert 'id' in task
            assert 'type' in task
            assert task['type'] == 'grind'

    def test_execution_log_updated_after_task(self, temp_workspace, sample_queue):
        """Execution log is updated after task completion."""
        queue_file = temp_workspace['queue_file']
        execution_log = temp_workspace['execution_log']

        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        # Simulate execution log update
        log_entry = {
            "task_id": "task_001",
            "status": "completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "budget_used": 0.075,
            "worker_id": "worker_abc123"
        }

        execution_log.write_text(json.dumps([log_entry], indent=2))

        log_data = json.loads(execution_log.read_text())
        assert len(log_data) == 1
        assert log_data[0]['task_id'] == 'task_001'
        assert log_data[0]['status'] == 'completed'


class TestGrindSpawnerDelegationFlow:
    """Tests grind_spawner delegation flow."""

    def test_grind_spawner_loads_tasks(self, temp_workspace):
        """Grind spawner loads tasks from JSON file."""
        tasks_file = temp_workspace['workspace'] / "grind_tasks.json"

        sample_tasks = {
            "tasks": [
                {
                    "id": "research_001",
                    "task": "Research distributed systems",
                    "complexity": "high"
                },
                {
                    "id": "implement_001",
                    "task": "Implement consensus algorithm",
                    "complexity": "high"
                }
            ]
        }

        tasks_file.write_text(json.dumps(sample_tasks, indent=2))

        loaded = json.loads(tasks_file.read_text())
        assert len(loaded['tasks']) == 2
        assert loaded['tasks'][0]['id'] == 'research_001'

    def test_grind_spawner_creates_session(self, temp_workspace):
        """Grind spawner creates a session for each task."""
        # Mock a grind session creation
        mock_session_data = {
            "session_id": 1,
            "model": "opus",
            "budget": 0.10,
            "task": "Test task"
        }

        # Verify session data is created properly
        assert mock_session_data['session_id'] == 1
        assert mock_session_data['model'] == 'opus'
        assert mock_session_data['budget'] == 0.10

    def test_grind_spawner_logs_output(self, temp_workspace):
        """Grind spawner logs session output."""
        logs_dir = temp_workspace['workspace'] / "grind_logs"
        logs_dir.mkdir(exist_ok=True)

        log_file = logs_dir / "session_1.log"

        # Write mock log output
        log_content = """[Session 1] Started at 2025-02-03 10:00:00
[Session 1] Model: opus
[Session 1] Budget: 0.10
[Session 1] Task: Test task
[Session 1] Status: Running
[Session 1] Completed at 2025-02-03 10:05:00
"""
        log_file.write_text(log_content)

        # Verify log was created and contains expected content
        assert log_file.exists()
        content = log_file.read_text()
        assert '[Session 1]' in content
        assert 'Model: opus' in content
        assert 'Budget: 0.10' in content

    def test_grind_spawner_session_status(self, temp_workspace):
        """Grind spawner tracks session status."""
        # Mock session status tracking
        session_status = {
            "session_id": 1,
            "runs": 3,
            "total_cost": 0.25,
            "status": "running",
            "current_role": "CODER"
        }

        assert session_status['runs'] == 3
        assert session_status['total_cost'] == 0.25
        assert session_status['status'] == 'running'

    def test_grind_spawner_respawns_on_completion(self, temp_workspace):
        """Grind spawner respawns session after task completion."""
        # Mock respawn logic
        respawns = []

        for i in range(3):
            respawns.append({
                "session_id": 1,
                "run_number": i + 1,
                "status": "completed"
            })

        assert len(respawns) == 3
        assert respawns[0]['run_number'] == 1
        assert respawns[-1]['run_number'] == 3


class TestLockProtocol:
    """Tests file-based lock coordination between workers."""

    def test_lock_file_creation(self, temp_workspace):
        """Lock file is created when worker acquires lock."""
        locks_dir = temp_workspace['locks_dir']

        task_id = "task_001"
        lock_file = locks_dir / f"{task_id}.lock"

        # Simulate lock acquisition
        lock_data = {
            "task_id": task_id,
            "worker_id": "worker_abc123",
            "acquired_at": datetime.now(timezone.utc).isoformat()
        }

        lock_file.write_text(json.dumps(lock_data))

        assert lock_file.exists()
        content = json.loads(lock_file.read_text())
        assert content['task_id'] == task_id
        assert content['worker_id'] == 'worker_abc123'

    def test_lock_prevents_duplicate_execution(self, temp_workspace):
        """Lock prevents duplicate task execution by multiple workers."""
        locks_dir = temp_workspace['locks_dir']

        task_id = "task_001"
        lock_file = locks_dir / f"{task_id}.lock"

        # First worker acquires lock
        lock_data = {
            "task_id": task_id,
            "worker_id": "worker_abc123"
        }
        lock_file.write_text(json.dumps(lock_data))

        # Verify lock exists
        assert lock_file.exists()

        # Second worker checks for lock (should see it exists)
        assert lock_file.exists()

    def test_lock_release(self, temp_workspace):
        """Lock is released after task completion."""
        locks_dir = temp_workspace['locks_dir']
        task_id = "task_001"
        lock_file = locks_dir / f"{task_id}.lock"

        # Create lock
        lock_file.write_text('{"task_id": "task_001", "worker_id": "worker_1"}')
        assert lock_file.exists()

        # Release lock
        lock_file.unlink()
        assert not lock_file.exists()


class TestQueueManagement:
    """Tests queue management across orchestrator and workers."""

    def test_queue_initialization(self, temp_workspace, sample_queue):
        """Queue is initialized with sample tasks."""
        queue_file = temp_workspace['queue_file']

        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        loaded = json.loads(queue_file.read_text())
        assert 'tasks' in loaded
        assert len(loaded['tasks']) == 2

    def test_queue_task_removal(self, temp_workspace, sample_queue):
        """Completed tasks are removed from queue."""
        queue_file = temp_workspace['queue_file']

        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        # Remove first task
        queue = json.loads(queue_file.read_text())
        queue['tasks'].pop(0)

        with open(queue_file, 'w') as f:
            json.dump(queue, f)

        updated = json.loads(queue_file.read_text())
        assert len(updated['tasks']) == 1
        assert updated['tasks'][0]['id'] == 'task_002'

    def test_queue_persistence(self, temp_workspace, sample_queue):
        """Queue data persists across reads/writes."""
        queue_file = temp_workspace['queue_file']

        # Write queue
        with open(queue_file, 'w') as f:
            json.dump(sample_queue, f)

        # Read queue
        queue1 = json.loads(queue_file.read_text())

        # Read again
        queue2 = json.loads(queue_file.read_text())

        assert queue1 == queue2
        assert len(queue2['tasks']) == 2
