#!/usr/bin/env python3
"""
Swarm Control Panel - Real-time monitoring and emergency controls.

A clean UI for:
- Streaming action logs in real-time
- Emergency STOP button
- Identity status overview
- Budget/cost monitoring

Run: python -m vivarium.runtime.control_panel_app
Open: http://localhost:8421
"""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import time
import threading
from collections import Counter, deque
from pathlib import Path
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from vivarium.runtime import config as runtime_config
from vivarium.runtime import resident_onboarding
from vivarium.runtime.runtime_contract import normalize_queue, normalize_task
from vivarium.runtime.vivarium_scope import (
    AUDIT_ROOT,
    MUTABLE_ROOT,
    MUTABLE_SWARM_DIR,
    SECURITY_ROOT,
    ensure_scope_layout,
)
from vivarium.utils import read_json, write_json, get_timestamp, append_jsonl
from vivarium.runtime.control_panel.frontend_template import CONTROL_PANEL_HTML
from vivarium.runtime.control_panel.middleware import (
    enforce_localhost_only,
    apply_security_headers,
    is_request_from_loopback,
)

ensure_scope_layout()

app = Flask(__name__)
app.before_request(enforce_localhost_only)
app.after_request(apply_security_headers)
app.config['SECRET_KEY'] = os.environ.get('VIVARIUM_CONTROL_PANEL_SECRET') or secrets.token_urlsafe(32)
LOCAL_UI_ORIGINS = [
    "http://127.0.0.1:8421",
    "http://localhost:8421",
]
socketio = SocketIO(app, cors_allowed_origins=LOCAL_UI_ORIGINS, async_mode='threading')

# Paths
CODE_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = MUTABLE_ROOT
ACTION_LOG = AUDIT_ROOT / "action_log.jsonl"
EXECUTION_LOG = AUDIT_ROOT / "execution_log.jsonl"
QUEUE_FILE = WORKSPACE / "queue.json"
KILL_SWITCH = MUTABLE_SWARM_DIR / "kill_switch.json"
FREE_TIME_BALANCES = MUTABLE_SWARM_DIR / "free_time_balances.json"
IDENTITIES_DIR = MUTABLE_SWARM_DIR / "identities"
DISCUSSIONS_DIR = WORKSPACE / ".swarm" / "discussions"
RUNTIME_SPEED_FILE = MUTABLE_SWARM_DIR / "runtime_speed.json"
GROQ_API_KEY_FILE = SECURITY_ROOT / "groq_api_key.txt"
WORKER_PROCESS_FILE = MUTABLE_SWARM_DIR / "worker_process.json"
# Operator-only UI controls (kept out of resident-visible world/config paths).
UI_SETTINGS_FILE = SECURITY_ROOT / "local_ui_settings.json"
LEGACY_UI_SETTINGS_FILE = CODE_ROOT / "config" / "local_ui_settings.json"
CREATIVE_SEED_PATTERN = re.compile(r"^[A-Z]{2}-\d{4}-[A-Z]{2}$")
CREATIVE_SEED_USED_FILE = MUTABLE_SWARM_DIR / "creative_seed_used.json"
CREATIVE_SEED_USED_MAX = 5000
API_AUDIT_LOG_FILE = AUDIT_ROOT / "api_audit.log"
LEGACY_API_AUDIT_LOG_FILE = CODE_ROOT / "api_audit.log"
MAILBOX_QUESTS_FILE = MUTABLE_SWARM_DIR / "mailbox_quests.json"
COMPLETED_REQUESTS_FILE = WORKSPACE / ".swarm" / "completed_requests.json"
BOUNTIES_FILE = MUTABLE_SWARM_DIR / "bounties.json"
HUMAN_REQUEST_FILE = WORKSPACE / ".swarm" / "human_request.json"
MESSAGES_TO_HUMAN = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
MESSAGES_FROM_HUMAN = WORKSPACE / ".swarm" / "messages_from_human.json"
MESSAGES_FROM_HUMAN_OUTBOX = WORKSPACE / ".swarm" / "messages_from_human_outbox.jsonl"

# --- MAKE PATHS AVAILABLE TO BLUEPRINTS VIA FLASK CONFIG ---
app.config.update({
    'SOCKETIO': socketio,
    'CODE_ROOT': CODE_ROOT,
    'WORKSPACE': WORKSPACE,
    'ACTION_LOG': ACTION_LOG,
    'EXECUTION_LOG': EXECUTION_LOG,
    'QUEUE_FILE': QUEUE_FILE,
    'KILL_SWITCH': KILL_SWITCH,
    'FREE_TIME_BALANCES': FREE_TIME_BALANCES,
    'IDENTITIES_DIR': IDENTITIES_DIR,
    'DISCUSSIONS_DIR': DISCUSSIONS_DIR,
    'RUNTIME_SPEED_FILE': RUNTIME_SPEED_FILE,
    'GROQ_API_KEY_FILE': GROQ_API_KEY_FILE,
    'WORKER_PROCESS_FILE': WORKER_PROCESS_FILE,
    'UI_SETTINGS_FILE': UI_SETTINGS_FILE,
    'LEGACY_UI_SETTINGS_FILE': LEGACY_UI_SETTINGS_FILE,
    'CREATIVE_SEED_PATTERN': CREATIVE_SEED_PATTERN,
    'CREATIVE_SEED_USED_FILE': CREATIVE_SEED_USED_FILE,
    'CREATIVE_SEED_USED_MAX': CREATIVE_SEED_USED_MAX,
    'MAILBOX_QUESTS_FILE': MAILBOX_QUESTS_FILE,
})
# -------------------------------------------------------------

# Register blueprints
from vivarium.runtime.control_panel.blueprints_registry import register_blueprints
from vivarium.runtime.control_panel.blueprints.bounties.routes import load_bounties
register_blueprints(app)

# Track last read position (lock guards against race with watcher thread + poll)
last_log_position = 0
last_execution_log_position = 0
_log_watcher_lock = threading.Lock()

# Centralized policy limits (UI/runtime tuning).
RESIDENT_COUNT_MIN = 1
RESIDENT_COUNT_MAX = 16
HUMAN_USERNAME_MAX_CHARS = 256
MESSAGES_FEED_MAX = 50
DM_MESSAGES_MAX_LIMIT = 500
DM_THREADS_DEFAULT_LIMIT = 40
INSIGHTS_HEALTH_BACKLOG_WARN = 8
INSIGHTS_SOCIAL_UNREAD_WARN = 5
REFERENCE_WEEKDAY_NAMES = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
MAILBOX_MESSAGE_BONUS_TOKENS = 8
MAILBOX_REPLY_BONUS_TOKENS = 12
QUEST_DEFAULT_BUDGET = 0.20
QUEST_DEFAULT_UPFRONT_TIP = 10
QUEST_DEFAULT_COMPLETION_REWARD = 30
HOT_RELOAD_ENABLED = (
    os.environ.get("VIVARIUM_HOT_RELOAD", "0").strip().lower()
    not in {"0", "false", "no"}
)

# Exclude backend runtime files from hot reload so UI state isn't reset when
# editing swarm_enrichment, worker_runtime, etc. Only control_panel_app.py
# changes trigger reload. Set VIVARIUM_HOT_RELOAD_WATCH_ALL=1 to watch everything.
RELOAD_EXCLUDE_PATTERNS = [
    "*swarm_enrichment*",
    "*worker_runtime*",
    "*resident_onboarding*",
    "*action_logger*",
    "*swarm_api*",
    "*config*",
    "*runtime_contract*",
    "*vivarium_scope*",
    "*safety_gateway*",
    "*quality_gates*",
    "*tool_router*",
    "*resident_facets*",
    "*one_time_tasks*",
    "*intent_gatekeeper*",
    "*groq_client*",
    "*secure_api_wrapper*",
    "*task_verifier*",
    "*inference_engine*",
    "*safety_validator*",
    "*hats*",
]


def _safe_int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _safe_float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def _parse_csv_items(raw: str, *, max_items: int = 10, max_len: int = 2000) -> list[str]:
    if not raw:
        return []
    items: list[str] = []
    for part in str(raw).split(","):
        value = part.strip()
        if not value:
            continue
        if len(value) > max_len:
            value = value[:max_len].rstrip()
        if value not in items:
            items.append(value)
        if len(items) >= max_items:
            break
    return items


def _fresh_hybrid_seed() -> str:
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    left = "".join(secrets.choice(letters) for _ in range(2))
    middle = "".join(secrets.choice("0123456789") for _ in range(4))
    right = "".join(secrets.choice(letters) for _ in range(2))
    return f"{left}-{middle}-{right}"


def _reserve_creativity_seed(seed: str) -> bool:
    normalized = str(seed or "").strip().upper()
    if not CREATIVE_SEED_PATTERN.fullmatch(normalized):
        return False
    payload = read_json(CREATIVE_SEED_USED_FILE, default={})
    used = payload.get("used", {}) if isinstance(payload, dict) else {}
    if not isinstance(used, dict):
        used = {}
    if normalized in used:
        return False
    used[normalized] = get_timestamp()
    if len(used) > CREATIVE_SEED_USED_MAX:
        # Keep most-recent reservations only.
        recent = sorted(used.items(), key=lambda item: item[1], reverse=True)[:CREATIVE_SEED_USED_MAX]
        used = {k: v for k, v in recent}
    write_json(CREATIVE_SEED_USED_FILE, {"used": used})
    return True


def _mask_secret(secret: str) -> str:
    value = (secret or "").strip()
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}...{value[-4:]}"


def _default_ui_settings() -> dict:
    return {
        "override_model": False,
        "model": "auto",
        "auto_scale": False,
        "budget_limit": 1.0,
        "task_min_budget": 0.05,
        "task_max_budget": 0.10,
        "resident_count": 1,
        "human_username": "human",
    }


def load_ui_settings() -> dict:
    defaults = _default_ui_settings()
    settings_path = UI_SETTINGS_FILE
    if not settings_path.exists() and LEGACY_UI_SETTINGS_FILE.exists():
        # One-time migration from legacy config path.
        settings_path = LEGACY_UI_SETTINGS_FILE
    if not settings_path.exists():
        return defaults
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return defaults
        merged = dict(defaults)
        merged.update(data)
        # Type normalization
        merged["override_model"] = bool(merged.get("override_model", False))
        merged["auto_scale"] = bool(merged.get("auto_scale", False))
        merged["model"] = str(merged.get("model") or "auto")
        try:
            merged["budget_limit"] = max(0.10, float(merged.get("budget_limit", 1.0)))
        except (TypeError, ValueError):
            merged["budget_limit"] = 1.0
        try:
            merged["task_min_budget"] = max(0.0, float(merged.get("task_min_budget", 0.05)))
        except (TypeError, ValueError):
            merged["task_min_budget"] = 0.05
        try:
            merged["task_max_budget"] = max(merged["task_min_budget"], float(merged.get("task_max_budget", 0.10)))
        except (TypeError, ValueError):
            merged["task_max_budget"] = max(merged["task_min_budget"], 0.10)
        try:
            merged["resident_count"] = _clamp_int(
                merged.get("resident_count", RESIDENT_COUNT_MIN),
                RESIDENT_COUNT_MIN,
                RESIDENT_COUNT_MAX,
            )
        except (TypeError, ValueError):
            merged["resident_count"] = RESIDENT_COUNT_MIN
        username = re.sub(r"[^a-zA-Z0-9 _.-]+", "", str(merged.get("human_username") or "human")).strip()
        merged["human_username"] = username[:HUMAN_USERNAME_MAX_CHARS] if username else "human"
        # Persist migrated settings to secure path for future reads.
        if settings_path != UI_SETTINGS_FILE:
            try:
                save_ui_settings(merged)
            except Exception:
                pass
        return merged
    except Exception:
        return defaults


def save_ui_settings(updates: dict) -> dict:
    current = load_ui_settings()
    if isinstance(updates, dict):
        current.update(updates)
    # normalize via loader rules
    normalized = {
        "override_model": bool(current.get("override_model", False)),
        "model": str(current.get("model") or "auto"),
        "auto_scale": bool(current.get("auto_scale", False)),
        "budget_limit": max(0.10, float(current.get("budget_limit", 1.0))),
        "task_min_budget": max(0.0, float(current.get("task_min_budget", 0.05))),
        "task_max_budget": max(0.0, float(current.get("task_max_budget", 0.10))),
        "resident_count": _clamp_int(
            current.get("resident_count", RESIDENT_COUNT_MIN),
            RESIDENT_COUNT_MIN,
            RESIDENT_COUNT_MAX,
        ),
        "human_username": re.sub(r"[^a-zA-Z0-9 _.-]+", "", str(current.get("human_username") or "human")).strip()[:HUMAN_USERNAME_MAX_CHARS] or "human",
        "updated_at": datetime.now().isoformat(),
    }
    if normalized["task_max_budget"] < normalized["task_min_budget"]:
        normalized["task_max_budget"] = normalized["task_min_budget"]
    UI_SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(UI_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2)
    return normalized


def get_human_username() -> str:
    """Operator display name for resident-facing messaging."""
    try:
        settings = load_ui_settings()
        value = str(settings.get("human_username") or "").strip()
        return value or "human"
    except Exception:
        return "human"


CONTROL_PANEL_HOST = os.environ.get("VIVARIUM_CONTROL_PANEL_HOST", "127.0.0.1").strip() or "127.0.0.1"
CONTROL_PANEL_PORT = _safe_int_env("VIVARIUM_CONTROL_PANEL_PORT", 8421)



class LogWatcher(FileSystemEventHandler):
    """Watch action/execution logs and stream entries to UI."""

    def __init__(self, socketio_instance):
        self.socketio = socketio_instance
        self.last_position = 0

    def on_modified(self, event):
        try:
            name = Path(event.src_path).name
        except Exception:
            name = event.src_path or ""
        if name == "action_log.jsonl" or name == "execution_log.jsonl":
            self.send_new_entries()

    def send_new_entries(self):
        global last_log_position
        global last_execution_log_position
        action_lines = []
        exec_lines = []
        with _log_watcher_lock:
            if not ACTION_LOG.exists():
                last_log_position = 0
            else:
                size = ACTION_LOG.stat().st_size
                if size < last_log_position:
                    last_log_position = 0
                with open(ACTION_LOG, "r", encoding="utf-8") as f:
                    f.seek(last_log_position)
                    action_lines = f.readlines()
                    last_log_position = f.tell()
            if not EXECUTION_LOG.exists():
                last_execution_log_position = 0
            else:
                size = EXECUTION_LOG.stat().st_size
                if size < last_execution_log_position:
                    last_execution_log_position = 0
                with open(EXECUTION_LOG, "r", encoding="utf-8") as f:
                    f.seek(last_execution_log_position)
                    exec_lines = f.readlines()
                    last_execution_log_position = f.tell()
        for line in action_lines:
            try:
                entry = json.loads(line.strip())
                self.socketio.emit("log_entry", entry)
            except Exception:
                pass
        for line in exec_lines:
            try:
                raw = json.loads(line.strip())
                mapped = _map_execution_entry_to_log(raw)
                self.socketio.emit("log_entry", mapped)
            except Exception:
                pass


def calculate_identity_level(sessions: int) -> int:
    """Calculate identity level based on sessions (ARPG-style progression)."""
    # Level formula: sqrt(sessions) rounded down, minimum level 1
    import math
    return max(1, int(math.sqrt(sessions)))


def calculate_respec_cost(sessions: int, respec_count: int = 0) -> int:
    """Calculate respec cost. First 3 changes are free; then BASE + (sessions * SCALE)."""
    RESPEC_FREE_CHANGES = 3
    if respec_count < RESPEC_FREE_CHANGES:
        return 0
    RESPEC_BASE_COST = 10
    RESPEC_SCALE_PER_SESSION = 3
    return RESPEC_BASE_COST + (sessions * RESPEC_SCALE_PER_SESSION)


def get_identities():
    """Get all identity info with token balances and profile snippets."""
    identities = []

    # Load token balances
    balances = {}
    if FREE_TIME_BALANCES.exists():
        try:
            with open(FREE_TIME_BALANCES) as f:
                balances = json.load(f)
        except:
            pass

    # Load identity files
    if IDENTITIES_DIR.exists():
        for f in IDENTITIES_DIR.glob("*.json"):
            try:
                with open(f) as file:
                    data = json.load(file)
                    identity_id = data.get('id', f.stem)
                    attrs = data.get('attributes', {})
                    profile = attrs.get('profile', {})
                    core = attrs.get('core', {})
                    sessions = data.get('sessions_participated', 0)
                    respec_count = attrs.get('meta', {}).get('respec_count', 0)

                    identities.append({
                        'id': identity_id,
                        'name': data.get('name', 'Unknown'),
                        'tokens': balances.get(identity_id, {}).get('tokens', 0),
                        'journal_tokens': balances.get(identity_id, {}).get('journal_tokens', 0),
                        'sessions': sessions,
                        'tasks_completed': data.get('tasks_completed', 0),
                        'profile_display': profile.get('display'),
                        'profile_thumbnail_html': profile.get('thumbnail_html'),
                        'profile_thumbnail_css': profile.get('thumbnail_css'),
                        'traits': core.get('personality_traits', []),
                        'values': core.get('core_values', []),
                        'level': calculate_identity_level(sessions),
                        'respec_cost': calculate_respec_cost(sessions, respec_count),
                    })
            except:
                pass

    return identities


@socketio.on('connect')
def on_socket_connect():
    """Reject websocket connections from non-loopback clients."""
    if not is_request_from_loopback():
        return False
    return None


# Identity API routes moved to blueprints/identities/routes.py
# Stop toggle routes moved to blueprints/stop_toggle/routes.py

# Spawner routes moved to blueprints/spawner/routes.py
# Runtime speed routes moved to blueprints/runtime_speed/routes.py

# ═══════════════════════════════════════════════════════════════════
# WORKER - Start/stop the queue worker from the UI (autonomous run)
# ═══════════════════════════════════════════════════════════════════

def _worker_process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _spawn_one_off_worker_if_paused(identity_id: str = None):
    """When run is paused, spawn a one-off worker to process the just-enqueued message task.
    Pass identity_id so the worker spawns as that identity and can respond to the message."""
    if get_worker_status().get("running"):
        return
    try:
        env = {
            **os.environ,
            "RESIDENT_SHARD_COUNT": "1",
            "RESIDENT_SHARD_ID": "0",
            "VIVARIUM_WORKER_DAEMON": "0",
        }
        if identity_id:
            env["RESIDENT_ALLOW_OVERRIDE"] = "1"
            env["RESIDENT_IDENTITY_OVERRIDE"] = str(identity_id)
        cmd = [sys.executable, "-m", "vivarium.runtime.worker_runtime", "run", "5"]
        subprocess.Popen(
            cmd,
            cwd=str(CODE_ROOT),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception:
        pass


def _normalize_swarm_pids(data: dict) -> list[int]:
    """Support legacy single pid and current multi-pid formats."""
    if not isinstance(data, dict):
        return []
    pids: list[int] = []
    raw = data.get("pids")
    if isinstance(raw, list):
        for value in raw:
            try:
                pids.append(int(value))
            except (TypeError, ValueError):
                continue
    elif data.get("pid") is not None:
        try:
            pids.append(int(data.get("pid")))
        except (TypeError, ValueError):
            pass
    return pids


def _list_worker_runtime_pids(exclude: set[int] | None = None) -> list[int]:
    """
    Detect worker_runtime processes not launched via the control panel PID file.
    """
    excluded = set(exclude or set())
    discovered: list[int] = []
    try:
        proc = subprocess.run(
            ["ps", "-ax", "-o", "pid=,command="],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return []

    for raw_line in proc.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        if pid in excluded:
            continue
        command = parts[1]
        if "vivarium.runtime.worker_runtime" not in command:
            continue
        if " run" not in command and not command.endswith("run"):
            continue
        discovered.append(pid)

    return sorted(set(discovered))


def _is_worker_running() -> bool:
    """Return True if the worker pool is running."""
    return get_worker_status().get("running", False)


def _load_worker_process() -> dict:
    """Return full worker pool status (for blueprint)."""
    return get_worker_status()


def _save_worker_process(pids: list[int], target_count: int) -> None:
    """Persist worker process PIDs to file."""
    MUTABLE_SWARM_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "pids": pids,
        "target_count": target_count,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(WORKER_PROCESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _start_worker_pool(requested_count: int | None = None) -> dict:
    """Start the worker pool. Returns result dict with success/error."""
    if requested_count is None:
        requested_count = load_ui_settings().get("resident_count", RESIDENT_COUNT_MIN)
    try:
        requested_count = _clamp_int(requested_count, RESIDENT_COUNT_MIN, RESIDENT_COUNT_MAX)
    except (TypeError, ValueError):
        requested_count = RESIDENT_COUNT_MIN

    status = get_worker_status()
    if status["running"]:
        if (
            status.get("running_source") == "managed"
            and not status.get("unmanaged_pids")
            and int(status.get("target_count", 1)) == requested_count
        ):
            return {
                "success": True,
                "message": "Worker already running",
                "pid": status["pid"],
                "running_count": status.get("running_count", 1),
                "target_count": requested_count,
            }
        for pid in status.get("pids", []):
            try:
                os.kill(pid, 15)
            except (OSError, ProcessLookupError):
                pass

    MUTABLE_SWARM_DIR.mkdir(parents=True, exist_ok=True)
    cwd = str(CODE_ROOT)
    cmd = [sys.executable, "-m", "vivarium.runtime.worker_runtime", "run"]
    base_env = os.environ.copy()
    base_env["VIVARIUM_WORKER_DAEMON"] = "1"
    base_env["RESIDENT_SHARD_COUNT"] = str(requested_count)
    pids: list[int] = []
    try:
        for shard_id in range(requested_count):
            env = dict(base_env)
            env["RESIDENT_SHARD_ID"] = str(shard_id)
            proc = subprocess.Popen(
                cmd,
                cwd=cwd,
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            pids.append(proc.pid)
        _save_worker_process(pids, requested_count)
        return {
            "success": True,
            "pid": pids[0] if pids else None,
            "pids": pids,
            "running_count": len(pids),
            "target_count": requested_count,
            "message": "Worker started",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def _stop_worker_pool() -> dict:
    """Stop the worker pool. Returns result dict."""
    status = get_worker_status()
    if not status["running"]:
        try:
            WORKER_PROCESS_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        return {"success": True, "message": "Worker not running"}

    for pid in status.get("pids", []):
        try:
            os.kill(pid, 15)
        except (OSError, ProcessLookupError):
            pass
    try:
        WORKER_PROCESS_FILE.unlink(missing_ok=True)
    except Exception:
        pass
    return {"success": True, "message": "Worker stopped"}


def get_worker_status():
    """Return swarm worker pool status."""
    try:
        configured_target = _clamp_int(
            load_ui_settings().get("resident_count", RESIDENT_COUNT_MIN),
            RESIDENT_COUNT_MIN,
            RESIDENT_COUNT_MAX,
        )
    except Exception:
        configured_target = RESIDENT_COUNT_MIN
    out = {
        "running": False,
        "pid": None,
        "pids": [],
        "unmanaged_pids": [],
        "running_count": 0,
        "target_count": configured_target,
        "started_at": None,
        "running_source": "none",
    }
    managed_pids: list[int] = []
    target_count = RESIDENT_COUNT_MIN
    started_at = None
    had_pid_file = WORKER_PROCESS_FILE.exists()
    if had_pid_file:
        try:
            with open(WORKER_PROCESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            all_pids = _normalize_swarm_pids(data)
            managed_pids = [pid for pid in all_pids if _worker_process_alive(pid)]
            started_at = data.get("started_at")
            try:
                target_count = _clamp_int(
                    data.get("target_count", len(all_pids) or RESIDENT_COUNT_MIN),
                    RESIDENT_COUNT_MIN,
                    RESIDENT_COUNT_MAX,
                )
            except (TypeError, ValueError):
                target_count = max(RESIDENT_COUNT_MIN, len(all_pids) or RESIDENT_COUNT_MIN)
        except Exception:
            managed_pids = []

    unmanaged = _list_worker_runtime_pids(set(managed_pids))
    combined = managed_pids + unmanaged
    if combined:
        out["running"] = True
        out["pid"] = combined[0]
        out["pids"] = combined
        out["unmanaged_pids"] = unmanaged
        out["running_count"] = len(combined)
        out["target_count"] = max(target_count, len(combined))
        out["started_at"] = started_at
        out["running_source"] = "mixed" if managed_pids and unmanaged else ("managed" if managed_pids else "unmanaged")
        return out

    # Process dead or missing; clear stale managed pid file.
    if had_pid_file:
        try:
            WORKER_PROCESS_FILE.unlink(missing_ok=True)
        except Exception:
            pass
    return out


# Worker routes moved to blueprints/worker/routes.py


def _stop_workers_for_maintenance(timeout_seconds: float = 3.0) -> dict:
    """
    Best-effort worker stop used by reset/rollback maintenance endpoints.
    """
    status = get_worker_status()
    pids = [int(pid) for pid in status.get("pids", []) if isinstance(pid, int) or str(pid).isdigit()]
    if not pids:
        try:
            WORKER_PROCESS_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        return {"success": True, "stopped_count": 0, "remaining_pids": []}

    for pid in pids:
        try:
            os.kill(pid, 15)  # SIGTERM
        except (OSError, ProcessLookupError):
            pass

    deadline = time.time() + max(0.5, float(timeout_seconds))
    remaining = list(pids)
    while time.time() < deadline:
        remaining = [pid for pid in remaining if _worker_process_alive(pid)]
        if not remaining:
            break
        time.sleep(0.1)

    try:
        WORKER_PROCESS_FILE.unlink(missing_ok=True)
    except Exception:
        pass

    return {
        "success": len(remaining) == 0,
        "stopped_count": max(0, len(pids) - len(remaining)),
        "remaining_pids": remaining,
    }


def _load_mailbox_quests() -> list[dict]:
    data = read_json(MAILBOX_QUESTS_FILE, default=[])
    return data if isinstance(data, list) else []


def _save_mailbox_quests(quests: list[dict]) -> None:
    MAILBOX_QUESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_json(MAILBOX_QUESTS_FILE, quests)


def _normalize_quest_budget(value, default: float = QUEST_DEFAULT_BUDGET) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = default
    if parsed < 0:
        return 0.0
    return round(min(parsed, 50.0), 4)


def _normalize_quest_tokens(value, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(0, min(parsed, 5000))


def _enqueue_identity_task(
    *,
    task_id: str,
    prompt: str,
    identity_id: str,
    min_budget: float,
    max_budget: float,
    model: str | None = None,
) -> dict:
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    task_model = (str(model).strip() if model else None) or None
    if task_model is None:
        ui_settings = load_ui_settings()
        override_model = bool(ui_settings.get("override_model"))
        ui_model = str(ui_settings.get("model") or "auto")
        task_model = ui_model if override_model and ui_model != "auto" else None
    queue.setdefault("tasks", []).append(
        normalize_task(
            {
                "id": task_id,
                "type": "cycle",
                "prompt": prompt,
                "identity_id": identity_id,
                "resident_identity": identity_id,
                "min_budget": max(0.0, float(min_budget)),
                "max_budget": max(float(min_budget), float(max_budget)),
                "intensity": "medium",
                "model": task_model,
                "depends_on": [],
                "parallel_safe": True,
            }
        )
    )
    write_json(QUEUE_FILE, normalize_queue(queue))
    return queue


def _remove_open_queue_task(task_id: str) -> tuple[dict | None, dict]:
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    tasks = list(queue.get("tasks", []))
    picked = None
    kept = []
    for task in tasks:
        if picked is None and str(task.get("id") or "") == str(task_id):
            picked = dict(task)
            continue
        kept.append(task)
    queue["tasks"] = kept
    write_json(QUEUE_FILE, normalize_queue(queue))
    return picked, queue


def _apply_queue_outcome(task_id: str, final_status: str) -> None:
    """Re-export for queue blueprint — delegates to worker_runtime."""
    from vivarium.runtime.worker_runtime import _apply_queue_outcome as _impl
    _impl(task_id, final_status)


def _latest_execution_status(task_id: str) -> tuple[str, dict]:
    entries = _read_jsonl_tail(EXECUTION_LOG, max_lines=12000)
    latest = {}
    for entry in entries:
        if str(entry.get("task_id") or "") == str(task_id):
            latest = entry
    status = str(latest.get("status") or "")
    return status, latest


def _refresh_mailbox_quests_state() -> list[dict]:
    quests = _load_mailbox_quests()
    changed = False
    for quest in quests:
        task_id = str(quest.get("task_id") or "").strip()
        if not task_id:
            continue
        status, latest = _latest_execution_status(task_id)
        previous = str(quest.get("status") or "")
        mapped = previous
        if status in {"queued", "in_progress", "pending_review", "requeue"}:
            mapped = "active"
        elif status in {"completed", "approved", "ready_for_merge"}:
            mapped = "awaiting_approval"
        elif status in {"failed"}:
            mapped = "failed"
        if quest.get("manual_paused"):
            mapped = "paused"
        if mapped != previous:
            quest["status"] = mapped
            quest["updated_at"] = datetime.now().isoformat()
            changed = True
        if latest:
            quest["last_event"] = {
                "status": status,
                "timestamp": latest.get("timestamp"),
                "result_summary": latest.get("result_summary"),
                "errors": latest.get("errors"),
            }
    if changed:
        _save_mailbox_quests(quests)
    return quests


def get_human_request():
    """Get the current human collaboration request."""
    if HUMAN_REQUEST_FILE.exists():
        try:
            with open(HUMAN_REQUEST_FILE) as f:
                data = json.load(f)
                return data.get('request', '')
        except:
            pass
    return ''


def save_human_request(request_text: str):
    """Save the human collaboration request."""
    HUMAN_REQUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'request': request_text,
        'updated_at': datetime.now().isoformat()
    }
    with open(HUMAN_REQUEST_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return data


# Higher reward band for human suggestions so residents prioritize them
SUGGESTION_MIN_BUDGET = 0.18
SUGGESTION_MAX_BUDGET = 0.40


def enqueue_human_suggestion(request_text: str) -> str | None:
    """Turn a human suggestion into an executable queue task (higher reward band)."""
    suggestion = (request_text or "").strip()
    if not suggestion:
        return None
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    task_id = f"suggestion-{int(time.time() * 1000)}"
    existing_ids = {t.get("id") for t in queue.get("tasks", []) if t.get("id")}
    while task_id in existing_ids:
        task_id = f"suggestion-{int(time.time() * 1000)}"
    ui_settings = load_ui_settings()
    override_model = bool(ui_settings.get("override_model"))
    model = str(ui_settings.get("model") or "auto")
    task_model = model if override_model and model != "auto" else None
    # Use higher min/max budget for suggestions so residents are more likely to pick them
    min_budget = float(ui_settings.get("task_min_budget", SUGGESTION_MIN_BUDGET))
    max_budget = float(ui_settings.get("task_max_budget", SUGGESTION_MAX_BUDGET))
    min_budget = max(min_budget, SUGGESTION_MIN_BUDGET)
    max_budget = max(max_budget, SUGGESTION_MAX_BUDGET)
    if max_budget < min_budget:
        max_budget = min_budget
    task = normalize_task({
        "id": task_id,
        "type": "cycle",
        "prompt": suggestion,
        "min_budget": min_budget,
        "max_budget": max_budget,
        "intensity": "medium",
        "model": task_model,
        "depends_on": [],
        "parallel_safe": True,
    })
    queue.setdefault("tasks", []).append(task)
    write_json(QUEUE_FILE, normalize_queue(queue))
    return task_id


def get_messages_to_human():
    """Get all messages from identities to the human."""
    messages = []
    if MESSAGES_TO_HUMAN.exists():
        try:
            with open(MESSAGES_TO_HUMAN, 'r') as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line))
        except:
            pass
    return messages


def get_human_responses():
    """Get human responses to identity messages."""
    if MESSAGES_FROM_HUMAN.exists():
        try:
            with open(MESSAGES_FROM_HUMAN, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}


def get_human_outbox_messages():
    """Get outbound messages sent by the human operator."""
    messages = []
    if MESSAGES_FROM_HUMAN_OUTBOX.exists():
        try:
            with open(MESSAGES_FROM_HUMAN_OUTBOX, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        messages.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            pass
    return messages


def _append_human_outbox_message(payload: dict) -> None:
    MESSAGES_FROM_HUMAN_OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    with open(MESSAGES_FROM_HUMAN_OUTBOX, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def save_human_response(message_id: str, response: str):
    """Save a human response to an identity message."""
    responses = get_human_responses()
    responder = get_human_username()
    responses[message_id] = {
        'response': response,
        'responded_at': datetime.now().isoformat(),
        'responder_name': responder,
    }
    MESSAGES_FROM_HUMAN.parent.mkdir(parents=True, exist_ok=True)
    with open(MESSAGES_FROM_HUMAN, 'w') as f:
        json.dump(responses, f, indent=2)

    # Mirror human reply into async group chat room + direct channel.
    try:
        original = next((m for m in get_messages_to_human() if str(m.get("id")) == str(message_id)), None)
        recipient_id = str((original or {}).get("from_id") or "").strip()
        recipient = str((original or {}).get("from_name") or recipient_id or "resident").strip()
        chat_line = f"[to {recipient}] {response}"
        _dm_enrichment().post_discussion_message(
            identity_id="human_operator",
            identity_name=responder,
            content=chat_line,
            room="human_async",
            mood="async",
            importance=4,
        )
        if recipient_id:
            _dm_enrichment().post_direct_message(
                sender_id="human_operator",
                sender_name=responder,
                recipient_id=recipient_id,
                content=response,
                importance=4,
            )
            # Reward resident for engaging with human async channel and queue a follow-up action.
            _dm_enrichment().grant_free_time(
                recipient_id,
                MAILBOX_REPLY_BONUS_TOKENS,
                reason="human_response_received",
            )
            followup_task_id = f"mailbox-followup-{recipient_id}-{int(time.time() * 1000)}"
            _enqueue_identity_task(
                task_id=followup_task_id,
                identity_id=recipient_id,
                prompt=(
                    f"Human replied to my message. Read their response and take one concrete next action "
                    f"that advances collaboration. Human response: {response}"
                ),
                min_budget=0.03,
                max_budget=0.20,
            )
        _append_human_outbox_message(
            {
                "id": f"human_out_{int(time.time() * 1000)}",
                "message_id": str(message_id),
                "to_id": recipient_id,
                "to_name": recipient,
                "content": response,
                "timestamp": datetime.now().isoformat(),
                "sender_name": responder,
                "source": "reply",
            }
        )
    except Exception:
        pass
    return responses[message_id]


# [EXTRACTED TO blueprints/messages] @app.route('/api/messages')
# def api_get_messages():
#     """Get messages from identities with any responses."""
#     ...


# [EXTRACTED TO blueprints/messages] @app.route('/api/messages/respond', methods=['POST'])
# def api_respond_to_message():
#     ...


# [EXTRACTED TO blueprints/messages] @app.route('/api/messages/send', methods=['POST'])
# def api_send_message_to_resident():
#     ...


# [EXTRACTED TO blueprints/messages] @app.route('/api/messages/mailbox')
# def api_mailbox_messages():
#     """Aggregate inbox/outbox threads for phone-style mailbox UI."""
#     ...


def get_completed_requests():
    """Get list of completed collaboration requests."""
    if COMPLETED_REQUESTS_FILE.exists():
        try:
            with open(COMPLETED_REQUESTS_FILE) as f:
                return json.load(f)
        except:
            pass
    return []


def add_completed_request(request_text: str):
    """Add a request to the completed log."""
    completed = get_completed_requests()

    # Get the current request's created time if available
    started_at = None
    if HUMAN_REQUEST_FILE.exists():
        try:
            with open(HUMAN_REQUEST_FILE) as f:
                data = json.load(f)
                started_at = data.get('updated_at')
        except:
            pass

    # Calculate duration if we have start time
    duration = ''
    if started_at:
        try:
            start = datetime.fromisoformat(started_at)
            end = datetime.now()
            delta = end - start
            hours = delta.total_seconds() / 3600
            if hours < 1:
                duration = f'{int(delta.total_seconds() / 60)} min'
            elif hours < 24:
                duration = f'{hours:.1f} hrs'
            else:
                duration = f'{delta.days} days'
        except:
            pass

    completed.insert(0, {
        'request': request_text,
        'completed_at': datetime.now().isoformat(),
        'started_at': started_at,
        'duration': duration
    })

    # Keep last 50 requests
    completed = completed[:50]

    COMPLETED_REQUESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPLETED_REQUESTS_FILE, 'w') as f:
        json.dump(completed, f, indent=2)

    return completed[0]


def _reset_log_watcher_positions() -> None:
    """Reset log watcher positions for fresh reset maintenance."""
    global last_log_position, last_execution_log_position
    last_log_position = 0
    last_execution_log_position = 0


def _dm_enrichment():
    from vivarium.runtime.swarm_enrichment import EnrichmentSystem
    return EnrichmentSystem(workspace=WORKSPACE)


def _parse_iso_timestamp(value):
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)
    return parsed


def _read_jsonl_tail(path: Path, max_lines: int = 12000):
    if not path.exists():
        return []
    lines = deque(maxlen=max_lines)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = line.strip()
                if entry:
                    lines.append(entry)
    except Exception:
        return []

    payloads = []
    for line in lines:
        try:
            payloads.append(json.loads(line))
        except Exception:
            continue
    return payloads


def _format_usd_display(amount: float) -> str:
    try:
        value = float(amount)
    except (TypeError, ValueError):
        return "$0.00"
    abs_value = abs(value)
    if abs_value == 0:
        return "$0.00"
    if abs_value < 0.01:
        return f"${value:.4f}"
    if abs_value < 1:
        return f"${value:.3f}"
    return f"${value:.2f}"


def _entry_timestamp_sort_key(entry: dict) -> tuple[int, str]:
    timestamp = _parse_iso_timestamp(entry.get("timestamp"))
    if timestamp is not None:
        return (0, timestamp.isoformat())
    return (1, str(entry.get("timestamp") or ""))


def _log_entry_dedupe_key(entry: dict) -> tuple[str, str, str, str, str, str]:
    metadata = entry.get("metadata") if isinstance(entry.get("metadata"), dict) else {}
    task_id = str(
        metadata.get("task_id")
        or entry.get("task_id")
        or ""
    )
    return (
        str(entry.get("timestamp") or ""),
        str(entry.get("actor") or ""),
        str(entry.get("action_type") or ""),
        str(entry.get("action") or ""),
        str(entry.get("detail") or ""),
        task_id,
    )


def _extract_usd_cost(detail: str) -> float:
    matches = re.findall(r"\$([0-9]+(?:\.[0-9]+)?)", str(detail or ""))
    if not matches:
        return 0.0
    try:
        return float(matches[-1])
    except (TypeError, ValueError):
        return 0.0


def _extract_token_count(detail: str) -> int:
    match = re.search(r"([0-9]+)\s*tokens?\b", str(detail or ""), flags=re.IGNORECASE)
    if not match:
        return 0
    try:
        return int(match.group(1))
    except (TypeError, ValueError):
        return 0


def _execution_detail_summary(raw: dict) -> str:
    parts: list[str] = []
    task_id = str(raw.get("task_id") or "task").strip()
    if task_id:
        parts.append(task_id)
    subtask_id = str(raw.get("subtask_id") or "").strip()
    if subtask_id:
        parts.append(f"subtask={subtask_id}")
    focus = str(raw.get("focus") or "").strip()
    if focus:
        parts.append(f"focus={focus}")
    hat_name = str(raw.get("hat_name") or "").strip()
    if hat_name:
        parts.append(f"hat={hat_name}")
    summary = str(raw.get("result_summary") or raw.get("errors") or "").strip()
    if summary:
        parts.append(summary)

    total_tokens = raw.get("total_tokens")
    if total_tokens is None:
        in_tokens = raw.get("input_tokens")
        out_tokens = raw.get("output_tokens")
        if isinstance(in_tokens, (int, float)) or isinstance(out_tokens, (int, float)):
            try:
                total_tokens = int(float(in_tokens or 0) + float(out_tokens or 0))
            except (TypeError, ValueError):
                total_tokens = None
    if total_tokens is not None:
        try:
            token_int = int(total_tokens)
            if token_int >= 0:
                parts.append(f"{token_int} tokens")
        except (TypeError, ValueError):
            pass

    budget_used = raw.get("budget_used")
    try:
        if budget_used is not None:
            parts.append(f"${float(budget_used):.6f}")
    except (TypeError, ValueError):
        pass
    return " | ".join(part for part in parts if part)


def _read_api_audit_entries(max_lines: int = 12000) -> list[dict]:
    candidates = [API_AUDIT_LOG_FILE, LEGACY_API_AUDIT_LOG_FILE]
    merged: list[dict] = []
    seen: set[tuple[str, str, str, str, str]] = set()
    for path in candidates:
        for entry in _read_jsonl_tail(path, max_lines=max_lines):
            if not isinstance(entry, dict):
                continue
            dedupe_key = (
                str(entry.get("timestamp") or ""),
                str(entry.get("event") or ""),
                str(entry.get("model") or ""),
                str(entry.get("cost") or ""),
                str(entry.get("user") or ""),
            )
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            merged.append(entry)
    merged.sort(key=lambda e: str(e.get("timestamp") or ""))
    return merged


def _map_api_audit_entry_to_log(raw: dict) -> dict:
    model = str(raw.get("model") or "").strip()
    event = str(raw.get("event") or "API_CALL")
    call_type = str(raw.get("call_type") or "").strip()
    input_tokens = raw.get("input_tokens")
    output_tokens = raw.get("output_tokens")
    tokens_total = None
    try:
        if input_tokens is not None or output_tokens is not None:
            tokens_total = int(float(input_tokens or 0) + float(output_tokens or 0))
    except (TypeError, ValueError):
        tokens_total = None

    cost = raw.get("cost")
    usd_cost = None
    try:
        if cost is not None:
            usd_cost = float(cost)
    except (TypeError, ValueError):
        usd_cost = None

    detail_parts = []
    if tokens_total is not None:
        detail_parts.append(f"{tokens_total} tokens")
    if usd_cost is not None:
        detail_parts.append(f"${usd_cost:.6f}")
    if model:
        detail_parts.append(model)
    if call_type:
        detail_parts.append(f"type={call_type}")
    detail = " | ".join(detail_parts) if detail_parts else event

    metadata = {
        "event": event,
        "call_type": call_type or None,
        "model": model or None,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "usd_cost": usd_cost,
        "identity_seed": raw.get("identity_seed"),
        "task_id": raw.get("task_id"),
        "identity_id": raw.get("identity_id"),
    }

    return {
        "timestamp": raw.get("timestamp"),
        "actor": raw.get("user") or "swarm_api",
        "action_type": "API",
        "action": event,
        "detail": detail,
        "session_id": None,
        "metadata": {k: v for k, v in metadata.items() if v is not None},
        "model": model or None,
    }


def _map_execution_entry_to_log(raw: dict) -> dict:
    meta = {"task_id": raw.get("task_id")}
    if raw.get("model"):
        meta["model"] = raw.get("model")
    if raw.get("subtask_id"):
        meta["subtask_id"] = raw.get("subtask_id")
    if raw.get("focus"):
        meta["focus"] = raw.get("focus")
    if raw.get("hat_name"):
        meta["hat_name"] = raw.get("hat_name")
    if raw.get("input_tokens") is not None:
        meta["input_tokens"] = raw.get("input_tokens")
    if raw.get("output_tokens") is not None:
        meta["output_tokens"] = raw.get("output_tokens")
    if raw.get("total_tokens") is not None:
        meta["total_tokens"] = raw.get("total_tokens")
    if raw.get("budget_used") is not None:
        meta["usd_cost"] = raw.get("budget_used")

    detail = _execution_detail_summary(raw)
    return {
        "timestamp": raw.get("timestamp"),
        "actor": raw.get("worker_id") or raw.get("identity_id") or "worker",
        "action_type": "EXECUTION",
        "action": raw.get("status") or "event",
        "detail": detail,
        "session_id": None,
        "metadata": meta,
        "model": raw.get("model"),
    }


def _count_discussion_messages_since(cutoff: datetime) -> int:
    total = 0
    if not DISCUSSIONS_DIR.exists():
        return total
    for room_file in DISCUSSIONS_DIR.glob("*.jsonl"):
        try:
            with open(room_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        payload = json.loads(line)
                    except Exception:
                        continue
                    timestamp = _parse_iso_timestamp(payload.get("timestamp"))
                    if timestamp and timestamp >= cutoff:
                        total += 1
        except Exception:
            continue
    return total


def _count_in_window(timestamps: list[datetime], start: datetime, end: datetime | None = None) -> int:
    if end is None:
        return sum(1 for ts in timestamps if ts >= start)
    return sum(1 for ts in timestamps if start <= ts < end)


def _pct_change(current: float, baseline: float | None) -> float | None:
    if baseline is None or baseline <= 0:
        return None
    return round(((current - baseline) / baseline) * 100.0, 1)


def _trend_snapshot(timestamps: list[datetime], now: datetime) -> dict:
    day_start = now - timedelta(days=1)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)
    prev_3w_start = now - timedelta(days=28)
    prev_3m_start = now - timedelta(days=120)

    day_count = _count_in_window(timestamps, day_start)
    week_count = _count_in_window(timestamps, week_start)
    month_count = _count_in_window(timestamps, month_start)

    prev_3w_total = _count_in_window(timestamps, prev_3w_start, week_start)
    prev_3m_total = _count_in_window(timestamps, prev_3m_start, month_start)
    prev_daily_3w_avg = prev_3w_total / 21.0 if prev_3w_total > 0 else None
    prev_daily_3m_avg = prev_3m_total / 90.0 if prev_3m_total > 0 else None

    return {
        "day": day_count,
        "week": week_count,
        "month": month_count,
        "day_trend_3w_pct": _pct_change(float(day_count), prev_daily_3w_avg),
        "day_trend_3m_pct": _pct_change(float(day_count), prev_daily_3m_avg),
        "prev_daily_3w_avg": round(prev_daily_3w_avg, 3) if prev_daily_3w_avg is not None else None,
        "prev_daily_3m_avg": round(prev_daily_3m_avg, 3) if prev_daily_3m_avg is not None else None,
    }


# Insights route moved to blueprints/insights - DELETED api_insights
# System/DM/Chatrooms routes moved to blueprints - DELETED

def background_watcher():
    """Background thread to watch log file and push updates."""
    watcher = LogWatcher(socketio)

    # Initial load of existing entries (either log can have content)
    if ACTION_LOG.exists() or EXECUTION_LOG.exists() or API_AUDIT_LOG_FILE.exists() or LEGACY_API_AUDIT_LOG_FILE.exists():
        watcher.send_new_entries()

    # Polling is more stable on some macOS/python combinations than FSEvents.
    use_native = str(os.environ.get("VIVARIUM_USE_NATIVE_WATCHDOG", "")).strip().lower() in {"1", "true", "yes"}
    observer = Observer() if use_native else PollingObserver(timeout=1.0)
    observer.schedule(watcher, str(ACTION_LOG.parent), recursive=False)
    observer.start()

    # Periodic poll so logs update even when FS events are unreliable (e.g. macOS).
    log_poll_interval = 0.33
    try:
        while True:
            time.sleep(log_poll_interval)
            try:
                watcher.send_new_entries()
            except Exception:
                pass
    except Exception:
        pass
    try:
        observer.stop()
        observer.join()
    except Exception:
        pass


def push_identities_periodically():
    """Push identity updates every 5 seconds."""
    while True:
        time.sleep(5)
        socketio.emit('identities', get_identities())


def _should_start_background_threads(use_reloader: bool) -> bool:
    """
    Prevent duplicate watcher threads under Werkzeug reloader parent process.
    """
    if not use_reloader:
        return True
    return os.environ.get("WERKZEUG_RUN_MAIN") == "true"


if __name__ == '__main__':
    print("=" * 60)
    print("SWARM CONTROL PANEL")
    print("=" * 60)
    print(f"Open: http://{CONTROL_PANEL_HOST}:{CONTROL_PANEL_PORT}")
    print(f"Watching: {ACTION_LOG}")
    print(f"Hot reload: {'ON' if HOT_RELOAD_ENABLED else 'OFF'} (set VIVARIUM_HOT_RELOAD=1 to enable)")
    print("=" * 60)

    # Start background threads (only in active reloader child process).
    if _should_start_background_threads(HOT_RELOAD_ENABLED):
        threading.Thread(target=background_watcher, daemon=True).start()
        threading.Thread(target=push_identities_periodically, daemon=True).start()

    run_kwargs = {
        "host": CONTROL_PANEL_HOST,
        "port": CONTROL_PANEL_PORT,
        "debug": HOT_RELOAD_ENABLED,
        "use_reloader": HOT_RELOAD_ENABLED,
        "allow_unsafe_werkzeug": True,
    }
    if HOT_RELOAD_ENABLED and os.environ.get("VIVARIUM_HOT_RELOAD_WATCH_ALL", "").strip() != "1":
        run_kwargs["exclude_patterns"] = RELOAD_EXCLUDE_PATTERNS

    socketio.run(app, **run_kwargs)
