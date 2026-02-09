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
import re
import httpx
from typing import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Tuple
from utils import (
    read_json,
    write_json,
    append_jsonl,
    read_jsonl,
    get_timestamp,
    ensure_dir,
    format_error,
)
from config import (
    LOCK_TIMEOUT_SECONDS,
    API_TIMEOUT_SECONDS,
    DEFAULT_MIN_BUDGET,
    DEFAULT_MAX_BUDGET,
    validate_model_id,
    validate_config,
)
from runtime_contract import normalize_queue, normalize_task, is_known_execution_status
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
try:
    from safety_gateway import SafetyGateway
except ImportError:
    SafetyGateway = None
try:
    from task_verifier import TaskVerifier
except ImportError:
    TaskVerifier = None
try:
    from quality_gates import QualityGateManager, QualityGateError
except ImportError:
    QualityGateManager = None
    QualityGateError = Exception
try:
    from tool_router import get_router as get_tool_router
except ImportError:
    get_tool_router = None
try:
    from intent_gatekeeper import UserIntent, get_gatekeeper as get_intent_gatekeeper
except ImportError:
    UserIntent = None
    get_intent_gatekeeper = None

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
MAX_REQUEUE_ATTEMPTS: int = int(os.environ.get("RESIDENT_MAX_REQUEUE_ATTEMPTS", "3"))
PHASE4_SEQUENCE_SPLIT_RE = re.compile(
    r"\b(?:and then|then|also|plus|after that|next|finally)\b",
    flags=re.IGNORECASE,
)
PHASE4_LEADING_FILLER_RE = re.compile(
    r"^(?:please|can you|could you|i want you to|let's|lets)\s+",
    flags=re.IGNORECASE,
)

_EXECUTION_LOG_STATE: Dict[str, Any] = {"offset": 0, "size": 0, "tasks": {}}
_SCAN_CURSOR: int = 0

# Generate unique resident ID (keep worker_id for compatibility in logs)
RESIDENT_ID: str = f"resident_{uuid.uuid4().hex[:8]}"
WORKER_ID: str = RESIDENT_ID
WORKER_SAFETY_GATEWAY = None
WORKER_TASK_VERIFIER = None
WORKER_QUALITY_GATES = None
WORKER_TOOL_ROUTER = None
WORKER_INTENT_GATEKEEPER = None


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


def _init_worker_safety_gateway():
    if SafetyGateway is None:
        _log("ERROR", "safety_gateway module unavailable; worker will fail closed.")
        return None
    try:
        return SafetyGateway(WORKSPACE)
    except Exception as exc:
        _log("ERROR", f"Failed to initialize worker safety gateway: {exc}")
        return None


WORKER_SAFETY_GATEWAY = _init_worker_safety_gateway()


def _init_worker_task_verifier():
    if TaskVerifier is None:
        _log("WARN", "task_verifier module unavailable; review lifecycle will fail open.")
        return None
    try:
        return TaskVerifier()
    except Exception as exc:
        _log("WARN", f"Failed to initialize task verifier: {exc}")
        return None


def _init_quality_gate_manager():
    if QualityGateManager is None:
        _log("WARN", "quality_gates module unavailable; quality state updates disabled.")
        return None
    try:
        return QualityGateManager(WORKSPACE)
    except Exception as exc:
        _log("WARN", f"Failed to initialize quality gate manager: {exc}")
        return None


def _init_worker_tool_router():
    if get_tool_router is None:
        _log("WARN", "tool_router module unavailable; tool-first routing disabled.")
        return None
    try:
        return get_tool_router()
    except Exception as exc:
        _log("WARN", f"Failed to initialize tool router: {exc}")
        return None


def _init_worker_intent_gatekeeper():
    if get_intent_gatekeeper is None:
        _log("WARN", "intent_gatekeeper module unavailable; intent-preserving prompts disabled.")
        return None
    try:
        return get_intent_gatekeeper()
    except Exception as exc:
        _log("WARN", f"Failed to initialize intent gatekeeper: {exc}")
        return None


WORKER_TASK_VERIFIER = _init_worker_task_verifier()
WORKER_QUALITY_GATES = _init_quality_gate_manager()
WORKER_TOOL_ROUTER = _init_worker_tool_router()
WORKER_INTENT_GATEKEEPER = _init_worker_intent_gatekeeper()




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
    return normalize_queue(data)


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
    if not is_known_execution_status(status):
        _log("WARN", f"Unknown execution status '{status}' (outside canonical contract)")
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
    return task_status in ("completed", "approved", "ready_for_merge", "failed")


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


def _resolve_safety_task_text(prompt: Optional[str], command: Optional[str], mode: Optional[str]) -> str:
    if mode == "local" and command:
        return command
    return prompt or command or ""


def _resolve_task_prompt(task: Dict[str, Any]) -> Optional[str]:
    prompt = (
        task.get("prompt")
        or task.get("instruction")
        or task.get("description")
        or task.get("atomic_instruction")
        or task.get("task")
    )
    if isinstance(prompt, str):
        return prompt
    return None


def _dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    deduped: List[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_string_list(value: Any) -> List[str]:
    if isinstance(value, list):
        coerced: List[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                coerced.append(text)
        return coerced
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _coerce_user_intent(payload: Any) -> Optional["UserIntent"]:
    if UserIntent is None or not isinstance(payload, dict):
        return None
    try:
        return UserIntent(
            goal=str(payload.get("goal") or ""),
            constraints=_coerce_string_list(payload.get("constraints")),
            preferences=_coerce_string_list(payload.get("preferences")),
            anti_goals=_coerce_string_list(payload.get("anti_goals")),
            clarifications=_coerce_string_list(payload.get("clarifications")),
            original_text=str(payload.get("original_text") or ""),
            extracted_at=str(payload.get("extracted_at") or get_timestamp()),
            confidence=_safe_float(payload.get("confidence", 0.5), 0.5),
        )
    except Exception:
        return None


def _resolve_task_intent(task: Dict[str, Any], prompt: Optional[str]) -> Optional["UserIntent"]:
    if WORKER_INTENT_GATEKEEPER is None:
        return None

    seeded_intent = _coerce_user_intent(task.get("phase4_intent") or task.get("intent"))
    if seeded_intent is not None:
        return seeded_intent

    if not prompt:
        return None

    try:
        return WORKER_INTENT_GATEKEEPER.extract_intent(prompt)
    except Exception as exc:
        _log("WARN", f"Intent extraction failed for {task.get('id', 'unknown')}: {exc}")
        return None


def _phase4_gut_check(prompt: str) -> Dict[str, Any]:
    text = (prompt or "").strip()
    signals: List[str] = []
    has_sequence_connector = bool(PHASE4_SEQUENCE_SPLIT_RE.search(text))

    if len(text) >= 220:
        signals.append("long_prompt")
    if text.count("\n") >= 2:
        signals.append("multi_line")
    if has_sequence_connector:
        signals.append("sequencing_connectors")
    punctuation_hits = text.count(",") + text.count(";")
    if punctuation_hits >= 2 or ":" in text or (has_sequence_connector and punctuation_hits >= 1):
        signals.append("compound_clauses")

    complexity_score = len(signals)
    return {
        "complexity_score": complexity_score,
        "signals": signals,
        "should_decompose": complexity_score >= 2,
    }


def _phase4_feature_breakdown(prompt: str, intent_goal: str, max_features: int = 5) -> List[str]:
    text = (prompt or "").strip()
    if not text:
        return [intent_goal] if intent_goal else []

    raw_segments: List[str] = []
    for line in text.splitlines():
        cleaned_line = line.strip().lstrip("-*0123456789. ").strip()
        if cleaned_line:
            raw_segments.append(cleaned_line)
    if not raw_segments:
        raw_segments = [text]

    candidates: List[str] = []
    for segment in raw_segments:
        for clause in re.split(r"[;:]", segment):
            for piece in PHASE4_SEQUENCE_SPLIT_RE.split(clause):
                cleaned = PHASE4_LEADING_FILLER_RE.sub("", piece.strip()).strip(" .,-")
                if len(cleaned) >= 8:
                    candidates.append(cleaned)

    if not candidates:
        fallback = (intent_goal or text).strip()
        return [fallback[:240]] if fallback else []

    deduped: List[str] = []
    seen = set()
    for candidate in candidates:
        key = candidate.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
        if len(deduped) >= max(2, max_features):
            break

    if len(deduped) == 1 and intent_goal and deduped[0].lower() != intent_goal.strip().lower():
        deduped.append(intent_goal.strip())

    return deduped[:max(1, max_features)]


def _phase4_is_candidate(
    task: Dict[str, Any],
    prompt: Optional[str],
    command: Optional[str],
    mode: Optional[str],
    gut_check: Optional[Dict[str, Any]] = None,
) -> bool:
    if not prompt or command or mode == "local":
        return False
    if task.get("phase4_planned") or task.get("phase4_generated") or task.get("phase4_skip"):
        return False

    explicit_request = bool(
        task.get("phase4_plan_request")
        or task.get("decompose")
        or task.get("split")
        or task.get("plan")
    )
    if explicit_request:
        return True

    if gut_check is None:
        gut_check = _phase4_gut_check(prompt)
    return bool(gut_check.get("should_decompose"))


def _phase4_atomize_task(
    task: Dict[str, Any],
    features: List[str],
    intent_payload: Dict[str, Any],
) -> List[Dict[str, Any]]:
    if not features:
        return []

    parent_id = str(task.get("id") or "task")
    base_depends = list(task.get("depends_on") or [])
    total_steps = len(features)

    min_budget = _safe_float(task.get("min_budget"), DEFAULT_MIN_BUDGET)
    max_budget = _safe_float(task.get("max_budget"), DEFAULT_MAX_BUDGET)
    if max_budget and min_budget > max_budget:
        min_budget = max_budget
    per_min, per_max = _split_budget(min_budget, max_budget, total_steps)

    intensity = str(task.get("intensity") or DEFAULT_INTENSITY)
    model = task.get("model")
    mode = task.get("mode")

    subtasks: List[Dict[str, Any]] = []
    for index, feature in enumerate(features, start=1):
        subtask_id = f"{parent_id}__phase4_{index:02d}"
        depends_on = [f"{parent_id}__phase4_{index - 1:02d}"] if index > 1 else list(base_depends)
        subtask_prompt = (
            f"Phase 4 decomposition step {index}/{total_steps} for parent task '{parent_id}'.\n"
            f"Focus area: {feature}\n"
            "Deliver the smallest verifiable unit that advances the parent goal."
        )
        subtask = normalize_task(
            {
                "id": subtask_id,
                "type": "grind",
                "prompt": subtask_prompt,
                "min_budget": per_min,
                "max_budget": per_max,
                "intensity": intensity,
                "depends_on": _dedupe_preserve_order(depends_on),
                "parallel_safe": False,
                "phase4_generated": True,
                "phase4_skip": True,
                "phase4_parent_task": parent_id,
                "phase4_intent": intent_payload,
            }
        )
        if mode:
            subtask["mode"] = mode
        if model:
            subtask["model"] = model
        subtasks.append(subtask)

    return subtasks


def _maybe_compile_phase4_plan(task: Dict[str, Any], queue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    prompt = _resolve_task_prompt(task)
    command = task.get("command") or task.get("shell")
    mode = (task.get("mode") or "").lower().strip() or None
    gut_check = _phase4_gut_check(prompt or "")

    if not _phase4_is_candidate(task, prompt, command, mode, gut_check):
        return None

    task_intent = _resolve_task_intent(task, prompt)
    if task_intent is None:
        return None

    max_subtasks = task.get("max_subtasks")
    feature_limit = max_subtasks if isinstance(max_subtasks, int) and max_subtasks > 0 else 5
    features = _phase4_feature_breakdown(task_intent.original_text or (prompt or ""), task_intent.goal, feature_limit)
    explicit_request = bool(
        task.get("phase4_plan_request")
        or task.get("decompose")
        or task.get("split")
        or task.get("plan")
    )
    if len(features) < 2 and not explicit_request:
        return None

    intent_payload = task_intent.to_dict()
    subtasks = _phase4_atomize_task(task, features, intent_payload)
    if not subtasks:
        return None

    queue_tasks = queue.setdefault("tasks", [])
    existing_ids = {str(existing.get("id")) for existing in queue_tasks if isinstance(existing, dict)}
    new_subtasks = [subtask for subtask in subtasks if subtask["id"] not in existing_ids]
    queue_tasks.extend(new_subtasks)

    subtask_ids = [subtask["id"] for subtask in subtasks]
    parent_dependencies = list(task.get("depends_on") or [])
    task["depends_on"] = _dedupe_preserve_order(parent_dependencies + subtask_ids)
    task["phase4_planned"] = True
    task["phase4_intent"] = intent_payload
    task["phase4_plan"] = {
        "gut_check": gut_check,
        "features": features,
        "subtasks": subtask_ids,
    }

    write_json(QUEUE_FILE, normalize_queue(queue))

    return {
        "complexity_score": gut_check.get("complexity_score", 0),
        "features": features,
        "subtask_ids": subtask_ids,
        "subtasks_added": len(new_subtasks),
    }


def _run_worker_safety_check(
    task_id: str,
    prompt: Optional[str],
    command: Optional[str],
    mode: Optional[str],
) -> Tuple[bool, Dict[str, Any]]:
    task_text = _resolve_safety_task_text(prompt, command, mode)
    if not task_text:
        return False, {
            "passed": False,
            "blocked_reason": "Task missing prompt/command for safety checks",
            "task_id": task_id,
            "checks": {},
        }

    if WORKER_SAFETY_GATEWAY is None:
        return False, {
            "passed": False,
            "blocked_reason": "Safety gateway unavailable",
            "task_id": task_id,
            "checks": {},
        }

    passed, report = WORKER_SAFETY_GATEWAY.pre_execute_safety_check(task_text)
    report["task_id"] = task_id
    return passed, report


def _resolve_files_for_review(task: Dict[str, Any], result: Dict[str, Any]) -> List[str]:
    file_candidates: List[str] = []
    for source in (task, result):
        for key in ("files_created", "files_modified", "artifacts"):
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                file_candidates.append(value.strip())
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item.strip():
                        file_candidates.append(item.strip())

    resolved: List[str] = []
    for raw_path in file_candidates:
        path = Path(raw_path)
        if not path.is_absolute():
            path = WORKSPACE / path
        resolved.append(str(path))
    return resolved


def _quality_gate_author_id(task: Dict[str, Any], resident_ctx: Optional["ResidentContext"]) -> str:
    if resident_ctx and getattr(resident_ctx, "identity", None):
        return resident_ctx.identity.identity_id
    return (
        task.get("identity_id")
        or task.get("resident_identity")
        or task.get("author_id")
        or RESIDENT_ID
    )


def _ensure_quality_gate_change(task: Dict[str, Any], resident_ctx: Optional["ResidentContext"]) -> Optional[str]:
    if WORKER_QUALITY_GATES is None:
        return None

    change_id = task.get("id", "unknown")
    try:
        state = WORKER_QUALITY_GATES.load_state()
        if change_id in state.get("changes", {}):
            return change_id

        title = (
            task.get("title")
            or task.get("prompt")
            or task.get("description")
            or task.get("task")
            or f"Task {change_id}"
        )
        description = task.get("description") or task.get("prompt") or task.get("task") or ""
        author_id = _quality_gate_author_id(task, resident_ctx)
        WORKER_QUALITY_GATES.submit_change_for_vote(
            title=str(title)[:240],
            description=str(description),
            author_id=str(author_id),
            change_id=str(change_id),
        )
        return change_id
    except Exception as exc:
        _log("WARN", f"Quality gate bootstrap failed for {change_id}: {exc}")
        return None


def _record_quality_gate_review(
    task: Dict[str, Any],
    resident_ctx: Optional["ResidentContext"],
    *,
    approved: bool,
) -> Dict[str, Any]:
    if WORKER_QUALITY_GATES is None:
        return {
            "quality_gate_status": "unavailable",
            "quality_gate_decision": None,
            "quality_gate_change_id": None,
        }

    change_id = _ensure_quality_gate_change(task, resident_ctx)
    if not change_id:
        return {
            "quality_gate_status": "error",
            "quality_gate_decision": None,
            "quality_gate_change_id": None,
        }

    decision = "approved" if approved else "rejected"
    try:
        change = WORKER_QUALITY_GATES.record_change_vote(change_id, decision)
        return {
            "quality_gate_status": change.get("status"),
            "quality_gate_decision": decision,
            "quality_gate_change_id": change_id,
        }
    except QualityGateError as exc:
        _log("WARN", f"Quality gate decision failed for {change_id}: {exc}")
        return {
            "quality_gate_status": "error",
            "quality_gate_decision": decision,
            "quality_gate_change_id": change_id,
            "quality_gate_error": str(exc),
        }


def _run_post_execution_review(
    task: Dict[str, Any],
    result: Dict[str, Any],
    resident_ctx: Optional["ResidentContext"],
    previous_review_attempt: int,
) -> Dict[str, Any]:
    task_id = task.get("id", "unknown")
    files_created = _resolve_files_for_review(task, result)
    verification_payload = {
        "success": result.get("status") == "completed",
        "error": result.get("errors"),
        "result": result.get("result_summary"),
        "model": result.get("model"),
    }

    verdict_name = "APPROVE"
    confidence = 1.0
    issues: List[str] = []
    suggestions: List[str] = []
    approved = True

    if WORKER_TASK_VERIFIER is not None:
        try:
            verification = WORKER_TASK_VERIFIER.verify_task_output(
                task=task,
                output=verification_payload,
                files_created=files_created,
            )
            verdict_name = getattr(getattr(verification, "verdict", None), "value", "APPROVE")
            confidence = float(getattr(verification, "confidence", 1.0))
            issues = list(getattr(verification, "issues", []) or [])
            suggestions = list(getattr(verification, "suggestions", []) or [])
            approved = bool(verification.should_accept())
        except Exception as exc:
            _log("WARN", f"Task verifier failed for {task_id}, failing open: {exc}")
    else:
        suggestions = ["Task verifier unavailable; accepted without critic review."]

    review_attempt = previous_review_attempt + (0 if approved else 1)
    append_execution_event(
        task_id,
        "pending_review",
        review_verdict=verdict_name,
        review_confidence=confidence,
        review_issues=issues,
        review_suggestions=suggestions,
        review_attempt=review_attempt,
    )

    quality_gate = _record_quality_gate_review(task, resident_ctx, approved=approved)
    review_summary = {
        "review_verdict": verdict_name,
        "review_confidence": confidence,
        "review_issues": issues,
        "review_suggestions": suggestions,
        "review_attempt": review_attempt,
        **quality_gate,
    }

    if approved:
        return {
            "status": "approved",
            "result_summary": result.get("result_summary"),
            "errors": None,
            **review_summary,
        }

    rejection_reason = "; ".join(issues) if issues else "critic rejected task output"
    if review_attempt >= max(1, MAX_REQUEUE_ATTEMPTS):
        return {
            "status": "failed",
            "result_summary": None,
            "errors": (
                f"Quality gate rejected task after {review_attempt} attempt(s): "
                f"{rejection_reason}"
            ),
            **review_summary,
        }

    return {
        "status": "requeue",
        "result_summary": None,
        "errors": f"Quality gate rejected task: {rejection_reason}",
        **review_summary,
    }


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

        safety_passed, safety_report = _run_worker_safety_check(
            task_id=f"{task_id}:{subtask_id}",
            prompt=sub_prompt,
            command=None,
            mode="llm",
        )
        if not safety_passed:
            error_msg = f"Safety check failed: {safety_report.get('blocked_reason', 'blocked')}"
            append_execution_event(
                task_id,
                "subtask_failed",
                subtask_id=subtask_id,
                focus=focus,
                errors=error_msg,
                safety_report=safety_report,
                **identity_fields,
            )
            return {
                "status": "failed",
                "error": error_msg,
                "subtask_id": subtask_id,
                "index": index,
            }

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
    prompt = _resolve_task_prompt(task)
    command = task.get("command") or task.get("shell")
    mode = (task.get("mode") or "").lower().strip() or None
    model = task.get("model")
    task_intent = _resolve_task_intent(task, prompt)
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
            "errors": "Task missing prompt/command",
            "safety_passed": False,
            "safety_report": {
                "passed": False,
                "blocked_reason": "Task missing prompt/command",
                "task_id": task_id,
                "checks": {},
            },
        }

    tool_route_info: Dict[str, Any] = {}

    safety_passed, safety_report = _run_worker_safety_check(task_id, prompt, command, mode)
    if not safety_passed:
        blocked_reason = safety_report.get("blocked_reason", "blocked by worker safety gateway")
        return {
            "status": "failed",
            "result_summary": None,
            "errors": f"Safety check failed: {blocked_reason}",
            "safety_passed": False,
            "safety_report": safety_report,
            **tool_route_info,
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
        delegated_result = _execute_delegated_subtasks(
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
        delegated_result["safety_passed"] = safety_passed
        delegated_result["safety_report"] = safety_report
        return delegated_result

    if plan and should_decompose:
        prompt = f"{prompt}\n\n{_build_facet_plan_text(plan)}"

    if resident_ctx and prompt:
        prompt = resident_ctx.apply_to_prompt(prompt)

    if prompt and mode != "local" and not command and WORKER_TOOL_ROUTER is not None:
        try:
            route_result = WORKER_TOOL_ROUTER.route(prompt, context={"task_id": task_id})
            if route_result and getattr(route_result, "found", False) and getattr(route_result, "tool", None):
                routed_tool = route_result.tool
                tool_name = str(routed_tool.get("name") or "unnamed_tool")
                tool_description = str(routed_tool.get("description") or "").strip()
                tool_code = str(routed_tool.get("code") or "").strip()
                tool_route = str(getattr(route_result, "route", "unknown"))
                tool_confidence = float(getattr(route_result, "confidence", 0.0))
                tool_route_info = {
                    "tool_route": tool_route,
                    "tool_name": tool_name,
                    "tool_confidence": tool_confidence,
                }
                if tool_code:
                    prompt = (
                        "RELEVANT TOOL CONTEXT (reuse before new generation)\n"
                        f"TOOL_NAME: {tool_name}\n"
                        f"TOOL_ROUTE: {tool_route}\n"
                        f"TOOL_CONFIDENCE: {tool_confidence:.2f}\n"
                        f"TOOL_DESCRIPTION: {tool_description or 'n/a'}\n\n"
                        f"{tool_code}\n\n"
                        "TASK:\n"
                        f"{prompt}"
                    )
                _log("INFO", f"Tool router selected {tool_name} via {tool_route} for {task_id}")
        except Exception as exc:
            _log("WARN", f"Tool routing failed for {task_id}: {exc}")

    if (
        prompt
        and mode != "local"
        and task_intent is not None
        and WORKER_INTENT_GATEKEEPER is not None
    ):
        try:
            prompt = WORKER_INTENT_GATEKEEPER.inject_into_prompt(prompt, task_intent)
        except Exception as exc:
            _log("WARN", f"Intent injection failed for {task_id}: {exc}")

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
            api_safety_report = result.get("safety_report")
            return {
                "status": "completed",
                "result_summary": result.get("result", "Task completed"),
                "errors": None,
                "model": result.get("model"),
                "safety_passed": bool((api_safety_report or safety_report).get("passed", True)),
                "safety_report": api_safety_report or safety_report,
                **tool_route_info,
            }

        error_msg = f"API returned {response.status_code}: {response.text}"
        _log("WARN", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg,
            "safety_passed": safety_passed,
            "safety_report": safety_report,
            **tool_route_info,
        }
    except httpx.ConnectError as e:
        error_msg = f"Cannot connect to API at {api_endpoint}: {e}"
        _log("ERROR", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg,
            "safety_passed": safety_passed,
            "safety_report": safety_report,
            **tool_route_info,
        }
    except httpx.TimeoutException as e:
        error_msg = f"API request timeout: {e}"
        _log("ERROR", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg,
            "safety_passed": safety_passed,
            "safety_report": safety_report,
            **tool_route_info,
        }
    except json.JSONDecodeError as e:
        error_msg = f"Invalid API response: {e}"
        _log("ERROR", error_msg)
        return {
            "status": "failed",
            "result_summary": None,
            "errors": error_msg,
            "safety_passed": safety_passed,
            "safety_report": safety_report,
            **tool_route_info,
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
            last_event = execution_log.get("tasks", {}).get(task_id, {})
            try:
                previous_review_attempt = int(last_event.get("review_attempt", 0))
            except (TypeError, ValueError):
                previous_review_attempt = 0
            if last_event.get("status") not in {"requeue", "pending_review"}:
                previous_review_attempt = 0

            identity_fields = {}
            if resident_ctx:
                identity_fields["identity_id"] = resident_ctx.identity.identity_id

            phase4_plan = _maybe_compile_phase4_plan(task, queue)
            if phase4_plan:
                append_execution_event(
                    task_id,
                    "queued",
                    phase4_plan_generated=True,
                    phase4_complexity_score=phase4_plan.get("complexity_score"),
                    phase4_features=phase4_plan.get("features"),
                    phase4_subtasks=phase4_plan.get("subtask_ids"),
                    phase4_subtasks_added=phase4_plan.get("subtasks_added"),
                    **identity_fields,
                )
                _log(
                    "INFO",
                    (
                        f"Phase 4 decomposition generated for {task_id}: "
                        f"{len(phase4_plan.get('subtask_ids', []))} subtasks"
                    ),
                )
                return True

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
                safety_passed=result.get("safety_passed"),
                safety_report=result.get("safety_report"),
                tool_route=result.get("tool_route"),
                tool_name=result.get("tool_name"),
                tool_confidence=result.get("tool_confidence"),
                **identity_fields,
            )

            final_status = result["status"]
            if final_status == "completed":
                review_result = _run_post_execution_review(
                    task=task,
                    result=result,
                    resident_ctx=resident_ctx,
                    previous_review_attempt=previous_review_attempt,
                )
                final_status = review_result["status"]
                append_execution_event(
                    task_id,
                    final_status,
                    completed_at=get_timestamp(),
                    result_summary=review_result.get("result_summary"),
                    errors=review_result.get("errors"),
                    model=result.get("model"),
                    safety_passed=result.get("safety_passed"),
                    safety_report=result.get("safety_report"),
                    review_verdict=review_result.get("review_verdict"),
                    review_confidence=review_result.get("review_confidence"),
                    review_issues=review_result.get("review_issues"),
                    review_suggestions=review_result.get("review_suggestions"),
                    review_attempt=review_result.get("review_attempt"),
                    quality_gate_status=review_result.get("quality_gate_status"),
                    quality_gate_decision=review_result.get("quality_gate_decision"),
                    quality_gate_change_id=review_result.get("quality_gate_change_id"),
                    quality_gate_error=review_result.get("quality_gate_error"),
                    tool_route=result.get("tool_route"),
                    tool_name=result.get("tool_name"),
                    tool_confidence=result.get("tool_confidence"),
                    **identity_fields,
                )

            _log("INFO", f"Completed task {task_id} - {final_status}")
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

        task: Dict[str, Any] = normalize_task({
            "id": task_id,
            "type": task_type,
            "prompt": prompt,
            "min_budget": min_budget,
            "max_budget": max_budget,
            "intensity": intensity,
            "depends_on": depends_on or [],
            "parallel_safe": True,
            "model": model,
        })

        queue["tasks"].append(task)

        write_json(QUEUE_FILE, normalize_queue(queue))

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
