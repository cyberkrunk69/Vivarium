"""
Smart Executor Runner - Dynamic Dependency Resolution

Run this with: python run_smart_executor.py

Tasks run in parallel, automatically detect dependencies,
spawn subtasks when needed, and resume when blocked.
"""

import sys
import json
from pathlib import Path

# Ensure we're in the right directory
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from smart_executor import SmartExecutor
from inference_engine import EngineType
import os


def main():
    print("=" * 60)
    print("  SMART SWARM - Dynamic Dependency Resolution")
    print("=" * 60)
    print()
    print("Tasks run in parallel, automatically detect dependencies,")
    print("spawn subtasks when needed, and resume when blocked.")
    print()

    # Determine engine from environment
    env_engine = os.environ.get("INFERENCE_ENGINE", "claude").lower()
    if env_engine == "groq":
        engine_type = EngineType.GROQ
        print(f"Engine: GROQ")
    else:
        engine_type = EngineType.CLAUDE
        print(f"Engine: CLAUDE")

    # Load tasks
    tasks_file = script_dir / "grind_tasks.json"
    if not tasks_file.exists():
        print(f"ERROR: {tasks_file} not found!")
        return 1

    tasks = json.loads(tasks_file.read_text())
    print(f"Loaded {len(tasks)} tasks")
    print("-" * 60)

    # Create executor
    executor = SmartExecutor(
        workspace=script_dir,
        max_parallel=4,
        engine_type=engine_type
    )

    # Add all tasks
    for i, t in enumerate(tasks):
        task_text = t.get("task", "")
        desc = task_text.split("\n")[0][:50]
        outputs = []

        # Extract expected outputs from task text
        if "OUTPUT:" in task_text:
            output_line = task_text.split("OUTPUT:")[1].split("\n")[0]
            outputs = [f.strip() for f in output_line.split(",") if f.strip()]

        executor.add_task(
            description=desc,
            task_text=task_text,
            outputs=outputs
        )
        print(f"  [{i+1}] {desc}")

    print()

    # Run
    try:
        executor.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())
