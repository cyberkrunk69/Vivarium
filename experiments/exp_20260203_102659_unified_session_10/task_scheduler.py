"""
Task Dependency Scheduler

Implements dependency-aware task scheduling with parallel execution,
auto-detection of dependencies, and progress visualization.
"""

import json
import re
import time
import threading
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import logging

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
    content: str
    dependencies: Set[str] = field(default_factory=set)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    worker_id: Optional[str] = None

    def duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

class DependencyGraph:
    """Manages task dependencies and topological ordering."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.dependents: Dict[str, Set[str]] = defaultdict(set)
        self.dependency_patterns = [
            # Explicit dependency patterns
            r'depends on (\w+)',
            r'requires (\w+)',
            r'after (\w+)',
            r'needs (\w+)',
            # File dependency patterns
            r'uses? ([a-zA-Z_][a-zA-Z0-9_]*\.py)',
            r'import (\w+)',
            r'from (\w+)',
            # Task chain patterns
            r'then (\w+)',
            r'followed by (\w+)'
        ]

    def add_task(self, task: Task):
        """Add task to dependency graph."""
        self.tasks[task.id] = task

        # Auto-detect dependencies from task content
        detected_deps = self._detect_dependencies(task.content)
        task.dependencies.update(detected_deps)

        # Update dependents mapping
        for dep_id in task.dependencies:
            self.dependents[dep_id].add(task.id)

    def _detect_dependencies(self, content: str) -> Set[str]:
        """Auto-detect dependencies from task content using patterns."""
        dependencies = set()

        for pattern in self.dependency_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                dep_id = match.strip()
                if dep_id and dep_id != content:
                    dependencies.add(dep_id)

        return dependencies

    def add_dependency(self, task_id: str, dependency_id: str):
        """Manually add dependency."""
        if task_id in self.tasks:
            self.tasks[task_id].dependencies.add(dependency_id)
            self.dependents[dependency_id].add(task_id)

    def remove_dependency(self, task_id: str, dependency_id: str):
        """Remove dependency."""
        if task_id in self.tasks:
            self.tasks[task_id].dependencies.discard(dependency_id)
            self.dependents[dependency_id].discard(task_id)

    def get_ready_tasks(self) -> List[Task]:
        """Get tasks ready for execution (dependencies met)."""
        ready_tasks = []

        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                if self._are_dependencies_met(task):
                    task.status = TaskStatus.READY
                    ready_tasks.append(task)
                else:
                    task.status = TaskStatus.BLOCKED

        return ready_tasks

    def _are_dependencies_met(self, task: Task) -> bool:
        """Check if all dependencies are completed."""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                # Missing dependency task
                return False
            if self.tasks[dep_id].status != TaskStatus.COMPLETED:
                return False
        return True

    def mark_completed(self, task_id: str, result: Any = None):
        """Mark task as completed and update dependent tasks."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.end_time = time.time()

            # Update dependent tasks
            for dependent_id in self.dependents[task_id]:
                if dependent_id in self.tasks:
                    dependent = self.tasks[dependent_id]
                    if dependent.status == TaskStatus.BLOCKED:
                        if self._are_dependencies_met(dependent):
                            dependent.status = TaskStatus.READY

    def mark_failed(self, task_id: str, error: str):
        """Mark task as failed."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.FAILED
            task.error = error
            task.end_time = time.time()

    def get_topological_order(self) -> List[str]:
        """Get topological ordering of tasks."""
        in_degree = defaultdict(int)

        # Calculate in-degrees
        for task_id, task in self.tasks.items():
            for dep_id in task.dependencies:
                in_degree[task_id] += 1

        # Kahn's algorithm
        queue = deque([task_id for task_id in self.tasks if in_degree[task_id] == 0])
        result = []

        while queue:
            task_id = queue.popleft()
            result.append(task_id)

            for dependent_id in self.dependents[task_id]:
                in_degree[dependent_id] -= 1
                if in_degree[dependent_id] == 0:
                    queue.append(dependent_id)

        # Check for cycles
        if len(result) != len(self.tasks):
            remaining = set(self.tasks.keys()) - set(result)
            raise ValueError(f"Circular dependency detected involving tasks: {remaining}")

        return result

    def visualize(self) -> str:
        """Generate ASCII visualization of dependency graph."""
        lines = ["Task Dependency Graph:", "=" * 25]

        # Group by status
        by_status = defaultdict(list)
        for task in self.tasks.values():
            by_status[task.status].append(task)

        for status in TaskStatus:
            if status in by_status:
                lines.append(f"\n{status.value.upper()}:")
                for task in by_status[status]:
                    deps_str = f" (deps: {', '.join(task.dependencies)})" if task.dependencies else ""
                    duration_str = f" [{task.duration():.2f}s]" if task.duration() else ""
                    lines.append(f"  â€¢ {task.id}{deps_str}{duration_str}")

        return "\n".join(lines)

class TaskScheduler:
    """Main task scheduler with parallel execution."""

    def __init__(self, max_workers: int = 4, executor_func=None):
        self.max_workers = max_workers
        self.dependency_graph = DependencyGraph()
        self.running_tasks: Dict[str, threading.Thread] = {}
        self.executor_func = executor_func or self._default_executor
        self.shutdown_requested = False
        self.logger = logging.getLogger(__name__)

    def add_task(self, task_id: str, content: str, dependencies: Set[str] = None) -> Task:
        """Add task to scheduler."""
        task = Task(
            id=task_id,
            content=content,
            dependencies=dependencies or set()
        )
        self.dependency_graph.add_task(task)
        return task

    def add_dependency(self, task_id: str, dependency_id: str):
        """Add manual dependency."""
        self.dependency_graph.add_dependency(task_id, dependency_id)

    def _default_executor(self, task: Task) -> Any:
        """Default task executor - just sleeps for demo."""
        time.sleep(0.1)  # Simulate work
        return f"Completed: {task.content}"

    def _execute_task(self, task: Task):
        """Execute single task in thread."""
        try:
            task.start_time = time.time()
            task.status = TaskStatus.RUNNING
            task.worker_id = threading.current_thread().name

            self.logger.info(f"Starting task {task.id}")

            result = self.executor_func(task)

            self.dependency_graph.mark_completed(task.id, result)
            self.logger.info(f"Completed task {task.id}")

        except Exception as e:
            error_msg = str(e)
            self.dependency_graph.mark_failed(task.id, error_msg)
            self.logger.error(f"Failed task {task.id}: {error_msg}")

        finally:
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]

    def run(self, timeout: Optional[float] = None) -> Dict[str, Any]:
        """Run scheduler until all tasks complete or timeout."""
        start_time = time.time()

        while not self.shutdown_requested:
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                self.logger.warning("Scheduler timeout reached")
                break

            # Get ready tasks
            ready_tasks = self.dependency_graph.get_ready_tasks()

            # Start new tasks if workers available
            available_workers = self.max_workers - len(self.running_tasks)
            for i, task in enumerate(ready_tasks[:available_workers]):
                thread = threading.Thread(
                    target=self._execute_task,
                    args=(task,),
                    name=f"worker-{task.id}"
                )
                thread.start()
                self.running_tasks[task.id] = thread

            # Check if all tasks are done
            all_tasks_done = all(
                task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]
                for task in self.dependency_graph.tasks.values()
            )

            if all_tasks_done and not self.running_tasks:
                break

            # Clean up finished threads
            finished_tasks = []
            for task_id, thread in self.running_tasks.items():
                if not thread.is_alive():
                    thread.join()
                    finished_tasks.append(task_id)

            for task_id in finished_tasks:
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]

            time.sleep(0.01)  # Small delay to prevent busy waiting

        # Wait for remaining tasks to finish
        for thread in self.running_tasks.values():
            thread.join()

        return self.get_results()

    def get_results(self) -> Dict[str, Any]:
        """Get execution results."""
        results = {
            "tasks": {},
            "summary": {
                "total": len(self.dependency_graph.tasks),
                "completed": 0,
                "failed": 0,
                "blocked": 0
            }
        }

        for task_id, task in self.dependency_graph.tasks.items():
            results["tasks"][task_id] = {
                "status": task.status.value,
                "result": task.result,
                "error": task.error,
                "duration": task.duration(),
                "dependencies": list(task.dependencies)
            }

            if task.status == TaskStatus.COMPLETED:
                results["summary"]["completed"] += 1
            elif task.status == TaskStatus.FAILED:
                results["summary"]["failed"] += 1
            elif task.status == TaskStatus.BLOCKED:
                results["summary"]["blocked"] += 1

        return results

    def shutdown(self):
        """Shutdown scheduler."""
        self.shutdown_requested = True
        for thread in self.running_tasks.values():
            thread.join()

    def visualize_progress(self) -> str:
        """Get visual progress representation."""
        return self.dependency_graph.visualize()

def integrate_with_grind_spawner(grind_spawner_path: str = "grind_spawner.py"):
    """Integration helper for grind_spawner.py"""

    def create_task_aware_spawner(original_spawner_class):
        """Decorator to add task scheduling to spawner."""

        class TaskAwareSpawner(original_spawner_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.task_scheduler = TaskScheduler(max_workers=4)

            def schedule_task(self, task_id: str, content: str, dependencies: Set[str] = None):
                """Schedule task with dependencies."""
                return self.task_scheduler.add_task(task_id, content, dependencies)

            def run_with_dependencies(self, timeout: Optional[float] = None):
                """Run spawner with dependency-aware scheduling."""
                return self.task_scheduler.run(timeout)

            def get_progress(self):
                """Get dependency progress visualization."""
                return self.task_scheduler.visualize_progress()

        return TaskAwareSpawner

    return create_task_aware_spawner

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create scheduler
    scheduler = TaskScheduler(max_workers=2)

    # Add tasks with dependencies
    scheduler.add_task("setup", "Initialize system")
    scheduler.add_task("data_load", "Load data files, depends on setup")
    scheduler.add_task("process_1", "Process batch 1, requires data_load")
    scheduler.add_task("process_2", "Process batch 2, requires data_load")
    scheduler.add_task("merge", "Merge results, after process_1 and process_2")

    # Add manual dependency
    scheduler.add_dependency("merge", "process_1")
    scheduler.add_dependency("merge", "process_2")

    print("Initial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    print("\nRunning scheduler...")
    results = scheduler.run(timeout=30)

    print("\nFinal results:")
    print(json.dumps(results, indent=2))
    print("\nFinal visualization:")
    print(scheduler.visualize_progress())