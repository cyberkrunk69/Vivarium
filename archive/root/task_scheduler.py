"""
Task Dependency Scheduler
========================

This module implements a lightweight, dependency‑aware scheduler that can:

* Parse a list of textual task specifications and automatically infer
  dependencies (e.g. “Task B depends on Task A”).
* Build a directed‑acyclic graph (DAG) of tasks.
* Execute tasks that have no unmet dependencies in parallel.
* Block tasks until all of their prerequisites have completed.
* Track overall progress and optionally visualise the dependency graph.

The implementation is deliberately self‑contained – it only relies on the
standard library plus ``tqdm`` (for progress bars) and ``networkx`` /
``matplotlib`` (optional visualisation).  If those optional packages are not
installed the core scheduling functionality still works.

Typical usage (from any other module, e.g. ``grind_spawner.py``)::

    from task_scheduler import TaskScheduler

    # Define tasks – each task is a dict with at least a ``name`` and a
    # ``callable`` (function) that performs the work.
    tasks = [
        {"name": "download_data", "func": download_data},
        {"name": "preprocess",    "func": preprocess,    "description": "preprocess depends on download_data"},
        {"name": "train_model",   "func": train_model,   "description": "train_model depends on preprocess"},
        {"name": "evaluate",      "func": evaluate,      "description": "evaluate depends on train_model"},
    ]

    scheduler = TaskScheduler(tasks)
    scheduler.run(max_workers=4)          # runs independent tasks in parallel
    scheduler.visualize(output_path="graph.png")   # optional visualisation
"""

from __future__ import annotations

import re
import threading
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, Iterable, List, Set, Tuple

# Optional, but very handy for progress bars and visualisation
try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    tqdm = lambda x, **kw: x  # type: ignore

try:
    import networkx as nx
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    nx = None  # type: ignore
    plt = None  # type: ignore


class DependencyError(RuntimeError):
    """Raised when a cyclic dependency is detected or an undefined task is referenced."""


class DependencyGraph:
    """
    Directed‑acyclic graph that stores tasks and their dependencies.

    Internally we keep:
        * ``_adj`` – adjacency list (outgoing edges)
        * ``_in_degree`` – number of incoming edges for each node
    """

    def __init__(self) -> None:
        self._adj: Dict[str, Set[str]] = defaultdict(set)
        self._in_degree: Dict[str, int] = defaultdict(int)
        self._tasks: Dict[str, Callable] = {}

    # --------------------------------------------------------------------- #
    # Public API – building the graph
    # --------------------------------------------------------------------- #
    def add_task(self, name: str, func: Callable) -> None:
        """Register a new task.  If the task already exists, its callable is replaced."""
        if name not in self._tasks:
            self._tasks[name] = func
            # Ensure the node exists in the graph structures
            self._adj[name] = self._adj.get(name, set())
            self._in_degree[name] = self._in_degree.get(name, 0)
        else:
            self._tasks[name] = func

    def add_dependency(self, before: str, after: str) -> None:
        """
        Declare that ``after`` depends on ``before`` (i.e. ``before`` → ``after``).

        Raises:
            DependencyError: if adding the edge would create a cycle or if either
                             node is unknown.
        """
        if before not in self._tasks or after not in self._tasks:
            raise DependencyError(f"Undefined task in dependency: {before!r} → {after!r}")

        if after in self._adj[before]:
            # Edge already present – nothing to do
            return

        # Temporarily add the edge and test for cycles
        self._adj[before].add(after)
        self._in_degree[after] += 1

        if self._has_cycle():
            # Roll‑back and raise
            self._adj[before].remove(after)
            self._in_degree[after] -= 1
            raise DependencyError(f"Cyclic dependency introduced: {before!r} → {after!r}")

    # --------------------------------------------------------------------- #
    # Query helpers
    # --------------------------------------------------------------------- #
    def ready_tasks(self) -> List[str]:
        """Return a list of tasks whose in‑degree is zero (i.e. ready to run)."""
        return [node for node, deg in self._in_degree.items() if deg == 0]

    def mark_completed(self, name: str) -> None:
        """Mark ``name`` as finished – decrement in‑degree of its successors."""
        for succ in self._adj[name]:
            self._in_degree[succ] -= 1
        # Remove the node from the graph to keep the data structures tidy
        self._adj.pop(name, None)
        self._in_degree.pop(name, None)

    def all_tasks(self) -> Set[str]:
        """Return the set of all task names currently in the graph."""
        return set(self._tasks.keys())

    def get_callable(self, name: str) -> Callable:
        """Retrieve the callable associated with ``name``."""
        return self._tasks[name]

    # --------------------------------------------------------------------- #
    # Internal utilities
    # --------------------------------------------------------------------- #
    def _has_cycle(self) -> bool:
        """Detect a cycle using Kahn's algorithm – O(V+E)."""
        indeg = dict(self._in_degree)  # copy
        q = deque([n for n, d in indeg.items() if d == 0])
        visited = 0

        while q:
            n = q.popleft()
            visited += 1
            for m in self._adj[n]:
                indeg[m] -= 1
                if indeg[m] == 0:
                    q.append(m)

        return visited != len(indeg)

    # --------------------------------------------------------------------- #
    # Optional visualisation
    # --------------------------------------------------------------------- #
    def visualize(self, output_path: str = "dependency_graph.png") -> None:
        """
        Render the dependency graph to ``output_path`` using ``networkx`` and
        ``matplotlib``.  If those libraries are unavailable the method becomes a
        no‑op.
        """
        if nx is None or plt is None:
            print("NetworkX / Matplotlib not installed – skipping visualisation.")
            return

        G = nx.DiGraph()
        for src, targets in self._adj.items():
            for tgt in targets:
                G.add_edge(src, tgt)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500)
        nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        plt.title("Task Dependency Graph")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"Dependency graph saved to {output_path}")


class TaskScheduler:
    """
    High‑level façade that:

    1. Accepts a list of task specifications (name, callable, optional description).
    2. Auto‑detects dependencies from the description using a simple regex.
    3. Builds a ``DependencyGraph``.
    4. Executes tasks respecting dependencies, running independent tasks in parallel.
    5. Provides progress feedback and optional visualisation.
    """

    # Regex pattern used for auto‑dependency detection.
    # Example accepted strings:
    #   "Task B depends on Task A"
    #   "B depends on A and C"
    #   "C depends on A, B"
    _DEP_REGEX = re.compile(
        r"(?P<task>\w+)\s+depends\s+on\s+(?P<deps>[\w\s,]+)",
        flags=re.IGNORECASE,
    )

    def __init__(self, task_specs: Iterable[Dict]) -> None:
        """
        ``task_specs`` – an iterable of dictionaries.  Each dict must contain:

            * ``name`` (str) – unique identifier.
            * ``func`` (Callable) – the work to be performed.
            * optional ``description`` (str) – free‑form text that may contain
              dependency statements.

        Example::

            tasks = [
                {"name": "download", "func": download},
                {"name": "preprocess", "func": preprocess,
                 "description": "preprocess depends on download"},
                {"name": "train", "func": train,
                 "description": "train depends on preprocess"},
            ]
        """
        self.graph = DependencyGraph()
        self._original_specs: Dict[str, Dict] = {}

        # First pass – register all tasks
        for spec in task_specs:
            name = spec["name"]
            func = spec["func"]
            self.graph.add_task(name, func)
            self._original_specs[name] = spec

        # Second pass – infer dependencies from description (if any)
        for spec in task_specs:
            name = spec["name"]
            description = spec.get("description", "")
            for dep in self._parse_dependencies(name, description):
                self.graph.add_dependency(dep, name)

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def run(self, max_workers: int = 4) -> None:
        """
        Execute all tasks respecting dependencies.

        Parameters
        ----------
        max_workers : int
            Maximum number of threads used for parallel execution.  The scheduler
            will never launch more workers than there are ready tasks at any
            moment.

        The method blocks until **all** tasks have completed (or an exception
        propagates).  Progress is displayed via ``tqdm``.
        """
        total_tasks = len(self.graph.all_tasks())
        completed = 0

        # Use a lock to protect shared state (graph mutation + progress counter)
        lock = threading.Lock()
        pbar = tqdm(total=total_tasks, desc="Scheduling", unit="task")

        # Helper that runs a single task and updates the graph
        def _run_task(task_name: str) -> Tuple[str, Exception | None]:
            try:
                func = self.graph.get_callable(task_name)
                func()  # The user‑provided callable does the real work
                return task_name, None
            except Exception as exc:  # pragma: no cover
                return task_name, exc

        # Main loop – keep pulling ready tasks until the graph is empty
        while True:
            with lock:
                ready = self.graph.ready_tasks()
                if not ready and not self.graph.all_tasks():
                    # No tasks left – we are done
                    break

            if not ready:
                # This should never happen in a DAG, but we guard against dead‑locks.
                raise DependencyError("No ready tasks found – possible cyclic dependency.")

            # Limit parallelism to the smaller of max_workers / ready tasks
            workers = min(max_workers, len(ready))

            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_to_name = {executor.submit(_run_task, name): name for name in ready}

                for future in as_completed(future_to_name):
                    name, exc = future.result()
                    if exc:
                        # Propagate the first exception – this aborts the whole run.
                        raise exc

                    with lock:
                        self.graph.mark_completed(name)
                        completed += 1
                        pbar.update(1)

        pbar.close()
        print("All tasks completed successfully.")

    def visualize(self, output_path: str = "dependency_graph.png") -> None:
        """Convenient wrapper around ``DependencyGraph.visualize``."""
        self.graph.visualize(output_path)

    # --------------------------------------------------------------------- #
    # Dependency auto‑detection helpers
    # --------------------------------------------------------------------- #
    @classmethod
    def _parse_dependencies(cls, task_name: str, description: str) -> List[str]:
        """
        Scan ``description`` for phrases like ``<task> depends on X, Y``.
        Returns a list of task names that ``task_name`` depends on.

        The parser is deliberately forgiving – it extracts any word‑like token
        after “depends on” and treats it as a dependency, ignoring punctuation.
        """
        deps: List[str] = []
        for match in cls._DEP_REGEX.finditer(description):
            # ``match.group('task')`` may be the same as ``task_name`` – we ignore it.
            dep_list = match.group("deps")
            # Split on commas, spaces and the word “and”
            tokens = re.split(r"[,\s]+and[,\s]*|[,\s]+", dep_list.strip())
            for token in tokens:
                token = token.strip()
                if token and token != task_name:
                    deps.append(token)
        return deps