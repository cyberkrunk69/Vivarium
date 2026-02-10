"""Core immutable world properties and control knobs for swarm simulation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Tuple


@dataclass(frozen=True)
class SwarmWorldPhysics:
    """
    Immutable world-level properties for the swarm simulation.

    This is intentionally not "math constants"; it defines structural invariants
    for how the simulation world stores state, tracks lifecycle, and validates
    execution vocabulary.
    """

    world_name: str = "vivarium_swarm"
    schema_version: str = "1.0"
    queue_contract_version: str = "1.1"
    environment_mode: str = "fresh_swarm_environment"
    state_layout_version: str = "1"
    required_directories: Tuple[str, ...] = ("inbox", "outbox", "audit", "state", "scratch")
    queue_filename: str = "task_queue.json"
    manifest_filename: str = "manifest.json"
    event_log_filename: str = "events.jsonl"
    allowed_task_statuses: Tuple[str, ...] = ("pending", "in_progress", "completed", "failed")
    known_execution_statuses: Tuple[str, ...] = (
        "queued",
        "in_progress",
        "completed",
        "failed",
        "pending_review",
        "approved",
        "requeue",
        "needs_qa",
        "needs_integration",
        "needs_e2e",
        "ready_for_merge",
        "subtask_started",
        "subtask_completed",
        "subtask_failed",
        "safety_blocked",
    )
    immutable_properties: Tuple[str, ...] = (
        "world_name",
        "schema_version",
        "queue_contract_version",
        "environment_mode",
        "state_layout_version",
        "required_directories",
        "queue_filename",
        "manifest_filename",
        "event_log_filename",
        "allowed_task_statuses",
        "known_execution_statuses",
    )

    def to_manifest(self) -> dict[str, Any]:
        """Serialize immutable world properties for manifest snapshots."""
        return {
            "world_name": self.world_name,
            "schema_version": self.schema_version,
            "queue_contract_version": self.queue_contract_version,
            "environment_mode": self.environment_mode,
            "state_layout_version": self.state_layout_version,
            "required_directories": list(self.required_directories),
            "queue_filename": self.queue_filename,
            "manifest_filename": self.manifest_filename,
            "event_log_filename": self.event_log_filename,
            "allowed_task_statuses": list(self.allowed_task_statuses),
            "known_execution_statuses": list(self.known_execution_statuses),
            "immutable_properties": list(self.immutable_properties),
        }


@dataclass
class SwarmWorldControls:
    """
    Runtime control surface for the swarm simulation world.

    These controls are intentionally mutable/configurable while the physics
    invariants remain fixed.
    """

    max_tasks: int = 2048
    max_instruction_chars: int = 4000
    max_metadata_keys: int = 64
    max_metadata_bytes: int = 16384
    max_result_chars: int = 64000

    def __post_init__(self) -> None:
        for field_name in (
            "max_tasks",
            "max_instruction_chars",
            "max_metadata_keys",
            "max_metadata_bytes",
            "max_result_chars",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{field_name} must be a positive integer")

    def to_manifest(self) -> dict[str, int]:
        """Serialize control values for manifest snapshots."""
        return {
            "max_tasks": self.max_tasks,
            "max_instruction_chars": self.max_instruction_chars,
            "max_metadata_keys": self.max_metadata_keys,
            "max_metadata_bytes": self.max_metadata_bytes,
            "max_result_chars": self.max_result_chars,
        }

    def validate_enqueue(
        self,
        *,
        current_task_count: int,
        instruction: str,
        metadata: Mapping[str, Any] | None,
    ) -> None:
        """Validate queue capacity and payload bounds before task enqueue."""
        if current_task_count >= self.max_tasks:
            raise ValueError(
                f"task queue reached max_tasks={self.max_tasks}; complete tasks before enqueueing more"
            )

        if len(instruction) > self.max_instruction_chars:
            raise ValueError(
                f"instruction length {len(instruction)} exceeds max_instruction_chars={self.max_instruction_chars}"
            )

        if metadata is None:
            return

        if not isinstance(metadata, Mapping):
            raise TypeError("metadata must be a mapping/dict when provided")

        if len(metadata) > self.max_metadata_keys:
            raise ValueError(
                f"metadata key count {len(metadata)} exceeds max_metadata_keys={self.max_metadata_keys}"
            )

        try:
            encoded = json.dumps(dict(metadata), ensure_ascii=False).encode("utf-8")
        except TypeError as exc:
            raise TypeError("metadata must be JSON-serializable") from exc

        if len(encoded) > self.max_metadata_bytes:
            raise ValueError(
                f"metadata payload {len(encoded)} bytes exceeds max_metadata_bytes={self.max_metadata_bytes}"
            )

    def validate_result(self, result: str) -> None:
        """Validate task result payload bounds."""
        if len(result) > self.max_result_chars:
            raise ValueError(
                f"result length {len(result)} exceeds max_result_chars={self.max_result_chars}"
            )


SWARM_WORLD_PHYSICS = SwarmWorldPhysics()
DEFAULT_WORLD_CONTROLS = SwarmWorldControls()

