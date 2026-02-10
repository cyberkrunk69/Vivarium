"""Legacy wrapper over the unified spawner session API."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from legacy_swarm_gen.grind_spawner_unified import UnifiedCycleSession

try:
    from knowledge_packs import get_relevant_packs
except Exception:  # pragma: no cover - optional legacy dependency
    def get_relevant_packs(_task_text: str) -> list[Any]:
        return []


class SpawnerWrapper:
    def __init__(self, *, workspace: Path | None = None, model: str = "llama-3.3-70b-versatile"):
        self.workspace = (workspace or Path.cwd()).resolve()
        self.model = model

    def execute_task(self, task_text: str) -> dict[str, Any]:
        relevant_packs = get_relevant_packs(task_text) or []
        prompt = task_text
        for pack in relevant_packs:
            lessons = getattr(pack, "lessons", None) or []
            for lesson in lessons:
                prompt += f" {lesson}"

        session = UnifiedCycleSession(
            session_id=int(time.time() * 1000) % 100000000,
            task=prompt,
            budget=0.1,
            workspace=self.workspace,
            model=self.model,
        )
        return session.execute()