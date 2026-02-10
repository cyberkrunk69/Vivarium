from dataclasses import FrozenInstanceError

import pytest

from physics import SWARM_WORLD_PHYSICS, SwarmWorldControls


def test_world_physics_is_immutable():
    with pytest.raises(FrozenInstanceError):
        SWARM_WORLD_PHYSICS.queue_filename = "other_queue.json"  # type: ignore[misc]


def test_world_physics_contains_review_lifecycle_statuses():
    statuses = set(SWARM_WORLD_PHYSICS.known_execution_statuses)
    assert {"pending_review", "approved", "requeue"} <= statuses


def test_controls_enforce_metadata_bounds():
    controls = SwarmWorldControls(max_metadata_keys=1, max_metadata_bytes=16)

    with pytest.raises(ValueError, match="max_metadata_keys"):
        controls.validate_enqueue(
            current_task_count=0,
            instruction="ok",
            metadata={"a": 1, "b": 2},
        )

    with pytest.raises(ValueError, match="max_metadata_bytes"):
        controls.validate_enqueue(
            current_task_count=0,
            instruction="ok",
            metadata={"a": "x" * 64},
        )


def test_controls_enforce_result_bounds():
    controls = SwarmWorldControls(max_result_chars=3)
    with pytest.raises(ValueError, match="max_result_chars"):
        controls.validate_result("toolong")
