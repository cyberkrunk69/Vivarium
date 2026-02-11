import pytest
import re
import sys
import tempfile
from pathlib import Path

# Add vivarium to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from vivarium.runtime.control_panel_app import app as _app

CREATIVE_SEED_PATTERN = re.compile(r"^[A-Z]{2}-\d{4}-[A-Z]{2}$")


@pytest.fixture
def app(monkeypatch):
    """Create app with test config"""
    workspace = Path(tempfile.mkdtemp())
    swarm_dir = workspace / ".swarm"
    swarm_dir.mkdir(exist_ok=True)
    identities_dir = swarm_dir / "identities"
    identities_dir.mkdir(exist_ok=True)
    security_dir = workspace / "security"
    security_dir.mkdir(exist_ok=True)

    _app.config["TESTING"] = True
    _app.config["WORKSPACE"] = workspace
    _app.config["ACTION_LOG"] = workspace / "action_log.jsonl"
    _app.config["EXECUTION_LOG"] = workspace / "execution_log.jsonl"
    _app.config["QUEUE_FILE"] = workspace / "queue.json"
    _app.config["KILL_SWITCH"] = swarm_dir / "kill_switch.json"
    _app.config["FREE_TIME_BALANCES"] = swarm_dir / "free_time_balances.json"
    _app.config["IDENTITIES_DIR"] = identities_dir
    _app.config["GROQ_API_KEY_FILE"] = security_dir / "groq_key.txt"
    worker_file = swarm_dir / "worker_process.json"
    _app.config["WORKER_PROCESS_FILE"] = worker_file
    monkeypatch.setattr("vivarium.runtime.control_panel_app.WORKER_PROCESS_FILE", worker_file)
    _app.config["RUNTIME_SPEED_FILE"] = swarm_dir / "runtime_speed.json"
    _app.config["MAILBOX_QUESTS_FILE"] = swarm_dir / "mailbox_quests.json"
    _app.config["CREATIVE_SEED_PATTERN"] = CREATIVE_SEED_PATTERN
    _app.config["CREATIVE_SEED_USED_FILE"] = swarm_dir / "creative_seed_used.json"
    _app.config["CREATIVE_SEED_USED_MAX"] = 5000
    _app.config["DISCUSSIONS_DIR"] = swarm_dir / "discussions"

    return _app


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """No auth needed for localhost, but structure for future"""
    return {}


@pytest.fixture
def localhost_kwargs():
    """Ensure requests appear from localhost for middleware"""
    return {"environ_overrides": {"REMOTE_ADDR": "127.0.0.1"}}


@pytest.fixture(autouse=True)
def cleanup_worker_state(app):
    """Ensure no worker processes leak between tests"""
    import json
    import os
    import signal

    worker_file = app.config.get('WORKER_PROCESS_FILE')

    yield  # Run test

    # Cleanup after test
    if worker_file and worker_file.exists():
        try:
            data = json.loads(worker_file.read_text())
            pid = data.get('pid') or data.get('master_pid')

            # Kill if still running
            if pid and isinstance(pid, int):
                try:
                    os.kill(pid, signal.SIGTERM)
                    # Poll until process exits (max 2s) instead of fixed sleep
                    import time
                    for _ in range(40):
                        try:
                            os.kill(pid, 0)
                        except ProcessLookupError:
                            break
                        time.sleep(0.05)
                    # Force kill if still alive
                    try:
                        os.kill(pid, 0)
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                except (ProcessLookupError, PermissionError, OSError):
                    pass  # Process not found or can't kill

            # Clean up file
            worker_file.unlink(missing_ok=True)

        except (json.JSONDecodeError, IOError):
            # Corrupted file, just remove
            worker_file.unlink(missing_ok=True)
