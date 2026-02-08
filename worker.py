"""
Parallel Worker for Black Swarm Orchestrator

Uses file-based lock protocol for coordination between multiple workers.
Lock Protocol from: claude-code-orchestrator EXECUTION_SWARM_SYSTEM.md

Target API: http://127.0.0.1:8420 (Black Swarm)
"""

import json
import os
import sys
import time
import uuid
import httpx
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from utils import read_json, append_jsonl, read_jsonl, get_timestamp, ensure_dir, format_error
from config import (
    LOCK_TIMEOUT_SECONDS,
    API_TIMEOUT_SECONDS,
    DEFAULT_MIN_BUDGET,
    DEFAULT_MAX_BUDGET,
    validate_model_id,
    validate_config,
)
from model_policy import resolve_model_choice

# ============================================================================
# CONSTANTS
# ============================================================================
WORKSPACE: Path = Path(__file__).parent
QUEUE_FILE: Path = WORKSPACE / "queue.json"
LOCKS_DIR: Path = WORKSPACE / "task_locks"
EXECUTION_LOG: Path = WORKSPACE / "execution_log.jsonl"

API_REQUEST_TIMEOUT: float = API_TIMEOUT_SECONDS
WORKER_CHECK_INTERVAL: float = 2.0  # Delay between queue checks in seconds
MAX_IDLE_CYCLES: int = 10  # Exit after N consecutive idle checks
DEFAULT_INTENSITY: str = "medium"
DEFAULT_TASK_TYPE: str = "grind"

# Generate unique worker ID
WORKER_ID: str = f"worker_{uuid.uuid4().hex[:8]}"


# ============================================================================
# LOGGING HELPERS
# ============================================================================
def _log(level: str, message: str) -> None:
    """
    Log a message with timestamp and level.

    Args:
        level: Log level (INFO, ERROR, WARN, DEBUG)
        message: Message to log
    """
    timestamp = get_timestamp()
    print(f"[{timestamp}] [{level}] [{WORKER_ID}] {message}")




def ensure_directories() -> None:
    """Create required directories if they don't exist."""
    try:
        ensure_dir(LOCKS_DIR)
    except OSError as e:
        _log("ERROR", f"Failed to create locks directory: {e}")
        raise


def read_queue() -> Dict[str, Any]:
    """Read the shared queue file (never write to it from workers)."""
    data = read_json(QUEUE_FILE)
    if not data:
        raise ValueError("Queue file is empty")
    return data


def read_execution_log() -> Dict[str, Any]:
    """Read the execution log (JSONL) and return latest status per task."""
    events = read_jsonl(EXECUTION_LOG)
    task_index: Dict[str, Any] = {}
    for event in events:
        task_id = event.get("task_id")
        if task_id:
            task_index[task_id] = event
    return {"tasks": task_index}


def append_execution_event(task_id: str, status: str, **fields: Any) -> None:
    """Append an execution event to the JSONL log."""
    record = {
        "task_id": task_id,
        "worker_id": WORKER_ID,
        "status": status,
        "timestamp": get_timestamp(),
        **fields,
    }
    append_jsonl(EXECUTION_LOG, record)


def infer_identity(task: Dict[str, Any]) -> Dict[str, str]:
    """Infer identity metadata for task attribution."""
    identity_id = (
        task.get("identity_id")
        or task.get("resident_id")
        or task.get("author_id")
        or WORKER_ID
    )
    identity_name = task.get("identity_name") or task.get("author_name") or identity_id
    return {"identity_id": identity_id, "identity_name": identity_name}


def infer_origin(task: Dict[str, Any]) -> str:
    """Infer task origin for balanced action paths."""
    if task.get("origin"):
        return task["origin"]
    if task.get("bounty_id") or task.get("is_bounty"):
        return "bounty"
    if task.get("request_id") or task.get("user_request"):
        return "user_request"
    task_type = (task.get("task_type") or task.get("type") or "").lower()
    if "maint" in task_type:
        return "maintenance"
    return "explore"


def task_priority_score(task: Dict[str, Any]) -> float:
    """Compute priority score with escalation for time-sensitive tasks."""
    score = float(task.get("priority", 0) or 0)
    if task.get("time_sensitive"):
        score += 5.0

    bounty = task.get("bounty_tokens") or task.get("bounty") or 0
    try:
        score += float(bounty)
    except (TypeError, ValueError):
        pass

    created_at = task.get("created_at")
    escalation = task.get("value_escalation") or 0
    try:
        escalation = float(escalation)
    except (TypeError, ValueError):
        escalation = 0.0

    if created_at and escalation > 0:
        try:
            if isinstance(created_at, (int, float)):
                age_seconds = time.time() - float(created_at)
            else:
                parsed = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
                age_seconds = (datetime.now(timezone.utc) - parsed).total_seconds()
            score += max(age_seconds / 3600.0, 0.0) * escalation
        except Exception:
            pass

    return score


def register_estimate_requests(queue: Dict[str, Any]) -> None:
    """Register estimate requests for tasks missing estimates."""
    try:
        from estimate_requests import register_request, resolve_request
        from utils.task_complexity import analyze_task_complexity
    except Exception:
        return

    for task in queue.get("tasks", []):
        task_id = task.get("id")
        if not task_id:
            continue
        if task.get("estimated_budget") is not None:
            try:
                resolve_request(task_id, reason="estimated")
            except Exception:
                pass
            continue
        summary = (
            task.get("summary")
            or task.get("prompt")
            or task.get("task")
            or task.get("instruction")
            or ""
        )
        time_sensitive = bool(task.get("time_sensitive") or task.get("urgent"))
        analysis = analyze_task_complexity(
            str(summary),
            metadata={"depends_on": task.get("depends_on", [])},
        )
        base_budget = float(task.get("max_budget") or DEFAULT_MAX_BUDGET)
        suggested_budget = round(base_budget * float(analysis.get("suggested_budget_multiplier", 1.0)), 4)
        try:
            register_request(
                task_id=task_id,
                summary=str(summary),
                time_sensitive=time_sensitive,
                complexity_score=analysis.get("complexity_score"),
                complexity_band=analysis.get("complexity_band"),
                suggested_model_tier=analysis.get("suggested_model_tier"),
                suggested_budget=suggested_budget,
            )
        except Exception:
            continue


def get_lock_path(task_id: str) -> Path:
    """Get the lock file path for a task."""
    return LOCKS_DIR / f"{task_id}.lock"


def is_lock_stale(lock_path: Path) -> bool:
    """Check if a lock file is stale (older than LOCK_TIMEOUT_SECONDS)."""
    if not lock_path.exists():
        return False

    try:
        lock_data = read_json(lock_path)

        started_at = datetime.fromisoformat(lock_data["started_at"].replace("Z", "+00:00"))
        age_seconds = (datetime.now(timezone.utc) - started_at).total_seconds()
        return age_seconds > LOCK_TIMEOUT_SECONDS
    except (json.JSONDecodeError, KeyError, ValueError, IOError) as e:
        _log("DEBUG", f"Lock file corrupted ({lock_path}): {e}")
        return True


def try_acquire_lock(task_id: str) -> bool:
    """Attempt to acquire lock for a task using atomic file creation."""
    lock_path = get_lock_path(task_id)

    if lock_path.exists():
        if is_lock_stale(lock_path):
            try:
                lock_path.unlink()
                _log("INFO", f"Removed stale lock for {task_id}")
            except OSError as e:
                _log("ERROR", f"Failed to remove stale lock ({task_id}): {e}")
                return False
        else:
            return False

    lock_data = {
        "worker_id": WORKER_ID,
        "started_at": get_timestamp(),
        "task_id": task_id
    }

    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w") as f:
            json.dump(lock_data, f, indent=2)  # Atomic operation, can't use write_json
        return True
    except FileExistsError:
        return False
    except (OSError, IOError) as e:
        _log("ERROR", f"Failed to acquire lock ({task_id}): {e}")
        return False


def release_lock(task_id: str) -> None:
    """Release the lock for a task."""
    lock_path = get_lock_path(task_id)
    try:
        if lock_path.exists():
            lock_path.unlink()
    except OSError as e:
        _log("ERROR", f"Failed to release lock ({task_id}): {e}")


def check_dependencies_complete(task: Dict[str, Any], execution_log: Dict[str, Any]) -> bool:
    """Check if all dependencies for a task are completed."""
    depends_on = task.get("depends_on", [])
    if not depends_on:
        return True

    tasks_log = execution_log.get("tasks", {})
    for dep_id in depends_on:
        dep_status = tasks_log.get(dep_id, {}).get("status")
        if dep_status != "completed":
            return False
    return True


def is_task_done(task_id: str, execution_log: Dict[str, Any]) -> bool:
    """Check if a task is already completed or failed."""
    task_status = execution_log.get("tasks", {}).get(task_id, {}).get("status")
    return task_status in ("completed", "failed")


def execute_task(task: Dict[str, Any], api_endpoint: str) -> Dict[str, Any]:
    """Execute a task by sending it to the Black Swarm API."""
    task_id = task.get("id", "unknown")
    min_budget = task.get("min_budget", DEFAULT_MIN_BUDGET)
    max_budget = task.get("max_budget", DEFAULT_MAX_BUDGET)
    intensity = task.get("intensity", DEFAULT_INTENSITY)
    prompt = task.get("prompt") or task.get("task") or task.get("instruction")
    requested_model = task.get("model")
    requested_tier = task.get("model_tier") or task.get("model_size") or task.get("model_choice")
    model, model_tier = resolve_model_choice(model=requested_model, model_tier=requested_tier)
    if not model_tier:
        model_tier = None
    if model:
        validate_model_id(model)

    if not prompt:
        return {
            "status": "failed",
            "result_summary": None,
            "errors": "Task missing prompt/instruction"
        }

    _log("INFO", f"Executing task {task_id} (budget: ${min_budget}-${max_budget}, intensity: {intensity})")

    payload = {
        "prompt": prompt,
        "model": model,
        "min_budget": min_budget,
        "max_budget": max_budget,
        "intensity": intensity,
        "task_id": task_id,
        "model_tier": model_tier,
    }

    try:
        with httpx.Client(timeout=API_REQUEST_TIMEOUT) as client:
            response = client.post(f"{api_endpoint}/grind", json=payload)

        if response.status_code == 200:
            result = response.json()
            return {
                "status": "completed",
                "result_summary": result.get("result", "Task completed"),
                "errors": None,
                "model": result.get("model"),
                "budget_used": result.get("budget_used"),
                "usage": result.get("usage"),
                "model_tier": result.get("model_tier", model_tier),
            }

        error_msg = f"API returned {response.status_code}: {response.text}"
        _log("WARN", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg
        }
    except httpx.ConnectError as e:
        error_msg = f"Cannot connect to API at {api_endpoint}: {e}"
        _log("ERROR", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg
        }
    except httpx.TimeoutException as e:
        error_msg = f"API request timeout: {e}"
        _log("ERROR", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg
        }
    except json.JSONDecodeError as e:
        error_msg = f"Invalid API response: {e}"
        _log("ERROR", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg
        }


def find_and_execute_task(queue: Dict[str, Any]) -> bool:
    """Find an available task, lock it, execute it, and report results."""
    execution_log = read_execution_log()
    api_endpoint = queue.get("api_endpoint", "http://127.0.0.1:8420")

    register_estimate_requests(queue)

    candidates = []
    for task in queue.get("tasks", []):
        task_id = task.get("id")
        if not task_id:
            continue

        if is_task_done(task_id, execution_log):
            continue

        if not check_dependencies_complete(task, execution_log):
            continue

        score = task_priority_score(task)
        candidates.append((score, task))

    candidates.sort(key=lambda item: item[0], reverse=True)

    for _, task in candidates:
        task_id = task.get("id")
        if not task_id:
            continue
        if not try_acquire_lock(task_id):
            continue

        _log("INFO", f"Acquired lock for {task_id}")
        identity = infer_identity(task)
        origin = infer_origin(task)
        activity_type = task.get("task_type") or task.get("type") or DEFAULT_TASK_TYPE
        activity_info = {"concurrent": 1, "decay_multiplier": 1.0}
        complexity_analysis = {}
        try:
            from utils.task_complexity import analyze_task_complexity

            complexity_text = (
                task.get("summary")
                or task.get("prompt")
                or task.get("task")
                or task.get("instruction")
                or ""
            )
            complexity_analysis = analyze_task_complexity(
                str(complexity_text),
                metadata={"depends_on": task.get("depends_on", [])},
            )
        except Exception:
            complexity_analysis = {}
        try:
            from activity_tracker import start_activity, end_activity

            activity_info = start_activity(identity["identity_id"], activity_type)
        except Exception:
            end_activity = None
        try:
            append_execution_event(
                task_id,
                "in_progress",
                started_at=get_timestamp(),
                identity_id=identity["identity_id"],
                identity_name=identity["identity_name"],
                origin=origin,
                activity_type=activity_type,
                novelty_decay=activity_info.get("decay_multiplier"),
                concurrent_activity=activity_info.get("concurrent"),
                model_tier=task.get("model_tier") or task.get("model_size") or task.get("model_choice"),
                complexity_score=complexity_analysis.get("complexity_score"),
                complexity_band=complexity_analysis.get("complexity_band"),
            )

            result = execute_task(task, api_endpoint)
            estimated_budget = task.get("estimated_budget", task.get("max_budget", DEFAULT_MAX_BUDGET))
            submission_id = None
            if result.get("status") == "completed":
                try:
                    from jury_duty import submit_change

                    submission = submit_change(
                        task_id=task_id,
                        author_id=identity["identity_id"],
                        author_name=identity["identity_name"],
                        summary=str(result.get("result_summary") or "")[:500],
                        task_type=activity_type,
                        origin=origin,
                        estimated_budget=estimated_budget,
                        actual_cost=result.get("budget_used"),
                        novelty_decay=activity_info.get("decay_multiplier", 1.0),
                        complexity_score=complexity_analysis.get("complexity_score"),
                    )
                    submission_id = submission.get("submission_id")
                except Exception as e:
                    _log("WARN", f"Jury submission failed for {task_id}: {e}")

            append_execution_event(
                task_id,
                result["status"],
                completed_at=get_timestamp(),
                result_summary=result.get("result_summary"),
                errors=result.get("errors"),
                model=result.get("model"),
                estimated_budget=estimated_budget,
                budget_used=result.get("budget_used"),
                submission_id=submission_id,
                origin=origin,
                novelty_decay=activity_info.get("decay_multiplier"),
                model_tier=result.get("model_tier"),
                complexity_score=complexity_analysis.get("complexity_score"),
                complexity_band=complexity_analysis.get("complexity_band"),
            )
            _log("INFO", f"Completed task {task_id} - {result['status']}")
        finally:
            if "end_activity" in locals() and end_activity:
                try:
                    end_activity(identity["identity_id"], activity_type)
                except Exception:
                    pass
            release_lock(task_id)
            _log("INFO", f"Released lock for {task_id}")

        return True

    return False


def worker_loop(max_iterations: Optional[int] = None) -> None:
    """Main worker loop. Continuously looks for and executes tasks."""
    try:
        ensure_directories()
        _log("INFO", "Starting worker loop")

        iterations = 0
        idle_count = 0

        while True:
            if max_iterations and iterations >= max_iterations:
                _log("INFO", f"Reached max iterations ({max_iterations})")
                break

            try:
                queue = read_queue()

                if find_and_execute_task(queue):
                    iterations += 1
                    idle_count = 0
                else:
                    idle_count += 1
                    if idle_count >= MAX_IDLE_CYCLES:
                        _log("INFO", f"No tasks available after {MAX_IDLE_CYCLES} checks. Exiting.")
                        break
                    _log("INFO", f"No tasks available, waiting... ({idle_count}/{MAX_IDLE_CYCLES})")
                    time.sleep(WORKER_CHECK_INTERVAL)
            except KeyboardInterrupt:
                _log("INFO", "Interrupted by user")
                break
            except Exception as e:
                _log("ERROR", f"Unexpected error in worker loop: {type(e).__name__}: {e}")
                raise

        _log("INFO", f"Worker finished. Executed {iterations} tasks.")
    except Exception as e:
        _log("ERROR", f"Fatal error in worker_loop: {type(e).__name__}: {e}")
        sys.exit(1)


def add_task(
    task_id: str,
    prompt: str,
    depends_on: Optional[List[str]] = None,
    task_type: str = "grind",
    min_budget: float = DEFAULT_MIN_BUDGET,
    max_budget: float = DEFAULT_MAX_BUDGET,
    intensity: str = DEFAULT_INTENSITY,
    model: Optional[str] = None,
    model_tier: Optional[str] = None,
) -> None:
    """Helper to add a task to the queue."""
    try:
        queue = read_queue()

        task: Dict[str, Any] = {
            "id": task_id,
            "type": task_type,
            "prompt": prompt,
            "min_budget": min_budget,
            "max_budget": max_budget,
            "intensity": intensity,
            "depends_on": depends_on or [],
            "parallel_safe": True,
            "model": model,
            "model_tier": model_tier,
        }

        queue["tasks"].append(task)

        write_json(QUEUE_FILE, queue)

        _log("INFO", f"Added task: {task_id}")
    except (IOError, TypeError) as e:
        _log("ERROR", f"Failed to add task {task_id}: {e}")
        raise


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "add" and len(sys.argv) >= 4:
                validate_config(require_groq_key=False)
                deps = sys.argv[4].split(",") if len(sys.argv) > 4 else None
                add_task(sys.argv[2], sys.argv[3], deps)
            elif sys.argv[1] == "run":
                try:
                    validate_config(require_groq_key=True)
                    max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else None
                    worker_loop(max_iter)
                except ValueError:
                    _log("ERROR", f"Invalid max_iterations: {sys.argv[2]}")
                    sys.exit(1)
            else:
                print("Usage:")
                print("  python worker.py run [max_iterations]  - Start worker")
                print("  python worker.py add <id> <instruction> [deps]  - Add task")
                sys.exit(1)
        else:
            worker_loop()
    except KeyboardInterrupt:
        _log("INFO", "Program interrupted")
        sys.exit(0)
    except Exception as e:
        _log("ERROR", f"Fatal error: {type(e).__name__}: {e}")
        sys.exit(1)
