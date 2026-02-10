"""Fresh runtime environment for new-swarm interaction loops."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from physics import SWARM_WORLD_PHYSICS, SwarmWorldControls, SwarmWorldPhysics

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class FreshSwarmEnvironment:
    """
    Isolated environment API for the new swarm runtime.

    This class intentionally keeps all state inside ``root`` and does not read
    legacy queue/spawner files.
    """

    root: Path
    world_physics: SwarmWorldPhysics = SWARM_WORLD_PHYSICS
    controls: SwarmWorldControls = field(default_factory=SwarmWorldControls)

    @property
    def inbox_dir(self) -> Path:
        return self.root / "inbox"

    @property
    def outbox_dir(self) -> Path:
        return self.root / "outbox"

    @property
    def audit_dir(self) -> Path:
        return self.root / "audit"

    @property
    def state_dir(self) -> Path:
        return self.root / "state"

    @property
    def scratch_dir(self) -> Path:
        return self.root / "scratch"

    @property
    def queue_file(self) -> Path:
        return self.state_dir / self.world_physics.queue_filename

    @property
    def manifest_file(self) -> Path:
        return self.root / self.world_physics.manifest_filename

    @property
    def event_log_file(self) -> Path:
        return self.audit_dir / self.world_physics.event_log_filename

    def bootstrap(self, *, reset: bool = False) -> None:
        """Create environment layout and initialize state files."""
        self.root.mkdir(parents=True, exist_ok=True)
        for dirname in self.world_physics.required_directories:
            (self.root / dirname).mkdir(parents=True, exist_ok=True)

        if reset or not self.queue_file.exists():
            self._write_json(
                self.queue_file,
                {
                    "version": self.world_physics.queue_contract_version,
                    "tasks": [],
                },
            )

        if reset or not self.manifest_file.exists():
            self._write_json(
                self.manifest_file,
                {
                    "schema_version": self.world_physics.schema_version,
                    "created_at": _utc_now(),
                    "mode": self.world_physics.environment_mode,
                    "world_physics": self.world_physics.to_manifest(),
                    "controls": self.controls.to_manifest(),
                    "legacy_dependencies": [],
                },
            )

        if reset:
            self.event_log_file.write_text("", encoding="utf-8")

    def enqueue_task(
        self,
        instruction: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Add a new task to the isolated queue."""
        if not instruction or not instruction.strip():
            raise ValueError("instruction must be non-empty")

        instruction_text = instruction.strip()
        metadata_payload = dict(metadata or {})
        queue = self._load_queue()
        self.controls.validate_enqueue(
            current_task_count=len(queue["tasks"]),
            instruction=instruction_text,
            metadata=metadata_payload if metadata is not None else None,
        )

        task = {
            "id": f"fresh_task_{uuid.uuid4().hex[:12]}",
            "instruction": instruction_text,
            "status": self.world_physics.allowed_task_statuses[0],
            "created_at": _utc_now(),
            "metadata": metadata_payload,
        }
        queue["tasks"].append(task)
        self._write_json(self.queue_file, queue)
        self.record_event(
            "task_enqueued",
            {"task_id": task["id"], "queue_size": len(queue["tasks"])},
        )
        return task

    def claim_next_task(self) -> Optional[Dict[str, Any]]:
        """Claim the next pending task, returning None when queue is empty."""
        queue = self._load_queue()
        for task in queue["tasks"]:
            if task.get("status") == self.world_physics.allowed_task_statuses[0]:
                task["status"] = self.world_physics.allowed_task_statuses[1]
                task["claimed_at"] = _utc_now()
                self._write_json(self.queue_file, queue)
                self.record_event("task_claimed", {"task_id": task.get("id")})
                return task
        return None

    def complete_task(self, task_id: str, *, result: str) -> bool:
        """Mark a claimed task as completed and persist its result."""
        result_text = result if isinstance(result, str) else str(result)
        self.controls.validate_result(result_text)
        queue = self._load_queue()
        for task in queue["tasks"]:
            if task.get("id") != task_id:
                continue
            task["status"] = self.world_physics.allowed_task_statuses[2]
            task["completed_at"] = _utc_now()
            task["result"] = result_text
            self._write_json(self.queue_file, queue)
            self.record_event("task_completed", {"task_id": task_id})
            return True
        return False

    def record_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Append a structured event to the local JSONL audit log."""
        if not event_type or not event_type.strip():
            raise ValueError("event_type must be non-empty")
        self.event_log_file.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": _utc_now(),
            "event_type": event_type.strip(),
            "payload": payload,
        }
        with open(self.event_log_file, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _load_queue(self) -> Dict[str, Any]:
        default_queue: Dict[str, Any] = {
            "version": self.world_physics.queue_contract_version,
            "tasks": [],
        }
        if not self.queue_file.exists():
            return default_queue
        with open(self.queue_file, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
        if not isinstance(loaded, dict):
            return default_queue
        tasks = loaded.get("tasks")
        if not isinstance(tasks, list):
            return default_queue
        return {
            "version": str(loaded.get("version") or self.world_physics.queue_contract_version),
            "tasks": tasks,
        }

    @staticmethod
    def _write_json(path: Path, payload: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

