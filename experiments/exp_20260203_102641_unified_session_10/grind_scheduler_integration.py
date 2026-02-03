"""
Integration of Task Dependency Scheduler with grind_spawner.py
Enables dependency-aware parallel execution of grind tasks.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

from task_scheduler import TaskScheduler, Task, TaskStatus


class GrindTaskScheduler:
    """
    Integrates task_scheduler.py with grind_spawner.py for dependency-aware execution.
    """

    def __init__(self, workspace: Path, max_concurrent: int = 3):
        self.workspace = workspace
        self.scheduler = TaskScheduler(max_concurrent=max_concurrent)
        self.grind_sessions: Dict[str, 'GrindSession'] = {}

        # Set task executor
        self.scheduler.set_task_executor(self._execute_grind_task)

    def add_grind_task(self, task_id: str, description: str, model: str = "sonnet",
                      budget: float = 0.05, explicit_deps: Optional[Set[str]] = None):
        """Add a grind task with dependency detection."""

        # Auto-detect dependencies from task description
        task = self.scheduler.add_task(task_id, description, explicit_deps)

        # Store grind-specific parameters
        task.grind_params = {
            "model": model,
            "budget": budget,
            "workspace": str(self.workspace)
        }

        return task

    async def _execute_grind_task(self, task: Task) -> str:
        """Execute a single grind task using GrindSession."""

        # Import here to avoid circular dependencies
        from grind_spawner import GrindSession

        params = getattr(task, 'grind_params', {})
        model = params.get("model", "sonnet")
        budget = params.get("budget", 0.05)

        # Create and run grind session
        session = GrindSession(
            session_id=hash(task.id) % 10000,  # Generate deterministic ID
            model=model,
            budget=budget,
            workspace=self.workspace,
            task=task.description
        )

        self.grind_sessions[task.id] = session

        try:
            # Run the grind session once
            result = session.run_once()

            # Check for success/failure
            if result.get("returncode", 0) == 0:
                return f"Task {task.id} completed successfully"
            else:
                error_msg = result.get("error", "Unknown error")
                raise Exception(f"Task {task.id} failed: {error_msg}")

        except Exception as e:
            raise Exception(f"Grind execution failed for {task.id}: {str(e)}")

        finally:
            # Cleanup session reference
            if task.id in self.grind_sessions:
                del self.grind_sessions[task.id]

    async def run_all_tasks(self) -> Dict[str, TaskStatus]:
        """Execute all tasks with dependency management."""
        print("🚀 Starting dependency-aware grind execution...")

        # Log initial state
        print(self.scheduler.get_progress_visualization())

        # Run scheduler
        results = await self.scheduler.run_scheduler()

        # Log final state
        print("\n" + self.scheduler.get_progress_visualization())
        print(f"\n✅ Execution complete. Results: {results}")

        return results

    def load_tasks_from_json(self, tasks_file: Path) -> int:
        """Load tasks from a JSON file with dependency detection."""

        if not tasks_file.exists():
            print(f"❌ Task file not found: {tasks_file}")
            return 0

        with open(tasks_file, 'r') as f:
            tasks_data = json.load(f)

        count = 0
        for task_entry in tasks_data.get("tasks", []):
            task_id = task_entry.get("id")
            description = task_entry.get("description", "")
            model = task_entry.get("model", "sonnet")
            budget = task_entry.get("budget", 0.05)
            explicit_deps = set(task_entry.get("dependencies", []))

            if task_id and description:
                self.add_grind_task(
                    task_id=task_id,
                    description=description,
                    model=model,
                    budget=budget,
                    explicit_deps=explicit_deps
                )
                count += 1

        print(f"📋 Loaded {count} tasks from {tasks_file}")
        return count

    def export_results(self, output_file: Path):
        """Export scheduler results to JSON."""

        state = self.scheduler.export_state()

        # Add execution metadata
        state["execution_metadata"] = {
            "workspace": str(self.workspace),
            "execution_time": datetime.now().isoformat(),
            "total_tasks": len(self.scheduler.dependency_graph.tasks),
            "completed_tasks": len([t for t in self.scheduler.dependency_graph.tasks.values()
                                  if t.status == TaskStatus.COMPLETED])
        }

        with open(output_file, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"💾 Results exported to {output_file}")

    def get_task_progress(self) -> Dict:
        """Get current task progress for monitoring."""

        tasks = self.scheduler.dependency_graph.tasks

        return {
            "total": len(tasks),
            "completed": len([t for t in tasks.values() if t.status == TaskStatus.COMPLETED]),
            "running": len([t for t in tasks.values() if t.status == TaskStatus.RUNNING]),
            "failed": len([t for t in tasks.values() if t.status == TaskStatus.FAILED]),
            "ready": len(self.scheduler.dependency_graph.get_ready_tasks()),
            "blocked": len(self.scheduler.dependency_graph.get_blocked_tasks()),
            "visualization": self.scheduler.get_progress_visualization()
        }


# CLI Integration
async def run_grind_with_dependencies(workspace: Path, tasks_file: Path,
                                    max_concurrent: int = 3, output_file: Optional[Path] = None):
    """
    Main function to run grind spawner with dependency management.

    Args:
        workspace: Path to the workspace directory
        tasks_file: JSON file containing task definitions
        max_concurrent: Maximum concurrent grind sessions
        output_file: Optional file to export results
    """

    scheduler = GrindTaskScheduler(workspace, max_concurrent=max_concurrent)

    # Load tasks
    task_count = scheduler.load_tasks_from_json(tasks_file)
    if task_count == 0:
        print("❌ No tasks loaded, exiting")
        return

    # Run execution
    try:
        results = await scheduler.run_all_tasks()

        # Export results if requested
        if output_file:
            scheduler.export_results(output_file)

        return results

    except Exception as e:
        print(f"❌ Execution failed: {e}")
        raise


# Example usage
def create_example_tasks_file(output_path: Path):
    """Create an example tasks file with dependencies."""

    example_tasks = {
        "tasks": [
            {
                "id": "SETUP_ENV",
                "description": "Initialize the development environment",
                "model": "sonnet",
                "budget": 0.03
            },
            {
                "id": "BUILD_CORE",
                "description": "PREREQUISITE: SETUP_ENV must exist. Build core functionality",
                "model": "sonnet",
                "budget": 0.05
            },
            {
                "id": "ADD_TESTS",
                "description": "depends on BUILD_CORE. Add comprehensive tests",
                "model": "sonnet",
                "budget": 0.04
            },
            {
                "id": "WRITE_DOCS",
                "description": "requires BUILD_CORE. Create documentation",
                "model": "haiku",
                "budget": 0.02
            },
            {
                "id": "DEPLOY_APP",
                "description": "PREREQUISITE: ADD_TESTS and WRITE_DOCS must exist. Deploy application",
                "model": "sonnet",
                "budget": 0.06,
                "dependencies": ["ADD_TESTS", "WRITE_DOCS"]
            }
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(example_tasks, f, indent=2)

    print(f"📝 Example tasks file created: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run grind spawner with dependency management")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(),
                       help="Workspace directory")
    parser.add_argument("--tasks", type=Path, required=True,
                       help="JSON file with task definitions")
    parser.add_argument("--max-concurrent", type=int, default=3,
                       help="Maximum concurrent sessions")
    parser.add_argument("--output", type=Path,
                       help="Output file for results")
    parser.add_argument("--example", action="store_true",
                       help="Create example tasks file")

    args = parser.parse_args()

    if args.example:
        create_example_tasks_file(args.tasks)
    else:
        asyncio.run(run_grind_with_dependencies(
            workspace=args.workspace,
            tasks_file=args.tasks,
            max_concurrent=args.max_concurrent,
            output_file=args.output
        ))