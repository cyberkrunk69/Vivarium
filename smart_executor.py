"""
Smart Task Executor - Integrates Claude/Groq with Dynamic Scheduler

This bridges the inference engines with the dynamic scheduler:
- Wraps Claude/Groq execution
- Detects when output indicates a missing dependency
- Spawns subtasks automatically
- Manages checkpointing for long tasks
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime

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

# Patterns in Claude's output indicating it couldn't proceed
BLOCKED_OUTPUT_PATTERNS = [
    r"file.*(?:doesn't|does not|not)\s+exist",
    r"couldn't find",
    r"no such file",
    r"missing.*(?:file|dependency|prerequisite)",
    r"need.*first",
    r"waiting for",
    r"blocked by",
]


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
        engine_type: EngineType = EngineType.AUTO
    ):
        self.workspace = workspace
        self.engine_type = engine_type
        self.scheduler = DynamicScheduler(max_workers=max_parallel)
        self.code_extractor = GroqArtifactExtractor(workspace_root=str(workspace))

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

    def _create_task_executor(self, task_text: str, task_id: str) -> Callable:
        """
        Create an executor function for a task.
        This wraps the Claude/Groq call with dependency checking.
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
            prompt = self._build_prompt(task_text)

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

    def _build_prompt(self, task_text: str) -> str:
        """Build execution prompt for a task."""
        return f"""You are an EXECUTION worker. Follow instructions EXACTLY.

WORKSPACE: {self.workspace}

TASK:
{task_text}

FILE OUTPUT FORMAT - When creating files, use this EXACT format:
<artifact type="file" path="relative/path/to/file.ext">
FILE_CONTENT_HERE
</artifact>

RULES:
1. Core system files (grind_spawner.py, orchestrator.py, etc.) are READ-ONLY
2. Be FAST - don't over-explain, just do the work
3. When done, output a brief summary

EXECUTE NOW."""

    def add_task(
        self,
        description: str,
        task_text: str,
        outputs: List[str] = None,
        depends_on: List[str] = None
    ) -> str:
        """Add a task to be executed."""
        task_id = self.scheduler.add_task(
            description=description,
            execute_fn=self._create_task_executor(task_text, description[:8]),
            depends_on=depends_on or []
        )

        # Store template for dependency resolution
        self.task_templates[task_id] = {
            "description": description,
            "text": task_text,
            "outputs": outputs or []
        }

        return task_id

    def run(self) -> Dict[str, Any]:
        """Run all tasks with dynamic scheduling."""
        print("=" * 60)
        print("  SMART EXECUTOR - Dynamic Dependency Resolution")
        print("=" * 60)
        print(f"  Tasks: {len(self.task_templates)}")
        print(f"  Workers: {self.scheduler.max_workers}")
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
        engine_type=EngineType.CLAUDE
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
