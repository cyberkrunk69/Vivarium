"""
Canonical queue and execution-event contract helpers.

Phase 0 intent:
- keep one task contract shape for queue.json
- keep one common vocabulary for execution_log.jsonl statuses
"""

from __future__ import annotations

from typing import Any, Dict, List

from physics import SWARM_WORLD_PHYSICS

QUEUE_CONTRACT_VERSION = SWARM_WORLD_PHYSICS.queue_contract_version
DEFAULT_API_ENDPOINT = "http://127.0.0.1:8420"

KNOWN_EXECUTION_STATUSES = set(SWARM_WORLD_PHYSICS.known_execution_statuses)


def normalize_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """Return a task dict with canonical defaults applied."""
    normalized = dict(task or {})
    normalized.setdefault("type", "cycle")
    normalized.setdefault("depends_on", [])
    normalized.setdefault("parallel_safe", True)
    normalized.setdefault("status", "pending")
    return normalized


def normalize_queue(queue: Dict[str, Any] | None) -> Dict[str, Any]:
    """Return queue.json data normalized to the canonical contract."""
    source = dict(queue or {})

    normalized: Dict[str, Any] = {
        "version": str(source.get("version") or QUEUE_CONTRACT_VERSION),
        "api_endpoint": source.get("api_endpoint") or DEFAULT_API_ENDPOINT,
        "tasks": [normalize_task(t) for t in (source.get("tasks") or []) if isinstance(t, dict)],
        "completed": list(source.get("completed") or []),
        "failed": list(source.get("failed") or []),
    }

    for key, value in source.items():
        if key not in normalized:
            normalized[key] = value

    return normalized


def validate_queue_contract(queue: Dict[str, Any]) -> List[str]:
    """Return validation errors for queue contract; empty list means valid."""
    errors: List[str] = []

    if not isinstance(queue, dict):
        return ["queue must be a JSON object"]

    for key in ("version", "api_endpoint", "tasks", "completed", "failed"):
        if key not in queue:
            errors.append(f"missing key: {key}")

    tasks = queue.get("tasks")
    if not isinstance(tasks, list):
        errors.append("tasks must be a list")
    else:
        for index, task in enumerate(tasks):
            if not isinstance(task, dict):
                errors.append(f"tasks[{index}] must be an object")
                continue
            if not task.get("id"):
                errors.append(f"tasks[{index}] is missing non-empty id")

    return errors


def is_known_execution_status(status: str) -> bool:
    """Return True when status is in the canonical execution-event vocabulary."""
    return status in KNOWN_EXECUTION_STATUSES
