"""
Resident Runtime for Vivarium

Uses file-based lock protocol for coordination between multiple residents.
Lock Protocol from: EXECUTION_SWARM_SYSTEM.md (legacy orchestrator spec)

Target API: http://127.0.0.1:8420 (Vivarium)
"""

from dotenv import load_dotenv
load_dotenv()

import json
import os
import sys
import time
import uuid
import hashlib
import random
import re
import threading
import httpx
from ipaddress import ip_address
from typing import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urlparse
from vivarium.utils import (
    read_json,
    write_json,
    append_jsonl,
    read_jsonl,
    get_timestamp,
    ensure_dir,
    format_error,
)
from vivarium.runtime.config import (
    LOCK_TIMEOUT_SECONDS,
    API_TIMEOUT_SECONDS,
    DEFAULT_MIN_BUDGET,
    DEFAULT_MAX_BUDGET,
    validate_model_id,
    validate_config,
)
from vivarium.runtime.runtime_contract import normalize_queue, normalize_task, is_known_execution_status
from vivarium.runtime.vivarium_scope import (
    AUDIT_ROOT,
    MUTABLE_COMMUNITY_LIBRARY_ROOT,
    MUTABLE_LOCKS_DIR,
    MUTABLE_QUEUE_FILE,
    MUTABLE_ROOT,
    MUTABLE_SWARM_DIR,
    SECURITY_ROOT,
    ensure_scope_layout,
    get_execution_token,
    get_mutable_version_control,
    resolve_mutable_path,
)
try:
    from vivarium.runtime.resident_onboarding import spawn_resident, release_identity_lock, ResidentContext
except ImportError:
    spawn_resident = None
    release_identity_lock = None
    ResidentContext = None
try:
    from vivarium.runtime.resident_facets import decompose_task as resident_decompose_task
except ImportError:
    resident_decompose_task = None
try:
    from vivarium.runtime.hats import HAT_LIBRARY, apply_hat
except ImportError:
    HAT_LIBRARY = None
    apply_hat = None
try:
    from vivarium.runtime.safety_gateway import SafetyGateway
except ImportError:
    SafetyGateway = None
try:
    from vivarium.runtime.task_verifier import TaskVerifier
except ImportError:
    TaskVerifier = None
try:
    from vivarium.runtime.quality_gates import QualityGateManager, QualityGateError
except ImportError:
    QualityGateManager = None
    QualityGateError = Exception
try:
    from vivarium.runtime.tool_router import get_router as get_tool_router
except ImportError:
    get_tool_router = None
try:
    from vivarium.runtime.intent_gatekeeper import UserIntent, get_gatekeeper as get_intent_gatekeeper
except ImportError:
    UserIntent = None
    get_intent_gatekeeper = None
try:
    from vivarium.runtime.swarm_enrichment import get_enrichment
except ImportError:
    get_enrichment = None

# ============================================================================
# CONSTANTS
# ============================================================================
ensure_scope_layout()
WORKSPACE: Path = MUTABLE_ROOT
REPO_ROOT: Path = Path(__file__).resolve().parents[2]
QUEUE_FILE: Path = MUTABLE_QUEUE_FILE
LOCKS_DIR: Path = MUTABLE_LOCKS_DIR
EXECUTION_LOG: Path = AUDIT_ROOT / "execution_log.jsonl"
PHASE5_REWARD_LEDGER: Path = MUTABLE_SWARM_DIR / "phase5_reward_ledger.json"
MVP_ARTIFACT_FINGERPRINTS_FILE: Path = MUTABLE_SWARM_DIR / "artifact_fingerprints.json"

API_REQUEST_TIMEOUT: float = API_TIMEOUT_SECONDS
WORKER_CHECK_INTERVAL: float = 2.0  # Delay between queue checks in seconds
MAX_IDLE_CYCLES: int = 10  # Exit after N consecutive idle checks
DEFAULT_INTENSITY: str = "medium"
DEFAULT_TASK_TYPE: str = "cycle"
CYCLE_EXECUTION_ENDPOINT: str = "/cycle"
DEFAULT_MIN_SCORE: float = float(os.environ.get("RESIDENT_MIN_SCORE", "0"))
ENRICHMENT_RECALL_MAX_CHARS: int = 600
ENRICHMENT_RECALL_LIMIT: int = 4
ENRICHMENT_RECALL_DISPLAY_LIMIT: int = 4
DISCUSSION_REPLY_LOOKBACK_LIMIT: int = 8
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
RUNTIME_SPEED_FILE: Path = MUTABLE_SWARM_DIR / "runtime_speed.json"
DEFAULT_RUNTIME_WAIT_SECONDS: float = float(os.environ.get("VIVARIUM_RUNTIME_WAIT_SECONDS", str(WORKER_CHECK_INTERVAL)))
AUTO_DISCUSSION_UPDATES: bool = (
    os.environ.get("VIVARIUM_AUTO_DISCUSSION_UPDATES", "1").strip().lower()
    not in {"0", "false", "no"}
)
PHASE4_SEQUENCE_SPLIT_RE = re.compile(
    r"\b(?:and then|then|also|plus|after that|next|finally)\b",
    flags=re.IGNORECASE,
)
PHASE4_LEADING_FILLER_RE = re.compile(
    r"^(?:please|can you|could you|i want you to|let's|lets)\s+",
    flags=re.IGNORECASE,
)
PHASE4_COMMA_NON_ACTION_PREFIXES: Tuple[str, ...] = (
    "with ",
    "using ",
    "via ",
    "for ",
    "including ",
    "without ",
    "where ",
    "when ",
    "while ",
    "because ",
)
MVP_DOCS_ONLY_MODE: bool = (
    os.environ.get("VIVARIUM_MVP_DOCS_ONLY", "1").strip().lower()
    not in {"0", "false", "no"}
)
MVP_JOURNALS_DIR: Path = MUTABLE_SWARM_DIR / "journals"
MVP_COMMUNITY_LIBRARY_ROOT: Path = MUTABLE_COMMUNITY_LIBRARY_ROOT
MVP_LIBRARY_DOCS_DIR: Path = MVP_COMMUNITY_LIBRARY_ROOT / "swarm_docs"
MVP_LIBRARY_RESIDENT_SUGGESTIONS_ROOT: Path = MVP_COMMUNITY_LIBRARY_ROOT / "resident_suggestions"
MVP_LEGACY_LIBRARY_DOCS_DIR: Path = WORKSPACE / "library" / "swarm_docs"
MVP_LEGACY_RESIDENT_SUGGESTIONS_ROOT: Path = WORKSPACE / "library" / "resident_suggestions"
MVP_ALLOWED_DOC_ROOTS: Tuple[Path, ...] = (
    MVP_JOURNALS_DIR,
    MVP_LIBRARY_DOCS_DIR,
    MVP_LIBRARY_RESIDENT_SUGGESTIONS_ROOT,
    MVP_LEGACY_LIBRARY_DOCS_DIR,
    MVP_LEGACY_RESIDENT_SUGGESTIONS_ROOT,
)

_EXECUTION_LOG_STATE: Dict[str, Any] = {"offset": 0, "size": 0, "tasks": {}}
_EXECUTION_LOG_LOCK = threading.Lock()
_SCAN_CURSOR: int = 0

# Generate unique resident ID (keep worker_id for compatibility in logs)
RESIDENT_ID: str = f"resident_{uuid.uuid4().hex[:8]}"
WORKER_ID: str = RESIDENT_ID
WORKER_SAFETY_GATEWAY = None
WORKER_TASK_VERIFIER = None
WORKER_QUALITY_GATES = None
WORKER_TOOL_ROUTER = None
WORKER_INTENT_GATEKEEPER = None
WORKER_ENRICHMENT = None
WORKER_MUTABLE_VCS = None
WORKER_INTERNAL_EXECUTION_TOKEN = get_execution_token()


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
        constraints_file = SECURITY_ROOT / "SAFETY_CONSTRAINTS.json"
        if not constraints_file.exists():
            constraints_file = REPO_ROOT / "config" / "SAFETY_CONSTRAINTS.json"
        return SafetyGateway(
            WORKSPACE,
            constraints_file=constraints_file,
            audit_log=AUDIT_ROOT / "safety_audit.log",
        )
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
    if MVP_DOCS_ONLY_MODE:
        _log("INFO", "MVP docs-only mode enabled; tool routing disabled.")
        return None
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


def _init_worker_enrichment():
    if get_enrichment is None:
        _log("WARN", "swarm_enrichment module unavailable; phase5 rewards disabled.")
        return None
    try:
        return get_enrichment(WORKSPACE)
    except Exception as exc:
        _log("WARN", f"Failed to initialize swarm enrichment system: {exc}")
        return None


def _init_mutable_version_control():
    if MVP_DOCS_ONLY_MODE:
        _log("INFO", "MVP docs-only mode enabled; mutable git checkpointing disabled.")
        return None
    try:
        return get_mutable_version_control()
    except Exception as exc:
        _log("WARN", f"Failed to initialize mutable auto-checkpoint manager: {exc}")
        return None


WORKER_TASK_VERIFIER = _init_worker_task_verifier()
WORKER_QUALITY_GATES = _init_quality_gate_manager()
WORKER_TOOL_ROUTER = _init_worker_tool_router()
WORKER_INTENT_GATEKEEPER = _init_worker_intent_gatekeeper()
WORKER_ENRICHMENT = _init_worker_enrichment()
WORKER_MUTABLE_VCS = _init_mutable_version_control()


def _build_enrichment_prompt_context(
    resident_ctx: Optional["ResidentContext"],
    task_prompt: Optional[str] = None,
) -> Optional[str]:
    """Build optional social/economic context for the active resident."""
    if resident_ctx is None or WORKER_ENRICHMENT is None:
        return None

    identity = getattr(resident_ctx, "identity", None)
    identity_id = str(getattr(identity, "identity_id", "")).strip()
    identity_name = str(getattr(identity, "name", "")).strip() or identity_id
    if not identity_id:
        return None

    sections: List[str] = []
    try:
        if hasattr(WORKER_ENRICHMENT, "get_morning_messages"):
            morning_messages = WORKER_ENRICHMENT.get_morning_messages(identity_id)
            if isinstance(morning_messages, str) and morning_messages.strip():
                sections.append(morning_messages.strip())
    except Exception as exc:
        _log("WARN", f"Failed to load morning messages for {identity_id}: {exc}")

    try:
        if hasattr(WORKER_ENRICHMENT, "get_discussion_context"):
            discussion_context = WORKER_ENRICHMENT.get_discussion_context(identity_id, identity_name)
            if isinstance(discussion_context, str) and discussion_context.strip():
                sections.append(discussion_context.strip())
    except Exception as exc:
        _log("WARN", f"Failed to load discussion context for {identity_id}: {exc}")

    try:
        if hasattr(WORKER_ENRICHMENT, "get_enrichment_context"):
            enrichment_context = WORKER_ENRICHMENT.get_enrichment_context(identity_id, identity_name)
            if isinstance(enrichment_context, str) and enrichment_context.strip():
                sections.append(enrichment_context.strip())
    except Exception as exc:
        _log("WARN", f"Failed to load enrichment context for {identity_id}: {exc}")

    # Add a compact, task-scoped memory recall block to reduce context bloat.
    try:
        if hasattr(WORKER_ENRICHMENT, "recall_memory"):
            recall = WORKER_ENRICHMENT.recall_memory(
                identity_id=identity_id,
                query=task_prompt or "",
                limit=ENRICHMENT_RECALL_LIMIT,
                max_chars=ENRICHMENT_RECALL_MAX_CHARS,
            )
            hits = recall.get("hits", []) if isinstance(recall, dict) else []
            if hits:
                recall_lines = [
                    "TARGETED MEMORY RECALL (token-efficient):",
                ]
                for item in hits[:ENRICHMENT_RECALL_DISPLAY_LIMIT]:
                    recall_lines.append(f"- {item}")
                sections.append("\n".join(recall_lines))
    except Exception as exc:
        _log("WARN", f"Failed to recall memory for {identity_id}: {exc}")

    # Make sure residents know that excellence and coming in under budget can earn manual rewards from the human.
    sections.append(
        "REWARDS: If you exceed the human's expectations, do a great job, and come in under budget, "
        "they will reward you manually based on quality (e.g. tip and feedback when they approve the task). "
        "Sharing what the human liked (tips, feedback, preferences) in town hall or in your journal is encouraged and can earn recognition—optional but incentivized. "
        "Gifting a fellow resident when they share useful info is good for your own gain too: it helps establish cooperation, and what is good for the whole is good for the singular."
    )

    if not sections:
        return None
    return "\n\n".join(sections)


def _truncate_single_line(value: Any, max_chars: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)] + "..."


def _publish_task_update_to_discussion(
    task: Dict[str, Any],
    resident_ctx: Optional["ResidentContext"],
    task_id: str,
    result_summary: Any,
) -> None:
    if not AUTO_DISCUSSION_UPDATES or resident_ctx is None or WORKER_ENRICHMENT is None:
        return
    if not hasattr(WORKER_ENRICHMENT, "post_discussion_message"):
        return

    identity = getattr(resident_ctx, "identity", None)
    identity_id = str(getattr(identity, "identity_id", "")).strip()
    identity_name = str(getattr(identity, "name", "")).strip() or identity_id or "resident"
    if not identity_id:
        return

    room = str(task.get("discussion_room") or "town_hall").strip() or "town_hall"
    dm_target = str(task.get("recipient_identity_id") or task.get("dm_to") or "").strip()
    if not dm_target and room.lower().startswith("dm:"):
        dm_target = room.split(":", 1)[1].strip()
    summary_line = _truncate_single_line(result_summary or "Task completed.", 240)
    focus_line = _truncate_single_line(
        _resolve_task_prompt(task) or task.get("task") or task.get("command") or "",
        160,
    )
    content = f"Task {task_id} update: {summary_line}"
    if focus_line:
        content += f"\nFocus: {focus_line}"

    reply_to = None
    try:
        if hasattr(WORKER_ENRICHMENT, "get_discussion_messages"):
            recent = WORKER_ENRICHMENT.get_discussion_messages(room, limit=DISCUSSION_REPLY_LOOKBACK_LIMIT)
            for message in reversed(recent):
                author_id = str(message.get("author_id") or "").strip()
                if author_id and author_id != identity_id:
                    reply_to = message.get("id")
                    break
    except Exception:
        reply_to = None

    try:
        if dm_target and dm_target != identity_id and hasattr(WORKER_ENRICHMENT, "post_direct_message"):
            WORKER_ENRICHMENT.post_direct_message(
                sender_id=identity_id,
                sender_name=identity_name,
                recipient_id=dm_target,
                content=content,
                importance=3,
                reply_to=reply_to,
            )
        else:
            WORKER_ENRICHMENT.post_discussion_message(
                identity_id=identity_id,
                identity_name=identity_name,
                content=content,
                room=room,
                mood="focused",
                importance=3,
                reply_to=reply_to,
            )
    except Exception as exc:
        _log("WARN", f"Failed to publish discussion update for {task_id}: {exc}")


def _slugify_token(value: str, fallback: str = "artifact") -> str:
    token = re.sub(r"[^a-zA-Z0-9._-]+", "_", str(value or "").strip()).strip("._-")
    return token[:80] if token else fallback


def _is_within_any(path: Path, roots: Tuple[Path, ...]) -> bool:
    for root in roots:
        try:
            if path == root or root in path.parents:
                return True
        except Exception:
            continue
    return False


def _resolve_mvp_markdown_target(task: Dict[str, Any]) -> Tuple[Optional[Path], Optional[str]]:
    raw_path = (
        task.get("doc_path")
        or task.get("artifact_path")
        or task.get("output_path")
    )
    if not raw_path:
        return None, None

    try:
        resolved = resolve_mutable_path(str(raw_path), cwd=WORKSPACE)
    except ValueError:
        return None, "doc target escapes mutable workspace"

    if resolved.suffix.lower() != ".md":
        return None, "doc target must end with .md"

    allowed_roots = tuple(root.resolve() for root in MVP_ALLOWED_DOC_ROOTS)
    resolved_rooted = resolved.resolve()
    if not _is_within_any(resolved_rooted, allowed_roots):
        return None, "doc target must stay within markdown artifact roots"

    return resolved_rooted, None


def _format_markdown_record(
    *,
    task_id: str,
    title: str,
    prompt: str,
    result: str,
    timestamp: datetime,
    identity_id: str,
    identity_name: str,
) -> str:
    iso = timestamp.isoformat()
    lines = [
        f"# {title}",
        "",
        f"- generated_at: {iso}",
        f"- task_id: {task_id}",
        f"- identity_id: {identity_id}",
        f"- identity_name: {identity_name}",
        "",
        "## Prompt",
        "",
        prompt.strip() if prompt.strip() else "_none_",
        "",
        "## Suggestion",
        "",
        result.strip(),
        "",
    ]
    return "\n".join(lines)


def _normalize_artifact_text(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _compute_artifact_fingerprint(identity_id: str, prompt: str, result_text: str) -> str:
    payload = "\n".join(
        [
            _normalize_artifact_text(identity_id),
            _normalize_artifact_text(prompt),
            _normalize_artifact_text(result_text),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_artifact_fingerprints() -> Dict[str, Any]:
    data = read_json(MVP_ARTIFACT_FINGERPRINTS_FILE, default={})
    if isinstance(data, dict):
        return data
    return {}


def _record_artifact_fingerprint(
    fingerprint: str,
    *,
    identity_id: str,
    task_id: str,
    journal_path: str,
    doc_path: Optional[str],
) -> None:
    ledger = _load_artifact_fingerprints()
    entries = ledger.get("entries")
    if not isinstance(entries, dict):
        entries = {}
    entries[fingerprint] = {
        "identity_id": identity_id,
        "task_id": task_id,
        "journal_path": journal_path,
        "doc_path": doc_path,
        "recorded_at": get_timestamp(),
    }
    ledger["entries"] = entries
    write_json(MVP_ARTIFACT_FINGERPRINTS_FILE, ledger)


def _persist_mvp_markdown_artifacts(
    task: Dict[str, Any],
    result_summary: str,
    resident_ctx: Optional["ResidentContext"],
) -> Dict[str, Any]:
    if not MVP_DOCS_ONLY_MODE:
        return {"enabled": False}

    result_text = str(result_summary or "").strip()
    if not result_text:
        return {"enabled": True, "written": False, "reason": "empty_result"}

    now = datetime.now(timezone.utc)
    task_id = str(task.get("id") or "task").strip() or "task"
    prompt = str(_resolve_task_prompt(task) or "").strip()

    identity = getattr(resident_ctx, "identity", None) if resident_ctx else None
    identity_id = str(getattr(identity, "identity_id", "")).strip() or "resident_unknown"
    identity_name = str(getattr(identity, "name", "")).strip() or identity_id
    fingerprint = _compute_artifact_fingerprint(identity_id=identity_id, prompt=prompt, result_text=result_text)
    existing_entries = _load_artifact_fingerprints().get("entries", {})
    existing_entry = existing_entries.get(fingerprint) if isinstance(existing_entries, dict) else None
    if isinstance(existing_entry, dict):
        return {
            "enabled": True,
            "written": False,
            "reason": "duplicate_artifact_payload_blocked",
            "existing_journal_path": existing_entry.get("journal_path"),
            "existing_doc_path": existing_entry.get("doc_path"),
        }

    identity_slug = _slugify_token(identity_id, fallback="resident")
    task_slug = _slugify_token(task_id, fallback="task")
    stamp = now.strftime("%Y%m%d-%H%M%S")
    date_label = now.strftime("%Y-%m-%d")

    MVP_JOURNALS_DIR.mkdir(parents=True, exist_ok=True)
    MVP_LIBRARY_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    MVP_LIBRARY_RESIDENT_SUGGESTIONS_ROOT.mkdir(parents=True, exist_ok=True)
    resident_suggestions_dir = MVP_LIBRARY_RESIDENT_SUGGESTIONS_ROOT / identity_slug
    resident_suggestions_dir.mkdir(parents=True, exist_ok=True)

    journal_path = MVP_JOURNALS_DIR / f"{identity_slug}_{date_label}.md"
    journal_entry = _format_markdown_record(
        task_id=task_id,
        title=f"Journal Entry: {task_id}",
        prompt=prompt,
        result=result_text,
        timestamp=now,
        identity_id=identity_id,
        identity_name=identity_name,
    )

    try:
        with open(journal_path, "a", encoding="utf-8") as jf:
            if journal_path.exists() and journal_path.stat().st_size > 0:
                jf.write("\n---\n\n")
            jf.write(journal_entry)
    except OSError as exc:
        return {
            "enabled": True,
            "written": False,
            "reason": f"journal_write_failed:{exc}",
        }

    doc_target, target_error = _resolve_mvp_markdown_target(task)
    doc_action = "created"
    doc_path = None
    if doc_target is None:
        doc_target = resident_suggestions_dir / f"{stamp}_{task_slug}.md"
    else:
        doc_action = "updated" if doc_target.exists() else "created"
        doc_target.parent.mkdir(parents=True, exist_ok=True)

    suggestion_doc = _format_markdown_record(
        task_id=task_id,
        title=f"Suggestion: {task_id}",
        prompt=prompt,
        result=result_text,
        timestamp=now,
        identity_id=identity_id,
        identity_name=identity_name,
    )
    edit_mode = str(task.get("doc_edit_mode") or "overwrite").strip().lower()
    try:
        if edit_mode == "append" and doc_target.exists():
            with open(doc_target, "a", encoding="utf-8") as df:
                df.write("\n\n---\n\n")
                df.write(suggestion_doc)
        else:
            with open(doc_target, "w", encoding="utf-8") as df:
                df.write(suggestion_doc)
        doc_path = str(doc_target)
    except OSError as exc:
        return {
            "enabled": True,
            "written": False,
            "reason": f"doc_write_failed:{exc}",
            "journal_path": str(journal_path),
            "doc_target_error": target_error,
        }

    try:
        _record_artifact_fingerprint(
            fingerprint,
            identity_id=identity_id,
            task_id=task_id,
            journal_path=str(journal_path),
            doc_path=doc_path,
        )
    except Exception as exc:
        _log("WARN", f"Failed to record artifact fingerprint for {task_id}: {exc}")

    return {
        "enabled": True,
        "written": True,
        "journal_path": str(journal_path),
        "doc_path": doc_path,
        "doc_action": doc_action,
        "doc_edit_mode": edit_mode,
        "doc_target_error": target_error,
    }




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
    """Read the execution log (JSONL) and return latest status per task. Thread-safe."""
    if EXECUTION_LOG.exists():
        try:
            size = EXECUTION_LOG.stat().st_size
            with _EXECUTION_LOG_LOCK:
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

    # Legacy fallback: JSON execution log (optional)
    legacy_path = WORKSPACE / "execution_log.json"
    legacy_log = read_json(legacy_path, default={})
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


def _notify_human_task_pending_approval(
    task_id: str,
    identity_id: str,
    identity_name: str,
    result_preview: str,
    review_verdict: str,
) -> None:
    """Append a mailbox message so the human sees that a task is ready for approval (no token cost)."""
    messages_file = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
    messages_file.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f"Task “{task_id}” is ready for your approval. "
        f"Verdict: {review_verdict}. "
        f"Result: {result_preview}"
    )
    message = {
        "id": f"msg_{identity_id or 'worker'}_{int(time.time() * 1000)}",
        "from_id": identity_id or "worker",
        "from_name": identity_name or "Resident",
        "content": content,
        "type": "task_pending_approval",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task_id": task_id,
    }
    try:
        append_jsonl(messages_file, message)
    except OSError as exc:
        _log("WARN", f"Could not notify human of pending task {task_id}: {exc}")


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


def _apply_queue_outcome(task_id: str, final_status: str) -> None:
    """
    Keep queue.json aligned with execution outcomes.

    - approved/completed/ready_for_merge -> move from open tasks to completed
    - failed -> move from open tasks to failed
    - requeue/pending_review/etc -> keep task in open queue
    """
    try:
        queue = read_queue()
        tasks = list(queue.get("tasks", []))
        task_index = None
        for idx, task in enumerate(tasks):
            if task.get("id") == task_id:
                task_index = idx
                break
        if task_index is None:
            return

        task = dict(tasks.pop(task_index))
        terminal_success = {"completed", "approved", "ready_for_merge"}
        terminal_failure = {"failed"}

        if final_status in terminal_success:
            task["status"] = "completed"
            queue.setdefault("completed", []).append(task)
        elif final_status in terminal_failure:
            task["status"] = "failed"
            queue.setdefault("failed", []).append(task)
        else:
            task["status"] = "pending" if final_status == "requeue" else final_status
            tasks.insert(task_index, task)

        queue["tasks"] = tasks
        write_json(QUEUE_FILE, normalize_queue(queue))
    except Exception as exc:
        _log("WARN", f"Failed to sync queue outcome for {task_id}: {exc}")


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


def _load_runtime_wait_seconds() -> Optional[float]:
    data = read_json(RUNTIME_SPEED_FILE, default={})
    if not isinstance(data, dict):
        return None
    raw = data.get("wait_seconds")
    try:
        wait_seconds = float(raw)
    except (TypeError, ValueError):
        return None
    if wait_seconds < 0:
        return None
    return min(wait_seconds, 300.0)


def _resolve_idle_wait_seconds(idle_count: int) -> float:
    runtime_wait = _load_runtime_wait_seconds()
    if runtime_wait is not None:
        return runtime_wait
    return max(0.0, DEFAULT_RUNTIME_WAIT_SECONDS if DEFAULT_RUNTIME_WAIT_SECONDS >= 0 else _compute_idle_sleep(idle_count))


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


def _is_loopback_host(host: Optional[str]) -> bool:
    value = (host or "").strip().lower()
    if not value:
        return False
    if value in {"localhost", "testclient"}:
        return True
    try:
        return ip_address(value).is_loopback
    except ValueError:
        return False


def _is_loopback_api_endpoint(endpoint: str) -> bool:
    parsed = urlparse((endpoint or "").strip())
    if parsed.scheme not in {"http", "https"}:
        return False
    return _is_loopback_host(parsed.hostname)


def _internal_api_headers() -> Dict[str, str]:
    return {
        "X-Vivarium-Internal-Token": WORKER_INTERNAL_EXECUTION_TOKEN,
    }


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
    if punctuation_hits >= 2:
        signals.append("comma_enumeration")
    if punctuation_hits >= 2 or ":" in text or (has_sequence_connector and punctuation_hits >= 1):
        signals.append("compound_clauses")

    complexity_score = len(signals)
    return {
        "complexity_score": complexity_score,
        "signals": signals,
        "should_decompose": complexity_score >= 2,
    }


def _phase4_should_split_comma_clauses(parts: List[str], source_text: str) -> bool:
    if len(parts) >= 3:
        return True
    if len(parts) < 2:
        return False
    if PHASE4_SEQUENCE_SPLIT_RE.search(source_text):
        return True

    normalized_parts = [part.strip().lower() for part in parts if part.strip()]
    if len(normalized_parts) < 2:
        return False
    if any(part.startswith(PHASE4_COMMA_NON_ACTION_PREFIXES) for part in normalized_parts):
        return False
    return all(len(part.split()) >= 2 for part in normalized_parts)


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
            clause = clause.strip()
            if not clause:
                continue

            comma_parts = [piece.strip() for piece in clause.split(",") if piece.strip()]
            if _phase4_should_split_comma_clauses(comma_parts, clause):
                clause_candidates = comma_parts
            else:
                clause_candidates = [clause]

            for clause_candidate in clause_candidates:
                for piece in PHASE4_SEQUENCE_SPLIT_RE.split(clause_candidate):
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
                "type": DEFAULT_TASK_TYPE,
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


def _phase5_reward_key(task_id: str, identity_id: str) -> str:
    return f"{task_id}::{identity_id}"


def _load_phase5_reward_ledger() -> Dict[str, Any]:
    try:
        data = read_json(PHASE5_REWARD_LEDGER, default={})
    except Exception as exc:
        _log("WARN", f"Phase 5 reward ledger unreadable; using empty state: {exc}")
        return {"version": 1, "grants": {}}
    if not isinstance(data, dict):
        return {"version": 1, "grants": {}}

    grants = data.get("grants")
    if not isinstance(grants, dict):
        grants = {}
    return {"version": int(_safe_float(data.get("version"), 1.0)), "grants": grants}


def _get_phase5_reward_grant(task_id: str, identity_id: str) -> Optional[Dict[str, Any]]:
    grants = _load_phase5_reward_ledger().get("grants", {})
    entry = grants.get(_phase5_reward_key(task_id, identity_id))
    return entry if isinstance(entry, dict) else None


def _record_phase5_reward_grant(entry: Dict[str, Any]) -> bool:
    task_id = str(entry.get("task_id") or "unknown").strip() or "unknown"
    identity_id = str(entry.get("identity_id") or "").strip()
    if not identity_id:
        return False

    try:
        ledger = _load_phase5_reward_ledger()
        grants = ledger.get("grants", {})
        grants[_phase5_reward_key(task_id, identity_id)] = entry
        ledger["grants"] = grants
        ledger["version"] = 1
        write_json(PHASE5_REWARD_LEDGER, ledger)
        return True
    except Exception as exc:
        _log("WARN", f"Failed to persist phase5 reward ledger for {task_id}: {exc}")
        return False


def _phase5_estimate_reward_tokens(
    task: Dict[str, Any],
    result: Dict[str, Any],
    review_confidence: float,
) -> int:
    max_budget = _safe_float(task.get("max_budget"), 0.0)
    budget_used = _safe_float(result.get("budget_used"), -1.0)
    if max_budget <= 0 or budget_used < 0:
        return 0

    budget_savings = max(0.0, max_budget - budget_used)
    if budget_savings <= 0:
        return 0

    savings_ratio = min(1.0, budget_savings / max_budget)
    bounded_confidence = max(0.0, min(_safe_float(review_confidence, 0.5), 1.0))
    savings_component = int(round(savings_ratio * 8))
    confidence_component = int(round(bounded_confidence * 2))
    return max(1, min(12, savings_component + confidence_component))


def _maybe_apply_phase5_reward(
    task: Dict[str, Any],
    result: Dict[str, Any],
    resident_ctx: Optional["ResidentContext"],
    review_confidence: float,
) -> Dict[str, Any]:
    if resident_ctx is None:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_reason": "resident_context_unavailable",
        }
    if WORKER_ENRICHMENT is None:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_reason": "enrichment_unavailable",
        }

    identity_id = str(getattr(getattr(resident_ctx, "identity", None), "identity_id", "")).strip()
    if not identity_id:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_reason": "identity_unavailable",
        }

    tokens = _phase5_estimate_reward_tokens(task, result, review_confidence)
    if tokens <= 0:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_reason": "not_under_budget",
        }

    task_id = str(task.get("id") or "unknown")
    existing_grant = _get_phase5_reward_grant(task_id, identity_id)
    if existing_grant:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_tokens_requested": int(
                _safe_float(existing_grant.get("tokens_requested"), 0.0)
            ),
            "phase5_reward_tokens_awarded": int(
                _safe_float(existing_grant.get("tokens_awarded"), 0.0)
            ),
            "phase5_reward_identity": identity_id,
            "phase5_reward_reason": "already_granted",
            "phase5_reward_granted_at": existing_grant.get("granted_at"),
            "phase5_reward_ledger_recorded": True,
        }

    reward_reason = f"worker_approved_under_budget:{task_id}"
    try:
        reward_result = WORKER_ENRICHMENT.grant_free_time(identity_id, tokens, reason=reward_reason)
    except Exception as exc:
        _log("WARN", f"Phase 5 reward grant failed for {task_id}: {exc}")
        return {
            "phase5_reward_applied": False,
            "phase5_reward_reason": "grant_failed",
            "phase5_reward_error": str(exc),
        }

    granted = reward_result.get("granted", {}) if isinstance(reward_result, dict) else {}
    granted_free = int(_safe_float(granted.get("free_time"), 0.0))
    granted_journal = int(_safe_float(granted.get("journal"), 0.0))
    granted_total = max(0, granted_free + granted_journal)
    granted_at = get_timestamp()
    ledger_recorded = _record_phase5_reward_grant(
        {
            "task_id": task_id,
            "identity_id": identity_id,
            "tokens_requested": tokens,
            "tokens_awarded": granted_total,
            "budget_used": _safe_float(result.get("budget_used"), -1.0),
            "max_budget": _safe_float(task.get("max_budget"), 0.0),
            "review_confidence": _safe_float(review_confidence, 0.0),
            "reason": reward_reason,
            "granted_at": granted_at,
        }
    )
    return {
        "phase5_reward_applied": True,
        "phase5_reward_tokens_requested": tokens,
        "phase5_reward_tokens_awarded": granted_total,
        "phase5_reward_identity": identity_id,
        "phase5_reward_reason": reward_reason,
        "phase5_reward_granted_at": granted_at,
        "phase5_reward_ledger_recorded": ledger_recorded,
    }


def apply_phase5_reward_for_human_approval(
    task_id: str,
    identity_id: str,
    task: Dict[str, Any],
    last_event: Dict[str, Any],
    enrichment: Any,
) -> Dict[str, Any]:
    """
    Grant phase5 completion reward when a human approves a task (called from control panel).
    Returns same shape as _maybe_apply_phase5_reward for consistency.
    """
    if not identity_id:
        return {"phase5_reward_applied": False, "phase5_reward_reason": "identity_unavailable"}
    budget_used = _safe_float(last_event.get("budget_used"), -1.0)
    review_confidence = _safe_float(last_event.get("review_confidence"), 0.5)
    result_for_tokens = {"budget_used": budget_used}
    tokens = _phase5_estimate_reward_tokens(task, result_for_tokens, review_confidence)
    if tokens <= 0:
        return {"phase5_reward_applied": False, "phase5_reward_reason": "not_under_budget"}
    existing_grant = _get_phase5_reward_grant(task_id, identity_id)
    if existing_grant:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_tokens_requested": int(_safe_float(existing_grant.get("tokens_requested"), 0)),
            "phase5_reward_tokens_awarded": int(_safe_float(existing_grant.get("tokens_awarded"), 0)),
            "phase5_reward_identity": identity_id,
            "phase5_reward_reason": "already_granted",
        }
    reward_reason = f"human_approved:{task_id}"
    try:
        reward_result = enrichment.grant_free_time(identity_id, tokens, reason=reward_reason)
    except Exception as exc:
        return {
            "phase5_reward_applied": False,
            "phase5_reward_reason": "grant_failed",
            "phase5_reward_error": str(exc),
        }
    granted = reward_result.get("granted", {}) if isinstance(reward_result, dict) else {}
    granted_total = max(0, int(_safe_float(granted.get("free_time"), 0)) + int(_safe_float(granted.get("journal"), 0)))
    granted_at = get_timestamp()
    _record_phase5_reward_grant({
        "task_id": task_id,
        "identity_id": identity_id,
        "tokens_requested": tokens,
        "tokens_awarded": granted_total,
        "budget_used": budget_used,
        "max_budget": _safe_float(task.get("max_budget"), 0.0),
        "review_confidence": review_confidence,
        "reason": reward_reason,
        "granted_at": granted_at,
    })
    return {
        "phase5_reward_applied": True,
        "phase5_reward_tokens_requested": tokens,
        "phase5_reward_tokens_awarded": granted_total,
        "phase5_reward_identity": identity_id,
        "phase5_reward_reason": reward_reason,
        "phase5_reward_granted_at": granted_at,
        "phase5_reward_ledger_recorded": True,
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
    identity_id = ""
    identity_name = "Resident"
    if resident_ctx and getattr(resident_ctx, "identity", None):
        identity_id = str(getattr(resident_ctx.identity, "identity_id", "")).strip()
        identity_name = str(getattr(resident_ctx.identity, "name", "")).strip() or identity_id
    append_execution_event(
        task_id,
        "pending_review",
        review_verdict=verdict_name,
        review_confidence=confidence,
        review_issues=issues,
        review_suggestions=suggestions,
        review_attempt=review_attempt,
        identity_id=identity_id or None,
        identity_name=identity_name or None,
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
    # Never auto-approve: require human to click Approve in the control panel. Reward is granted on approval.
    phase5_reward = {
        "phase5_reward_applied": False,
        "phase5_reward_reason": "awaiting_human_approval",
    }

    # Notify human via mailbox so they know to approve (resident or guild claiming completion messages human)
    result_preview = (result.get("result_summary") or result.get("errors") or "Done")[:200]
    _notify_human_task_pending_approval(
        task_id=task_id,
        identity_id=identity_id,
        identity_name=identity_name,
        result_preview=result_preview,
        review_verdict=verdict_name,
    )

    # Always return pending_review so task stays in queue until human approves
    if approved:
        return {
            "status": "pending_review",
            "result_summary": result.get("result_summary"),
            "errors": None,
            **review_summary,
            **phase5_reward,
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
            **phase5_reward,
        }

    return {
        "status": "requeue",
        "result_summary": None,
        "errors": f"Quality gate rejected task: {rejection_reason}",
        **review_summary,
        **phase5_reward,
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
    if not _is_loopback_api_endpoint(api_endpoint):
        return {
            "status": "failed",
            "result_summary": None,
            "errors": f"API endpoint must be loopback-only: {api_endpoint}",
        }

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
                response = client.post(
                    f"{api_endpoint}{CYCLE_EXECUTION_ENDPOINT}",
                    json=payload,
                    headers=_internal_api_headers(),
                )
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
    if not _is_loopback_api_endpoint(api_endpoint):
        return {
            "status": "failed",
            "result_summary": None,
            "errors": f"API endpoint must be loopback-only: {api_endpoint}",
            "safety_passed": False,
            "safety_report": {
                "passed": False,
                "blocked_reason": "Non-loopback API endpoint is not allowed",
                "task_id": task_id,
                "checks": {},
            },
        }

    min_budget = _safe_float(task.get("min_budget"), DEFAULT_MIN_BUDGET)
    max_budget = _safe_float(task.get("max_budget"), DEFAULT_MAX_BUDGET)
    if min_budget < 0:
        min_budget = 0.0
    if max_budget < 0:
        max_budget = 0.0
    if max_budget and min_budget > max_budget:
        min_budget = max_budget
    intensity = task.get("intensity", DEFAULT_INTENSITY)
    prompt = _resolve_task_prompt(task)
    recall_query = prompt
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
        checkpoint_sha = None
        if delegated_result.get("status") == "completed" and WORKER_MUTABLE_VCS is not None:
            try:
                checkpoint = WORKER_MUTABLE_VCS.checkpoint(
                    task_id=task_id,
                    summary=str(delegated_result.get("result_summary") or "delegated task"),
                    metadata={"mode": "delegate"},
                )
                checkpoint_sha = checkpoint.commit_sha
            except Exception as exc:
                _log("WARN", f"Auto-checkpoint failed for delegated task {task_id}: {exc}")
        delegated_result["mutable_checkpoint"] = checkpoint_sha
        delegated_result["safety_passed"] = safety_passed
        delegated_result["safety_report"] = safety_report
        return delegated_result

    if plan and should_decompose:
        prompt = f"{prompt}\n\n{_build_facet_plan_text(plan)}"

    if resident_ctx and prompt:
        prompt = resident_ctx.apply_to_prompt(prompt)
        enrichment_prompt = _build_enrichment_prompt_context(resident_ctx, task_prompt=recall_query)
        if enrichment_prompt:
            prompt = f"{prompt}\n\n{enrichment_prompt}"
        if MVP_DOCS_ONLY_MODE:
            prompt = (
                "MVP MODE: You are currently limited to documentation artifacts.\n"
                "- Do NOT perform direct code changes.\n"
                "- You MAY read non-physics repository files for context.\n"
                "- Community Library root: library/community_library/\n"
                "- Store improvement proposals as markdown in library/community_library/resident_suggestions/<identity_id>/\n"
                "- Shared docs live in library/community_library/swarm_docs/ (legacy library/swarm_docs still readable).\n"
                "- Produce markdown proposals, plans, or review notes.\n"
                "- Prefer concrete change suggestions and acceptance criteria.\n\n"
                f"{prompt}"
            )

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
            response = client.post(
                f"{api_endpoint}{CYCLE_EXECUTION_ENDPOINT}",
                json=payload,
                headers=_internal_api_headers(),
            )

        if response.status_code == 200:
            result = response.json()
            api_safety_report = result.get("safety_report")
            result_summary = result.get("result", "Task completed")
            _publish_task_update_to_discussion(task, resident_ctx, task_id, result_summary)
            markdown_artifacts = _persist_mvp_markdown_artifacts(task, result_summary, resident_ctx)
            checkpoint_sha = None
            if WORKER_MUTABLE_VCS is not None:
                try:
                    checkpoint = WORKER_MUTABLE_VCS.checkpoint(
                        task_id=task_id,
                        summary=str(result_summary),
                        metadata={"mode": mode or "llm", "model": result.get("model")},
                    )
                    checkpoint_sha = checkpoint.commit_sha
                except Exception as exc:
                    _log("WARN", f"Auto-checkpoint failed for {task_id}: {exc}")
            return {
                "status": "completed",
                "result_summary": result_summary,
                "errors": None,
                "model": result.get("model"),
                "budget_used": result.get("budget_used"),
                "safety_passed": bool((api_safety_report or safety_report).get("passed", True)),
                "safety_report": api_safety_report or safety_report,
                "mutable_checkpoint": checkpoint_sha,
                "mvp_markdown_artifacts": markdown_artifacts,
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
                budget_used=result.get("budget_used"),
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
                    budget_used=result.get("budget_used"),
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
                    phase5_reward_applied=review_result.get("phase5_reward_applied"),
                    phase5_reward_tokens_requested=review_result.get("phase5_reward_tokens_requested"),
                    phase5_reward_tokens_awarded=review_result.get("phase5_reward_tokens_awarded"),
                    phase5_reward_identity=review_result.get("phase5_reward_identity"),
                    phase5_reward_reason=review_result.get("phase5_reward_reason"),
                    phase5_reward_granted_at=review_result.get("phase5_reward_granted_at"),
                    phase5_reward_ledger_recorded=review_result.get("phase5_reward_ledger_recorded"),
                    phase5_reward_error=review_result.get("phase5_reward_error"),
                    tool_route=result.get("tool_route"),
                    tool_name=result.get("tool_name"),
                    tool_confidence=result.get("tool_confidence"),
                    **identity_fields,
                )

            _apply_queue_outcome(task_id, final_status)
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
                    _log("WARN", "No identity available this day; exiting.")
                    return
                _log(
                    "INFO",
                    f"Resident {resident_ctx.identity.name} ({resident_ctx.identity.identity_id}) "
                    f"day {resident_ctx.day_count}, week {((resident_ctx.day_count - 1) // 7) + 1}",
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
                    max_idle = MAX_IDLE_CYCLES if os.environ.get("VIVARIUM_WORKER_DAEMON") not in ("1", "true", "yes") else None
                    if max_idle is not None and idle_count >= max_idle:
                        _log("INFO", f"No tasks available after {MAX_IDLE_CYCLES} checks. Exiting.")
                        break
                    wait_seconds = _resolve_idle_wait_seconds(idle_count)
                    _log(
                        "INFO",
                        f"No tasks available, waiting {wait_seconds:.2f}s... "
                        f"({idle_count}/{MAX_IDLE_CYCLES if max_idle else '∞'})",
                    )
                    time.sleep(wait_seconds)
            except KeyboardInterrupt:
                _log("INFO", "Interrupted by user")
                break
            except Exception as e:
                _log("ERROR", f"Unexpected error in resident loop: {type(e).__name__}: {e}")
                raise

        if resident_ctx and release_identity_lock:
            try:
                release_identity_lock(resident_ctx.identity.identity_id, resident_ctx.resident_id)
            except Exception:
                pass
        _log("INFO", f"Resident finished. Executed {iterations} tasks.")
    except Exception as e:
        _log("ERROR", f"Fatal error in worker_loop: {type(e).__name__}: {e}")
        sys.exit(1)


def add_task(
    task_id: str,
    prompt: str,
    depends_on: Optional[List[str]] = None,
    task_type: str = DEFAULT_TASK_TYPE,
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
                print("  python -m vivarium.runtime.worker_runtime run [max_iterations]  - Start resident runtime")
                print("  python -m vivarium.runtime.worker_runtime add <id> <instruction> [deps]  - Add task")
                sys.exit(1)
        else:
            worker_loop()
    except KeyboardInterrupt:
        _log("INFO", "Program interrupted")
        sys.exit(0)
    except Exception as e:
        _log("ERROR", f"Fatal error: {type(e).__name__}: {e}")
        sys.exit(1)
