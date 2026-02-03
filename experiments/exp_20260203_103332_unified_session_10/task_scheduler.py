"""
Task Dependency Scheduler
Handles dependency-aware task scheduling with parallel execution and progress tracking.
"""

import re
import json
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Callable, Any
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
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    executor_func: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class DependencyGraph:
    """Manages task dependencies and topological ordering."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.dependents: Dict[str, Set[str]] = defaultdict(set)  # task_id -> who depends on it

    def add_task(self, task: Task):
        """Add a task to the dependency graph."""
        self.tasks[task.id] = task

        # Update dependents mapping
        for dep_id in task.dependencies:
            self.dependents[dep_id].add(task.id)

    def remove_task(self, task_id: str):
        """Remove a task from the dependency graph."""
        if task_id not in self.tasks:
            return

        task = self.tasks[task_id]

        # Remove from dependents of its dependencies
        for dep_id in task.dependencies:
            self.dependents[dep_id].discard(task_id)

        # Remove its dependents mapping
        del self.dependents[task_id]

        # Remove the task itself
        del self.tasks[task_id]

    def get_ready_tasks(self) -> List[Task]:
        """Get tasks that are ready to run (all dependencies satisfied)."""
        ready_tasks = []

        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are completed
                deps_satisfied = all(
                    self.tasks.get(dep_id, Task("")).status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )

                if deps_satisfied:
                    task.status = TaskStatus.READY
                    ready_tasks.append(task)
                elif any(
                    self.tasks.get(dep_id, Task("")).status == TaskStatus.FAILED
                    for dep_id in task.dependencies
                ):
                    task.status = TaskStatus.BLOCKED

        return ready_tasks

    def has_circular_dependencies(self) -> bool:
        """Check for circular dependencies using DFS."""
        visited = set()
        rec_stack = set()

        def has_cycle(task_id: str) -> bool:
            if task_id in rec_stack:
                return True
            if task_id in visited:
                return False

            visited.add(task_id)
            rec_stack.add(task_id)

            task = self.tasks.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    if has_cycle(dep_id):
                        return True

            rec_stack.remove(task_id)
            return False

        for task_id in self.tasks:
            if task_id not in visited:
                if has_cycle(task_id):
                    return True
        return False

    def get_dependency_visualization(self) -> Dict[str, Any]:
        """Generate dependency visualization data."""
        nodes = []
        edges = []

        for task in self.tasks.values():
            nodes.append({
                "id": task.id,
                "label": task.description[:50] + "..." if len(task.description) > 50 else task.description,
                "status": task.status.value,
                "metadata": task.metadata
            })

            for dep_id in task.dependencies:
                edges.append({
                    "from": dep_id,
                    "to": task.id
                })

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total": len(self.tasks),
                "pending": len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
                "ready": len([t for t in self.tasks.values() if t.status == TaskStatus.READY]),
                "running": len([t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]),
                "completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
                "failed": len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED]),
                "blocked": len([t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED])
            }
        }


class TaskScheduler:
    """Dependency-aware task scheduler with parallel execution."""

    def __init__(self, max_concurrent_tasks: int = 4):
        self.graph = DependencyGraph()
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[str, threading.Thread] = {}
        self.lock = threading.Lock()
        self.completion_callbacks: List[Callable] = []
        self.is_running = False

    def add_task(self, task_id: str, description: str, dependencies: Optional[List[str]] = None,
                 executor_func: Optional[Callable] = None, metadata: Optional[Dict] = None):
        """Add a task to the scheduler."""
        task = Task(
            id=task_id,
            description=description,
            dependencies=set(dependencies or []),
            executor_func=executor_func,
            metadata=metadata or {}
        )

        # Auto-detect dependencies from task text
        auto_deps = self._auto_detect_dependencies(description)
        task.dependencies.update(auto_deps)

        self.graph.add_task(task)
        return task

    def _auto_detect_dependencies(self, description: str) -> Set[str]:
        """Auto-detect task dependencies from description text."""
        dependencies = set()

        # Pattern: "requires X" or "depends on X" or "needs X"
        patterns = [
            r"requires?\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            r"depends?\s+on\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            r"needs?\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            r"after\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            r"wait\s+for\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            dependencies.update(matches)

        return dependencies

    def remove_task(self, task_id: str):
        """Remove a task from the scheduler."""
        with self.lock:
            self.graph.remove_task(task_id)

    def start(self):
        """Start the task scheduler."""
        if self.is_running:
            return

        if self.graph.has_circular_dependencies():
            raise ValueError("Circular dependencies detected in task graph")

        self.is_running = True
        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        scheduler_thread.start()

    def stop(self):
        """Stop the task scheduler."""
        self.is_running = False

    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.is_running:
            with self.lock:
                # Clean up completed threads
                completed_threads = [tid for tid, thread in self.running_tasks.items() if not thread.is_alive()]
                for tid in completed_threads:
                    del self.running_tasks[tid]

                # Get ready tasks
                ready_tasks = self.graph.get_ready_tasks()

                # Start new tasks if we have capacity
                available_slots = self.max_concurrent_tasks - len(self.running_tasks)
                tasks_to_start = ready_tasks[:available_slots]

                for task in tasks_to_start:
                    thread = threading.Thread(target=self._execute_task, args=(task,), daemon=True)
                    thread.start()
                    self.running_tasks[task.id] = thread
                    task.status = TaskStatus.RUNNING
                    task.started_at = time.time()

            # Check if all tasks are done
            if self._all_tasks_done():
                break

            time.sleep(0.1)  # Short sleep to prevent busy waiting

    def _execute_task(self, task: Task):
        """Execute a single task."""
        try:
            if task.executor_func:
                task.result = task.executor_func(task)
            else:
                # Default execution - just mark as completed
                time.sleep(0.1)  # Simulate work
                task.result = f"Completed: {task.description}"

            with self.lock:
                task.status = TaskStatus.COMPLETED
                task.completed_at = time.time()

        except Exception as e:
            with self.lock:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = time.time()

        # Notify completion callbacks
        for callback in self.completion_callbacks:
            try:
                callback(task)
            except Exception:
                pass  # Don't let callback errors break the scheduler

    def _all_tasks_done(self) -> bool:
        """Check if all tasks are in a terminal state."""
        terminal_states = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.BLOCKED}
        return all(task.status in terminal_states for task in self.graph.tasks.values())

    def wait_for_completion(self, timeout: Optional[float] = None):
        """Wait for all tasks to complete."""
        start_time = time.time()

        while not self._all_tasks_done():
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError("Tasks did not complete within timeout")
            time.sleep(0.1)

    def get_status(self) -> Dict[str, Any]:
        """Get current scheduler status."""
        with self.lock:
            return {
                "is_running": self.is_running,
                "running_tasks": len(self.running_tasks),
                "max_concurrent": self.max_concurrent_tasks,
                "dependency_graph": self.graph.get_dependency_visualization()
            }

    def add_completion_callback(self, callback: Callable[[Task], None]):
        """Add a callback to be called when tasks complete."""
        self.completion_callbacks.append(callback)

    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get history of all tasks with timing information."""
        history = []

        for task in self.graph.tasks.values():
            duration = None
            if task.started_at and task.completed_at:
                duration = task.completed_at - task.started_at

            history.append({
                "id": task.id,
                "description": task.description,
                "status": task.status.value,
                "dependencies": list(task.dependencies),
                "started_at": task.started_at,
                "completed_at": task.completed_at,
                "duration": duration,
                "result": task.result,
                "error": task.error,
                "metadata": task.metadata
            })

        return history


def integrate_with_grind_spawner(grind_spawner_instance, scheduler: TaskScheduler):
    """Integration function to connect TaskScheduler with grind_spawner.py"""

    def task_executor(task: Task):
        """Execute a grind task using the spawner."""
        if hasattr(grind_spawner_instance, 'execute_task'):
            return grind_spawner_instance.execute_task(task.metadata.get('grind_config', {}))
        else:
            # Fallback execution
            return f"Executed grind task: {task.description}"

    def add_grind_task(task_id: str, description: str, grind_config: Dict, dependencies: Optional[List[str]] = None):
        """Add a grind task to the scheduler."""
        return scheduler.add_task(
            task_id=task_id,
            description=description,
            dependencies=dependencies,
            executor_func=task_executor,
            metadata={'grind_config': grind_config}
        )

    # Add the integration method to the scheduler
    scheduler.add_grind_task = add_grind_task

    return scheduler


# Example usage and testing
if __name__ == "__main__":
    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=2)

    # Add some example tasks with dependencies
    scheduler.add_task("task1", "Initialize system", [])
    scheduler.add_task("task2", "Load configuration requires task1", ["task1"])
    scheduler.add_task("task3", "Setup database depends on task1", ["task1"])
    scheduler.add_task("task4", "Start server needs task2 and task3", ["task2", "task3"])

    # Add completion callback for logging
    def log_completion(task: Task):
        print(f"Task {task.id} completed with status {task.status.value}")

    scheduler.add_completion_callback(log_completion)

    # Start scheduler and wait for completion
    print("Starting task scheduler...")
    scheduler.start()

    try:
        scheduler.wait_for_completion(timeout=10)
        print("\nAll tasks completed!")

        # Print final status
        status = scheduler.get_status()
        print(f"Final status: {json.dumps(status, indent=2)}")

    except TimeoutError:
        print("Tasks timed out!")
    finally:
        scheduler.stop()