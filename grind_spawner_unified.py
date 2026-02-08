"""
Unified Grind Spawner (minimal, repo-consistent).

This file exists because the Control Panel UI starts the spawner by launching
`grind_spawner_unified.py` in a detached subprocess.

Goals:
- Provide a stable CLI that matches `control_panel.py` expectations:
  `--sessions`, `--budget`, `--workspace`, `--model`
- Provide the small API surface used by `test_swarm_fixes.py`:
  `UnifiedGrindSession`, `EngineType`

The spawner can run a single task (`--task`) or delegate over a tasks JSON file
(`--tasks-file`). In Groq mode, it expects the model to return `<artifact ...>`
blocks that can be extracted into real files.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
from typing import Any, Dict, List, Optional, Tuple

from groq_code_extractor import GroqArtifactExtractor
from inference_engine import EngineType, get_engine


HALT_FILENAME = "HALT"
PAUSE_FILENAME = "PAUSE"


def _load_tasks(tasks_file: Path) -> List[Dict[str, Any]]:
    """
    Load tasks from a JSON file.

    Supported formats:
    - List[str]
    - List[{"task": "...", ...}]
    """
    if not tasks_file.exists():
        return []

    data = json.loads(tasks_file.read_text(encoding="utf-8"))
    tasks: List[Dict[str, Any]] = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                tasks.append({"task": item})
            elif isinstance(item, dict):
                if "task" in item and isinstance(item["task"], str):
                    tasks.append(item)
            else:
                continue
    return tasks


def _should_halt(workspace: Path) -> Tuple[bool, Optional[str]]:
    halt_file = workspace / HALT_FILENAME
    if not halt_file.exists():
        return False, None
    try:
        return True, halt_file.read_text(encoding="utf-8")[:4000]
    except Exception:
        return True, "HALT file present"


def _is_paused(workspace: Path) -> bool:
    return (workspace / PAUSE_FILENAME).exists()


@dataclass
class UnifiedGrindSession:
    """
    Represents a single grind session for one task.

    This is intentionally lightweight; it primarily builds a grounded prompt and
    (optionally) executes it via the configured inference engine.
    """

    session_id: int
    task: str
    budget: float
    workspace: Path
    model: str = "llama-3.3-70b-versatile"
    force_engine: EngineType = EngineType.AUTO

    def _normalize_analysis_task(self, task_text: str) -> str:
        """
        Normalize certain ambiguous "analysis write" tasks into a deterministic form.

        Expected by `test_swarm_fixes.py`.
        Example:
          "Write to test_output.txt: Why does the swarm hallucinate?"
        becomes:
          "Create analysis file at test_output.txt that answers: Why does the swarm hallucinate?"
        """
        prefix = "Write to "
        if task_text.startswith(prefix) and ":" in task_text:
            left, right = task_text[len(prefix) :].split(":", 1)
            path = left.strip()
            question = right.strip()
            if path and question:
                return f"Create analysis file at {path} that answers: {question}"
        return task_text

    def get_prompt(self) -> str:
        """
        Build an execution prompt with strict grounding rules.

        Required strings are asserted by `test_swarm_fixes.py`.
        """
        normalized_task = self._normalize_analysis_task(self.task)
        return f"""You are an autonomous coding agent operating inside a local workspace.

WORKSPACE: {self.workspace}
SESSION_ID: {self.session_id}
BUDGET_USD: {self.budget}

TASK:
{normalized_task}

CRITICAL GROUNDING RULES
1. READ THE FILE FIRST before editing it.
2. NEVER make up function names, file paths, or CLI flags.
3. NEVER guess data structures or APIs — locate them in the repo first.
4. If you cannot find required code/files, explicitly say what is missing and stop.
5. When creating/modifying files, output them using the artifact format below.

ARTIFACT FORMAT (preferred)
<artifact type="file" path="relative/path/to/file.ext">
FULL FILE CONTENT HERE
</artifact>

Do the work now. If you make changes, include all necessary files as artifacts.
"""

    def execute(self) -> Dict[str, Any]:
        """
        Execute the session task using the configured inference engine.
        """
        engine = get_engine(self.force_engine)
        prompt = self.get_prompt()
        result = engine.execute(
            prompt=prompt,
            model=self.model,
            workspace=self.workspace,
            timeout=1200,
            max_tokens=4096,
            session_id=self.session_id,
        )

        saved_files: List[str] = []
        if result.success and result.output:
            extractor = GroqArtifactExtractor(workspace_root=str(self.workspace))
            saved_files = extractor.extract_and_save(result.output)

        return {
            "success": result.success,
            "output": result.output,
            "saved_files": saved_files,
            "cost_usd": result.cost_usd,
            "model": result.model,
            "error": result.error,
        }


def _worker_loop(
    worker_id: int,
    q: "Queue[Dict[str, Any]]",
    workspace: Path,
    per_task_budget: float,
    model: str,
    engine_type: EngineType,
) -> None:
    while True:
        should_halt, _ = _should_halt(workspace)
        if should_halt:
            return

        while _is_paused(workspace):
            time.sleep(1.0)
            should_halt, _ = _should_halt(workspace)
            if should_halt:
                return

        try:
            task_obj = q.get_nowait()
        except Empty:
            return

        task_text = task_obj.get("task") or task_obj.get("prompt") or ""
        task_text = str(task_text).strip()
        if not task_text:
            q.task_done()
            continue

        session = UnifiedGrindSession(
            session_id=(worker_id * 100000) + int(time.time()) % 100000,
            task=task_text,
            budget=per_task_budget,
            workspace=workspace,
            model=model,
            force_engine=engine_type,
        )

        try:
            session.execute()
        except Exception as e:
            # Keep the spawner alive; surface error to stdout for logs.
            print(f"[spawner] worker {worker_id} task failed: {e}", file=sys.stderr)
        finally:
            q.task_done()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Unified Grind Spawner")
    parser.add_argument("--sessions", type=int, default=3)
    parser.add_argument("--budget", type=float, default=0.10)
    parser.add_argument("--workspace", type=str, default=str(Path(__file__).parent))
    parser.add_argument("--model", type=str, default="llama-3.3-70b-versatile")

    parser.add_argument("--task", type=str, default=None, help="Run a single task then exit")
    parser.add_argument("--tasks-file", type=str, default="grind_tasks.json")
    parser.add_argument("--delegate", action="store_true", help="Run tasks from tasks file")
    parser.add_argument("--once", action="store_true", help="Run one pass then exit")
    parser.add_argument(
        "--engine",
        type=str,
        default=os.environ.get("INFERENCE_ENGINE", "auto"),
        help="auto|groq|claude",
    )

    args = parser.parse_args(argv)
    workspace = Path(args.workspace).resolve()
    sessions = max(1, int(args.sessions))
    budget_total = max(0.0, float(args.budget))
    model = str(args.model)

    engine_str = str(args.engine).lower().strip()
    engine_type = EngineType.AUTO
    if engine_str == "groq":
        engine_type = EngineType.GROQ
    elif engine_str == "claude":
        engine_type = EngineType.CLAUDE

    # Determine tasks
    tasks: List[Dict[str, Any]] = []
    if args.task:
        tasks = [{"task": args.task}]
    else:
        # Default to delegate mode for the control panel start button.
        tasks_file = (workspace / args.tasks_file).resolve()
        tasks = _load_tasks(tasks_file)
        if not tasks and not args.delegate:
            # If delegate wasn't requested and no single task was provided, do nothing.
            print(f"[spawner] No tasks found in {tasks_file}; exiting.")
            return 0

    if not tasks:
        print("[spawner] No tasks to run; exiting.")
        return 0

    # Budget is tracked externally by the engine; we pass a per-task budget hint.
    per_task_budget = (budget_total / max(len(tasks), 1)) if budget_total > 0 else 0.0

    q: Queue[Dict[str, Any]] = Queue()
    for t in tasks:
        q.put(t)

    print(
        f"[spawner] Starting: sessions={sessions} tasks={len(tasks)} "
        f"workspace={workspace} model={model} engine={engine_type.value}"
    )

    # One pass over the queue; for "persistent" operation, the control panel can restart.
    with ThreadPoolExecutor(max_workers=sessions) as pool:
        for worker_id in range(sessions):
            pool.submit(_worker_loop, worker_id, q, workspace, per_task_budget, model, engine_type)

        # Wait for completion or halt.
        while True:
            should_halt, reason = _should_halt(workspace)
            if should_halt:
                print(f"[spawner] HALT detected. Reason: {reason or ''}".strip())
                break
            if q.unfinished_tasks == 0:
                break
            time.sleep(0.5)

    print("[spawner] Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

