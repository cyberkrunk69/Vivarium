from pathlib import Path

from swarm_environment import FreshSwarmEnvironment


def test_bootstrap_creates_fresh_layout(tmp_path: Path):
    env = FreshSwarmEnvironment(tmp_path / "fresh_env")
    env.bootstrap(reset=True)

    assert env.manifest_file.exists()
    assert env.queue_file.exists()
    assert env.audit_dir.exists()
    assert env.scratch_dir.exists()


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
    assert queue["tasks"][0]["status"] == "completed"
    assert queue["tasks"][0]["result"] == "done"

