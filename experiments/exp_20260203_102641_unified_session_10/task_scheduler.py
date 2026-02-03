"""
Task Dependency Scheduler
Manages task dependencies and enables parallel execution of independent tasks.
"""

import asyncio
import re
import json
import time
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    id: str
    description: str
    dependencies: Set[str] = field(default_factory=set)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class DependencyGraph:
    """Manages task dependencies and provides topological ordering."""

    def __init__(self):
        self.graph: Dict[str, Set[str]] = defaultdict(set)  # task_id -> dependencies
        self.reverse_graph: Dict[str, Set[str]] = defaultdict(set)  # task_id -> dependents
        self.tasks: Dict[str, Task] = {}

    def add_task(self, task: Task):
        """Add a task to the dependency graph."""
        self.tasks[task.id] = task

        # Update graph structures
        for dep in task.dependencies:
            self.graph[task.id].add(dep)
            self.reverse_graph[dep].add(task.id)

    def remove_task(self, task_id: str):
        """Remove a task and update dependencies."""
        if task_id not in self.tasks:
            return

        # Remove from dependents
        for dep in self.graph[task_id]:
            self.reverse_graph[dep].discard(task_id)

        # Remove from dependencies
        for dependent in self.reverse_graph[task_id]:
            self.graph[dependent].discard(task_id)

        del self.graph[task_id]
        del self.reverse_graph[task_id]
        del self.tasks[task_id]

    def get_ready_tasks(self) -> List[str]:
        """Get tasks that have all dependencies completed."""
        ready_tasks = []

        for task_id, task in self.tasks.items():
            if task.status != TaskStatus.PENDING:
                continue

            # Check if all dependencies are completed
            all_deps_completed = True
            for dep_id in task.dependencies:
                dep_task = self.tasks.get(dep_id)
                if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                    all_deps_completed = False
                    break

            if all_deps_completed:
                ready_tasks.append(task_id)

        return ready_tasks

    def get_blocked_tasks(self) -> List[str]:
        """Get tasks blocked by unmet dependencies."""
        blocked = []

        for task_id, task in self.tasks.items():
            if task.status != TaskStatus.PENDING:
                continue

            # Check for unmet dependencies
            for dep_id in task.dependencies:
                dep_task = self.tasks.get(dep_id)
                if not dep_task or dep_task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                    blocked.append(task_id)
                    break

        return blocked

    def has_cycles(self) -> bool:
        """Check for circular dependencies using DFS."""
        visited = set()
        rec_stack = set()

        def dfs(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False

            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph[node]:
                if dfs(neighbor):
                    return True

            rec_stack.remove(node)
            return False

        for task_id in self.tasks:
            if task_id not in visited:
                if dfs(task_id):
                    return True
        return False

    def topological_sort(self) -> List[str]:
        """Return tasks in topological order."""
        in_degree = {task_id: len(deps) for task_id, deps in self.graph.items()}
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            task_id = queue.popleft()
            result.append(task_id)

            for dependent in self.reverse_graph[task_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return result


class TaskScheduler:
    """Main task scheduler with dependency management and parallel execution."""

    def __init__(self, max_concurrent: int = 3):
        self.dependency_graph = DependencyGraph()
        self.max_concurrent = max_concurrent
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_executor = None  # Will be set by integration

        # Dependency detection patterns
        self.dependency_patterns = [
            r"(?:requires?|needs?|depends? on|after)\s+([A-Z_][A-Z0-9_]*)",
            r"(?:prerequisite|precondition):\s*([A-Z_][A-Z0-9_]*)",
            r"PREREQUISITE:\s*([A-Z_][A-Z0-9_]*)",
            r"@depends\(([^)]+)\)",
            r"#depends:\s*([A-Z_][A-Z0-9_]*)"
        ]

    def auto_detect_dependencies(self, task_description: str) -> Set[str]:
        """Automatically detect dependencies from task text."""
        dependencies = set()

        # Apply regex patterns
        for pattern in self.dependency_patterns:
            matches = re.findall(pattern, task_description, re.IGNORECASE)
            for match in matches:
                # Clean up the dependency name
                dep = match.strip().upper()
                if dep:
                    dependencies.add(dep)

        # Look for file dependencies
        file_deps = re.findall(r"([A-Z_][A-Z0-9_]*\.(?:md|py|json))\s+must exist",
                              task_description, re.IGNORECASE)
        for file_dep in file_deps:
            dependencies.add(file_dep.upper())

        return dependencies

    def add_task(self, task_id: str, description: str, explicit_deps: Optional[Set[str]] = None):
        """Add a task with automatic and explicit dependency detection."""
        auto_deps = self.auto_detect_dependencies(description)

        # Combine explicit and auto-detected dependencies
        all_deps = set()
        if explicit_deps:
            all_deps.update(explicit_deps)
        all_deps.update(auto_deps)

        task = Task(
            id=task_id,
            description=description,
            dependencies=all_deps
        )

        self.dependency_graph.add_task(task)
        return task

    def set_task_executor(self, executor_func):
        """Set the function that executes individual tasks."""
        self.task_executor = executor_func

    async def execute_task(self, task_id: str) -> bool:
        """Execute a single task."""
        task = self.dependency_graph.tasks.get(task_id)
        if not task or not self.task_executor:
            return False

        task.status = TaskStatus.RUNNING
        task.start_time = time.time()

        try:
            # Call the external task executor
            result = await self.task_executor(task)

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.end_time = time.time()
            return True

        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.end_time = time.time()
            return False

    async def run_scheduler(self) -> Dict[str, TaskStatus]:
        """Main scheduler loop - executes tasks with dependency management."""

        # Check for cycles first
        if self.dependency_graph.has_cycles():
            raise ValueError("Circular dependencies detected!")

        total_tasks = len(self.dependency_graph.tasks)
        completed_count = 0

        while completed_count < total_tasks:
            # Get ready tasks
            ready_tasks = self.dependency_graph.get_ready_tasks()

            # Start new tasks up to max concurrent limit
            available_slots = self.max_concurrent - len(self.running_tasks)
            tasks_to_start = ready_tasks[:available_slots]

            for task_id in tasks_to_start:
                task_coro = self.execute_task(task_id)
                self.running_tasks[task_id] = asyncio.create_task(task_coro)

            # Wait for any running task to complete
            if self.running_tasks:
                done, pending = await asyncio.wait(
                    self.running_tasks.values(),
                    return_when=asyncio.FIRST_COMPLETED
                )

                # Process completed tasks
                for completed_task in done:
                    # Find the task ID
                    completed_task_id = None
                    for tid, task_obj in self.running_tasks.items():
                        if task_obj == completed_task:
                            completed_task_id = tid
                            break

                    if completed_task_id:
                        del self.running_tasks[completed_task_id]
                        completed_count += 1

                        # Log completion
                        task = self.dependency_graph.tasks[completed_task_id]
                        print(f"âœ“ Task {completed_task_id} completed in {task.duration():.2f}s")

            # Check for deadlock (no ready tasks, no running tasks)
            if not ready_tasks and not self.running_tasks:
                blocked_tasks = self.dependency_graph.get_blocked_tasks()
                if blocked_tasks:
                    raise RuntimeError(f"Deadlock detected! Blocked tasks: {blocked_tasks}")
                break

            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)

        # Return final status
        return {task_id: task.status for task_id, task in self.dependency_graph.tasks.items()}

    def get_progress_visualization(self) -> str:
        """Generate a text-based progress visualization."""
        lines = []
        lines.append("=== TASK DEPENDENCY PROGRESS ===")

        # Group tasks by status
        by_status = defaultdict(list)
        for task_id, task in self.dependency_graph.tasks.items():
            by_status[task.status].append(task)

        # Show counts
        total = len(self.dependency_graph.tasks)
        completed = len(by_status[TaskStatus.COMPLETED])
        running = len(by_status[TaskStatus.RUNNING])
        ready = len([t for t in by_status[TaskStatus.PENDING]
                    if t.id in self.dependency_graph.get_ready_tasks()])
        blocked = len(self.dependency_graph.get_blocked_tasks())

        lines.append(f"Progress: {completed}/{total} completed ({completed/total*100:.1f}%)")
        lines.append(f"Running: {running}, Ready: {ready}, Blocked: {blocked}")
        lines.append("")

        # Show dependency graph
        lines.append("Dependencies:")
        for task_id, task in self.dependency_graph.tasks.items():
            status_symbol = {
                TaskStatus.COMPLETED: "âœ“",
                TaskStatus.RUNNING: "âŸ³",
                TaskStatus.READY: "â—‹",
                TaskStatus.PENDING: "â—‹",
                TaskStatus.FAILED: "âœ—",
                TaskStatus.BLOCKED: "â§—"
            }.get(task.status, "?")

            deps_str = f" (deps: {', '.join(task.dependencies)})" if task.dependencies else ""
            lines.append(f"  {status_symbol} {task_id}{deps_str}")

        return "\n".join(lines)

    def export_state(self) -> Dict:
        """Export scheduler state for persistence."""
        return {
            "tasks": {
                task_id: {
                    "description": task.description,
                    "dependencies": list(task.dependencies),
                    "status": task.status.value,
                    "result": task.result,
                    "error": task.error,
                    "start_time": task.start_time,
                    "end_time": task.end_time
                }
                for task_id, task in self.dependency_graph.tasks.items()
            },
            "max_concurrent": self.max_concurrent
        }

    def import_state(self, state: Dict):
        """Import scheduler state from persistence."""
        self.max_concurrent = state.get("max_concurrent", 3)

        for task_id, task_data in state.get("tasks", {}).items():
            task = Task(
                id=task_id,
                description=task_data["description"],
                dependencies=set(task_data["dependencies"]),
                status=TaskStatus(task_data["status"]),
                result=task_data.get("result"),
                error=task_data.get("error"),
                start_time=task_data.get("start_time"),
                end_time=task_data.get("end_time")
            )
            self.dependency_graph.add_task(task)


# Integration helper functions
async def example_task_executor(task: Task) -> str:
    """Example task executor - replace with actual implementation."""
    print(f"Executing task: {task.id}")
    await asyncio.sleep(1)  # Simulate work
    return f"Task {task.id} completed"


async def main():
    """Example usage of the task scheduler."""
    scheduler = TaskScheduler(max_concurrent=2)
    scheduler.set_task_executor(example_task_executor)

    # Add some example tasks
    scheduler.add_task("TASK_A", "Initialize the system")
    scheduler.add_task("TASK_B", "PREREQUISITE: TASK_A must exist. Setup database")
    scheduler.add_task("TASK_C", "depends on TASK_A. Configure API")
    scheduler.add_task("TASK_D", "requires TASK_B and TASK_C. Deploy application")

    # Run the scheduler
    print("Starting task scheduler...")
    results = await scheduler.run_scheduler()

    print("\n" + scheduler.get_progress_visualization())
    print(f"\nFinal results: {results}")


if __name__ == "__main__":
    asyncio.run(main())