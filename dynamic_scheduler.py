"""
Dynamic Task Scheduler with Runtime Dependency Resolution

This scheduler supports:
1. Tasks discovering dependencies mid-execution
2. Spawning subtasks dynamically
3. Partial progress - work on what you can
4. Block only when you actually need something
5. Resume when dependencies complete

Architecture:
- TaskRunner: Executes a task, can yield when blocked
- DependencyGraph: Tracks what's waiting on what
- Scheduler: Orchestrates everything, maximizes parallelism
- WorkQueue: Tasks ready to run
- BlockedQueue: Tasks waiting on dependencies
"""

import threading
import queue
import time
import json
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Set, Callable, Any
from enum import Enum
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
import uuid


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"      # Waiting on dependency
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """A task that can be executed, blocked, and resumed."""
    id: str
    description: str
    execute_fn: Callable  # Function to run
    state: TaskState = TaskState.PENDING

    # Dependencies
    depends_on: Set[str] = field(default_factory=set)  # Task IDs we need
    blocks: Set[str] = field(default_factory=set)      # Task IDs waiting on us

    # Progress tracking
    progress: float = 0.0  # 0-1
    checkpoint: Dict = field(default_factory=dict)  # State for resume

    # Results
    result: Any = None
    error: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    parent_id: Optional[str] = None  # If spawned by another task

    def __hash__(self):
        return hash(self.id)


class DependencyGraph:
    """Tracks task dependencies dynamically."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.lock = threading.RLock()

    def add_task(self, task: Task) -> None:
        with self.lock:
            self.tasks[task.id] = task

    def get_task(self, task_id: str) -> Optional[Task]:
        with self.lock:
            return self.tasks.get(task_id)

    def add_dependency(self, task_id: str, depends_on_id: str) -> None:
        """Task task_id now depends on depends_on_id."""
        with self.lock:
            task = self.tasks.get(task_id)
            dep = self.tasks.get(depends_on_id)
            if task and dep:
                task.depends_on.add(depends_on_id)
                dep.blocks.add(task_id)

    def remove_dependency(self, task_id: str, depends_on_id: str) -> None:
        """Dependency satisfied."""
        with self.lock:
            task = self.tasks.get(task_id)
            dep = self.tasks.get(depends_on_id)
            if task:
                task.depends_on.discard(depends_on_id)
            if dep:
                dep.blocks.discard(task_id)

    def is_ready(self, task_id: str) -> bool:
        """Can this task run (no pending dependencies)?"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            # Check all dependencies are completed
            for dep_id in task.depends_on:
                dep = self.tasks.get(dep_id)
                if not dep or dep.state != TaskState.COMPLETED:
                    return False
            return True

    def get_ready_tasks(self) -> List[Task]:
        """Get all tasks that can run now."""
        with self.lock:
            ready = []
            for task in self.tasks.values():
                if task.state == TaskState.PENDING and self.is_ready(task.id):
                    ready.append(task)
            return ready

    def get_blocked_tasks(self) -> List[Task]:
        """Get tasks waiting on dependencies."""
        with self.lock:
            return [t for t in self.tasks.values() if t.state == TaskState.BLOCKED]

    def mark_completed(self, task_id: str, result: Any = None) -> List[str]:
        """Mark task complete, return newly unblocked task IDs."""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return []

            task.state = TaskState.COMPLETED
            task.result = result
            task.completed_at = datetime.now()

            # Find tasks that were waiting on this
            unblocked = []
            for blocked_id in list(task.blocks):
                blocked_task = self.tasks.get(blocked_id)
                if blocked_task:
                    blocked_task.depends_on.discard(task_id)
                    # Check if now ready
                    if not blocked_task.depends_on and blocked_task.state == TaskState.BLOCKED:
                        unblocked.append(blocked_id)

            return unblocked


class TaskContext:
    """
    Context passed to task execution - allows tasks to:
    - Spawn subtasks
    - Declare dependencies
    - Report progress
    - Checkpoint state
    """

    def __init__(self, task: Task, scheduler: 'DynamicScheduler'):
        self.task = task
        self.scheduler = scheduler
        self._blocked_on: Optional[str] = None

    def spawn_subtask(self, description: str, execute_fn: Callable,
                      wait: bool = False) -> str:
        """
        Spawn a subtask.
        If wait=True, block until it completes.
        Returns subtask ID.
        """
        subtask_id = self.scheduler.add_task(
            description=description,
            execute_fn=execute_fn,
            parent_id=self.task.id
        )

        if wait:
            self.wait_for(subtask_id)

        return subtask_id

    def wait_for(self, task_id: str) -> Any:
        """Block until another task completes, return its result."""
        self._blocked_on = task_id
        self.scheduler.graph.add_dependency(self.task.id, task_id)

        # This will cause the scheduler to pause this task
        raise BlockedOnDependency(task_id)

    def need_file(self, filepath: str) -> bool:
        """Check if a file exists, if not return False (caller should spawn task to create it)."""
        return Path(filepath).exists()

    def checkpoint(self, state: Dict) -> None:
        """Save checkpoint for resume."""
        self.task.checkpoint = state

    def progress(self, pct: float) -> None:
        """Report progress 0-1."""
        self.task.progress = pct
        print(f"    [{self.task.id[:8]}] {int(pct*100)}%")


class BlockedOnDependency(Exception):
    """Raised when a task needs to wait for another task."""
    def __init__(self, dependency_id: str):
        self.dependency_id = dependency_id


class DynamicScheduler:
    """
    Orchestrates task execution with dynamic dependencies.

    Key behaviors:
    - Runs tasks in parallel up to max_workers
    - When a task blocks, parks it and runs something else
    - When a dependency completes, resumes blocked tasks
    - Tasks can spawn subtasks at any time
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.graph = DependencyGraph()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.running: Dict[str, Future] = {}  # task_id -> Future
        self.blocked: Dict[str, Task] = {}    # task_id -> Task (waiting)

        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        # Callbacks
        self.on_task_complete: Optional[Callable[[Task], None]] = None
        self.on_task_start: Optional[Callable[[Task], None]] = None
        self.on_task_blocked: Optional[Callable[[Task, str], None]] = None

    def add_task(self, description: str, execute_fn: Callable,
                 depends_on: List[str] = None, parent_id: str = None) -> str:
        """Add a task to the scheduler."""
        task_id = str(uuid.uuid4())[:8]

        task = Task(
            id=task_id,
            description=description,
            execute_fn=execute_fn,
            depends_on=set(depends_on or []),
            parent_id=parent_id
        )

        self.graph.add_task(task)

        # Set up dependency links
        for dep_id in task.depends_on:
            dep = self.graph.get_task(dep_id)
            if dep:
                dep.blocks.add(task_id)

        return task_id

    def _run_task(self, task: Task) -> None:
        """Execute a task (runs in thread pool)."""
        task.state = TaskState.RUNNING
        task.started_at = datetime.now()

        if self.on_task_start:
            self.on_task_start(task)

        ctx = TaskContext(task, self)

        try:
            result = task.execute_fn(ctx)

            # Task completed successfully
            unblocked = self.graph.mark_completed(task.id, result)

            if self.on_task_complete:
                self.on_task_complete(task)

            # Resume any tasks that were waiting on this
            for unblocked_id in unblocked:
                self._resume_task(unblocked_id)

        except BlockedOnDependency as e:
            # Task is waiting on another task
            task.state = TaskState.BLOCKED

            with self.lock:
                self.blocked[task.id] = task
                if task.id in self.running:
                    del self.running[task.id]

            if self.on_task_blocked:
                self.on_task_blocked(task, e.dependency_id)

            print(f"    [{task.id[:8]}] BLOCKED waiting for {e.dependency_id[:8]}")

        except Exception as e:
            task.state = TaskState.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            print(f"    [{task.id[:8]}] FAILED: {e}")

    def _resume_task(self, task_id: str) -> None:
        """Resume a blocked task."""
        with self.lock:
            task = self.blocked.pop(task_id, None)

        if task:
            task.state = TaskState.PENDING
            print(f"    [{task_id[:8]}] RESUMED")
            self._schedule_task(task)

    def _schedule_task(self, task: Task) -> None:
        """Submit a task to the thread pool."""
        with self.lock:
            if len(self.running) >= self.max_workers:
                return  # Will be picked up later

            future = self.executor.submit(self._run_task, task)
            self.running[task.id] = future

    def run(self, block: bool = True) -> None:
        """
        Start the scheduler.
        If block=True, wait until all tasks complete.
        """
        print(f"[SCHEDULER] Starting with {self.max_workers} workers")

        while not self.stop_event.is_set():
            # Get tasks ready to run
            ready = self.graph.get_ready_tasks()

            if not ready and not self.running and not self.blocked:
                # Nothing to do
                break

            # Schedule ready tasks
            for task in ready:
                if task.state == TaskState.PENDING:
                    self._schedule_task(task)

            # Brief sleep to avoid spinning
            time.sleep(0.1)

            # Clean up completed futures
            with self.lock:
                done = [tid for tid, f in self.running.items() if f.done()]
                for tid in done:
                    del self.running[tid]

            if not block:
                break

        print("[SCHEDULER] Complete")

    def stop(self) -> None:
        """Stop the scheduler gracefully."""
        self.stop_event.set()
        self.executor.shutdown(wait=True)

    def status(self) -> Dict:
        """Get scheduler status."""
        with self.lock:
            return {
                "running": len(self.running),
                "blocked": len(self.blocked),
                "pending": len(self.graph.get_ready_tasks()),
                "completed": len([t for t in self.graph.tasks.values()
                                 if t.state == TaskState.COMPLETED]),
                "failed": len([t for t in self.graph.tasks.values()
                              if t.state == TaskState.FAILED]),
            }


# Example usage
if __name__ == "__main__":
    scheduler = DynamicScheduler(max_workers=4)

    def task_a(ctx: TaskContext):
        print("Task A: Starting")
        ctx.progress(0.5)
        time.sleep(1)
        ctx.progress(1.0)
        return "A result"

    def task_b(ctx: TaskContext):
        print("Task B: Starting, need A's result")
        # This will block until A completes
        ctx.wait_for("task_a")
        print("Task B: Got A's result, continuing")
        return "B result"

    def task_c(ctx: TaskContext):
        print("Task C: Independent task")
        time.sleep(0.5)

        # Dynamically spawn a subtask
        sub_id = ctx.spawn_subtask(
            "Subtask from C",
            lambda c: print("Subtask running!") or "sub result"
        )
        print(f"Task C: Spawned subtask {sub_id}")
        return "C result"

    # Add tasks
    scheduler.add_task("Task A", task_a)
    scheduler.add_task("Task B", task_b, depends_on=["task_a"])
    scheduler.add_task("Task C", task_c)

    # Run
    scheduler.run()
    print(f"Final status: {scheduler.status()}")
