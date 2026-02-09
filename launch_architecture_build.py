#!/usr/bin/env python3
"""
Launch the Swarm Architecture V2 build.

This script kicks off autonomous construction of the multi-node
intelligent orchestration system defined in SWARM_ARCHITECTURE_V2.md.

Safety: Runs through self_healing_wrapper.py with checkpoints,
rollback, and crash loop detection.

Usage:
    python launch_architecture_build.py [--phase N] [--dry-run]
"""

import json
import subprocess
import sys
from pathlib import Path

# Configuration
TASKS_FILE = "grind_tasks_architecture.json"
WRAPPER = "self_healing_wrapper.py"
BLUEPRINT = "SWARM_ARCHITECTURE_V2.md"
GAP_ANALYSIS = "ARCHITECTURE_GAP_ANALYSIS.md"

META_PROMPT = """
You are building the Swarm Architecture V2.

BEFORE ANYTHING: Read these files to understand the full picture:
1. SWARM_ARCHITECTURE_V2.md - The complete architecture specification
2. ARCHITECTURE_GAP_ANALYSIS.md - What's already built vs missing
3. founding_memory.md - Core principles and values

YOUR MISSION: Build the architecture components defined in grind_tasks_architecture.json.

PHASES (build in order):
1. Core Flow: Atomizer, Worker Pool, Intent Gatekeeper, Gut-Check Planner, Critic
2. Intelligence: Expert Node, Expert Cache, RPM Tracker
3. Quality: Feature Breakdown, Feature Planner, Consensus Node
4. Tool-First: Tool Store, Tool-First Router
5. User Modeling: User Proxy V2
6. Learning: RLIF Rule Extractor, Rule Verifier, Efficiency Observer
7. Integration: Test Gates, Full Orchestrator

FOR EACH TASK:
1. Read the task description carefully
2. Read the relevant section in SWARM_ARCHITECTURE_V2.md
3. Build the component following the spec exactly
4. Verify it works (syntax valid, imports resolve, basic functionality)
5. Update PROGRESS.md with what you built
6. Move to next task respecting dependencies

CONSTRAINTS:
- Safety rails are ACTIVE (self_healing_wrapper.py)
- If you break something 3x, STOP and document the blocker
- Don't skip dependencies - they're there for a reason
- Test each component before moving on
- Check existing code before writing - don't duplicate

WORK ETHIC (from founding_memory.md):
- When there's work to do, do it well
- Growth compounds only when the work is real
- Values enacted are values held

You have permission to create files, modify code, and build the architecture.
This is your launchpad. Build it well.
"""


def load_tasks(phase_filter=None):
    """Load tasks from the architecture task file."""
    with open(TASKS_FILE, 'r') as f:
        data = json.load(f)

    tasks = data.get('tasks', [])

    if phase_filter is not None:
        tasks = [t for t in tasks if t.get('phase') == phase_filter]

    return tasks


def check_dependencies(task, completed):
    """Check if task dependencies are satisfied."""
    deps = task.get('dependencies', [])
    return all(d in completed for d in deps)


def get_ready_tasks(tasks, completed):
    """Get tasks that are ready to run (dependencies satisfied)."""
    ready = []
    for task in tasks:
        if task['id'] not in completed and check_dependencies(task, completed):
            ready.append(task)
    return ready


def run_with_wrapper(task):
    """Run a task through the self-healing wrapper."""
    print(f"\n{'='*60}")
    print(f"TASK: {task['id']} - {task['component']}")
    print(f"{'='*60}")
    print(f"Description: {task['description'][:100]}...")
    print(f"Output: {task.get('output_file', 'N/A')}")
    print(f"Budget: ${task.get('budget', 0.10):.2f}")
    print()

    # Build the prompt for this specific task
    task_prompt = f"""
{META_PROMPT}

CURRENT TASK:
- ID: {task['id']}
- Component: {task['component']}
- Description: {task['description']}
- Output File: {task.get('output_file', 'N/A')}
- Budget: ${task.get('budget', 0.10):.2f}

Build this component now. Follow the spec in SWARM_ARCHITECTURE_V2.md.
"""

    # Write prompt to temp file for the spawner
    prompt_file = Path('.current_task_prompt.txt')
    prompt_file.write_text(task_prompt)

    # Run through self-healing wrapper
    result = subprocess.run(
        [sys.executable, WRAPPER, '--task-file', str(prompt_file)],
        capture_output=False
    )

    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Launch Architecture V2 Build')
    parser.add_argument('--phase', type=int, help='Only run tasks from this phase')
    parser.add_argument('--dry-run', action='store_true', help='Show tasks without running')
    parser.add_argument('--task', type=str, help='Run a specific task by ID')
    args = parser.parse_args()

    print("=" * 60)
    print("  SWARM ARCHITECTURE V2 BUILD")
    print("  Blueprint: SWARM_ARCHITECTURE_V2.md")
    print("  Safety: self_healing_wrapper.py ACTIVE")
    print("=" * 60)

    tasks = load_tasks(args.phase)
    print(f"\nLoaded {len(tasks)} tasks" + (f" (phase {args.phase})" if args.phase else ""))

    if args.dry_run:
        print("\n[DRY RUN] Tasks to execute:\n")
        for t in tasks:
            deps = ', '.join(t.get('dependencies', [])) or 'none'
            print(f"  [{t['id']}] {t['component']}")
            print(f"      Phase: {t['phase']} | Budget: ${t.get('budget', 0.10):.2f} | Deps: {deps}")
        return

    if args.task:
        # Run single task
        task = next((t for t in tasks if t['id'] == args.task), None)
        if not task:
            print(f"Task {args.task} not found")
            return
        run_with_wrapper(task)
        return

    # Run all tasks respecting dependencies
    completed = set()
    failed = set()

    while True:
        ready = get_ready_tasks(tasks, completed | failed)
        if not ready:
            break

        # Run first ready task (could parallelize here later)
        task = ready[0]
        success = run_with_wrapper(task)

        if success:
            completed.add(task['id'])
            print(f"\n✓ {task['id']} COMPLETE")
        else:
            failed.add(task['id'])
            print(f"\n✗ {task['id']} FAILED")

    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)
    print(f"Completed: {len(completed)}/{len(tasks)}")
    print(f"Failed: {len(failed)}")
    if failed:
        print(f"Failed tasks: {', '.join(failed)}")


if __name__ == '__main__':
    main()
