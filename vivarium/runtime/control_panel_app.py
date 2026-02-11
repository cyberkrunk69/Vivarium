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
import hashlib
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
    CHANGE_JOURNAL_FILE,
    AUDIT_ROOT,
    MUTABLE_ROOT,
    MUTABLE_SWARM_DIR,
    SECURITY_ROOT,
    ensure_scope_layout,
    get_mutable_version_control,
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

# --- MAKE PATHS AVAILABLE TO BLUEPRINTS VIA FLASK CONFIG ---
app.config.update({
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
})
# -------------------------------------------------------------

# Register blueprints
from vivarium.runtime.control_panel.blueprints_registry import BLUEPRINT_SPECS

for bp, url_prefix in BLUEPRINT_SPECS:
    kwargs = {"url_prefix": url_prefix} if url_prefix else {}
    app.register_blueprint(bp, **kwargs)

# Track last read position (lock guards against race with watcher thread + poll)
last_log_position = 0
last_execution_log_position = 0
_log_watcher_lock = threading.Lock()

# Centralized policy limits (UI/runtime tuning).
RESIDENT_COUNT_MIN = 1
RESIDENT_COUNT_MAX = 16
HUMAN_USERNAME_MAX_CHARS = 256
ROLLBACK_DAYS_MIN = 1
ROLLBACK_DAYS_MAX = 180
ROLLBACK_AVAILABLE_DAYS_WINDOW = 14
ROLLBACK_AFFECTED_PREVIEW_MAX = 6
ROLLBACK_CHECKPOINT_SCAN_MAX = 10000
MESSAGES_FEED_MAX = 50
DM_MESSAGES_MAX_LIMIT = 500
DM_THREADS_DEFAULT_LIMIT = 40
INSIGHTS_HEALTH_BACKLOG_WARN = 8
INSIGHTS_SOCIAL_UNREAD_WARN = 5
REFERENCE_WEEKDAY_NAMES = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
API_AUDIT_LOG_FILE = AUDIT_ROOT / "api_audit.log"
LEGACY_API_AUDIT_LOG_FILE = CODE_ROOT / "api_audit.log"
# Resident "day" length: use resident_onboarding.get_resident_cycle_seconds() so it scales with UI runtime speed.
MAILBOX_QUESTS_FILE = MUTABLE_SWARM_DIR / "mailbox_quests.json"
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


def get_stop_status():
    """Check if kill switch is engaged."""
    if KILL_SWITCH.exists():
        try:
            with open(KILL_SWITCH) as f:
                data = json.load(f)
                return data.get('halt', False)
        except:
            pass
    return False


def set_stop_status(stopped: bool):
    """Set kill switch status."""
    KILL_SWITCH.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'halt': stopped,
        'reason': 'Manual stop from control panel' if stopped else None,
        'timestamp': datetime.now().isoformat()
    }
    with open(KILL_SWITCH, 'w') as f:
        json.dump(data, f, indent=2)
    return stopped


@app.route('/')
def index():
    return render_template_string(CONTROL_PANEL_HTML)


@app.route('/favicon.ico')
def favicon():
    # Avoid noisy 404 errors during local development.
    return ("", 204)


@socketio.on('connect')
def on_socket_connect():
    """Reject websocket connections from non-loopback clients."""
    if not is_request_from_loopback():
        return False
    return None


# Identity API routes moved to blueprints/identities/routes.py


@app.route('/api/stop_status')
def api_stop_status():
    return jsonify({'stopped': get_stop_status()})


@app.route('/api/toggle_stop', methods=['POST'])
def api_toggle_stop():
    current = get_stop_status()
    new_status = set_stop_status(not current)
    socketio.emit('stop_status', {'stopped': new_status})
    return jsonify({'stopped': new_status})


# Spawner process tracking
SPAWNER_PROCESS_FILE = WORKSPACE / ".swarm" / "spawner_process.json"
SPAWNER_CONFIG_FILE = WORKSPACE / ".swarm" / "spawner_config.json"
DEFAULT_RUNTIME_SPEED_SECONDS = max(0.0, _safe_float_env("VIVARIUM_RUNTIME_WAIT_SECONDS", 2.0))


def get_spawner_status():
    """Get current spawner process status."""
    status = {
        'running': False,
        'paused': False,
        'pid': None,
        'started_at': None,
        'config': None
    }

    # Check process file
    if SPAWNER_PROCESS_FILE.exists():
        try:
            with open(SPAWNER_PROCESS_FILE) as f:
                data = json.load(f)
                status['pid'] = data.get('pid')
                status['started_at'] = data.get('started_at')
                status['running'] = data.get('running', False)

                # Verify process is actually running
                if status['pid'] and status['running']:
                    import subprocess
                    try:
                        # Windows: check if PID exists
                        result = subprocess.run(
                            ['tasklist', '/FI', f'PID eq {status["pid"]}'],
                            capture_output=True, text=True
                        )
                        if str(status['pid']) not in result.stdout:
                            status['running'] = False
                    except:
                        pass
        except:
            pass

    # Check pause status
    pause_file = WORKSPACE / "PAUSE"
    if pause_file.exists():
        status['paused'] = True

    # Load config
    if SPAWNER_CONFIG_FILE.exists():
        try:
            with open(SPAWNER_CONFIG_FILE) as f:
                status['config'] = json.load(f)
        except:
            pass

    return status


def save_spawner_process(pid: int, running: bool, config: dict = None):
    """Save spawner process info."""
    SPAWNER_PROCESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'pid': pid,
        'running': running,
        'started_at': datetime.now().isoformat(),
        'config': config
    }
    with open(SPAWNER_PROCESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def save_spawner_config(config: dict):
    """Save spawner configuration."""
    SPAWNER_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    config['updated_at'] = datetime.now().isoformat()
    with open(SPAWNER_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def _sanitize_spawner_start_payload(data: dict):
    sessions = data.get('sessions', 3)
    budget_limit = data.get('budget_limit', 1.0)
    auto_scale = bool(data.get('auto_scale', False))
    model = str(data.get('model', 'llama-3.3-70b-versatile')).strip()

    try:
        sessions = int(sessions)
    except (TypeError, ValueError):
        raise ValueError("sessions must be an integer")
    if sessions < 1 or sessions > 32:
        raise ValueError("sessions must be between 1 and 32")

    try:
        budget_limit = float(budget_limit)
    except (TypeError, ValueError):
        raise ValueError("budget_limit must be a number")
    if budget_limit <= 0:
        raise ValueError("budget_limit must be > 0")

    if not model:
        raise ValueError("model must be non-empty")
    if len(model) > 120:
        raise ValueError("model is too long")

    return {
        "sessions": sessions,
        "budget_limit": budget_limit,
        "auto_scale": auto_scale,
        "model": model,
    }


@app.route('/api/spawner/status')
def api_spawner_status():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'running': False,
        'paused': False,
        'pid': None,
        'config': None,
        'golden_path_only': True,
        'message': 'Golden path enforced: run queue tasks through vivarium.runtime.worker_runtime.'
    })


@app.route('/api/spawner/start', methods=['POST'])
def api_start_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use queue.json + python -m vivarium.runtime.worker_runtime run.'
    }), 410


@app.route('/api/spawner/pause', methods=['POST'])
def api_pause_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use runtime safety controls only.'
    }), 410


@app.route('/api/spawner/resume', methods=['POST'])
def api_resume_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use runtime safety controls only.'
    }), 410


@app.route('/api/spawner/kill', methods=['POST'])
def api_kill_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use runtime safety controls only.'
    }), 410


@app.route('/api/spawner/config', methods=['POST'])
def api_update_spawner_config():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Configuration updates are ignored.'
    }), 410


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


@app.route("/api/worker/status")
def api_worker_status():
    return jsonify(get_worker_status())


@app.route("/api/worker/start", methods=["POST"])
def api_worker_start():
    """Start the queue worker as a subprocess so the swarm can run autonomously."""
    body = request.get_json(force=True, silent=True) or {}
    requested_count = body.get("resident_count", load_ui_settings().get("resident_count", 1))
    try:
        requested_count = _clamp_int(requested_count, RESIDENT_COUNT_MIN, RESIDENT_COUNT_MAX)
    except (TypeError, ValueError):
        requested_count = RESIDENT_COUNT_MIN

    status = get_worker_status()
    if status["running"]:
        # Only no-op when an already managed pool matches target.
        # If status is unmanaged/mixed, replace it with managed daemon workers.
        if (
            status.get("running_source") == "managed"
            and not status.get("unmanaged_pids")
            and int(status.get("target_count", 1)) == requested_count
        ):
            return jsonify({
                "success": True,
                "message": "Worker already running",
                "pid": status["pid"],
                "running_count": status.get("running_count", 1),
                "target_count": requested_count,
            })
        # Reconfigure pool size by stopping old workers first.
        for pid in status.get("pids", []):
            try:
                os.kill(pid, 15)
            except (OSError, ProcessLookupError):
                pass

    MUTABLE_SWARM_DIR.mkdir(parents=True, exist_ok=True)
    cwd = str(CODE_ROOT)
    cmd = [sys.executable, "-m", "vivarium.runtime.worker_runtime", "run"]
    base_env = os.environ.copy()
    base_env["VIVARIUM_WORKER_DAEMON"] = "1"  # run until Stop, don't exit when queue empty
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
        data = {
            "pids": pids,
            "target_count": requested_count,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(WORKER_PROCESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return jsonify({
            "success": True,
            "pid": pids[0] if pids else None,
            "pids": pids,
            "running_count": len(pids),
            "target_count": requested_count,
            "message": "Worker started",
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/worker/stop", methods=["POST"])
def api_worker_stop():
    """Stop the worker subprocess so the user can pause autonomous run."""
    status = get_worker_status()
    if not status["running"]:
        try:
            WORKER_PROCESS_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        return jsonify({"success": True, "message": "Worker not running"})

    for pid in status.get("pids", []):
        try:
            os.kill(pid, 15)  # SIGTERM
        except (OSError, ProcessLookupError):
            pass
    try:
        WORKER_PROCESS_FILE.unlink(missing_ok=True)
    except Exception:
        pass
    return jsonify({"success": True, "message": "Worker stopped"})


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


def get_runtime_speed():
    """Get current worker-loop wait seconds and resident day length (scaled with speed)."""
    cycle_seconds = float(resident_onboarding.get_resident_cycle_seconds())
    cycle_id = int(time.time() // cycle_seconds) if cycle_seconds > 0 else int(time.time())
    weekday_idx = cycle_id % 7
    payload = {
        "wait_seconds": DEFAULT_RUNTIME_SPEED_SECONDS,
        "updated_at": None,
        "current_cycle_id": cycle_id,
        "reference_weekday_index": weekday_idx,
        "reference_weekday_name": REFERENCE_WEEKDAY_NAMES[weekday_idx],
    }
    if not RUNTIME_SPEED_FILE.exists():
        payload["cycle_seconds"] = round(cycle_seconds, 1)
        return payload
    try:
        with open(RUNTIME_SPEED_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        wait = float(data.get("wait_seconds", DEFAULT_RUNTIME_SPEED_SECONDS))
        payload["wait_seconds"] = max(0.0, min(300.0, wait))
        payload["updated_at"] = data.get("updated_at")
    except Exception:
        pass
    payload["cycle_seconds"] = round(cycle_seconds, 1)
    return payload


def save_runtime_speed(wait_seconds: float):
    """Persist worker-loop wait seconds for auditable pacing."""
    clamped = max(0.0, min(300.0, float(wait_seconds)))
    payload = {
        "wait_seconds": clamped,
        "updated_at": datetime.now().isoformat(),
    }
    RUNTIME_SPEED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RUNTIME_SPEED_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return payload


def _parse_utc_timestamp(raw: str):
    value = str(raw or "").strip()
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _load_checkpoint_events(limit: int = 5000) -> list[dict]:
    """Load checkpoint-created events from change journal."""
    if not CHANGE_JOURNAL_FILE.exists():
        return []
    events: list[dict] = []
    try:
        with open(CHANGE_JOURNAL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if payload.get("event") != "checkpoint_created":
                    continue
                commit_sha = str(payload.get("commit_sha") or "").strip()
                if not commit_sha:
                    continue
                ts = _parse_utc_timestamp(payload.get("timestamp"))
                if ts is None:
                    continue
                events.append(
                    {
                        "timestamp": ts,
                        "timestamp_iso": ts.isoformat(),
                        "day_tag": ts.date().isoformat(),
                        "task_id": str(payload.get("task_id") or ""),
                        "summary": str(payload.get("summary") or ""),
                        "commit_sha": commit_sha,
                    }
                )
    except OSError:
        return []
    events.sort(key=lambda item: item["timestamp"])
    if limit > 0 and len(events) > limit:
        events = events[-limit:]
    return events


def _rollback_preview_by_days(days: int) -> dict:
    now = datetime.now(timezone.utc)
    safe_days = _clamp_int(days, ROLLBACK_DAYS_MIN, ROLLBACK_DAYS_MAX)
    checkpoints = _load_checkpoint_events(limit=ROLLBACK_CHECKPOINT_SCAN_MAX)
    if not checkpoints:
        return {
            "success": False,
            "error": "No checkpoints available yet. Run tasks first so checkpoints are created.",
            "days": safe_days,
            "available_days": [],
        }

    cutoff = now - timedelta(days=safe_days)
    target = None
    for cp in checkpoints:
        if cp["timestamp"] <= cutoff:
            target = cp
        else:
            break
    if target is None:
        oldest = checkpoints[0]
        oldest_age_days = max(0.0, (now - oldest["timestamp"]).total_seconds() / 86400.0)
        return {
            "success": False,
            "error": (
                f"Not enough checkpoint history for {safe_days} day(s). "
                f"Oldest checkpoint is ~{oldest_age_days:.1f} day(s) old."
            ),
            "days": safe_days,
            "oldest_available_days": round(oldest_age_days, 2),
            "available_days": sorted({cp["day_tag"] for cp in checkpoints}, reverse=True)[:ROLLBACK_AVAILABLE_DAYS_WINDOW],
        }

    affected = [cp for cp in checkpoints if cp["timestamp"] > target["timestamp"]]
    recent_days = sorted({cp["day_tag"] for cp in checkpoints}, reverse=True)[:ROLLBACK_AVAILABLE_DAYS_WINDOW]
    return {
        "success": True,
        "days": safe_days,
        "target": {
            "commit_sha": target["commit_sha"],
            "timestamp": target["timestamp_iso"],
            "day_tag": target["day_tag"],
            "task_id": target["task_id"],
            "summary": target["summary"],
        },
        "checkpoints_total": len(checkpoints),
        "checkpoints_since_target": len(affected),
        "available_days": recent_days,
        "affected_preview": [
            {
                "day_tag": cp["day_tag"],
                "task_id": cp["task_id"],
                "summary": cp["summary"],
                "timestamp": cp["timestamp_iso"],
            }
            for cp in affected[-ROLLBACK_AFFECTED_PREVIEW_MAX:]
        ],
    }


@app.route('/api/runtime_speed', methods=['GET'])
def api_get_runtime_speed():
    return jsonify(get_runtime_speed())


@app.route('/api/runtime_speed', methods=['POST'])
def api_set_runtime_speed():
    data = request.json or {}
    raw = data.get("wait_seconds", DEFAULT_RUNTIME_SPEED_SECONDS)
    try:
        wait_seconds = float(raw)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "wait_seconds must be a number"}), 400
    saved = save_runtime_speed(wait_seconds)
    return jsonify({"success": True, **saved})


@app.route('/api/rollback/preview')
def api_rollback_preview():
    raw_days = request.args.get("days", "1")
    try:
        days = int(raw_days)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "days must be an integer"}), 400
    preview = _rollback_preview_by_days(days)
    status_code = 200 if preview.get("success") else 400
    return jsonify(preview), status_code


@app.route('/api/rollback/by_days', methods=['POST'])
def api_rollback_by_days():
    body = request.get_json(force=True, silent=True) or {}
    raw_days = body.get("days", 1)
    reason = str(body.get("reason") or "").strip()
    try:
        days = int(raw_days)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "days must be an integer"}), 400

    if days < ROLLBACK_DAYS_MIN or days > ROLLBACK_DAYS_MAX:
        return jsonify(
            {
                "success": False,
                "error": f"days must be between {ROLLBACK_DAYS_MIN} and {ROLLBACK_DAYS_MAX}",
            }
        ), 400

    worker_status = get_worker_status()
    if worker_status.get("running"):
        if bool(body.get("force_stop")):
            stop_result = _stop_workers_for_maintenance()
            if not stop_result.get("success"):
                return jsonify({
                    "success": False,
                    "error": "Could not stop all workers before rollback.",
                    "running_count": len(stop_result.get("remaining_pids", [])),
                    "remaining_pids": stop_result.get("remaining_pids", []),
                }), 409
        else:
            return jsonify({
                "success": False,
                "error": "Stop the swarm before rollback to avoid race conditions.",
                "running_count": worker_status.get("running_count", 0),
            }), 409

    preview = _rollback_preview_by_days(days)
    if not preview.get("success"):
        return jsonify(preview), 400

    target = preview.get("target") or {}
    commit_sha = str(target.get("commit_sha") or "").strip()
    if not commit_sha:
        return jsonify({"success": False, "error": "Could not resolve rollback target commit"}), 500

    rollback_reason = reason or f"UI rollback by {days} day(s)"
    try:
        vcs = get_mutable_version_control()
        ok = vcs.rollback_to(commit_sha=commit_sha, reason=rollback_reason)
    except Exception as exc:
        return jsonify({"success": False, "error": f"Rollback failed: {exc}"}), 500

    if not ok:
        return jsonify({"success": False, "error": "Rollback command did not complete successfully"}), 500

    return jsonify({
        "success": True,
        "days": days,
        "target": target,
        "message": "Rollback applied to mutable world state.",
    })


@app.route('/api/ui_settings', methods=['GET'])
def api_get_ui_settings():
    """Get persisted UI defaults (local, gitignored)."""
    return jsonify({"success": True, **load_ui_settings()})


@app.route('/api/ui_settings', methods=['POST'])
def api_set_ui_settings():
    """Persist UI defaults (local, gitignored)."""
    data = request.get_json(force=True, silent=True) or {}
    allowed = {
        "override_model",
        "model",
        "auto_scale",
        "budget_limit",
        "task_min_budget",
        "task_max_budget",
        "resident_count",
        "human_username",
    }
    updates = {k: data[k] for k in allowed if k in data}
    saved = save_ui_settings(updates)
    return jsonify({"success": True, **saved})


def _reload_groq_runtime_clients() -> None:
    """Reset Groq client singleton so new key is used immediately."""
    try:
        from vivarium.runtime import groq_client
        groq_client._groq_engine = None
    except Exception:
        pass


def _persist_groq_api_key(api_key: str) -> None:
    GROQ_API_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    GROQ_API_KEY_FILE.write_text(api_key.strip() + "\n", encoding="utf-8")
    try:
        os.chmod(GROQ_API_KEY_FILE, 0o600)
    except OSError:
        pass


def _delete_persisted_groq_api_key() -> None:
    try:
        if GROQ_API_KEY_FILE.exists():
            GROQ_API_KEY_FILE.unlink()
    except OSError:
        pass


def _load_persisted_groq_api_key() -> str:
    if not GROQ_API_KEY_FILE.exists():
        return ""
    try:
        return GROQ_API_KEY_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _ensure_groq_key_loaded() -> dict:
    live_key = (runtime_config.get_groq_api_key() or "").strip()
    if live_key:
        return {"configured": True, "key": live_key, "source": "env"}

    persisted = _load_persisted_groq_api_key()
    if persisted:
        runtime_config.set_groq_api_key(persisted)
        _reload_groq_runtime_clients()
        return {"configured": True, "key": persisted, "source": "security_file"}

    return {"configured": False, "key": "", "source": None}


@app.route('/api/groq_key', methods=['GET'])
def api_get_groq_key_status():
    state = _ensure_groq_key_loaded()
    return jsonify(
        {
            "success": True,
            "configured": state["configured"],
            "source": state["source"],
            "masked_key": _mask_secret(state["key"]) if state["configured"] else None,
        }
    )


@app.route('/api/groq_key', methods=['POST'])
def api_set_groq_key():
    data = request.json or {}
    api_key = str(data.get("api_key", "")).strip()
    if not api_key:
        return jsonify({"success": False, "error": "api_key is required"}), 400
    if len(api_key) < 16:
        return jsonify({"success": False, "error": "api_key is too short"}), 400
    if len(api_key) > 256:
        return jsonify({"success": False, "error": "api_key is too long"}), 400

    _persist_groq_api_key(api_key)
    runtime_config.set_groq_api_key(api_key)
    _reload_groq_runtime_clients()
    return jsonify(
        {
            "success": True,
            "configured": True,
            "masked_key": _mask_secret(api_key),
            "source": "security_file",
        }
    )


@app.route('/api/groq_key', methods=['DELETE'])
def api_delete_groq_key():
    _delete_persisted_groq_api_key()
    runtime_config.set_groq_api_key(None)
    _reload_groq_runtime_clients()
    return jsonify({"success": True, "configured": False})


# Human request storage
HUMAN_REQUEST_FILE = WORKSPACE / ".swarm" / "human_request.json"

# Message queue for identity <-> human communication
MESSAGES_TO_HUMAN = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
MESSAGES_FROM_HUMAN = WORKSPACE / ".swarm" / "messages_from_human.json"
MESSAGES_FROM_HUMAN_OUTBOX = WORKSPACE / ".swarm" / "messages_from_human_outbox.jsonl"


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


@app.route('/api/human_request', methods=['GET'])
def api_get_human_request():
    return jsonify({'request': get_human_request()})


@app.route('/api/human_request', methods=['POST'])
def api_save_human_request():
    data = request.get_json(force=True, silent=True) or {}
    request_text = str(data.get('request', ''))
    try:
        result = save_human_request(request_text)
        task_id = enqueue_human_suggestion(request_text)
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500
    return jsonify({'success': True, 'updated_at': result['updated_at'], 'task_id': task_id})


# Message queue endpoints
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


@app.route('/api/quests/create', methods=['POST'])
def api_create_mailbox_quest():
    """
    Create an identity-targeted quest from mailbox UI.
    """
    data = request.get_json(force=True, silent=True) or {}
    identity_id = str(data.get("identity_id") or "").strip()
    prompt = str(data.get("prompt") or "").strip()
    title = str(data.get("title") or "").strip() or "Mailbox Quest"
    if not identity_id:
        return jsonify({"success": False, "error": "identity_id is required"}), 400
    if not prompt:
        return jsonify({"success": False, "error": "prompt is required"}), 400

    budget = _normalize_quest_budget(data.get("budget"), QUEST_DEFAULT_BUDGET)
    upfront_tip = _normalize_quest_tokens(data.get("upfront_tip"), QUEST_DEFAULT_UPFRONT_TIP)
    completion_reward = _normalize_quest_tokens(data.get("completion_reward"), QUEST_DEFAULT_COMPLETION_REWARD)
    min_budget = max(0.01, round(min(0.10, budget), 4))
    max_budget = max(min_budget, budget)

    identities = get_identities()
    identity = next((i for i in identities if str(i.get("id")) == identity_id), None)
    identity_name = str((identity or {}).get("name") or identity_id)
    quest_id = f"quest_{int(time.time() * 1000)}"
    task_id = f"quest-task-{identity_id}-{int(time.time() * 1000)}"
    quest_prompt = (
        f"Quest for {identity_name} ({identity_id}).\n"
        f"Objective: {prompt}\n\n"
        "Run this quest while still participating in normal resident social life: "
        "coordination, DMs, and shared room interactions stay active."
    )

    try:
        _enqueue_identity_task(
            task_id=task_id,
            prompt=quest_prompt,
            identity_id=identity_id,
            min_budget=min_budget,
            max_budget=max_budget,
        )
        if upfront_tip > 0:
            _dm_enrichment().grant_free_time(identity_id, upfront_tip, reason=f"{quest_id}_upfront_tip")
        _dm_enrichment().post_discussion_message(
            identity_id="human_operator",
            identity_name=get_human_username(),
            content=f"[quest assigned to {identity_name}] {title}: {prompt}",
            room="human_async",
            mood="async",
            importance=4,
        )
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

    quests = _load_mailbox_quests()
    quests.insert(
        0,
        {
            "id": quest_id,
            "task_id": task_id,
            "identity_id": identity_id,
            "identity_name": identity_name,
            "title": title,
            "prompt": prompt,
            "budget": max_budget,
            "upfront_tip": upfront_tip,
            "completion_reward": completion_reward,
            "status": "active",
            "manual_paused": False,
            "completion_approved": False,
            "completion_reward_paid": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        },
    )
    _save_mailbox_quests(quests)
    return jsonify({"success": True, "quest_id": quest_id, "task_id": task_id})


@app.route('/api/quests/status')
def api_quest_status():
    quests = _refresh_mailbox_quests_state()
    return jsonify({"success": True, "quests": quests[:120]})


@app.route('/api/quests/tip', methods=['POST'])
def api_quest_tip():
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    tokens = _normalize_quest_tokens(data.get("tokens"), 10)
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    if tokens <= 0:
        return jsonify({"success": False, "error": "tokens must be > 0"}), 400

    quests = _load_mailbox_quests()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404
    identity_id = str(quest.get("identity_id") or "").strip()
    if not identity_id:
        return jsonify({"success": False, "error": "quest identity missing"}), 400

    try:
        _dm_enrichment().grant_free_time(identity_id, tokens, reason=f"{quest_id}_manual_tip")
        quest["updated_at"] = datetime.now().isoformat()
        quest["last_tip_tokens"] = tokens
        quest["last_tip_at"] = quest["updated_at"]
        _save_mailbox_quests(quests)
        return jsonify({"success": True, "quest": quest})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route('/api/quests/pause', methods=['POST'])
def api_quest_pause():
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    quests = _load_mailbox_quests()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404

    task_id = str(quest.get("task_id") or "").strip()
    removed_task = None
    if task_id:
        removed_task, _ = _remove_open_queue_task(task_id)
    quest["paused_task"] = removed_task
    quest["manual_paused"] = True
    quest["status"] = "paused"
    quest["updated_at"] = datetime.now().isoformat()
    _save_mailbox_quests(quests)
    return jsonify({"success": True, "quest": quest, "removed_from_open_queue": bool(removed_task)})


@app.route('/api/quests/resume', methods=['POST'])
def api_quest_resume():
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    quests = _load_mailbox_quests()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404

    paused_task = quest.get("paused_task")
    if isinstance(paused_task, dict) and paused_task.get("id"):
        queue = normalize_queue(read_json(QUEUE_FILE, default={}))
        if not any(str(t.get("id") or "") == str(paused_task.get("id")) for t in queue.get("tasks", [])):
            queue.setdefault("tasks", []).append(normalize_task(paused_task))
            write_json(QUEUE_FILE, normalize_queue(queue))
    quest["paused_task"] = None
    quest["manual_paused"] = False
    quest["status"] = "active"
    quest["updated_at"] = datetime.now().isoformat()
    _save_mailbox_quests(quests)
    return jsonify({"success": True, "quest": quest})


@app.route('/api/quests/approve', methods=['POST'])
def api_quest_approve():
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    quests = _refresh_mailbox_quests_state()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404
    if str(quest.get("status")) not in {"awaiting_approval", "completed"}:
        return jsonify({"success": False, "error": "quest is not awaiting approval"}), 409
    if quest.get("completion_reward_paid"):
        return jsonify({"success": False, "error": "completion reward already paid"}), 409

    identity_id = str(quest.get("identity_id") or "").strip()
    reward = _normalize_quest_tokens(quest.get("completion_reward"), QUEST_DEFAULT_COMPLETION_REWARD)
    try:
        if reward > 0 and identity_id:
            _dm_enrichment().grant_free_time(identity_id, reward, reason=f"{quest_id}_completion_reward")
        quest["completion_approved"] = True
        quest["completion_reward_paid"] = reward > 0
        quest["status"] = "completed"
        quest["updated_at"] = datetime.now().isoformat()
        _save_mailbox_quests(quests)
        return jsonify({"success": True, "quest": quest, "reward": reward})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


# Completed requests log
COMPLETED_REQUESTS_FILE = WORKSPACE / ".swarm" / "completed_requests.json"


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


@app.route('/api/completed_requests', methods=['GET'])
def api_get_completed_requests():
    """Get completed requests history."""
    return jsonify(get_completed_requests())


@app.route('/api/completed_requests', methods=['POST'])
def api_add_completed_request():
    """Mark a request as completed."""
    data = request.json
    request_text = data.get('request', '').strip()

    if not request_text:
        return jsonify({'success': False, 'error': 'No request text'})

    result = add_completed_request(request_text)
    return jsonify({'success': True, 'completed': result})


# Bounty API endpoints
CRUCIBLE_NAME = "Commons Crucible"
DEFAULT_SLOT_POLICY = {
    "in_slot_multiplier": 1.0,
    "overflow_decay": 0.5,
    "min_multiplier": 0.05,
    "min_description_chars": 20,
    "allow_artifact_override": True,
    "max_rewarded_submissions_per_identity": 1,
}

BOUNTIES_FILE = WORKSPACE / ".swarm" / "bounties.json"


def _get_slots_for_bounty(bounty: dict) -> int:
    slots = bounty.get("slots", bounty.get("max_teams", 1))
    try:
        return max(1, int(slots))
    except (TypeError, ValueError):
        return 1


def _normalize_slot_policy(policy):
    merged = DEFAULT_SLOT_POLICY.copy()
    if isinstance(policy, dict):
        for key in DEFAULT_SLOT_POLICY:
            if key in policy:
                merged[key] = policy[key]
    # Clamp numeric fields
    try:
        merged["overflow_decay"] = float(merged["overflow_decay"])
    except (TypeError, ValueError):
        merged["overflow_decay"] = DEFAULT_SLOT_POLICY["overflow_decay"]
    merged["overflow_decay"] = max(0.1, min(0.95, merged["overflow_decay"]))
    try:
        merged["min_multiplier"] = float(merged["min_multiplier"])
    except (TypeError, ValueError):
        merged["min_multiplier"] = DEFAULT_SLOT_POLICY["min_multiplier"]
    merged["min_multiplier"] = max(0.0, min(1.0, merged["min_multiplier"]))
    try:
        merged["in_slot_multiplier"] = float(merged["in_slot_multiplier"])
    except (TypeError, ValueError):
        merged["in_slot_multiplier"] = DEFAULT_SLOT_POLICY["in_slot_multiplier"]
    merged["in_slot_multiplier"] = max(0.1, min(2.0, merged["in_slot_multiplier"]))
    try:
        merged["min_description_chars"] = int(merged["min_description_chars"])
    except (TypeError, ValueError):
        merged["min_description_chars"] = DEFAULT_SLOT_POLICY["min_description_chars"]
    merged["min_description_chars"] = max(0, merged["min_description_chars"])
    try:
        merged["max_rewarded_submissions_per_identity"] = int(
            merged["max_rewarded_submissions_per_identity"]
        )
    except (TypeError, ValueError):
        merged["max_rewarded_submissions_per_identity"] = (
            DEFAULT_SLOT_POLICY["max_rewarded_submissions_per_identity"]
        )
    merged["max_rewarded_submissions_per_identity"] = max(
        1, merged["max_rewarded_submissions_per_identity"]
    )
    merged["allow_artifact_override"] = bool(merged.get("allow_artifact_override", True))
    return merged


def _compute_slot_multiplier(slot_index: int, slots: int, policy: dict) -> float:
    if slots <= 0 or slot_index <= slots:
        return float(policy.get("in_slot_multiplier", 1.0))
    overflow = max(0, slot_index - slots)
    decay = float(policy.get("overflow_decay", 0.5))
    multiplier = float(policy.get("in_slot_multiplier", 1.0)) * (decay ** overflow)
    return max(float(policy.get("min_multiplier", 0.05)), multiplier)


def _evaluate_submission(bounty, identity_id, description, artifacts):
    teams = bounty.get("teams", [])
    slots = _get_slots_for_bounty(bounty)
    slot_index = len(teams) + 1
    policy = _normalize_slot_policy(bounty.get("slot_policy"))

    multiplier = _compute_slot_multiplier(slot_index, slots, policy)
    reasons = []

    if not identity_id:
        reasons.append("missing_identity")

    if identity_id:
        submitted = [t for t in teams if t.get("identity_id") == identity_id]
        if len(submitted) >= policy.get("max_rewarded_submissions_per_identity", 1):
            reasons.append("repeat_submission")

    min_chars = policy.get("min_description_chars", 0)
    desc_ok = len((description or "").strip()) >= min_chars if min_chars else True
    has_artifacts = bool(artifacts)
    if not desc_ok and not (policy.get("allow_artifact_override", True) and has_artifacts):
        reasons.append("insufficient_contribution")

    if slot_index > slots:
        reasons.append("overflow")

    if reasons and any(r in ["missing_identity", "repeat_submission", "insufficient_contribution"] for r in reasons):
        multiplier = 0.0

    if not reasons:
        reason = "in_slot"
    else:
        reason = ",".join(reasons)

    return {
        "slot_index": slot_index,
        "slots": slots,
        "slot_multiplier": round(multiplier, 4),
        "slot_reason": reason,
        "policy": policy,
    }


def _normalize_submission_text(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _submission_fingerprint(
    identity_id: str,
    description: str,
    artifacts: list,
    members: list,
) -> str:
    normalized_artifacts = sorted(
        {
            _normalize_submission_text(item)
            for item in artifacts
            if _normalize_submission_text(item)
        }
    )
    normalized_members = sorted(
        {
            _normalize_submission_text(item)
            for item in members
            if _normalize_submission_text(item)
        }
    )
    payload = "\n".join(
        [
            _normalize_submission_text(identity_id),
            _normalize_submission_text(description),
            ",".join(normalized_members),
            ",".join(normalized_artifacts),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_bounties():
    """Load bounties from file."""
    if BOUNTIES_FILE.exists():
        try:
            with open(BOUNTIES_FILE) as f:
                return json.load(f)
        except:
            pass
    return []


def save_bounties(bounties):
    """Save bounties to file."""
    BOUNTIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BOUNTIES_FILE, 'w') as f:
        json.dump(bounties, f, indent=2)


@app.route('/api/bounties', methods=['GET'])
def api_get_bounties():
    """Get all non-completed bounties."""
    bounties = load_bounties()
    # Filter to show open and claimed (not completed unless recent)
    active = [b for b in bounties if b.get('status') in ('open', 'claimed')]
    return jsonify(active)


@app.route('/api/bounties', methods=['POST'])
def api_create_bounty():
    """Create a new bounty."""
    data = request.json
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    reward = int(data.get('reward', 50))
    slots = data.get('slots', data.get('max_teams', 1))
    try:
        slots = max(1, int(slots))
    except (TypeError, ValueError):
        slots = 1
    game_mode = (data.get('game_mode') or 'hybrid').lower()
    if game_mode not in ('pvp', 'coop', 'hybrid'):
        game_mode = 'hybrid'
    slot_policy = _normalize_slot_policy(data.get('slot_policy'))

    if not title:
        return jsonify({'success': False, 'error': 'Title required'})

    bounties = load_bounties()
    bounty = {
        'id': f"bounty_{int(time.time()*1000)}",
        'title': title,
        'description': description,
        'reward': reward,
        'game_name': CRUCIBLE_NAME,
        'game_mode': game_mode,
        'status': 'open',
        'created_at': datetime.now().isoformat(),
        'claimed_by': None,
        # Project-level cost tracking
        'max_teams': slots,  # Back-compat: guild slots with full rewards
        'slots': slots,
        'slot_policy': slot_policy,
        'slot_state': {
            'slots': slots,
            'filled': 0,
            'overflow': 0
        },
        'teams': [],  # List of guild submissions
        'cost_tracking': {
            'api_cost': 0.0,
            'sessions_used': 0,
            'tokens_spent': 0,
            'started_at': None,
            'artifacts_created': []
        }
    }
    bounties.append(bounty)
    save_bounties(bounties)

    return jsonify({'success': True, 'bounty': bounty})


@app.route('/api/bounties/<bounty_id>', methods=['DELETE'])
def api_delete_bounty(bounty_id):
    """Delete an unclaimed bounty."""
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    if bounty.get('status') != 'open':
        return jsonify({'success': False, 'error': 'Can only delete open bounties'})

    bounties = [b for b in bounties if b['id'] != bounty_id]
    save_bounties(bounties)

    return jsonify({'success': True})


@app.route('/api/bounties/<bounty_id>/submit', methods=['POST'])
def api_submit_to_bounty(bounty_id):
    """Submit work to a bounty (for competing guilds)."""
    data = request.json or {}
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    if bounty.get('status') not in ('open', 'claimed'):
        return jsonify({'success': False, 'error': 'Bounty is not open for submissions'})

    # Normalize slot policy and evaluate rewards
    bounty['slot_policy'] = _normalize_slot_policy(bounty.get('slot_policy'))
    bounty['slots'] = _get_slots_for_bounty(bounty)

    identity_id = data.get('identity_id')
    description = data.get('description', '')
    raw_artifacts = data.get('artifacts', [])
    artifacts = []
    if isinstance(raw_artifacts, list):
        for artifact in raw_artifacts:
            normalized = str(artifact or '').strip()
            if normalized and normalized not in artifacts:
                artifacts.append(normalized)
    guild_id = str(data.get('guild_id') or '').strip() or None
    guild_name = str(data.get('guild_name') or '').strip() or None
    raw_members = data.get('members', [])
    members = []
    if isinstance(raw_members, list):
        for member in raw_members:
            normalized = str(member or '').strip()
            if normalized and normalized not in members:
                members.append(normalized)
    if not members and identity_id:
        members = [str(identity_id).strip()]

    # Block duplicate submission payloads to prevent reward-gaming via dupes.
    candidate_fingerprint = _submission_fingerprint(identity_id, description, artifacts, members)
    for existing in bounty.get('teams', []):
        existing_fp = existing.get('submission_fingerprint')
        if not existing_fp:
            existing_fp = _submission_fingerprint(
                existing.get('identity_id'),
                existing.get('description', ''),
                existing.get('artifacts', []),
                existing.get('members', []),
            )
        if existing_fp == candidate_fingerprint:
            return jsonify({
                'success': False,
                'error': 'Duplicate submission blocked: identical payload already exists.'
            }), 409

    slot_info = _evaluate_submission(bounty, identity_id, description, artifacts)

    # Create submission
    submission = {
        'id': f"sub_{int(time.time()*1000)}",
        'identity_id': identity_id,
        'identity_name': data.get('identity_name', 'Unknown'),
        'members': members,
        'guild_id': guild_id,
        'guild_name': guild_name,
        'description': description,
        'artifacts': artifacts,  # List of file paths
        'submitted_at': datetime.now().isoformat(),
        'notes': data.get('notes', ''),
        'slot_index': slot_info['slot_index'],
        'slots': slot_info['slots'],
        'slot_multiplier': slot_info['slot_multiplier'],
        'slot_reason': slot_info['slot_reason'],
        'reward_cap': int(round(bounty.get('reward', 0) * slot_info['slot_multiplier']))
        ,
        'submission_fingerprint': candidate_fingerprint,
    }

    if 'teams' not in bounty:
        bounty['teams'] = []
    bounty['teams'].append(submission)

    # Update slot state
    slots = bounty.get('slots', _get_slots_for_bounty(bounty))
    team_count = len(bounty['teams'])
    bounty['slot_state'] = {
        'slots': slots,
        'filled': min(team_count, slots),
        'overflow': max(0, team_count - slots)
    }

    # Mark bounty as claimed if this is the first submission
    if bounty['status'] == 'open' and len(bounty['teams']) == 1:
        bounty['status'] = 'claimed'
        bounty['cost_tracking']['started_at'] = datetime.now().isoformat()
        if guild_id:
            bounty['claimed_by'] = {
                'type': 'guild',
                'id': guild_id,
                'name': guild_name or guild_id,
                'claimed_by_identity': identity_id,
                'claimed_by_name': data.get('identity_name', 'Unknown'),
            }
        elif identity_id:
            bounty['claimed_by'] = {
                'type': 'individual',
                'id': identity_id,
                'name': data.get('identity_name', 'Unknown'),
            }

    save_bounties(bounties)

    return jsonify({'success': True, 'submission': submission})


@app.route('/api/bounties/<bounty_id>/submissions')
def api_get_bounty_submissions(bounty_id):
    """Get all submissions for a bounty (guild submissions)."""
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    return jsonify({
        'success': True,
        'bounty_id': bounty_id,
        'bounty_title': bounty.get('title'),
        'submissions': bounty.get('teams', [])
    })


@app.route('/api/bounties/<bounty_id>/track_cost', methods=['POST'])
def api_track_bounty_cost(bounty_id):
    """Track API cost against a bounty."""
    data = request.json or {}
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    # Initialize cost tracking if missing
    if 'cost_tracking' not in bounty:
        bounty['cost_tracking'] = {
            'api_cost': 0.0,
            'sessions_used': 0,
            'tokens_spent': 0,
            'started_at': None,
            'artifacts_created': []
        }

    # Update tracking
    if data.get('api_cost'):
        bounty['cost_tracking']['api_cost'] += float(data['api_cost'])
    if data.get('session_increment'):
        bounty['cost_tracking']['sessions_used'] += 1
    if data.get('tokens_spent'):
        bounty['cost_tracking']['tokens_spent'] += int(data['tokens_spent'])
    if data.get('artifact'):
        bounty['cost_tracking']['artifacts_created'].append(data['artifact'])
    if not bounty['cost_tracking']['started_at']:
        bounty['cost_tracking']['started_at'] = datetime.now().isoformat()

    save_bounties(bounties)
    return jsonify({'success': True, 'cost_tracking': bounty['cost_tracking']})


@app.route('/api/bounties/<bounty_id>/complete', methods=['POST'])
def api_complete_bounty(bounty_id):
    """Mark a bounty as complete and distribute rewards."""
    data = request.json or {}
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    # Calculate project costs from action log if not tracked
    cost_tracking = bounty.get('cost_tracking', {})
    if cost_tracking.get('started_at') and ACTION_LOG.exists():
        try:
            start_time = datetime.fromisoformat(cost_tracking['started_at'])
            total_api_cost = cost_tracking.get('api_cost', 0.0)

            # Scan action log for API costs since bounty started
            with open(ACTION_LOG, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get('action_type') == 'API':
                            entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                            if entry_time >= start_time:
                                # Extract cost from detail like "1523 tokens | $0.003"
                                detail = entry.get('detail', '')
                                if '$' in detail:
                                    cost_str = detail.split('$')[-1]
                                    try:
                                        total_api_cost += float(cost_str)
                                    except:
                                        pass
                    except:
                        pass

            cost_tracking['api_cost'] = total_api_cost
            cost_tracking['completed_at'] = datetime.now().isoformat()

            # Calculate duration
            if cost_tracking.get('started_at'):
                start = datetime.fromisoformat(cost_tracking['started_at'])
                duration = datetime.now() - start
                hours = duration.total_seconds() / 3600
                cost_tracking['duration_hours'] = round(hours, 2)

        except Exception as e:
            print(f"Error calculating bounty costs: {e}")

    # Handle manual reward distribution for competing guilds
    winner_reward = data.get('winner_reward', bounty.get('reward', 50))
    runner_up_reward = data.get('runner_up_reward', 0)

    try:
        import sys
        sys.path.insert(0, str(WORKSPACE))
        from vivarium.runtime.swarm_enrichment import get_enrichment

        enrichment = get_enrichment(WORKSPACE)

        # If there are guild submissions, distribute according to placement
        teams = bounty.get('teams', [])
        if teams and len(teams) == 1:
            # Persist slot multiplier for single-claimer distribution
            try:
                bounty['slot_multiplier'] = float(teams[0].get('slot_multiplier', 1.0))
                bounty['slot_reason'] = teams[0].get('slot_reason', 'in_slot')
            except (TypeError, ValueError):
                bounty['slot_multiplier'] = 1.0
                bounty['slot_reason'] = 'in_slot'
            if not bounty.get('claimed_by'):
                first_team = teams[0]
                if first_team.get('guild_id'):
                    bounty['claimed_by'] = {
                        'type': 'guild',
                        'id': first_team.get('guild_id'),
                        'name': first_team.get('guild_name') or first_team.get('guild_id'),
                        'claimed_by_identity': first_team.get('identity_id'),
                        'claimed_by_name': first_team.get('identity_name', 'Unknown'),
                    }
                elif first_team.get('identity_id'):
                    bounty['claimed_by'] = {
                        'type': 'individual',
                        'id': first_team.get('identity_id'),
                        'name': first_team.get('identity_name', 'Unknown'),
                    }
            save_bounties(bounties)
        if teams and len(teams) > 1:
            # Winner gets winner_reward, runner-up gets runner_up_reward
            result = {
                'success': True,
                'distributions': [],
                'total_distributed': 0,
                'cost_tracking': cost_tracking
            }
            for i, team in enumerate(teams):
                reward = winner_reward if i == 0 else (runner_up_reward if i == 1 else 0)
                try:
                    slot_multiplier = float(team.get('slot_multiplier', 1.0))
                except (TypeError, ValueError):
                    slot_multiplier = 1.0
                reward = int(round(reward * max(0.0, slot_multiplier)))
                if reward > 0:
                    team_members = []
                    raw_team_members = team.get('members', [])
                    if isinstance(raw_team_members, list):
                        for member_id in raw_team_members:
                            normalized_member = str(member_id or '').strip()
                            if normalized_member and normalized_member not in team_members:
                                team_members.append(normalized_member)
                    if not team_members and team.get('identity_id'):
                        team_members = [str(team.get('identity_id')).strip()]
                    for member_id in team_members:
                        enrichment.grant_free_time(member_id, reward, f"bounty_{bounty_id}_place_{i+1}")
                        result['total_distributed'] += reward
                        result['distributions'].append({
                            'identity': member_id,
                            'reward': reward,
                            'place': i + 1,
                            'slot_multiplier': slot_multiplier
                        })
        else:
            # Single guild/claimant - use original distribution
            result = enrichment.distribute_bounty(bounty_id)
            result['cost_tracking'] = cost_tracking

        # Update bounty status
        bounty['status'] = 'completed'
        bounty['completed_at'] = datetime.now().isoformat()
        bounty['cost_tracking'] = cost_tracking
        save_bounties(bounties)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'cost_tracking': cost_tracking})


# ═══════════════════════════════════════════════════════════════════════════════
# ARTIFACTS VIEWER - View files created by residents
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/artifact/view')
def api_view_artifact():
    """View contents of a file artifact."""
    file_path = request.args.get('path', '')

    if not file_path:
        return jsonify({'success': False, 'error': 'No path provided'})

    # Security: Only allow viewing files within workspace
    try:
        # Resolve the path relative to workspace
        if not os.path.isabs(file_path):
            full_path = WORKSPACE / file_path
        else:
            full_path = Path(file_path)

        # Ensure it's within workspace (prevent directory traversal)
        full_path = full_path.resolve()
        if not str(full_path).startswith(str(WORKSPACE.resolve())):
            return jsonify({'success': False, 'error': 'Access denied: path outside workspace'})

        if not full_path.exists():
            return jsonify({'success': False, 'error': 'File not found'})

        if not full_path.is_file():
            return jsonify({'success': False, 'error': 'Not a file'})

        # Check file size (limit to 500KB for viewing)
        if full_path.stat().st_size > 500 * 1024:
            return jsonify({'success': False, 'error': 'File too large (>500KB)'})

        # Detect file type for syntax highlighting
        ext = full_path.suffix.lower()
        file_type_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.json': 'json',
            '.md': 'markdown',
            '.html': 'html',
            '.css': 'css',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.sql': 'sql',
            '.txt': 'text',
            '.log': 'text',
        }
        file_type = file_type_map.get(ext, 'text')

        # Read content
        try:
            content = full_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = full_path.read_text(encoding='latin-1')

        return jsonify({
            'success': True,
            'path': str(full_path.relative_to(WORKSPACE)),
            'filename': full_path.name,
            'content': content,
            'file_type': file_type,
            'size': full_path.stat().st_size,
            'modified': datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/artifacts/list')
def api_list_artifacts():
    """List recent artifacts (files created/modified by the swarm)."""
    try:
        # Get files from journals and Community Library
        artifacts_by_path = {}

        def add_artifact(path_obj: Path, artifact_type: str) -> None:
            try:
                rel_path = str(path_obj.relative_to(WORKSPACE))
                modified = datetime.fromtimestamp(path_obj.stat().st_mtime).isoformat()
            except Exception:
                return
            existing = artifacts_by_path.get(rel_path)
            if not existing or str(existing.get("modified", "")) < modified:
                artifacts_by_path[rel_path] = {
                    "path": rel_path,
                    "name": path_obj.name,
                    "type": artifact_type,
                    "modified": modified,
                }

        # Journals
        journals_dir = WORKSPACE / ".swarm" / "journals"
        if journals_dir.exists():
            for f in sorted(journals_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                add_artifact(f, "journal")

        # Community creative works
        library_dir = WORKSPACE / "library" / "creative_works"
        if library_dir.exists():
            for f in sorted(library_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                add_artifact(f, "creative_work")

        # Community library docs and resident suggestions
        community_root = WORKSPACE / "library" / "community_library"
        if community_root.exists():
            docs_dir = community_root / "swarm_docs"
            if docs_dir.exists():
                for f in sorted(docs_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                    add_artifact(f, "community_doc")
            suggestions_dir = community_root / "resident_suggestions"
            if suggestions_dir.exists():
                for f in sorted(suggestions_dir.glob("**/*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                    add_artifact(f, "community_doc")

        # Skills created
        skills_dir = WORKSPACE / "skills"
        if skills_dir.exists():
            for f in sorted(skills_dir.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
                add_artifact(f, "skill")

        artifacts = sorted(
            artifacts_by_path.values(),
            key=lambda item: str(item.get("modified") or ""),
            reverse=True,
        )
        return jsonify({'success': True, 'artifacts': artifacts[:120]})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ═══════════════════════════════════════════════════════════════════
# SWARM INSIGHTS API - At-a-glance health + behavior metrics
# ═══════════════════════════════════════════════════════════════════

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


@app.route('/api/insights')
def api_insights():
    """Aggregate queue/execution/social/safety signals for quick UI scanning."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)

    queue = {}
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
                queue = json.load(f)
        except Exception:
            queue = {}
    queue_tasks = queue.get("tasks", []) if isinstance(queue.get("tasks"), list) else []
    queue_completed = queue.get("completed", []) if isinstance(queue.get("completed"), list) else []
    queue_failed = queue.get("failed", []) if isinstance(queue.get("failed"), list) else []
    queue_summary = {
        "open": len(queue_tasks),
        "completed": len(queue_completed),
        "failed": len(queue_failed),
    }

    execution_entries = _read_jsonl_tail(EXECUTION_LOG)
    completed_24h = 0
    approved_24h = 0
    failed_24h = 0
    requeue_24h = 0
    pending_review_24h = 0
    last_event_at = None
    for entry in execution_entries:
        status = str(entry.get("status") or "").strip().lower()
        timestamp = _parse_iso_timestamp(entry.get("timestamp"))
        if timestamp and (last_event_at is None or timestamp > last_event_at):
            last_event_at = timestamp
        if not timestamp or timestamp < cutoff:
            continue
        if status in {"completed", "approved"}:
            completed_24h += 1
        if status == "approved":
            approved_24h += 1
        if status == "failed":
            failed_24h += 1
        if status == "requeue":
            requeue_24h += 1
        if status == "pending_review":
            pending_review_24h += 1

    failure_streak = 0
    for entry in reversed(execution_entries):
        status = str(entry.get("status") or "").strip().lower()
        if not status:
            continue
        if status == "failed":
            failure_streak += 1
            continue
        if status in {"in_progress", "pending_review", "requeue"}:
            continue
        break

    reviewed_total = approved_24h + failed_24h + requeue_24h
    approval_rate_24h = round((approved_24h / reviewed_total) * 100, 1) if reviewed_total > 0 else None
    execution_summary = {
        "completed_24h": completed_24h,
        "approved_24h": approved_24h,
        "failed_24h": failed_24h,
        "requeue_24h": requeue_24h,
        "pending_review_24h": pending_review_24h,
        "approval_rate_24h": approval_rate_24h,
        "failure_streak": failure_streak,
        "last_event_at": last_event_at.isoformat() if last_event_at else None,
    }

    execution_cost_all_time = 0.0
    for entry in execution_entries:
        budget_used = entry.get("budget_used")
        if budget_used is not None:
            try:
                execution_cost_all_time += float(budget_used)
            except (TypeError, ValueError):
                pass

    action_entries = _read_jsonl_tail(ACTION_LOG, max_lines=60000)
    api_audit_entries = _read_api_audit_entries(max_lines=60000)
    action_cost_all_time = 0.0
    for entry in action_entries:
        if str(entry.get("action_type") or "").strip().upper() != "API":
            continue
        action_cost_all_time += _extract_usd_cost(entry.get("detail", ""))

    api_calls_24h = 0
    api_cost_24h = 0.0
    safety_blocks_24h = 0
    errors_24h = 0
    actor_counter = Counter()
    action_type_timestamps: dict[str, list[datetime]] = {}
    for entry in action_entries:
        timestamp = _parse_iso_timestamp(entry.get("timestamp"))
        if not timestamp:
            continue
        action_type = str(entry.get("action_type") or "").strip().upper() or "UNKNOWN"
        action_type_timestamps.setdefault(action_type, []).append(timestamp)
        if timestamp < cutoff:
            continue
        actor = str(entry.get("actor") or "").strip()
        action_blob = f"{entry.get('action', '')} {entry.get('detail', '')}".upper()
        if actor and actor not in {"SYSTEM", "UNKNOWN"}:
            actor_counter[actor] += 1
        if action_type == "API":
            api_calls_24h += 1
            api_cost_24h += _extract_usd_cost(entry.get("detail", ""))
        if action_type == "SAFETY" and "BLOCKED" in action_blob:
            safety_blocks_24h += 1
        if action_type == "ERROR":
            errors_24h += 1

    # Add execution_log budget_used (actual LLM costs from worker) - action_log API entries
    # are rarely written; execution_log is the source of truth for per-task costs
    for entry in execution_entries:
        timestamp = _parse_iso_timestamp(entry.get("timestamp"))
        if not timestamp or timestamp < cutoff:
            continue
        budget_used = entry.get("budget_used")
        if budget_used is not None:
            try:
                api_cost_24h += float(budget_used)
            except (TypeError, ValueError):
                pass
    api_calls_24h_from_audit = 0
    api_cost_24h_from_audit = 0.0
    api_cost_all_time_from_audit = 0.0
    for entry in api_audit_entries:
        cost = entry.get("cost")
        try:
            cost_val = float(cost)
        except (TypeError, ValueError):
            cost_val = 0.0
        api_cost_all_time_from_audit += cost_val
        ts = _parse_iso_timestamp(entry.get("timestamp"))
        if ts and ts >= cutoff:
            api_calls_24h_from_audit += 1
            api_cost_24h_from_audit += cost_val

    # Use API audit as fallback source when action_log lacks API events.
    if api_calls_24h == 0 and api_calls_24h_from_audit > 0:
        api_calls_24h = api_calls_24h_from_audit
    if api_cost_24h == 0.0 and api_cost_24h_from_audit > 0:
        api_cost_24h = api_cost_24h_from_audit
    if action_cost_all_time == 0.0 and api_cost_all_time_from_audit > 0:
        action_cost_all_time = api_cost_all_time_from_audit

    ops_summary = {
        "api_calls_24h": api_calls_24h,
        "api_cost_24h": round(api_cost_24h, 6),
        "api_cost_all_time": round(execution_cost_all_time + action_cost_all_time, 6),
        "safety_blocks_24h": safety_blocks_24h,
        "errors_24h": errors_24h,
    }
    budget_events_24h = 0
    for ts in action_type_timestamps.get("BUDGET", []):
        if ts >= cutoff:
            budget_events_24h += 1
    ui_settings = load_ui_settings()
    task_min_budget = float(ui_settings.get("task_min_budget", 0.05) or 0.05)
    task_max_budget = float(ui_settings.get("task_max_budget", max(task_min_budget, 0.10)) or max(task_min_budget, 0.10))
    if task_max_budget < task_min_budget:
        task_max_budget = task_min_budget
    queue_budget_exposure = 0.0
    for task in queue_tasks:
        try:
            queue_budget_exposure += float(task.get("max_budget", task.get("budget", 0.0)) or 0.0)
        except Exception:
            continue

    identities = get_identities()
    identity_name_map = {item.get("id"): item.get("name") for item in identities}
    active_identity_ids = {
        actor for actor in actor_counter
        if actor in identity_name_map or actor.startswith("identity_")
    }
    top_actor = None
    if actor_counter:
        actor_id, actor_actions = actor_counter.most_common(1)[0]
        top_actor = {
            "id": actor_id,
            "name": identity_name_map.get(actor_id) or actor_id,
            "actions": actor_actions,
        }
    identities_summary = {
        "count": len(identities),
        "active_24h": len(active_identity_ids),
        "top_actor": top_actor,
    }

    messages = get_messages_to_human()
    responses = get_human_responses()
    unread_messages = 0
    for msg in messages:
        msg_id = msg.get("id")
        if msg_id and msg_id not in responses:
            unread_messages += 1
    bounties = load_bounties()
    open_bounties = len([b for b in bounties if b.get("status") == "open"])
    claimed_bounties = len([b for b in bounties if b.get("status") == "claimed"])
    completed_bounties = len([b for b in bounties if b.get("status") == "completed"])
    social_summary = {
        "total_messages": len(messages),
        "unread_messages": unread_messages,
        "open_bounties": open_bounties,
        "claimed_bounties": claimed_bounties,
        "completed_bounties": completed_bounties,
        "chat_messages_24h": _count_discussion_messages_since(cutoff),
    }

    backlog_pressure = "low"
    if queue_summary["open"] >= 12:
        backlog_pressure = "high"
    elif queue_summary["open"] >= 5:
        backlog_pressure = "medium"

    kill_switch = get_stop_status()
    health_state = "stable"
    if kill_switch:
        health_state = "critical"
    elif (
        execution_summary["failure_streak"] >= 3
        or execution_summary["failed_24h"] > max(1, execution_summary["completed_24h"])
        or ops_summary["safety_blocks_24h"] > 0
    ):
        health_state = "watch"
    if (
        execution_summary["failure_streak"] >= 6
        or ops_summary["errors_24h"] >= 5
        or ops_summary["safety_blocks_24h"] >= 3
    ):
        health_state = "critical"

    health_summary = {
        "state": health_state,
        "kill_switch": kill_switch,
        "backlog_pressure": backlog_pressure,
    }

    # Direct-message activity trends (all dm__ rooms).
    dm_timestamps: list[datetime] = []
    if DISCUSSIONS_DIR.exists():
        for room_file in DISCUSSIONS_DIR.glob("dm__*.jsonl"):
            try:
                with open(room_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            payload = json.loads(line)
                        except Exception:
                            continue
                        ts = _parse_iso_timestamp(payload.get("timestamp"))
                        if ts:
                            dm_timestamps.append(ts)
            except Exception:
                continue

    metric_cards = []

    # Existing core cards, now with expandable details.
    queue_open = int(queue_summary["open"])
    queue_tone = "warn" if queue_open >= 8 else "teal"
    metric_cards.append({
        "id": "queue",
        "label": "Queue",
        "headline": str(queue_open),
        "subline": f"{queue_summary['completed']} completed • {queue_summary['failed']} failed",
        "tone": queue_tone,
        "details": [
            f"Open tasks: {queue_summary['open']}",
            f"Completed tasks: {queue_summary['completed']}",
            f"Failed tasks: {queue_summary['failed']}",
            f"Backlog pressure: {backlog_pressure}",
        ],
    })

    throughput_tone = "bad" if failed_24h > completed_24h else ("good" if completed_24h > 0 else "")
    metric_cards.append({
        "id": "throughput",
        "label": "Throughput (24h)",
        "headline": f"{completed_24h} / {failed_24h}",
        "subline": "completed / failed",
        "tone": throughput_tone,
        "details": [
            f"Completed: {completed_24h}",
            f"Failed: {failed_24h}",
            f"Requeue: {requeue_24h}",
            f"Pending review: {pending_review_24h}",
            f"Failure streak: {failure_streak}",
        ],
    })

    quality_headline = "--" if approval_rate_24h is None else f"{approval_rate_24h:.1f}%"
    quality_tone = "good" if (approval_rate_24h or 0) >= 85 else ("warn" if (approval_rate_24h or 0) >= 60 else ("bad" if approval_rate_24h else ""))
    metric_cards.append({
        "id": "quality",
        "label": "Quality (24h)",
        "headline": quality_headline,
        "subline": f"{approved_24h} approved • {pending_review_24h} pending",
        "tone": quality_tone,
        "details": [
            f"Approval rate: {quality_headline}",
            f"Approved: {approved_24h}",
            f"Pending review: {pending_review_24h}",
            f"Requeue: {requeue_24h}",
            f"Last execution event: {execution_summary['last_event_at'] or 'n/a'}",
        ],
    })

    cost_tone = "warn" if api_cost_24h > 1.0 else ("teal" if api_cost_24h > 0 else "")
    metric_cards.append({
        "id": "cost_api",
        "label": "Cost + API (24h)",
        "headline": _format_usd_display(api_cost_24h),
        "subline": f"{api_calls_24h} API calls",
        "tone": cost_tone,
        "details": [
            f"API cost (24h): ${api_cost_24h:.6f}",
            f"API calls (24h): {api_calls_24h}",
            f"Safety blocks (24h): {safety_blocks_24h}",
            f"Errors (24h): {errors_24h}",
        ],
    })
    spend_queue_tone = "warn" if queue_budget_exposure > 1.0 else ("teal" if (api_cost_24h > 0 or queue_budget_exposure > 0) else "")
    metric_cards.append({
        "id": "spend_queue",
        "label": "Spend + Queue",
        "headline": _format_usd_display(api_cost_24h),
        "subline": (
            f"all-time {_format_usd_display(execution_cost_all_time + action_cost_all_time)} "
            f"• queue est ${queue_budget_exposure:.2f}"
        ),
        "tone": spend_queue_tone,
        "details": [
            f"API cost (24h): ${api_cost_24h:.6f}",
            f"API cost (all-time): ${execution_cost_all_time + action_cost_all_time:.6f}",
            f"Budget actions (24h): {budget_events_24h}",
            f"Queued budget exposure: ${queue_budget_exposure:.4f}",
            f"Per-task default range: ${task_min_budget:.2f} - ${task_max_budget:.2f}",
        ],
    })

    safety_tone = "bad" if (safety_blocks_24h > 0 or errors_24h > 0) else "good"
    metric_cards.append({
        "id": "safety_errors",
        "label": "Safety + Errors (24h)",
        "headline": f"{safety_blocks_24h} / {errors_24h}",
        "subline": "blocked safety / errors",
        "tone": safety_tone,
        "details": [
            f"Safety blocks: {safety_blocks_24h}",
            f"Errors: {errors_24h}",
            f"Kill switch: {'ON' if kill_switch else 'OFF'}",
            f"Health state: {health_state.upper()}",
        ],
    })

    metric_cards.append({
        "id": "social",
        "label": "Social",
        "headline": str(unread_messages),
        "subline": f"{open_bounties} open • {claimed_bounties} claimed bounties",
        "tone": "warn" if unread_messages > INSIGHTS_SOCIAL_UNREAD_WARN else ("teal" if unread_messages > 0 else ""),
        "details": [
            f"Unread human messages: {unread_messages}",
            f"Open bounties: {open_bounties}",
            f"Claimed bounties: {claimed_bounties}",
            f"Completed bounties: {completed_bounties}",
            f"Discussion messages (24h): {social_summary['chat_messages_24h']}",
        ],
    })

    top_actor_name = (top_actor or {}).get("name") or "none"
    top_actor_actions = int((top_actor or {}).get("actions") or 0)
    metric_cards.append({
        "id": "identities",
        "label": "Active Identities (24h)",
        "headline": f"{identities_summary['active_24h']}/{identities_summary['count']}",
        "subline": f"top actor: {top_actor_name}",
        "tone": "good" if identities_summary["active_24h"] > 0 else "",
        "details": [
            f"Active identities (24h): {identities_summary['active_24h']}",
            f"Total identities: {identities_summary['count']}",
            f"Top actor: {top_actor_name} ({top_actor_actions} actions)",
        ],
    })

    metric_cards.append({
        "id": "health",
        "label": "Swarm Health",
        "headline": health_state.upper(),
        "subline": f"backlog {backlog_pressure} • streak {failure_streak}",
        "tone": "good" if health_state == "stable" else ("warn" if health_state == "watch" else "bad"),
        "details": [
            f"Health state: {health_state.upper()}",
            f"Backlog pressure: {backlog_pressure}",
            f"Failure streak: {failure_streak}",
            f"Kill switch: {'ON' if kill_switch else 'OFF'}",
        ],
    })

    dm_trends = _trend_snapshot(dm_timestamps, now)
    metric_cards.append({
        "id": "dm_activity",
        "label": "DM Activity",
        "headline": str(dm_trends["day"]),
        "subline": f"day sends • week {dm_trends['week']} • month {dm_trends['month']}",
        "tone": "teal" if dm_trends["day"] > 0 else "",
        "details": [
            f"DMs today: {dm_trends['day']}",
            f"DMs this week: {dm_trends['week']}",
            f"DMs this month: {dm_trends['month']}",
            f"Day change vs 3-week baseline: {dm_trends['day_trend_3w_pct'] if dm_trends['day_trend_3w_pct'] is not None else 'n/a'}%",
            f"Day change vs 3-month baseline: {dm_trends['day_trend_3m_pct'] if dm_trends['day_trend_3m_pct'] is not None else 'n/a'}%",
        ],
    })

    # Add cards for ALL action types with day/week/month and trend.
    for action_type in sorted(action_type_timestamps.keys()):
        snapshot = _trend_snapshot(action_type_timestamps[action_type], now)
        tone = "teal" if snapshot["day"] > 0 else ""
        if action_type in {"ERROR"} and snapshot["day"] > 0:
            tone = "bad"
        if action_type in {"SAFETY", "BUDGET"} and snapshot["day"] > 0:
            tone = "warn"
        metric_cards.append({
            "id": f"action_{action_type.lower()}",
            "label": f"Action: {action_type}",
            "headline": str(snapshot["day"]),
            "subline": f"day • week {snapshot['week']} • month {snapshot['month']}",
            "tone": tone,
            "details": [
                f"{action_type} today: {snapshot['day']}",
                f"{action_type} this week: {snapshot['week']}",
                f"{action_type} this month: {snapshot['month']}",
                f"Day change vs 3-week baseline: {snapshot['day_trend_3w_pct'] if snapshot['day_trend_3w_pct'] is not None else 'n/a'}%",
                f"Day change vs 3-month baseline: {snapshot['day_trend_3m_pct'] if snapshot['day_trend_3m_pct'] is not None else 'n/a'}%",
            ],
        })

    return jsonify(
        {
            "success": True,
            "timestamp": now.isoformat(),
            "queue": queue_summary,
            "execution": execution_summary,
            "ops": ops_summary,
            "social": social_summary,
            "identities": identities_summary,
            "health": health_summary,
            "metric_cards": metric_cards,
        }
    )


# ═══════════════════════════════════════════════════════════════════
# QUEUE - Add task from UI
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/queue/add', methods=['POST'])
def api_queue_add():
    """Add a task to the queue from UI. Body: { "task_id": "...", "instruction": "..." }."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = (data.get('task_id') or '').strip()
    instruction = (data.get('instruction') or '').strip()
    if not instruction:
        return jsonify({'success': False, 'error': 'instruction is required'}), 400
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    existing_ids = {t.get('id') for t in queue.get('tasks', []) if t.get('id')}
    if not task_id:
        task_id = f"task-{int(time.time() * 1000)}"
    if task_id in existing_ids:
        base = task_id
        suffix = 1
        while f"{base}-{suffix}" in existing_ids:
            suffix += 1
        task_id = f"{base}-{suffix}"
    ui_settings = load_ui_settings()
    override_model = bool(ui_settings.get("override_model"))
    model = str(ui_settings.get("model") or "auto")
    task_model = model if override_model and model != "auto" else None
    min_budget = float(ui_settings.get("task_min_budget", 0.05))
    max_budget = float(ui_settings.get("task_max_budget", max(min_budget, 0.10)))
    if max_budget < min_budget:
        max_budget = min_budget
    task = normalize_task({
        'id': task_id,
        'type': 'cycle',
        'prompt': instruction,
        'min_budget': min_budget,
        'max_budget': max_budget,
        'intensity': 'medium',
        'model': task_model,
        'depends_on': [],
        'parallel_safe': True,
    })
    queue.setdefault('tasks', []).append(task)
    write_json(QUEUE_FILE, normalize_queue(queue))
    return jsonify({'success': True, 'task_id': task_id})


@app.route('/api/queue/update', methods=['POST'])
def api_queue_update():
    """Update an open queue task's id and/or instruction."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get('task_id') or '').strip()
    new_task_id = str(data.get('new_task_id') or '').strip()
    instruction = str(data.get('instruction') or '').strip()
    if not task_id:
        return jsonify({'success': False, 'error': 'task_id is required'}), 400
    if not instruction:
        return jsonify({'success': False, 'error': 'instruction is required'}), 400

    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    tasks = list(queue.get('tasks', []))
    target_idx = None
    for idx, task in enumerate(tasks):
        if str(task.get('id') or '').strip() == task_id:
            target_idx = idx
            break
    if target_idx is None:
        return jsonify({'success': False, 'error': 'task not found in open queue'}), 404

    final_id = new_task_id or task_id
    existing_ids = {
        str(t.get('id') or '').strip()
        for i, t in enumerate(tasks)
        if i != target_idx and str(t.get('id') or '').strip()
    }
    if final_id in existing_ids:
        return jsonify({'success': False, 'error': f'task id already exists: {final_id}'}), 409

    updated = dict(tasks[target_idx])
    updated['id'] = final_id
    updated['prompt'] = instruction
    tasks[target_idx] = normalize_task(updated)
    queue['tasks'] = tasks
    write_json(QUEUE_FILE, normalize_queue(queue))
    return jsonify({'success': True, 'task_id': final_id})


@app.route('/api/queue/delete', methods=['POST'])
def api_queue_delete():
    """Delete a task from open/completed/failed queue collections."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get('task_id') or '').strip()
    if not task_id:
        return jsonify({'success': False, 'error': 'task_id is required'}), 400

    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    removed_from = None
    for section in ('tasks', 'completed', 'failed'):
        items = list(queue.get(section, []))
        new_items = [item for item in items if str(item.get('id') or '').strip() != task_id]
        if len(new_items) != len(items):
            queue[section] = new_items
            removed_from = section
            break
    if not removed_from:
        return jsonify({'success': False, 'error': 'task not found'}), 404

    write_json(QUEUE_FILE, normalize_queue(queue))
    return jsonify({'success': True, 'task_id': task_id, 'removed_from': removed_from})


@app.route('/api/queue/state')
def api_queue_state():
    """Return queue tasks for UI visualization, including tasks pending human approval."""
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    open_tasks = queue.get('tasks', []) if isinstance(queue.get('tasks'), list) else []
    completed = queue.get('completed', []) if isinstance(queue.get('completed'), list) else []
    failed = queue.get('failed', []) if isinstance(queue.get('failed'), list) else []
    # Tasks that are still "open" but have execution status pending_review (need human to click Approve).
    pending_review = []
    for task in open_tasks[:50]:
        tid = task.get('id')
        if not tid:
            continue
        status, last_event = _latest_execution_status(tid)
        if status != 'pending_review':
            continue
        pending_review.append({
            **task,
            'identity_id': last_event.get('identity_id') or last_event.get('worker_id'),
            'result_summary': last_event.get('result_summary'),
            'review_verdict': last_event.get('review_verdict'),
        })
    return jsonify({
        'success': True,
        'open': open_tasks[:50],
        'pending_review': pending_review,
        'completed': completed[-25:],
        'failed': failed[-25:],
    })


# ─── One-time tasks (per identity) ─────────────────────────────────────────

@app.route('/api/one_time_tasks', methods=['GET'])
def api_one_time_tasks_list():
    """List one-time-per-identity task definitions."""
    try:
        from vivarium.runtime.one_time_tasks import get_one_time_tasks, get_completions
        tasks = get_one_time_tasks(WORKSPACE)
        completions = get_completions(WORKSPACE)
        out = []
        for t in tasks:
            tid = t.get("id", "")
            out.append({
                "id": tid,
                "title": t.get("title", tid),
                "prompt": t.get("prompt", ""),
                "bonus_tokens": int(t.get("bonus_tokens", 0)),
                "completions_count": len(completions.get(tid, [])),
            })
        return jsonify({"success": True, "tasks": out})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/one_time_tasks', methods=['POST'])
def api_one_time_tasks_create():
    """Create or update a one-time-per-identity task."""
    data = request.get_json(force=True, silent=True) or {}
    try:
        from vivarium.runtime.one_time_tasks import add_one_time_task
        result = add_one_time_task(WORKSPACE, data)
        if result.get("success"):
            return jsonify(result)
        return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/one_time_tasks/<task_id>', methods=['PATCH'])
def api_one_time_tasks_update(task_id):
    """Update a one-time task (e.g. bonus_tokens)."""
    try:
        from vivarium.runtime.one_time_tasks import update_one_time_task
        data = request.json or {}
        result = update_one_time_task(WORKSPACE, task_id, data)
        if result.get("success"):
            return jsonify(result)
        return jsonify(result), 400 if result.get("error") != "task not found" else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/one_time_tasks/<task_id>', methods=['DELETE'])
def api_one_time_tasks_delete(task_id):
    """Remove a one-time-per-identity task by id."""
    try:
        from vivarium.runtime.one_time_tasks import delete_one_time_task
        result = delete_one_time_task(WORKSPACE, task_id)
        if result.get("success"):
            return jsonify(result)
        return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def _apply_queue_outcome(task_id: str, final_status: str) -> None:
    """Move task from open to completed/failed in queue (used when human approves)."""
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    tasks = list(queue.get("tasks", []))
    task_index = None
    for idx, task in enumerate(tasks):
        if task.get("id") == task_id:
            task_index = idx
            break
    if task_index is None:
        return
    task = dict(tasks.pop(task_index))
    if final_status in ("completed", "approved", "ready_for_merge"):
        task["status"] = "completed"
        queue.setdefault("completed", []).append(task)
    elif final_status == "failed":
        task["status"] = "failed"
        queue.setdefault("failed", []).append(task)
    else:
        task["status"] = "pending" if final_status == "requeue" else final_status
        tasks.insert(task_index, task)
    queue["tasks"] = tasks
    write_json(QUEUE_FILE, normalize_queue(queue))


@app.route('/api/queue/task/approve', methods=['POST'])
def api_queue_task_approve():
    """Human approves a task that is pending_review; reward is granted, optional tip/feedback, task marked completed."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    status, last_event = _latest_execution_status(task_id)
    if status != "pending_review":
        return jsonify({
            "success": False,
            "error": f"Task is not pending approval (status: {status})",
        }), 409
    identity_id = str(last_event.get("identity_id") or last_event.get("worker_id") or "").strip()
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    task = next((t for t in queue.get("tasks", []) if t.get("id") == task_id), None)
    if not task:
        return jsonify({"success": False, "error": "Task not found in queue"}), 404
    tip_tokens = max(0, int(data.get("tip_tokens") or 0))
    feedback = str(data.get("feedback") or "").strip()
    # Append approved event to execution log so state is consistent
    approved_record = {
        "task_id": task_id,
        "status": "approved",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identity_id": identity_id,
        "approved_by": "human_operator",
        "tip_tokens": tip_tokens,
        "feedback_sent": bool(feedback),
    }
    append_jsonl(EXECUTION_LOG, approved_record)
    _apply_queue_outcome(task_id, "approved")
    # Grant completion reward to the resident
    from vivarium.runtime.worker_runtime import apply_phase5_reward_for_human_approval
    reward_out = apply_phase5_reward_for_human_approval(
        task_id=task_id,
        identity_id=identity_id,
        task=task,
        last_event=last_event,
        enrichment=_dm_enrichment(),
    )
    # One-time task bonus: if this task is a one-time task and identity hasn't completed it, grant and record
    one_time_bonus_awarded = 0
    try:
        from vivarium.runtime.one_time_tasks import get_task_by_id, grant_and_record
        if get_task_by_id(task_id, WORKSPACE):
            one_time_result = grant_and_record(
                WORKSPACE,
                task_id,
                identity_id,
                _dm_enrichment(),
            )
            if one_time_result.get("granted"):
                one_time_bonus_awarded = one_time_result.get("tokens", 0)
    except Exception:
        pass
    tip_awarded = 0
    if tip_tokens > 0 and identity_id:
        try:
            tip_result = _dm_enrichment().grant_free_time(
                identity_id, tip_tokens, reason="human_tip_excellence"
            )
            granted = (tip_result or {}).get("granted", {})
            tip_awarded = int(granted.get("free_time", 0)) + int(granted.get("journal", 0))
        except Exception:
            pass
    if feedback and identity_id:
        try:
            human_name = get_human_username()
            _dm_enrichment().post_direct_message(
                sender_id="human_operator",
                sender_name=human_name,
                recipient_id=identity_id,
                content=f"[Feedback on task {task_id}] {feedback}",
                importance=4,
            )
        except Exception:
            pass
    return jsonify({
        "success": True,
        "task_id": task_id,
        "reward_applied": reward_out.get("phase5_reward_applied"),
        "tokens_awarded": reward_out.get("phase5_reward_tokens_awarded", 0),
        "tip_awarded": tip_awarded,
        "one_time_bonus_awarded": one_time_bonus_awarded,
    })


@app.route('/api/queue/task/requeue', methods=['POST'])
def api_queue_task_requeue():
    """Human sends task back for another attempt (try again); task stays in open queue."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    status, last_event = _latest_execution_status(task_id)
    if status != "pending_review":
        return jsonify({
            "success": False,
            "error": f"Task is not pending approval (status: {status})",
        }), 409
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    if not any(t.get("id") == task_id for t in queue.get("tasks", [])):
        return jsonify({"success": False, "error": "Task not found in queue"}), 404
    requeue_record = {
        "task_id": task_id,
        "status": "requeue",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "requested_by": "human_operator",
        "reason": "try_again",
    }
    append_jsonl(EXECUTION_LOG, requeue_record)
    _apply_queue_outcome(task_id, "requeue")
    return jsonify({"success": True, "task_id": task_id})


@app.route('/api/queue/task/remove', methods=['POST'])
def api_queue_task_remove():
    """Human removes task from queue (mark as failed); resident does not get completion reward."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    status, last_event = _latest_execution_status(task_id)
    if status != "pending_review":
        return jsonify({
            "success": False,
            "error": f"Task is not pending approval (status: {status})",
        }), 409
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    if not any(t.get("id") == task_id for t in queue.get("tasks", [])):
        return jsonify({"success": False, "error": "Task not found in queue"}), 404
    remove_record = {
        "task_id": task_id,
        "status": "failed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": "Removed by human operator",
        "removed_by": "human_operator",
    }
    append_jsonl(EXECUTION_LOG, remove_record)
    _apply_queue_outcome(task_id, "failed")
    return jsonify({"success": True, "task_id": task_id})


@app.route('/api/system/fresh_reset', methods=['POST'])
def api_system_fresh_reset():
    """
    Wipe stale runtime state and return system to clean baseline.

    Safety: refuses while swarm is running.
    """
    body = request.get_json(force=True, silent=True) or {}
    worker = get_worker_status()
    if worker.get("running"):
        if bool(body.get("force_stop")):
            stop_result = _stop_workers_for_maintenance()
            if not stop_result.get("success"):
                return jsonify({
                    "success": False,
                    "error": "Could not stop all workers before fresh reset.",
                    "running_count": len(stop_result.get("remaining_pids", [])),
                    "remaining_pids": stop_result.get("remaining_pids", []),
                }), 409
        else:
            return jsonify({
                "success": False,
                "error": "Stop swarm before running fresh reset.",
            }), 409

    try:
        # Reset queue baseline.
        fresh_queue = {
            "version": "1.0",
            "api_endpoint": "http://127.0.0.1:8420",
            "tasks": [],
            "completed": [],
            "failed": [],
        }
        write_json(QUEUE_FILE, fresh_queue)

        # Reset local onboarding trackers used by resident runtime.
        local_swarm_dir = CODE_ROOT / ".swarm"
        local_swarm_dir.mkdir(parents=True, exist_ok=True)
        write_json(local_swarm_dir / "resident_days.json", {})
        write_json(local_swarm_dir / "identity_locks.json", {"cycle_id": 0, "locks": {}})

        # Remove transient mutable files (including mailbox).
        transient_files = [
            MUTABLE_SWARM_DIR / "completed_requests.json",
            MUTABLE_SWARM_DIR / "daily_wind_down_allowance.json",
            MUTABLE_SWARM_DIR / "free_time_balances.json",
            MUTABLE_SWARM_DIR / "human_request.json",
            MUTABLE_SWARM_DIR / "journal_rollups.json",
            MUTABLE_SWARM_DIR / "bounties.json",
            MUTABLE_SWARM_DIR / "guilds.json",
            MUTABLE_SWARM_DIR / "artifact_fingerprints.json",
            MUTABLE_SWARM_DIR / "phase5_reward_ledger.json",
            MUTABLE_SWARM_DIR / "creative_seed_used.json",
            MESSAGES_TO_HUMAN,
            MESSAGES_FROM_HUMAN,
            MESSAGES_FROM_HUMAN_OUTBOX,
            WORKSPACE / ".swarm" / "one_time_tasks.json",
            WORKSPACE / ".swarm" / "one_time_completions.json",
            ACTION_LOG,
            EXECUTION_LOG,
            API_AUDIT_LOG_FILE,
            LEGACY_API_AUDIT_LOG_FILE,
        ]
        for file_path in transient_files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except OSError:
                pass

        # Reset log watcher positions so it re-reads from start when logs are recreated.
        global last_log_position, last_execution_log_position
        last_log_position = 0
        last_execution_log_position = 0

        # Wipe generated directories and recreate.
        wipe_dirs = [
            MUTABLE_SWARM_DIR / "discussions",
            MUTABLE_SWARM_DIR / "journals",
            MUTABLE_SWARM_DIR / "identities",
            WORKSPACE / "library" / "community_library" / "resident_suggestions",
            WORKSPACE / "library" / "creative_works",
        ]
        for directory in wipe_dirs:
            try:
                if directory.exists():
                    shutil.rmtree(directory)
                directory.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass

        return jsonify({"success": True})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


# ═══════════════════════════════════════════════════════════════════
# DIRECT MESSAGES API - Resident-to-resident private channels
# ═══════════════════════════════════════════════════════════════════

def _dm_enrichment():
    from vivarium.runtime.swarm_enrichment import EnrichmentSystem
    return EnrichmentSystem(workspace=WORKSPACE)


def _identity_name_map() -> dict:
    return {item.get("id"): item.get("name") for item in get_identities() if item.get("id")}


@app.route('/api/dm/threads/<identity_id>')
def api_dm_threads(identity_id):
    """List DM threads for one resident identity."""
    ident = str(identity_id or "").strip()
    if not ident:
        return jsonify({'success': False, 'error': 'identity_id required'}), 400
    try:
        threads = _dm_enrichment().get_direct_threads(ident, limit=DM_THREADS_DEFAULT_LIMIT)
        names = _identity_name_map()
        for thread in threads:
            peer_id = thread.get("peer_id")
            if peer_id:
                thread["peer_name"] = names.get(peer_id, peer_id)
        return jsonify({'success': True, 'identity_id': ident, 'threads': threads})
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500


@app.route('/api/dm/messages')
def api_dm_messages():
    """Get DM messages between two identities."""
    identity_id = str(request.args.get("identity_id") or "").strip()
    peer_id = str(request.args.get("peer_id") or "").strip()
    limit = request.args.get("limit", 100, type=int)
    if not identity_id or not peer_id:
        return jsonify({'success': False, 'error': 'identity_id and peer_id required'}), 400
    try:
        messages = _dm_enrichment().get_direct_messages(
            identity_id,
            peer_id,
            limit=_clamp_int(limit, 1, DM_MESSAGES_MAX_LIMIT),
        )
        return jsonify({'success': True, 'identity_id': identity_id, 'peer_id': peer_id, 'messages': messages})
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500


@app.route('/api/dm/send', methods=['POST'])
def api_dm_send():
    """Send a resident-to-resident private DM."""
    data = request.get_json(force=True, silent=True) or {}
    from_id = str(data.get("from_id") or "").strip()
    to_id = str(data.get("to_id") or "").strip()
    content = str(data.get("content") or "").strip()
    if not from_id or not to_id:
        return jsonify({'success': False, 'error': 'from_id and to_id are required'}), 400
    if from_id == to_id:
        return jsonify({'success': False, 'error': 'from_id and to_id must differ'}), 400
    if not content:
        return jsonify({'success': False, 'error': 'content is required'}), 400
    try:
        names = _identity_name_map()
        result = _dm_enrichment().post_direct_message(
            sender_id=from_id,
            sender_name=names.get(from_id, from_id),
            recipient_id=to_id,
            content=content,
            importance=3,
        )
        if not result.get("success"):
            return jsonify({'success': False, 'error': result.get('reason', 'send_failed')}), 400
        return jsonify({'success': True, 'room': result.get('room'), 'message': result.get('message')})
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500


# ═══════════════════════════════════════════════════════════════════
# CHAT ROOMS API - View watercooler, town hall, etc.
# ═══════════════════════════════════════════════════════════════════

# Room display names and icons
ROOM_INFO = {
    'watercooler': {'name': 'Break Room', 'icon': '☕', 'description': 'Casual chat, status updates'},
    'town_hall': {'name': 'Town Hall', 'icon': '🏛️', 'description': 'Proposals, votes, community decisions'},
    'human_async': {'name': 'Human Async', 'icon': '🕰️', 'description': 'Async group chat with the human operator'},
    'improvements': {'name': 'Improvements', 'icon': '💡', 'description': 'System enhancement ideas'},
    'struggles': {'name': 'Struggles', 'icon': '🤔', 'description': 'Challenges and help requests'},
    'discoveries': {'name': 'Discoveries', 'icon': '✨', 'description': 'Interesting findings'},
    'project_war_room': {'name': 'War Room', 'icon': '⚔️', 'description': 'Active project coordination'},
}


@app.route('/api/chatrooms')
def api_get_chatrooms():
    """Get list of available chat rooms with message counts."""
    rooms = []

    if DISCUSSIONS_DIR.exists():
        for room_file in DISCUSSIONS_DIR.glob("*.jsonl"):
            room_name = room_file.stem
            if room_name.startswith('town_hall_') or room_name.startswith('permanent'):
                continue  # Skip archives

            info = ROOM_INFO.get(room_name, {'name': room_name.title(), 'icon': '💬', 'description': ''})

            # Count messages and get latest
            message_count = 0
            latest_timestamp = None
            latest_preview = None

            try:
                with open(room_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    message_count = len([l for l in lines if l.strip()])

                    if lines:
                        for line in reversed(lines):
                            if line.strip():
                                msg = json.loads(line)
                                latest_timestamp = msg.get('timestamp')
                                author = msg.get('author_name', 'Unknown')
                                content = msg.get('content', '') or ''
                                latest_preview = f"{author}: {content}"
                                break
            except:
                pass

            rooms.append({
                'id': room_name,
                'name': info['name'],
                'icon': info['icon'],
                'description': info['description'],
                'message_count': message_count,
                'latest_timestamp': latest_timestamp,
                'latest_preview': latest_preview
            })

    # Sort by latest activity
    rooms.sort(key=lambda r: r.get('latest_timestamp') or '', reverse=True)
    return jsonify({'success': True, 'rooms': rooms})


@app.route('/api/chatrooms/<room_id>')
def api_get_chatroom_messages(room_id):
    """Get messages from a specific chat room."""
    limit = request.args.get('limit', 50, type=int)

    if not DISCUSSIONS_DIR.exists():
        return jsonify({'success': True, 'messages': [], 'room': room_id})

    room_file = DISCUSSIONS_DIR / f"{room_id}.jsonl"
    if not room_file.exists():
        return jsonify({'success': True, 'messages': [], 'room': room_id})

    messages = []
    try:
        with open(room_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    # Return most recent, reverse to show newest last
    info = ROOM_INFO.get(room_id, {'name': room_id.title(), 'icon': '💬', 'description': ''})

    return jsonify({
        'success': True,
        'room': room_id,
        'room_name': info['name'],
        'room_icon': info['icon'],
        'messages': messages[-limit:]
    })


@app.route('/api/logs/recent')
def api_logs_recent():
    """Return a recent tail of action + execution entries for UI backfill."""
    limit = request.args.get('limit', 500, type=int)
    safe_limit = max(1, min(5000, int(limit)))
    action_entries = _read_jsonl_tail(ACTION_LOG, max_lines=safe_limit)
    execution_entries = _read_jsonl_tail(EXECUTION_LOG, max_lines=safe_limit)
    api_audit_entries = _read_api_audit_entries(max_lines=safe_limit)
    mapped_execution = []
    for raw in execution_entries:
        mapped_execution.append(_map_execution_entry_to_log(raw))
    mapped_api_audit = []
    for raw in api_audit_entries:
        mapped_api_audit.append(_map_api_audit_entry_to_log(raw))
    merged = list(action_entries) + mapped_execution + mapped_api_audit
    merged.sort(key=_entry_timestamp_sort_key)
    deduped_entries = []
    seen: set[tuple[str, str, str, str, str, str]] = set()
    for entry in merged:
        dedupe_key = _log_entry_dedupe_key(entry)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        deduped_entries.append(entry)
    trimmed_entries = deduped_entries[-safe_limit:]
    return jsonify({
        'success': True,
        'entries': trimmed_entries,
        'limit': safe_limit,
        'returned': len(trimmed_entries),
        'available': len(deduped_entries),
        'is_truncated': len(deduped_entries) > safe_limit,
    })


@app.route('/api/logs/raw')
def api_logs_raw():
    """Return raw log file content for operator inspection/download."""
    kind = str(request.args.get('kind', 'action') or 'action').strip().lower()
    if kind in {'action', 'actions'}:
        source = ACTION_LOG
    elif kind in {'execution', 'exec'}:
        source = EXECUTION_LOG
    elif kind in {'api', 'audit', 'api_audit'}:
        source = API_AUDIT_LOG_FILE if API_AUDIT_LOG_FILE.exists() else LEGACY_API_AUDIT_LOG_FILE
    else:
        return jsonify({'success': False, 'error': 'kind must be action, execution, or api'}), 400

    if not source.exists():
        return app.response_class("", mimetype="text/plain")
    try:
        raw_text = source.read_text(encoding='utf-8')
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500
    return app.response_class(raw_text, mimetype="text/plain")


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
