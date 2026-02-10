import json
from pathlib import Path

import pytest

from physics import SwarmWorldControls
from swarm_environment import FreshSwarmEnvironment


def test_bootstrap_creates_fresh_layout(tmp_path: Path):
    env = FreshSwarmEnvironment(tmp_path / "fresh_env")
    env.bootstrap(reset=True)

    assert env.manifest_file.exists()
    assert env.queue_file.exists()
    assert env.audit_dir.exists()
    assert env.scratch_dir.exists()
    manifest = json.loads(env.manifest_file.read_text(encoding="utf-8"))
    assert manifest["mode"] == "fresh_swarm_environment"
    assert manifest["world_physics"]["queue_filename"] == "task_queue.json"
    assert manifest["controls"]["max_tasks"] > 0


def test_queue_lifecycle_round_trip(tmp_path: Path):
    env = FreshSwarmEnvironment(tmp_path / "fresh_env")
    env.bootstrap(reset=True)

    task = env.enqueue_task("Refactor module boundaries")
    claimed = env.claim_next_task()
    assert claimed is not None
    assert claimed["id"] == task["id"]
    assert claimed["status"] == "in_progress"

    updated = env.complete_task(task["id"], result="done")
    assert updated is True

    queue = env._load_queue()
    assert queue["version"] == "1.1"
    assert queue["tasks"][0]["status"] == "completed"
    assert queue["tasks"][0]["result"] == "done"


def test_controls_enforce_max_tasks(tmp_path: Path):
    env = FreshSwarmEnvironment(
        tmp_path / "fresh_env",
        controls=SwarmWorldControls(max_tasks=1),
    )
    env.bootstrap(reset=True)
    env.enqueue_task("first task")

    with pytest.raises(ValueError, match="max_tasks"):
        env.enqueue_task("second task")


def test_controls_enforce_instruction_size(tmp_path: Path):
    env = FreshSwarmEnvironment(
        tmp_path / "fresh_env",
        controls=SwarmWorldControls(max_instruction_chars=5),
    )
    env.bootstrap(reset=True)

    with pytest.raises(ValueError, match="max_instruction_chars"):
        env.enqueue_task("this is too long")

