"""
Smart Task Executor - Integrates Groq with Dynamic Scheduler

This bridges the inference engines with the dynamic scheduler:
- Wraps model execution
- Detects when output indicates a missing dependency
- Spawns subtasks automatically
- Manages checkpointing for long tasks
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime

try:
    from hats import HAT_LIBRARY, apply_hat
except ImportError:
    HAT_LIBRARY = None
    apply_hat = None
try:
    from resident_facets import decompose_task as resident_decompose_task
except ImportError:
    resident_decompose_task = None

from dynamic_scheduler import (
    DynamicScheduler,
    TaskContext,
    Task,
    TaskState,
    BlockedOnDependency
)
from inference_engine import get_engine, EngineType, InferenceResult
from groq_code_extractor import GroqArtifactExtractor


# Patterns that indicate a task needs something that doesn't exist
DEPENDENCY_PATTERNS = [
    # "PREREQUISITE: X.md must exist"
    (r'PREREQUISITE:\s*(\S+\.(?:md|py|json))\s+must\s+exist', 'file'),
    # "First, read X.py"
    (r'(?:First,?\s+)?[Rr]ead\s+(\S+\.(?:md|py|json))', 'file'),
    # "Requires X to be implemented"
    (r'[Rr]equires?\s+(\S+)\s+to\s+be\s+implemented', 'task'),
    # "Depends on X"
    (r'[Dd]epends?\s+on\s+(\S+)', 'task'),
]

# Patterns in model output indicating it couldn't proceed
BLOCKED_OUTPUT_PATTERNS = [
    r"file.*(?:doesn't|does not|not)\s+exist",
    r"couldn't find",
    r"no such file",
    r"missing.*(?:file|dependency|prerequisite)",
    r"need.*first",
    r"waiting for",
    r"blocked by",
]

FOCUS_HAT_MAP = {
    "strategy": "Strategist",
    "build": "Builder",
    "review": "Reviewer",
    "document": "Documenter",
}


class SmartExecutor:
    """
    Executes tasks with dynamic dependency resolution.

    When a task can't proceed because something is missing,
    automatically spawns a subtask to create it.
    """

    def __init__(
        self,
        workspace: Path,
        max_parallel: int = 4,
        engine_type: EngineType = EngineType.AUTO,
        identity_label: Optional[str] = None,
    ):
        self.workspace = workspace
        self.engine_type = engine_type
        self.scheduler = DynamicScheduler(max_workers=max_parallel)
        self.code_extractor = GroqArtifactExtractor(workspace_root=str(workspace))
        self.identity_label = identity_label or "Resident"

        # Track what files/artifacts exist
        self.artifacts: Dict[str, Path] = {}

        # Task definitions for spawning
        self.task_templates: Dict[str, Dict] = {}

        # Set up callbacks
        self.scheduler.on_task_start = self._on_task_start
        self.scheduler.on_task_complete = self._on_task_complete
        self.scheduler.on_task_blocked = self._on_task_blocked

    def _on_task_start(self, task: Task) -> None:
        desc = task.description[:50]
        print(f"[{task.id}] START: {desc}...")

    def _on_task_complete(self, task: Task) -> None:
        print(f"[{task.id}] DONE")

    def _on_task_blocked(self, task: Task, dep_id: str) -> None:
        print(f"[{task.id}] BLOCKED on {dep_id}")

    def _detect_dependencies(self, task_text: str) -> List[Dict]:
        """
        Scan task description for dependencies.
        Returns list of {type: 'file'|'task', name: str}
        """
        deps = []
        for pattern, dep_type in DEPENDENCY_PATTERNS:
            matches = re.findall(pattern, task_text, re.IGNORECASE)
            for match in matches:
                deps.append({"type": dep_type, "name": match})
        return deps

    def _check_file_exists(self, filename: str) -> bool:
        """Check if a file exists in workspace or experiments."""
        # Check direct path
        if (self.workspace / filename).exists():
            return True
        # Check experiments
        for exp_dir in (self.workspace / "experiments").glob("*"):
            if (exp_dir / filename).exists():
                return True
        return False

    def _find_task_for_file(self, filename: str) -> Optional[str]:
        """Find which task creates a given file."""
        for task_id, template in self.task_templates.items():
            outputs = template.get("outputs", [])
            if filename in outputs or any(filename in o for o in outputs):
                return task_id
        return None

    def _create_task_executor(
        self,
        task_text: str,
        task_id: str,
        hat_name: Optional[str] = None,
    ) -> Callable:
        """
        Create an executor function for a task.
        This wraps the model call with dependency checking.
        """
        def executor(ctx: TaskContext) -> Dict[str, Any]:
            # Check for file dependencies
            deps = self._detect_dependencies(task_text)
            for dep in deps:
                if dep["type"] == "file":
                    if not self._check_file_exists(dep["name"]):
                        # File doesn't exist - need to create it
                        print(f"    [{task_id}] Missing: {dep['name']}")

                        # Find or create a task to produce this file
                        producer_id = self._find_task_for_file(dep["name"])
                        if producer_id:
                            print(f"    [{task_id}] Waiting for task {producer_id} to create it")
                            ctx.wait_for(producer_id)
                        else:
                            # Spawn a new task to create the file
                            print(f"    [{task_id}] Spawning subtask to create {dep['name']}")
                            sub_id = ctx.spawn_subtask(
                                f"Create {dep['name']}",
                                self._create_file_generator(dep["name"]),
                                wait=True
                            )

            # All dependencies satisfied - run the actual task
            ctx.progress(0.1)

            engine = get_engine(self.engine_type)
            prompt = self._build_prompt(task_text, hat_name=hat_name)

            ctx.progress(0.2)

            result = engine.execute(
                prompt=prompt,
                workspace=self.workspace,
                session_id=hash(task_id) % 1000
            )

            ctx.progress(0.8)

            # Extract any files created
            if result.success and result.output:
                saved = self.code_extractor.extract_and_save(result.output)
                if saved:
                    print(f"    [{task_id}] CREATED: {', '.join(saved)}")
                    for f in saved:
                        self.artifacts[Path(f).name] = Path(f)

            ctx.progress(1.0)

            return {
                "success": result.success,
                "output": result.output,
                "files": saved if result.success else [],
                "error": result.error
            }

        return executor

    def _create_file_generator(self, filename: str) -> Callable:
        """Create a task that generates a specific file."""
        def generator(ctx: TaskContext) -> Dict:
            engine = get_engine(self.engine_type)

            prompt = f"""Create the file: {filename}

Based on the filename, generate appropriate content:
- If it's a .md file, create a design document
- If it's a .py file, create a Python module
- If it's a .json file, create a configuration

Use the artifact format:
<artifact type="file" path="{filename}">
CONTENT HERE
</artifact>

Create the file now."""
            prompt = self._apply_hat_overlay(prompt, "Builder")

            result = engine.execute(
                prompt=prompt,
                workspace=self.workspace
            )

            if result.success and result.output:
                saved = self.code_extractor.extract_and_save(result.output)
                if saved:
                    print(f"    [subtask] CREATED: {filename}")
                    return {"success": True, "file": filename}

            return {"success": False, "error": "Failed to create file"}

        return generator

    def _apply_hat_overlay(self, prompt: str, hat_name: Optional[str]) -> str:
        if not prompt or not hat_name or not HAT_LIBRARY or not apply_hat:
            return prompt
        hat_key = FOCUS_HAT_MAP.get(hat_name.lower(), hat_name)
        hat = HAT_LIBRARY.get_hat(hat_key)
        if not hat:
            return prompt
        return apply_hat(prompt, hat)

    def _build_prompt(self, task_text: str, hat_name: Optional[str] = None) -> str:
        """Build execution prompt for a task."""
        base_prompt = f"""You are {self.identity_label}. You can optionally wear a hat to focus, but your identity stays the same.

If you choose to take this task, make real changes rather than only describing them.

WORKSPACE: {self.workspace}

TASK:
{task_text}

GUIDANCE (voluntary):
1. When acting, use your tools to modify files directly:
   - Use the Edit tool to modify existing files
   - Use the Write tool to create new files
   - Use the Read tool to examine files first
2. Avoid only describing changes; apply them when appropriate
3. After making changes, verify they worked

PROTECTED FILES (READ-ONLY):
- grind_spawner.py, orchestrator.py, roles.py
- safety_gateway.py, safety_constitutional.py

ALTERNATIVE OUTPUT FORMAT (if tools unavailable):
<artifact type="file" path="relative/path/to/file.ext">
COMPLETE FILE CONTENT
</artifact>

If you take this task, act directly and make real changes."""
        return self._apply_hat_overlay(base_prompt, hat_name)

    def add_task(
        self,
        description: str,
        task_text: str,
        outputs: List[str] = None,
        depends_on: List[str] = None,
        hat: Optional[str] = None,
    ) -> str:
        """Add a task to be executed."""
        task_id = self.scheduler.add_task(
            description=description,
            execute_fn=self._create_task_executor(task_text, description[:8], hat_name=hat),
            depends_on=depends_on or []
        )

        # Store template for dependency resolution
        self.task_templates[task_id] = {
            "description": description,
            "text": task_text,
            "outputs": outputs or [],
            "hat": hat,
        }

        return task_id

    def add_decomposed_task(
        self,
        description: str,
        task_text: str,
        max_subtasks: int = 3,
    ) -> List[str]:
        """
        Decompose a task into atomic steps and schedule them sequentially.
        Each subtask uses a hat focus but remains the same identity.
        """
        if not resident_decompose_task:
            return [self.add_task(description, task_text)]

        plan = resident_decompose_task(
            task_text,
            resident_id="resident_executor",
            identity_id=self.identity_label,
            max_subtasks=max_subtasks,
        )

        task_ids: List[str] = []
        prev_id: Optional[str] = None
        for sub in plan.subtasks:
            focus = getattr(sub, "suggested_focus", None)
            hat = FOCUS_HAT_MAP.get((focus or "").lower(), None) if focus else None
            sub_desc = getattr(sub, "description", "") or task_text
            label = f"{description} :: {sub_desc[:48]}".strip()
            deps = [prev_id] if prev_id else None
            sub_id = self.add_task(label, sub_desc, depends_on=deps, hat=hat)
            task_ids.append(sub_id)
            prev_id = sub_id

        return task_ids

    def run(self) -> Dict[str, Any]:
        """Run all tasks with dynamic scheduling."""
        print("=" * 60)
        print("  SMART EXECUTOR - Dynamic Dependency Resolution")
        print("=" * 60)
        print(f"  Tasks: {len(self.task_templates)}")
        print(f"  Residents: {self.scheduler.max_workers}")
        print("-" * 60)

        self.scheduler.run(block=True)

        status = self.scheduler.status()
        print("\n" + "=" * 60)
        print("  COMPLETE")
        print("=" * 60)
        print(f"  Completed: {status['completed']}")
        print(f"  Failed: {status['failed']}")
        print(f"  Artifacts: {len(self.artifacts)}")
        print("=" * 60)

        return status


# Quick test
if __name__ == "__main__":
    from pathlib import Path

    executor = SmartExecutor(
        workspace=Path("."),
        max_parallel=4,
        engine_type=EngineType.GROQ,
    )

    # Add tasks with dependencies
    executor.add_task(
        "Design dual server",
        "DESIGN: Create DUAL_SERVER_DESIGN.md with architecture for admin + LAN servers",
        outputs=["DUAL_SERVER_DESIGN.md"]
    )

    executor.add_task(
        "Implement dual server",
        "PREREQUISITE: DUAL_SERVER_DESIGN.md must exist.\n\nImplement the dual server based on the design.",
        depends_on=[]  # Will be detected dynamically!
    )

    executor.run()
