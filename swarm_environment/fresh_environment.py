"""Fresh runtime environment for new-swarm interaction loops."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


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
        return self.state_dir / "task_queue.json"

    @property
    def manifest_file(self) -> Path:
        return self.root / "manifest.json"

    @property
    def event_log_file(self) -> Path:
        return self.audit_dir / "events.jsonl"

    def bootstrap(self, *, reset: bool = False) -> None:
        """Create environment layout and initialize state files."""
        for path in (
            self.root,
            self.inbox_dir,
            self.outbox_dir,
            self.audit_dir,
            self.state_dir,
            self.scratch_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)

        if reset or not self.queue_file.exists():
            self._write_json(self.queue_file, {"tasks": []})

        if reset or not self.manifest_file.exists():
            self._write_json(
                self.manifest_file,
                {
                    "schema_version": "1.0",
                    "created_at": _utc_now(),
                    "mode": "fresh_swarm_environment",
                    "legacy_dependencies": [],
                },
            )

        if reset:
            self.event_log_file.write_text("", encoding="utf-8")

    def enqueue_task(
        self,
        instruction: str,
        *,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Add a new task to the isolated queue."""
        if not instruction or not instruction.strip():
            raise ValueError("instruction must be non-empty")
        queue = self._load_queue()
        task = {
            "id": f"fresh_task_{uuid.uuid4().hex[:12]}",
            "instruction": instruction.strip(),
            "status": "pending",
            "created_at": _utc_now(),
            "metadata": metadata or {},
        }
        queue["tasks"].append(task)
        self._write_json(self.queue_file, queue)
        self.record_event("task_enqueued", {"task_id": task["id"]})
        return task

    def claim_next_task(self) -> Optional[Dict[str, Any]]:
        """Claim the next pending task, returning None when queue is empty."""
        queue = self._load_queue()
        for task in queue["tasks"]:
            if task.get("status") == "pending":
                task["status"] = "in_progress"
                task["claimed_at"] = _utc_now()
                self._write_json(self.queue_file, queue)
                self.record_event("task_claimed", {"task_id": task.get("id")})
                return task
        return None

    def complete_task(self, task_id: str, *, result: str) -> bool:
        """Mark a claimed task as completed and persist its result."""
        queue = self._load_queue()
        for task in queue["tasks"]:
            if task.get("id") != task_id:
                continue
            task["status"] = "completed"
            task["completed_at"] = _utc_now()
            task["result"] = result
            self._write_json(self.queue_file, queue)
            self.record_event("task_completed", {"task_id": task_id})
            return True
        return False

    def record_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Append a structured event to the local JSONL audit log."""
        self.event_log_file.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": _utc_now(),
            "event_type": event_type,
            "payload": payload,
        }
        with open(self.event_log_file, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _load_queue(self) -> Dict[str, List[Dict[str, Any]]]:
        if not self.queue_file.exists():
            return {"tasks": []}
        with open(self.queue_file, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
        if not isinstance(loaded, dict):
            return {"tasks": []}
        tasks = loaded.get("tasks")
        if not isinstance(tasks, list):
            return {"tasks": []}
        return {"tasks": tasks}

    @staticmethod
    def _write_json(path: Path, payload: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

