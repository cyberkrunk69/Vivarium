"""
Vivarium Parallel Orchestrator

Spawns multiple workers that coordinate using file-based locks.
Target API: http://127.0.0.1:8420

Usage:
    python orchestrator.py start [num_workers] [--dry-run]  - Start orchestrator with N workers
    python orchestrator.py status                           - Show execution status
    python orchestrator.py add <id> <type> --prompt "..."  - Add a task to queue
    python orchestrator.py clear                            - Clear all tasks and logs

Options for 'add':
    --prompt STR      Task prompt (required)
    --min FLOAT       Minimum budget in dollars (default: 0.05)
    --max FLOAT       Maximum budget in dollars (default: 0.10)
    --intensity STR   low|medium|high (default: medium)
    --model STR       Groq model id (must be in whitelist)
"""

import subprocess
import sys
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from utils import read_json, write_json, read_jsonl
from config import SWARM_API_URL, validate_config, WORKER_TIMEOUT_SECONDS, validate_model_id
from logger import json_log
from safety_killswitch import KillSwitch, CircuitBreaker
from safety_sandbox import init_sandbox

WORKSPACE = Path(__file__).parent
QUEUE_FILE = WORKSPACE / "queue.json"
LOCKS_DIR = WORKSPACE / "task_locks"
EXECUTION_LOG = WORKSPACE / "execution_log.jsonl"


def spawn_worker(worker_id: int) -> Dict:
    """
    Spawn a single worker subprocess.

    Executes worker.py in a separate process and captures its output.
    Used by ProcessPoolExecutor to run workers in parallel.

    Args:
        worker_id: Numeric identifier for logging purposes.

    Returns:
        dict: Execution result containing:
            - worker_id: The input worker ID
            - stdout: Standard output from the worker
            - stderr: Standard error from the worker
            - returncode: Process exit code (0 = success)

    Example:
        result = spawn_worker(0)
        if result["returncode"] == 0:
            print(f"Worker {result['worker_id']} succeeded")
    """
    try:
        result = subprocess.run(
            [sys.executable, str(WORKSPACE / "worker.py"), "run"],
            capture_output=True,
            text=True,
            timeout=WORKER_TIMEOUT_SECONDS
        )
        return {
            "worker_id": worker_id,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired as e:
        return {
            "worker_id": worker_id,
            "stdout": e.stdout or "",
            "stderr": f"Worker timed out after {WORKER_TIMEOUT_SECONDS}s",
            "returncode": 124
        }


def start_orchestrator(num_workers: int = 4, dry_run: bool = False) -> None:
    """
    Start the orchestrator with multiple parallel workers.

    Initializes the execution environment, spawns worker processes using
    ProcessPoolExecutor, and monitors their completion. Workers coordinate
    using file-based locks to avoid duplicate task execution.

    Args:
        num_workers: Number of parallel worker processes (default: 4, must be 1-32).
        dry_run: If True, shows what would happen without executing workers.

    Raises:
        ValueError: If num_workers is invalid.

    Example:
        # Start with default 4 workers
        start_orchestrator()

        # Start with 8 workers for heavy workloads
        start_orchestrator(num_workers=8)

        # CLI: python orchestrator.py start 8
        # CLI with dry-run: python orchestrator.py start 4 --dry-run
    """
    if num_workers < 1 or num_workers > 32:
        raise ValueError(f"num_workers must be between 1 and 32, got {num_workers}")

    # Initialize safety systems
    kill_switch = KillSwitch(workspace=str(WORKSPACE))
    circuit_breaker = CircuitBreaker(
        cost_threshold=100.0,
        failure_threshold=5,
        time_window=300
    )

    # Initialize sandbox for file operation validation
    init_sandbox(str(WORKSPACE))
    print("[SAFETY] Workspace sandbox initialized")

    # Check halt flag before starting
    halt_status = kill_switch.check_halt_flag()
    if halt_status["should_stop"] or halt_status["halted"]:
        print(f"[SAFETY] Cannot start: System is halted")
        print(f"[SAFETY] Reason: {halt_status['reason']}")
        print(f"[SAFETY] Clear HALT file or use KillSwitch.clear_halt()")
        return

    if halt_status["paused"]:
        print(f"[SAFETY] System is paused: {halt_status['reason']}")
        print(f"[SAFETY] Resume with KillSwitch.resume() or remove PAUSE file")
        return

    # Check circuit breaker
    cb_status = circuit_breaker.status()
    if cb_status['tripped']:
        print(f"[SAFETY] Cannot start: Circuit breaker is tripped")
        print(f"[SAFETY] Reason: {cb_status['reason']}")
        print(f"[SAFETY] Reset with CircuitBreaker.reset()")
        return

    print(f"Starting Vivarium Orchestrator with {num_workers} workers...")
    print(f"Target API: {SWARM_API_URL}")

    # Log orchestrator start event
    json_log("INFO", "Orchestrator started",
             num_workers=num_workers,
             dry_run=dry_run,
             api_url=SWARM_API_URL)
    if dry_run:
        print("[DRY RUN MODE - No actual execution]")
    print("-" * 50)

    # Ensure directories exist
    LOCKS_DIR.mkdir(exist_ok=True)

    # Initialize execution log (JSONL append-only)
    if not EXECUTION_LOG.exists():
        EXECUTION_LOG.parent.mkdir(parents=True, exist_ok=True)
        EXECUTION_LOG.write_text("")

    queue = read_json(QUEUE_FILE)
    task_count = len(queue.get("tasks", []))
    print(f"Tasks in queue: {task_count}")

    # Log task queue event
    json_log("INFO", "Task queue loaded",
             task_count=task_count,
             num_workers=num_workers)

    if task_count == 0:
        print("ERROR: No tasks in queue - cannot proceed")
        print(f"  Queue file: {QUEUE_FILE}")
        print(f"  Add tasks with: python orchestrator.py add <id> <type> [options]")
        return

    if dry_run:
        print("\n[DRY RUN] Would execute with:")
        for i, task in enumerate(queue.get("tasks", [])[:5]):
            print(f"  {i+1}. Task ID: {task.get('id')} | Type: {task.get('type')} | Budget: ${task.get('min_budget')}-${task.get('max_budget')}")
        if task_count > 5:
            print(f"  ... and {task_count - 5} more task(s)")
        print(f"[DRY RUN] Would spawn {num_workers} workers")
        return

    start_time = time.time()

    # Spawn workers in parallel
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(spawn_worker, i) for i in range(num_workers)]

        for future in as_completed(futures):
            # Check halt flag during execution
            halt_status = kill_switch.check_halt_flag()
            if halt_status["should_stop"] or halt_status["halted"]:
                print(f"\n[SAFETY] HALT detected - stopping orchestrator")
                print(f"[SAFETY] Reason: {halt_status['reason']}")
                executor.shutdown(wait=False, cancel_futures=True)
                break

            result = future.result()
            print(f"\nWorker {result['worker_id']} finished (exit code: {result['returncode']})")

            # Record failures in circuit breaker
            if result['returncode'] != 0:
                error_msg = result.get('stderr', 'Unknown error')[:200]
                circuit_breaker.record_failure(error_msg)
                if circuit_breaker.tripped:
                    print(f"\n[CIRCUIT BREAKER] TRIPPED: {circuit_breaker.trip_reason}")
                    kill_switch.global_halt(f"Circuit breaker tripped: {circuit_breaker.trip_reason}")
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
            else:
                circuit_breaker.record_success()

            if result['stdout']:
                for line in result['stdout'].strip().split('\n')[-5:]:
                    print(f"  {line}")
            if result['stderr']:
                error_msg = result['stderr'][:300]
                print(f"  ERROR from worker {result['worker_id']}: {error_msg}")
                print(f"  Action: Check worker.py logs for details")

            # Log worker task completion event
            json_log("INFO", "Worker task completed",
                     worker_id=result['worker_id'],
                     returncode=result['returncode'],
                     success=result['returncode'] == 0,
                     has_stderr=bool(result['stderr']))

    elapsed = time.time() - start_time
    print(f"\n{'=' * 50}")
    print(f"Orchestrator finished in {elapsed:.2f}s")

    # Log orchestrator completion event
    json_log("INFO", "Orchestrator completed",
             num_workers=num_workers,
             elapsed_seconds=elapsed)

    show_status()


def show_status() -> None:
    """
    Show current execution status.

    Displays a summary of task counts by status (completed, in_progress,
    pending, failed), lists any failed tasks with their errors, and
    shows active lock files.

    Example:
        # Check progress during or after execution
        show_status()

        # CLI: python orchestrator.py status
    """
    print("\n" + "=" * 50)
    print("EXECUTION STATUS")
    print("=" * 50)

    queue = read_json(QUEUE_FILE)
    if not EXECUTION_LOG.exists():
        print(f"ERROR: Execution log not found: {EXECUTION_LOG}")
        return

    events = read_jsonl(EXECUTION_LOG, default=[])
    task_index: Dict[str, Dict] = {}
    for event in events:
        task_id = event.get("task_id")
        if task_id:
            task_index[task_id] = event

    total_tasks = len(queue.get("tasks", []))
    completed = sum(1 for t in task_index.values() if t.get("status") == "completed")
    in_progress = sum(1 for t in task_index.values() if t.get("status") == "in_progress")
    failed = sum(1 for t in task_index.values() if t.get("status") == "failed")
    pending = max(total_tasks - completed - in_progress - failed, 0)

    print(f"Total Tasks:  {total_tasks:>5}")
    print(f"Completed:    {completed:>5} ({100*completed//total_tasks if total_tasks else 0}%)")
    print(f"In Progress:  {in_progress:>5}")
    print(f"Pending:      {pending:>5}")
    print(f"Failed:       {failed:>5}")

    # Show failed tasks with details
    failed_tasks = [t for t in task_index.values() if t.get("status") == "failed"]
    if failed_tasks:
        print("\n" + "-" * 50)
        print(f"FAILED TASKS ({len(failed_tasks)})")
        print("-" * 50)
        for task in failed_tasks:
            task_id = task.get('id', 'unknown')
            error_msg = task.get('errors', 'No error details recorded')
            print(f"ID: {task_id}")
            print(f"  Error: {error_msg}")
            print(f"  Action: Review execution_log.jsonl for details")
            print()

    # Show active locks
    if LOCKS_DIR.exists():
        locks = list(LOCKS_DIR.glob("*.lock"))
        if locks:
            print("-" * 50)
            print(f"ACTIVE LOCKS ({len(locks)})")
            print("-" * 50)
            for lock in locks:
                print(f"  {lock.name}")

    print("=" * 50)


def add_task(
    task_id: str,
    task_type: str,
    prompt: str,
    min_budget: float = 0.05,
    max_budget: float = 0.10,
    intensity: str = "medium",
    depends_on: Optional[List[str]] = None,
    model: Optional[str] = None,
) -> None:
    """
    Add a grind task to the queue.

    Creates a new task entry with the specified parameters and appends
    it to queue.json. Tasks are marked as parallel_safe by default.

    Args:
        task_id: Unique identifier (e.g., "task_001").
        task_type: Task category (e.g., "grind").
        prompt: Task prompt sent to the Groq API.
        min_budget: Minimum budget in dollars (default: 0.05, must be > 0).
        max_budget: Maximum budget in dollars (default: 0.10, must be >= min_budget).
        intensity: Execution intensity - "low", "medium", or "high".
        depends_on: List of task IDs that must complete first.
        model: Optional Groq model id (must be in whitelist if provided).

    Raises:
        ValueError: If budget or intensity parameters are invalid.

    Example:
        # Add simple task
        add_task("task_001", "grind", "Summarize the code changes in this repo.")

        # Add high-priority task with custom budget
        add_task("task_002", "grind", "Audit error handling in worker.py",
                 min_budget=0.10, max_budget=0.20, intensity="high")

        # CLI: python orchestrator.py add task_001 grind --prompt "Audit locks" --min 0.05 --max 0.10
    """
    # Input validation
    if not task_id or not isinstance(task_id, str):
        raise ValueError("task_id must be a non-empty string")
    if not task_type or not isinstance(task_type, str):
        raise ValueError("task_type must be a non-empty string")
    if not prompt or not isinstance(prompt, str):
        raise ValueError("prompt must be a non-empty string")
    if min_budget <= 0:
        raise ValueError(f"min_budget must be > 0, got {min_budget}")
    if max_budget < min_budget:
        raise ValueError(f"max_budget ({max_budget}) must be >= min_budget ({min_budget})")
    if intensity not in ["low", "medium", "high"]:
        raise ValueError(f"intensity must be 'low', 'medium', or 'high', got '{intensity}'")

    queue = read_json(QUEUE_FILE)
    if "tasks" not in queue:
        queue["tasks"] = []
        queue["api_endpoint"] = SWARM_API_URL

    # Check for duplicate task ID
    if any(t.get("id") == task_id for t in queue.get("tasks", [])):
        raise ValueError(f"Task ID '{task_id}' already exists in queue")

    if model:
        validate_model_id(model)

    task = {
        "id": task_id,
        "type": task_type,
        "prompt": prompt,
        "min_budget": min_budget,
        "max_budget": max_budget,
        "intensity": intensity,
        "status": "pending",
        "depends_on": depends_on or [],
        "parallel_safe": True,
        "model": model,
    }

    queue["tasks"].append(task)
    write_json(QUEUE_FILE, queue)
    print(f"✓ Added task: {task_id}")
    print(f"  Type: {task_type} | Budget: ${min_budget}-${max_budget} | Intensity: {intensity}")

    # Log task addition event
    json_log("INFO", "Task added to queue",
             task_id=task_id,
             task_type=task_type,
             min_budget=min_budget,
             max_budget=max_budget,
             intensity=intensity)


def clear_all() -> None:
    """
    Clear all tasks, logs, and locks.

    Resets the system to a clean state by:
    - Emptying the task queue
    - Clearing the execution log
    - Removing all lock files

    Use before starting a fresh batch of tasks.

    Example:
        clear_all()
        add_task("new_task_001", "grind")

        # CLI: python orchestrator.py clear
    """
    write_json(QUEUE_FILE, {
        "version": "1.0",
        "api_endpoint": SWARM_API_URL,
        "tasks": [],
        "completed": [],
        "failed": []
    })

    EXECUTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    EXECUTION_LOG.write_text("")

    if LOCKS_DIR.exists():
        for lock in LOCKS_DIR.glob("*.lock"):
            lock.unlink()

    print("Cleared all tasks, logs, and locks.")


def parse_add_args(args: List[str]) -> Tuple[str, str, str, float, float, str, Optional[str]]:
    """Parse arguments for 'add' command."""
    if len(args) < 2:
        raise ValueError("'add' command requires: task_id and task_type arguments")

    task_id = args[0]
    task_type = args[1]
    min_b, max_b, intensity = 0.05, 0.10, "medium"
    prompt = None
    model = None

    i = 2
    while i < len(args):
        if args[i] == "--min" and i + 1 < len(args):
            try:
                min_b = float(args[i + 1])
                i += 2
            except ValueError:
                raise ValueError(f"--min requires numeric value, got '{args[i + 1]}'")
        elif args[i] == "--max" and i + 1 < len(args):
            try:
                max_b = float(args[i + 1])
                i += 2
            except ValueError:
                raise ValueError(f"--max requires numeric value, got '{args[i + 1]}'")
        elif args[i] == "--intensity" and i + 1 < len(args):
            intensity = args[i + 1]
            i += 2
        elif args[i] in ("--prompt", "--task") and i + 1 < len(args):
            prompt = args[i + 1]
            i += 2
        elif args[i] == "--model" and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        else:
            i += 1

    if not prompt:
        raise ValueError("'add' command requires --prompt")

    return task_id, task_type, prompt, min_b, max_b, intensity, model


if __name__ == "__main__":
    validate_config()
    try:
        if len(sys.argv) < 2:
            print(__doc__)
            sys.exit(1)

        cmd = sys.argv[1]

        if cmd == "start":
            num_workers = 4
            dry_run = False

            # Parse num_workers and --dry-run flag
            for arg in sys.argv[2:]:
                if arg == "--dry-run":
                    dry_run = True
                else:
                    try:
                        num_workers = int(arg)
                    except ValueError:
                        raise ValueError(f"Invalid number of workers: '{arg}' (must be 1-32)")

            start_orchestrator(num_workers, dry_run)

        elif cmd == "status":
            show_status()

        elif cmd == "add":
            task_id, task_type, prompt, min_b, max_b, intensity, model = parse_add_args(sys.argv[2:])
            add_task(task_id, task_type, prompt, min_b, max_b, intensity, model=model)

        elif cmd == "clear":
            clear_all()

        else:
            print(__doc__)
            sys.exit(1)

    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
