"""
Resident Runtime for Vivarium

Uses file-based lock protocol for coordination between multiple residents.
Lock Protocol from: EXECUTION_SWARM_SYSTEM.md (legacy orchestrator spec)

Target API: http://127.0.0.1:8420 (Vivarium)
"""

import json
import os
import sys
import time
import uuid
import hashlib
import random
import httpx
from typing import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Tuple
from utils import read_json, append_jsonl, read_jsonl, get_timestamp, ensure_dir, format_error
from config import (
    LOCK_TIMEOUT_SECONDS,
    API_TIMEOUT_SECONDS,
    DEFAULT_MIN_BUDGET,
    DEFAULT_MAX_BUDGET,
    validate_model_id,
    validate_config,
)
try:
    from resident_onboarding import spawn_resident, ResidentContext
except ImportError:
    spawn_resident = None
    ResidentContext = None
try:
    from resident_facets import decompose_task as resident_decompose_task
except ImportError:
    resident_decompose_task = None
try:
    from hats import HAT_LIBRARY, apply_hat
except ImportError:
    HAT_LIBRARY = None
    apply_hat = None

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
DEFAULT_MIN_SCORE: float = float(os.environ.get("RESIDENT_MIN_SCORE", "0"))
FOCUS_HAT_MAP = {
    "strategy": "Strategist",
    "build": "Builder",
    "review": "Reviewer",
    "document": "Documenter",
}
DEFAULT_SUBTASK_PARALLELISM: int = int(os.environ.get("RESIDENT_SUBTASK_PARALLELISM", "3"))
RESIDENT_SHARD_COUNT: int = int(os.environ.get("RESIDENT_SHARD_COUNT", "1"))
RESIDENT_SHARD_ID_RAW: str = os.environ.get("RESIDENT_SHARD_ID", "auto").strip().lower()
RESIDENT_SCAN_LIMIT: int = int(os.environ.get("RESIDENT_SCAN_LIMIT", "0"))
RESIDENT_BACKOFF_MAX: int = int(os.environ.get("RESIDENT_BACKOFF_MAX", "5"))
RESIDENT_JITTER_MAX: float = float(os.environ.get("RESIDENT_JITTER_MAX", "0.5"))

_EXECUTION_LOG_STATE: Dict[str, Any] = {"offset": 0, "size": 0, "tasks": {}}
_SCAN_CURSOR: int = 0

# Generate unique resident ID (keep worker_id for compatibility in logs)
RESIDENT_ID: str = f"resident_{uuid.uuid4().hex[:8]}"
WORKER_ID: str = RESIDENT_ID


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
    print(f"[{timestamp}] [{level}] [{RESIDENT_ID}] {message}")




def ensure_directories() -> None:
    """Create required directories if they don't exist."""
    try:
        ensure_dir(LOCKS_DIR)
    except OSError as e:
        _log("ERROR", f"Failed to create locks directory: {e}")
        raise


def read_queue() -> Dict[str, Any]:
    """Read the shared queue file (never write to it from residents)."""
    data = read_json(QUEUE_FILE, default=None)
    if not data:
        return {"tasks": [], "completed": [], "failed": []}
    return data


def read_execution_log() -> Dict[str, Any]:
    """Read the execution log (JSONL) and return latest status per task."""
    if EXECUTION_LOG.exists():
        try:
            size = EXECUTION_LOG.stat().st_size
            if size < _EXECUTION_LOG_STATE["size"]:
                _EXECUTION_LOG_STATE["offset"] = 0
                _EXECUTION_LOG_STATE["tasks"] = {}
            with open(EXECUTION_LOG, "r", encoding="utf-8") as f:
                f.seek(_EXECUTION_LOG_STATE["offset"])
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    task_id = event.get("task_id")
                    if task_id:
                        _EXECUTION_LOG_STATE["tasks"][task_id] = event
                _EXECUTION_LOG_STATE["offset"] = f.tell()
            _EXECUTION_LOG_STATE["size"] = size
            if _EXECUTION_LOG_STATE["tasks"]:
                return {"tasks": dict(_EXECUTION_LOG_STATE["tasks"])}
        except OSError:
            pass

    events = read_jsonl(EXECUTION_LOG, default=[])
    task_index: Dict[str, Any] = {}
    for event in events:
        task_id = event.get("task_id")
        if task_id:
            task_index[task_id] = event
    if task_index:
        return {"tasks": task_index}

    # Legacy fallback: JSON execution log
    legacy_path = WORKSPACE / "execution_log.json"
    legacy_log = read_json(legacy_path, default=None)
    if legacy_log and isinstance(legacy_log, dict):
        legacy_tasks = legacy_log.get("tasks", {})
        if isinstance(legacy_tasks, dict):
            return {"tasks": legacy_tasks}

    return {"tasks": {}}


def append_execution_event(task_id: str, status: str, **fields: Any) -> None:
    """Append an execution event to the JSONL log."""
    record = {
        "task_id": task_id,
        "resident_id": RESIDENT_ID,
        "worker_id": WORKER_ID,
        "status": status,
        "timestamp": get_timestamp(),
        **fields,
    }
    append_jsonl(EXECUTION_LOG, record)


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
        "resident_id": RESIDENT_ID,
        "worker_id": WORKER_ID,
        "started_at": get_timestamp(),
        "task_id": task_id,
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


def _task_shard(task_id: str, shard_count: int) -> int:
    digest = hashlib.sha1(task_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % shard_count


def _resolve_shard_id(resident_id: str) -> Optional[int]:
    if RESIDENT_SHARD_COUNT <= 1:
        return None
    if RESIDENT_SHARD_ID_RAW and RESIDENT_SHARD_ID_RAW != "auto":
        try:
            return int(RESIDENT_SHARD_ID_RAW) % RESIDENT_SHARD_COUNT
        except ValueError:
            return None
    digest = hashlib.sha1(resident_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % RESIDENT_SHARD_COUNT


def _select_tasks_for_scan(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not tasks:
        return tasks
    if RESIDENT_SCAN_LIMIT <= 0 or RESIDENT_SCAN_LIMIT >= len(tasks):
        return tasks
    global _SCAN_CURSOR
    start = _SCAN_CURSOR % len(tasks)
    _SCAN_CURSOR = (_SCAN_CURSOR + RESIDENT_SCAN_LIMIT) % len(tasks)
    rotated = tasks[start:] + tasks[:start]
    return rotated[:RESIDENT_SCAN_LIMIT]


def _compute_idle_sleep(idle_count: int) -> float:
    backoff = min(idle_count, max(1, RESIDENT_BACKOFF_MAX))
    jitter = random.random() * max(0.0, RESIDENT_JITTER_MAX)
    return WORKER_CHECK_INTERVAL * (1 + backoff) + jitter


def _build_facet_plan_text(plan: Any) -> str:
    lines = [
        "RESIDENT FACET PLAN",
        "Facets are optional focus modes. The resident remains the same identity.",
        "",
    ]
    subtasks = getattr(plan, "subtasks", []) or []
    for sub in subtasks:
        desc = getattr(sub, "description", "")
        focus = getattr(sub, "suggested_focus", None)
        shard = getattr(sub, "shard_id", None)
        line = f"- {desc}"
        if focus:
            line += f" (focus: {focus}"
            if shard:
                line += f", shard: {shard}"
            line += ")"
        lines.append(line)
    return "\n".join(lines)


def _should_delegate_task(task: Dict[str, Any]) -> bool:
    mode = str(task.get("decompose") or "").lower().strip()
    if mode in {"atomic", "delegate", "delegated", "sharded"}:
        return True
    return bool(task.get("delegate") or task.get("atomic"))


def _split_budget(min_budget: float, max_budget: float, parts: int) -> Tuple[float, float]:
    if parts <= 1:
        return min_budget, max_budget
    per_min = min_budget / parts if min_budget else min_budget
    per_max = max_budget / parts if max_budget else max_budget
    if per_min and per_max and per_min > per_max:
        per_min = per_max
    return per_min, per_max


def _apply_hat_overlay(prompt: str, focus: Optional[str]) -> str:
    if not prompt or not focus or not HAT_LIBRARY or not apply_hat:
        return prompt
    hat_name = FOCUS_HAT_MAP.get(focus.lower(), focus.title())
    hat = HAT_LIBRARY.get_hat(hat_name)
    if not hat:
        return prompt
    return apply_hat(prompt, hat)


def _execute_delegated_subtasks(
    task_id: str,
    plan: Any,
    api_endpoint: str,
    resident_ctx: Optional["ResidentContext"],
    min_budget: float,
    max_budget: float,
    intensity: str,
    model: Optional[str],
    parallelism: Optional[int] = None,
) -> Dict[str, Any]:
    subtasks: Iterable[Any] = getattr(plan, "subtasks", []) or []
    subtasks_list = list(subtasks)
    if not subtasks_list:
        return {"status": "failed", "result_summary": None, "errors": "No subtasks generated"}

    per_min, per_max = _split_budget(min_budget, max_budget, len(subtasks_list))
    max_parallel = parallelism if isinstance(parallelism, int) and parallelism > 0 else DEFAULT_SUBTASK_PARALLELISM
    max_parallel = max(1, min(max_parallel, len(subtasks_list)))

    def run_subtask(index: int, sub: Any) -> Dict[str, Any]:
        subtask_id = getattr(sub, "subtask_id", None) or f"subtask_{index:02d}"
        focus = getattr(sub, "suggested_focus", None)
        sub_prompt = getattr(sub, "description", "") or ""
        sub_prompt = _apply_hat_overlay(sub_prompt, focus)
        if resident_ctx and sub_prompt:
            sub_prompt = resident_ctx.apply_to_prompt(sub_prompt)

        identity_fields = {}
        if resident_ctx:
            identity_fields["identity_id"] = resident_ctx.identity.identity_id

        append_execution_event(
            task_id,
            "subtask_started",
            subtask_id=subtask_id,
            focus=focus,
            **identity_fields,
        )

        payload = {
            "prompt": sub_prompt,
            "model": model,
            "min_budget": per_min,
            "max_budget": per_max,
            "intensity": intensity,
            "task_id": task_id,
            "subtask_id": subtask_id,
        }
        if resident_ctx:
            payload["resident_id"] = resident_ctx.resident_id
            payload["identity_id"] = resident_ctx.identity.identity_id

        try:
            with httpx.Client(timeout=API_REQUEST_TIMEOUT) as client:
                response = client.post(f"{api_endpoint}/grind", json=payload)
        except httpx.ConnectError as exc:
            error_msg = f"Connection error: {exc}"
            append_execution_event(
                task_id,
                "subtask_failed",
                subtask_id=subtask_id,
                focus=focus,
                errors=error_msg,
                **identity_fields,
            )
            return {
                "status": "failed",
                "error": error_msg,
                "subtask_id": subtask_id,
                "index": index,
            }

        if response.status_code != 200:
            error_msg = f"API returned {response.status_code}: {response.text}"
            append_execution_event(
                task_id,
                "subtask_failed",
                subtask_id=subtask_id,
                focus=focus,
                errors=error_msg,
                **identity_fields,
            )
            return {
                "status": "failed",
                "error": error_msg,
                "subtask_id": subtask_id,
                "index": index,
            }

        result = response.json()
        append_execution_event(
            task_id,
            "subtask_completed",
            subtask_id=subtask_id,
            focus=focus,
            result_summary=result.get("result"),
            model=result.get("model"),
            **identity_fields,
        )
        return {
            "status": "completed",
            "result": result.get("result", f"{subtask_id} completed"),
            "subtask_id": subtask_id,
            "index": index,
        }

    results_by_index: Dict[int, str] = {}
    failures: List[str] = []

    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        futures = {
            executor.submit(run_subtask, idx, sub): idx
            for idx, sub in enumerate(subtasks_list, start=1)
        }
        for future in as_completed(futures):
            outcome = future.result()
            if outcome.get("status") != "completed":
                failures.append(outcome.get("error", "subtask failed"))
            else:
                results_by_index[outcome.get("index", 0)] = outcome.get("result", "subtask completed")

    if failures:
        return {
            "status": "failed",
            "result_summary": None,
            "errors": "; ".join(failures),
        }

    summary = " | ".join(
        results_by_index[idx]
        for idx in sorted(results_by_index.keys())
    )
    return {
        "status": "completed",
        "result_summary": summary,
        "errors": None,
        "model": model,
    }


def execute_task(
    task: Dict[str, Any],
    api_endpoint: str,
    resident_ctx: Optional["ResidentContext"] = None,
) -> Dict[str, Any]:
    """Execute a task by sending it to the Vivarium API."""
    task_id = task.get("id", "unknown")
    min_budget = task.get("min_budget", DEFAULT_MIN_BUDGET)
    max_budget = task.get("max_budget", DEFAULT_MAX_BUDGET)
    intensity = task.get("intensity", DEFAULT_INTENSITY)
    prompt = (
        task.get("prompt")
        or task.get("instruction")
        or task.get("description")
        or task.get("atomic_instruction")
        or task.get("task")
    )
    command = task.get("command") or task.get("shell")
    mode = (task.get("mode") or "").lower().strip() or None
    model = task.get("model")
    if model:
        validate_model_id(model)

    if mode == "local" and not command:
        command = task.get("task")
    if command and not mode:
        mode = "local"

    if not prompt and not command:
        return {
            "status": "failed",
            "result_summary": None,
            "errors": "Task missing prompt/command"
        }

    _log("INFO", f"Executing task {task_id} (budget: ${min_budget}-${max_budget}, intensity: {intensity})")

    should_decompose = bool(task.get("decompose") or task.get("split") or task.get("facet"))
    should_delegate = _should_delegate_task(task)
    if command or mode == "local":
        should_delegate = False

    plan = None
    if resident_ctx and prompt and resident_decompose_task and (should_decompose or should_delegate):
        max_subtasks = task.get("max_subtasks")
        if not isinstance(max_subtasks, int) or max_subtasks <= 0:
            max_subtasks = 3
        plan = resident_decompose_task(
            prompt,
            resident_id=resident_ctx.resident_id,
            identity_id=resident_ctx.identity.identity_id,
            max_subtasks=max_subtasks,
        )

    if plan and should_delegate:
        subtask_parallelism = task.get("subtask_parallelism")
        return _execute_delegated_subtasks(
            task_id=task_id,
            plan=plan,
            api_endpoint=api_endpoint,
            resident_ctx=resident_ctx,
            min_budget=min_budget,
            max_budget=max_budget,
            intensity=intensity,
            model=model,
            parallelism=subtask_parallelism,
        )

    if plan and should_decompose:
        prompt = f"{prompt}\n\n{_build_facet_plan_text(plan)}"

    if resident_ctx and prompt:
        prompt = resident_ctx.apply_to_prompt(prompt)

    payload = {
        "prompt": prompt,
        "model": model,
        "min_budget": min_budget,
        "max_budget": max_budget,
        "intensity": intensity,
        "task_id": task_id,
    }
    if resident_ctx:
        payload["resident_id"] = resident_ctx.resident_id
        payload["identity_id"] = resident_ctx.identity.identity_id
    if command:
        payload["task"] = command
    if mode:
        payload["mode"] = mode

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


def _should_accept_task(
    task: Dict[str, Any],
    resident_ctx: Optional["ResidentContext"],
    min_score: float,
) -> Tuple[bool, str]:
    if not resident_ctx:
        return True, "no resident context"

    identity_id = task.get("identity_id") or task.get("resident_identity")
    if identity_id and identity_id != resident_ctx.identity.identity_id:
        return False, "identity mismatch"

    score, reason = resident_ctx.score_task(task)
    if score < min_score:
        return False, f"score {score:.2f} < {min_score:.2f} ({reason})"
    return True, reason


def find_and_execute_task(
    queue: Dict[str, Any],
    resident_ctx: Optional["ResidentContext"],
    min_score: float,
    shard_id: Optional[int],
) -> bool:
    """Find an available task, lock it, execute it, and report results."""
    execution_log = read_execution_log()
    api_endpoint = queue.get("api_endpoint", "http://127.0.0.1:8420")

    tasks = _select_tasks_for_scan(queue.get("tasks", []))
    for task in tasks:
        task_id = task.get("id")
        if not task_id:
            continue
        if shard_id is not None and _task_shard(task_id, RESIDENT_SHARD_COUNT) != shard_id:
            continue

        if is_task_done(task_id, execution_log):
            continue

        if not check_dependencies_complete(task, execution_log):
            continue

        accept, reason = _should_accept_task(task, resident_ctx, min_score)
        if not accept:
            _log("INFO", f"Skipping {task_id} (voluntary): {reason}")
            continue

        if not try_acquire_lock(task_id):
            continue

        _log("INFO", f"Acquired lock for {task_id}")
        try:
            identity_fields = {}
            if resident_ctx:
                identity_fields["identity_id"] = resident_ctx.identity.identity_id
            append_execution_event(
                task_id,
                "in_progress",
                started_at=get_timestamp(),
                **identity_fields,
            )

            result = execute_task(task, api_endpoint, resident_ctx=resident_ctx)
            append_execution_event(
                task_id,
                result["status"],
                completed_at=get_timestamp(),
                result_summary=result.get("result_summary"),
                errors=result.get("errors"),
                model=result.get("model"),
                **identity_fields,
            )
            _log("INFO", f"Completed task {task_id} - {result['status']}")
        finally:
            release_lock(task_id)
            _log("INFO", f"Released lock for {task_id}")

        return True

    return False


def worker_loop(max_iterations: Optional[int] = None) -> None:
    """Main resident loop. Continuously looks for and executes tasks."""
    try:
        ensure_directories()
        resident_ctx = None
        if spawn_resident:
            try:
                resident_ctx = spawn_resident(WORKSPACE)
                if not resident_ctx:
                    _log("WARN", "No identity available this cycle; exiting.")
                    return
                _log(
                    "INFO",
                    f"Resident {resident_ctx.identity.name} ({resident_ctx.identity.identity_id}) "
                    f"day {resident_ctx.day_count}, cycle {resident_ctx.cycle_id}",
                )
            except Exception as exc:
                _log("WARN", f"Resident onboarding failed: {exc}")

        shard_source = resident_ctx.resident_id if resident_ctx else RESIDENT_ID
        shard_id = _resolve_shard_id(shard_source)
        if shard_id is not None:
            _log(
                "INFO",
                f"Shard assignment {shard_id}/{RESIDENT_SHARD_COUNT} "
                f"(scan_limit={RESIDENT_SCAN_LIMIT or 'full'})",
            )

        _log("INFO", "Starting resident loop")

        iterations = 0
        idle_count = 0

        while True:
            if max_iterations and iterations >= max_iterations:
                _log("INFO", f"Reached max iterations ({max_iterations})")
                break

            try:
                queue = read_queue()

                if find_and_execute_task(queue, resident_ctx, DEFAULT_MIN_SCORE, shard_id):
                    iterations += 1
                    idle_count = 0
                else:
                    idle_count += 1
                    if idle_count >= MAX_IDLE_CYCLES:
                        _log("INFO", f"No tasks available after {MAX_IDLE_CYCLES} checks. Exiting.")
                        break
                    _log("INFO", f"No tasks available, waiting... ({idle_count}/{MAX_IDLE_CYCLES})")
                    time.sleep(_compute_idle_sleep(idle_count))
            except KeyboardInterrupt:
                _log("INFO", "Interrupted by user")
                break
            except Exception as e:
                _log("ERROR", f"Unexpected error in resident loop: {type(e).__name__}: {e}")
                raise

        _log("INFO", f"Resident finished. Executed {iterations} tasks.")
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
            print("  python worker.py run [max_iterations]  - Start resident runtime")
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
