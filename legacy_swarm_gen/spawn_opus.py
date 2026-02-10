#!/usr/bin/env python3
"""
Spawn Opus research instances.

Usage:
    py spawn_opus.py                    # Run opus_research_tasks.json
    py spawn_opus.py --task "custom"    # Run single custom task
    py spawn_opus.py --tasks file.json  # Run tasks from specific file
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = REPO_ROOT

def spawn_opus_researchers(tasks_file: str = "opus_research_tasks.json"):
    """Spawn Opus instances from task file."""
    tasks_path = WORKSPACE / tasks_file

    if not tasks_path.exists():
        print(f"Error: {tasks_path} not found")
        return 1

    print(f"Spawning Opus researchers from {tasks_file}...")

    # Use grind_spawner with opus model
    cmd = [
        sys.executable,  # Use same Python that ran this script
        str(WORKSPACE / "grind_spawner.py"),
        "--delegate",
        "--model", "opus",
        "--once"
    ]

    # Temporarily swap task file
    grind_tasks = WORKSPACE / "grind_tasks.json"
    backup = None

    if grind_tasks.exists():
        backup = grind_tasks.read_text()

    try:
        # Copy opus tasks to grind_tasks.json
        grind_tasks.write_text(tasks_path.read_text())

        # Run spawner
        result = subprocess.run(cmd, cwd=str(WORKSPACE))
        return result.returncode

    finally:
        # Restore original grind_tasks.json
        if backup:
            grind_tasks.write_text(backup)


def spawn_single_opus(task: str, budget: float = 5.0):
    """Spawn single Opus instance with custom task."""
    import json

    tasks_file = WORKSPACE / "grind_tasks.json"
    backup = None

    if tasks_file.exists():
        backup = tasks_file.read_text()

    try:
        # Create temporary task file
        tasks_file.write_text(json.dumps([{
            "task": task,
            "budget": budget,
            "model": "opus"
        }], indent=2))

        cmd = [
            sys.executable,
            str(WORKSPACE / "grind_spawner.py"),
            "--delegate",
            "--model", "opus",
            "--once"
        ]

        result = subprocess.run(cmd, cwd=str(WORKSPACE))
        return result.returncode

    finally:
        if backup:
            tasks_file.write_text(backup)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spawn Opus research instances")
    parser.add_argument("--tasks", default="opus_research_tasks.json",
                        help="Task file to use (default: opus_research_tasks.json)")
    parser.add_argument("--task", type=str,
                        help="Single custom task to run")
    parser.add_argument("--budget", type=float, default=5.0,
                        help="Budget for single task (default: $5.00)")

    args = parser.parse_args()

    if args.task:
        sys.exit(spawn_single_opus(args.task, args.budget))
    else:
        sys.exit(spawn_opus_researchers(args.tasks))
