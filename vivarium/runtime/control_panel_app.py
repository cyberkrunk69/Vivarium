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
from ipaddress import ip_address
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
from vivarium.utils import read_json, write_json, get_timestamp

ensure_scope_layout()

app = Flask(__name__)
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

# Track last read position
last_log_position = 0

# Centralized policy limits (UI/runtime tuning).
RESIDENT_COUNT_MIN = 1
RESIDENT_COUNT_MAX = 16
HUMAN_USERNAME_MAX_CHARS = 48
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
CREATIVE_SEED_PATTERN = re.compile(r"^[A-Z]{2}-\d{4}-[A-Z]{2}$")
CREATIVE_SEED_USED_FILE = MUTABLE_SWARM_DIR / "creative_seed_used.json"
CREATIVE_SEED_USED_MAX = 5000
API_AUDIT_LOG_FILE = CODE_ROOT / "api_audit.log"
MAILBOX_QUESTS_FILE = MUTABLE_SWARM_DIR / "mailbox_quests.json"
MAILBOX_MESSAGE_BONUS_TOKENS = 8
MAILBOX_REPLY_BONUS_TOKENS = 12
QUEST_DEFAULT_BUDGET = 0.20
QUEST_DEFAULT_UPFRONT_TIP = 10
QUEST_DEFAULT_COMPLETION_REWARD = 30
HOT_RELOAD_ENABLED = (
    os.environ.get("VIVARIUM_HOT_RELOAD", "1").strip().lower()
    not in {"0", "false", "no"}
)


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


def _parse_csv_items(raw: str, *, max_items: int = 10, max_len: int = 64) -> list[str]:
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


def _is_loopback_host(host: str) -> bool:
    value = (host or "").strip().lower()
    if not value:
        return False
    if value in {"localhost", "testclient"}:
        return True
    try:
        return ip_address(value).is_loopback
    except ValueError:
        return False


def _request_source_host() -> str:
    forwarded = (request.headers.get("X-Forwarded-For") or "").strip()
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return (request.remote_addr or "").strip()


@app.before_request
def enforce_localhost_only():
    if _is_loopback_host(_request_source_host()):
        return None
    return jsonify({"success": False, "error": "Control panel is localhost-only"}), 403


@app.after_request
def apply_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


CONTROL_PANEL_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarm Control Panel</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js" crossorigin="anonymous"></script>
    <style>
        :root {
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --bg-hover: #1a1a25;
            --border: #2a2a3a;
            --text: #e0e0e0;
            --text-dim: #888;
            --red: #ff4444;
            --red-glow: rgba(255, 68, 68, 0.3);
            --orange: #ffa500;
            --yellow: #ffd700;
            --green: #44ff44;
            --teal: #00d4d4;
            --blue: #4488ff;
            --purple: #aa44ff;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }

        .title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--teal);
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--green);
            animation: pulse 2s infinite;
        }

        .status-dot.stopped {
            background: var(--red);
            animation: none;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Emergency Stop Button */
        .stop-button {
            background: var(--red);
            color: white;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2px;
            box-shadow: 0 0 20px var(--red-glow);
            transition: all 0.2s;
        }

        .stop-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px var(--red-glow);
        }

        .stop-button:active {
            transform: scale(0.98);
        }

        .stop-button.stopped {
            background: var(--green);
            box-shadow: 0 0 20px rgba(68, 255, 68, 0.3);
        }

        /* Control Buttons Group */
        .control-buttons {
            display: flex;
            gap: 0.5rem;
        }

        .control-btn {
            padding: 0.75rem 1.25rem;
            font-size: 0.9rem;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.2s;
        }

        .control-btn:hover {
            transform: scale(1.03);
        }

        .control-btn:active {
            transform: scale(0.98);
        }

        .control-btn.start {
            background: var(--green);
            color: var(--bg-dark);
        }

        .control-btn.start:disabled {
            background: var(--text-dim);
            cursor: not-allowed;
            transform: none;
        }

        .control-btn.pause {
            background: var(--yellow);
            color: var(--bg-dark);
        }

        .control-btn.pause.paused {
            background: var(--teal);
        }

        .control-btn.stop {
            background: var(--red);
            color: white;
            box-shadow: 0 0 15px var(--red-glow);
        }

        .control-btn.stop.engaged {
            background: var(--green);
            color: var(--bg-dark);
            box-shadow: 0 0 15px rgba(68, 255, 68, 0.3);
        }

        .spawner-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-hover);
            border-radius: 6px;
            font-size: 0.85rem;
        }

        .spawner-status .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--text-dim);
        }

        .spawner-status .dot.running {
            background: var(--green);
            animation: pulse 2s infinite;
        }

        .spawner-status .dot.paused {
            background: var(--yellow);
        }

        .spawner-status .dot.stopped {
            background: var(--red);
        }

        .spawner-status .start-hint {
            margin-left: 0.5rem;
            font-size: 0.75rem;
            color: var(--text-dim);
            max-width: 42em;
        }
        .spawner-status .start-hint code {
            background: var(--bg-dark);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            font-size: 0.7rem;
        }

        .add-task-bar {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }
        .add-task-input {
            padding: 0.4rem 0.6rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--bg-dark);
            color: var(--text);
            font-size: 0.85rem;
        }
        .add-task-input::placeholder { color: var(--text-dim); }
        .add-task-input.add-task-instruction { flex: 1; min-width: 12rem; }
        .add-task-bar .add-task-btn {
            flex-shrink: 0;
            padding: 0.4rem 0.8rem;
            background: var(--teal);
            color: var(--bg-dark);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }
        .add-task-bar .add-task-btn:hover { filter: brightness(1.1); }
.resident-count-control {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    margin-right: 0.5rem;
    color: var(--text-dim);
    font-size: 0.75rem;
}
.resident-count-control input {
    width: 54px;
    padding: 0.25rem 0.35rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--bg-dark);
    color: var(--text);
    font-size: 0.8rem;
}

        .queue-panel {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.6rem;
            padding: 0.6rem 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }
        .queue-column {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.55rem 0.7rem;
            min-height: 120px;
        }
        .queue-column h4 {
            margin: 0 0 0.4rem 0;
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .queue-list {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            font-size: 0.78rem;
            max-height: 180px;
            overflow: auto;
        }
        .queue-item {
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.35rem 0.45rem;
            background: var(--bg-dark);
        }
        .queue-item .qid {
            color: var(--teal);
            font-weight: 600;
        }
        .queue-item .qprompt {
            margin-top: 0.2rem;
            line-height: 1.35;
        }
        .queue-item .qactions {
            display: flex;
            gap: 0.3rem;
            margin-top: 0.3rem;
        }
        .queue-item .qbtn {
            padding: 0.16rem 0.4rem;
            border-radius: 4px;
            border: 1px solid var(--border);
            background: var(--bg-hover);
            color: var(--text);
            font-size: 0.68rem;
            cursor: pointer;
        }
        .queue-item .qbtn.delete {
            background: rgba(255, 68, 68, 0.12);
            border-color: rgba(255, 68, 68, 0.4);
            color: #ff7d7d;
        }
        .queue-empty {
            color: var(--text-dim);
            font-size: 0.75rem;
        }

        .insights-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(170px, 1fr));
            gap: 0.6rem;
            padding: 0.75rem 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }

        .insights-collapsible {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }

        .insights-summary {
            cursor: pointer;
            padding: 0.55rem 1rem;
            list-style: none;
            color: var(--text-dim);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }

        .insights-summary::after {
            content: '▼';
            font-size: 0.65rem;
            transition: transform 0.2s;
        }

        .insights-collapsible[open] .insights-summary::after {
            transform: rotate(180deg);
        }

        .insight-card {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            min-height: 64px;
        }

        .insight-label {
            color: var(--text-dim);
            font-size: 0.65rem;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .insight-value {
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .insight-sub {
            color: var(--text-dim);
            font-size: 0.7rem;
            margin-top: 0.15rem;
        }

        .insight-value.good { color: var(--green); }
        .insight-value.warn { color: var(--yellow); }
        .insight-value.bad { color: var(--red); }
        .insight-value.teal { color: var(--teal); }

        .insight-card summary {
            list-style: none;
            cursor: pointer;
            padding: 0.55rem 0.7rem;
        }
        .insight-card summary::-webkit-details-marker {
            display: none;
        }
        .insight-card summary::after {
            content: '+';
            float: right;
            color: var(--text-dim);
            font-weight: 700;
        }
        .insight-card[open] summary::after {
            content: '−';
        }
        .insight-detail {
            border-top: 1px solid var(--border);
            padding: 0.45rem 0.7rem 0.6rem;
            font-size: 0.72rem;
            color: var(--text-dim);
            line-height: 1.35;
            white-space: pre-line;
        }

        @media (max-width: 1200px) {
            .insights-strip {
                grid-template-columns: repeat(2, minmax(160px, 1fr));
            }
        }

        /* Main Content */
        .main {
            display: flex;
            flex: 1;
            overflow: hidden;
        }

        /* Sidebar - scrollable with collapsible sections */
        .sidebar {
            width: 300px;
            background: var(--bg-card);
            border-right: 1px solid var(--border);
            padding: 1rem;
            overflow-y: auto;
        }

        /* Collapsible section for sidebar */
        .sidebar-section {
            margin-bottom: 0.5rem;
        }

        .sidebar-section summary {
            cursor: pointer;
            padding: 0.5rem;
            background: var(--bg-hover);
            border-radius: 4px;
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            list-style: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .sidebar-section summary::after {
            content: '▼';
            font-size: 0.6rem;
            transition: transform 0.2s;
        }

        .sidebar-section[open] summary::after {
            transform: rotate(180deg);
        }

        .sidebar-section-content {
            padding: 0.5rem 0;
        }

        /* Identities grid/scroll for many identities */
        #identities {
            max-height: calc(100vh - 400px);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .identity-card {
            flex-shrink: 0;
        }

        .sidebar h3 {
            color: var(--text-dim);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1rem;
        }

        .identity-card {
            background: var(--bg-hover);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }

        .identity-name {
            color: var(--teal);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .identity-stat {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-dim);
        }

        .token-count {
            color: var(--yellow);
        }

        /* Log Panel */
        .log-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .log-header {
            padding: 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .log-filters {
            display: flex;
            gap: 0.5rem;
        }

        .filter-btn {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            color: var(--text-dim);
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .filter-btn.active {
            background: var(--teal);
            color: var(--bg-dark);
            border-color: var(--teal);
        }

        .log-container {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            font-size: 0.85rem;
        }

        .log-entry {
            padding: 0.3rem 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            gap: 1rem;
        }
        .log-empty {
            color: var(--text-dim);
            padding: 0.8rem 0.2rem;
            font-size: 0.8rem;
            font-style: italic;
        }

        .log-time {
            color: var(--text-dim);
            min-width: 80px;
        }

        .log-day {
            color: var(--purple);
            min-width: 30px;
        }

        .log-actor {
            color: var(--teal);
            min-width: 100px;
        }

        .log-type {
            min-width: 70px;
            font-weight: 600;
        }

        .log-action {
            color: var(--text-dim);
            min-width: 100px;
        }

        .log-detail {
            flex: 1;
            color: var(--text);
        }

        /* Log type colors */
        .type-TOOL { color: var(--blue); }
        .type-COST, .type-API { color: var(--yellow); }
        .type-SOCIAL, .type-IDENTITY, .type-JOURNAL { color: var(--teal); }
        .type-SAFETY, .type-ERROR { color: var(--red); }
        .type-BUDGET { color: var(--orange); }
        .type-TEST { color: var(--green); }
        .type-SYSTEM { color: var(--purple); }

        /* Budget exceeded / blocked = red */
        .log-entry.danger .log-type,
        .log-entry.danger .log-action {
            color: var(--red) !important;
        }

        /* Footer Stats */
        .footer {
            background: var(--bg-card);
            border-top: 1px solid var(--border);
            padding: 0.5rem 2rem;
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-dim);
        }

        .stat {
            display: flex;
            gap: 0.5rem;
        }

        .stat-value {
            color: var(--text);
        }

        /* Day Vibe Badge */
        .day-vibe {
            background: var(--bg-hover);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .day-vibe.friday { background: linear-gradient(135deg, #ff6b6b, #feca57); color: #1a1a25; }
        .day-vibe.weekend { background: linear-gradient(135deg, #5f27cd, #00d2d3); }
        .day-vibe.monday { background: linear-gradient(135deg, #2d3436, #636e72); }
        .day-vibe.humpday { background: linear-gradient(135deg, #20bf6b, #26de81); color: #1a1a25; }

        /* Slide-out Panel */
        .slideout-toggle {
            position: fixed;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-right: none;
            padding: 1rem 0.5rem;
            cursor: pointer;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            color: var(--text-dim);
            font-size: 0.8rem;
            border-radius: 8px 0 0 8px;
            z-index: 100;
            transition: all 0.2s;
        }

        .slideout-toggle:hover {
            background: var(--bg-hover);
            color: var(--text);
        }

        .slideout-panel {
            position: fixed;
            right: -400px;
            top: 0;
            width: 400px;
            height: 100vh;
            background: var(--bg-card);
            border-left: 1px solid var(--border);
            z-index: 200;
            transition: right 0.3s ease;
            display: flex;
            flex-direction: column;
        }

        .slideout-panel.open {
            right: 0;
        }

        .slideout-header {
            padding: 1rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .slideout-header h3 {
            color: var(--teal);
            margin: 0;
        }

        .slideout-close {
            background: none;
            border: none;
            color: var(--text-dim);
            font-size: 1.5rem;
            cursor: pointer;
        }

        .slideout-content {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }

        .completed-request {
            background: var(--bg-hover);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 3px solid var(--green);
        }

        .completed-request .request-text {
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        .completed-request .request-meta {
            font-size: 0.75rem;
            color: var(--text-dim);
            display: flex;
            justify-content: space-between;
        }

        .slideout-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 150;
            display: none;
        }

        .slideout-overlay.open {
            display: block;
        }

        .chat-room-card {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.55rem;
            margin-bottom: 0.5rem;
        }

        .chat-room-card-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .chat-room-open-btn {
            background: var(--teal);
            color: var(--bg-dark);
            border: none;
            border-radius: 6px;
            padding: 0.25rem 0.55rem;
            cursor: pointer;
            font-size: 0.72rem;
            font-weight: 700;
        }

        .chatroom-modal {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.82);
            z-index: 1200;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .chatroom-modal.open {
            display: flex;
        }

        .chatroom-modal-panel {
            width: min(1100px, 96vw);
            height: min(840px, 88vh);
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chatroom-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border);
        }

        .chatroom-modal-meta {
            font-size: 0.75rem;
            color: var(--text-dim);
            padding: 0.4rem 1rem;
            border-bottom: 1px solid var(--border);
        }

        .chatroom-modal-messages {
            flex: 1;
            overflow-y: auto;
            padding: 0.8rem 1rem;
        }

        .chat-msg {
            background: var(--bg-hover);
            border-radius: 8px;
            padding: 0.6rem;
            margin-bottom: 0.55rem;
            border-left: 3px solid var(--teal);
        }

        .mailbox-launcher {
            background: var(--bg-hover);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.35rem 0.65rem;
            cursor: pointer;
            font-size: 0.78rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }

        .mailbox-badge {
            min-width: 1.1rem;
            height: 1.1rem;
            border-radius: 999px;
            background: var(--red);
            color: #fff;
            font-size: 0.65rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0 0.25rem;
            opacity: 0;
            transform: scale(0.9);
            transition: opacity 120ms ease, transform 120ms ease;
        }

        .mailbox-badge.show {
            opacity: 1;
            transform: scale(1);
            animation: mailboxPulse 1.2s ease-in-out infinite;
        }

        @keyframes mailboxPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.12); }
            100% { transform: scale(1); }
        }

        .mailbox-modal {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.82);
            z-index: 1300;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .mailbox-modal.open {
            display: flex;
        }

        .mailbox-phone {
            width: min(460px, 96vw);
            height: min(840px, 90vh);
            background: linear-gradient(180deg, #151a20 0%, #0f1318 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .mailbox-head {
            padding: 0.7rem 0.85rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .mailbox-threads {
            padding: 0.6rem 0.75rem;
            border-bottom: 1px solid var(--border);
            max-height: 190px;
            overflow-y: auto;
        }

        .mailbox-thread-item {
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-card);
            padding: 0.45rem 0.5rem;
            cursor: pointer;
            margin-bottom: 0.35rem;
        }

        .mailbox-thread-item.active {
            border-color: var(--teal);
            background: rgba(3, 218, 198, 0.09);
        }

        .mailbox-messages {
            flex: 1;
            overflow-y: auto;
            padding: 0.7rem 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }

        .mailbox-msg {
            max-width: 88%;
            border-radius: 10px;
            padding: 0.45rem 0.55rem;
            font-size: 0.82rem;
            line-height: 1.35;
            border: 1px solid var(--border);
        }

        .mailbox-msg.in {
            align-self: flex-start;
            background: var(--bg-card);
        }

        .mailbox-msg.out {
            align-self: flex-end;
            background: rgba(3, 218, 198, 0.12);
            border-color: rgba(3, 218, 198, 0.35);
        }

        .mailbox-compose {
            border-top: 1px solid var(--border);
            padding: 0.65rem 0.75rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">SWARM CONTROL PANEL</div>
        <div class="day-vibe" id="dayVibe">
            <span id="dayVibeIcon">*</span>
            <span id="dayVibeText">Loading...</span>
        </div>
        <div class="spawner-status">
            <div class="dot" id="workerDot"></div>
            <span id="workerStatus">Swarm: —</span>
        </div>
        <div class="control-buttons">
            <label class="resident-count-control" title="How many residents run in parallel">
                Active residents
                <input type="number" id="residentCount" min="1" max="16" step="1" value="1" onchange="persistUiSettings()">
            </label>
            <button class="mailbox-launcher" id="mailboxLauncher" onclick="openMailboxModal()" title="Open communication mailbox">
                <span>📬</span>
                <span>Mailbox</span>
                <span id="mailboxUnreadBadge" class="mailbox-badge">0</span>
            </button>
            <button class="control-btn start" id="workerStartBtn" onclick="startWorker()">Start swarm</button>
            <button class="control-btn stop" id="workerStopBtn" onclick="stopWorker()" style="display:none;">Stop swarm</button>
            <button class="control-btn pause" id="pauseBtn" onclick="togglePause()" disabled style="display:none;">DISABLED</button>
            <button class="control-btn stop" id="stopBtn" onclick="toggleStop()">HALT</button>
        </div>
    </div>

    <div class="add-task-bar">
        <input type="text" id="addTaskId" placeholder="Task ID (e.g. task-001)" class="add-task-input" />
        <input type="text" id="addTaskInstruction" placeholder="Instruction (e.g. Draft a docs improvement proposal)" class="add-task-input add-task-instruction" />
        <button type="button" class="control-btn add-task-btn" onclick="addTaskFromUI()">Add task</button>
    </div>

    <div class="queue-panel">
        <div class="queue-column">
            <h4>Open Queue</h4>
            <div id="queueOpenList" class="queue-list"><div class="queue-empty">No open tasks</div></div>
        </div>
        <div class="queue-column">
            <h4>Recent Completed</h4>
            <div id="queueCompletedList" class="queue-list"><div class="queue-empty">No completed tasks yet</div></div>
        </div>
        <div class="queue-column">
            <h4>Recent Failed</h4>
            <div id="queueFailedList" class="queue-list"><div class="queue-empty">No failed tasks</div></div>
        </div>
    </div>

    <details class="insights-collapsible">
        <summary class="insights-summary">Stats</summary>
        <div class="insights-strip" id="insightCards">
            <details class="insight-card" open>
                <summary>
                    <div class="insight-label">Loading</div>
                    <div class="insight-value">--</div>
                    <div class="insight-sub">Fetching metrics…</div>
                </summary>
                <div class="insight-detail">Insights API is loading.</div>
            </details>
        </div>
    </details>

    <!-- Slide-out toggle button -->
    <div class="slideout-toggle" onclick="toggleSlideout()">
        Completed Requests
    </div>

    <!-- Slide-out overlay -->
    <div class="slideout-overlay" id="slideoutOverlay" onclick="toggleSlideout()"></div>

    <!-- Slide-out panel -->
    <div class="slideout-panel" id="slideoutPanel">
        <div class="slideout-header">
            <h3>Completed Requests</h3>
            <button class="slideout-close" onclick="toggleSlideout()">&times;</button>
        </div>
        <div class="slideout-content" id="completedRequestsContainer">
            <p style="color: var(--text-dim);">No completed requests yet</p>
        </div>
    </div>

    <div class="main">
        <div class="sidebar">
            <!-- Identities Section - Always visible, scrollable -->
            <h3 style="display: flex; align-items: center; justify-content: space-between;">
                <span>Identities</span>
                <span id="identityCount" style="font-size: 0.7rem; color: var(--text-dim); font-weight: normal;"></span>
            </h3>
            <div id="identities">
                <!-- Populated by JS -->
            </div>

            <!-- Collapsible: Collaboration Request -->
            <details class="sidebar-section" open>
                <summary>
                    Collaboration Request
                    <span id="requestActiveIndicator" style="display: none; font-size: 0.65rem; padding: 0.1rem 0.3rem;
                          background: rgba(76, 175, 80, 0.2); color: var(--green); border-radius: 4px;">
                        ACTIVE
                    </span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card" style="margin-bottom: 0;">
                        <label style="font-size: 0.7rem; color: var(--text-dim); display: block; margin-bottom: 0.25rem;">
                            Human username (shown to residents)
                        </label>
                        <input type="text" id="humanUsername" value="human" maxlength="48" onchange="persistUiSettings()"
                            placeholder="human"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.35rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.78rem;">
                        <textarea id="humanRequest"
                            placeholder="What should we work on together?"
                            style="width: 100%; height: 60px; background: var(--bg-dark); border: 1px solid var(--border);
                                   color: var(--text); padding: 0.5rem; border-radius: 4px; font-family: inherit;
                                   font-size: 0.8rem; resize: vertical;"></textarea>
                        <div style="display: flex; gap: 0.3rem; margin-top: 0.3rem;">
                            <button onclick="saveRequest()"
                                style="flex: 1; padding: 0.3rem; background: var(--teal);
                                       border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer;
                                       font-weight: 600; font-size: 0.75rem;">
                                Update
                            </button>
                            <button onclick="markRequestComplete()"
                                style="padding: 0.3rem 0.5rem; background: var(--green);
                                       border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer;
                                       font-weight: 600; font-size: 0.75rem;">
                                Done
                            </button>
                        </div>
                        <div id="requestStatus" style="font-size: 0.65rem; color: var(--green); margin-top: 0.2rem; text-align: center;"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Budget & Scaling -->
            <details class="sidebar-section">
                <summary>Budget & Model</summary>
                <div class="sidebar-section-content">
            <div class="identity-card">
                <div class="identity-stat">
                    <span>Daily Budget</span>
                    <span class="stat-value" id="sessionBudget">$0.05</span>
                </div>
                <div class="identity-stat">
                    <span>Total Spent</span>
                    <span class="stat-value" id="totalSpent">$0.00</span>
                </div>

                <!-- Model Selector with Auto Mode -->
                <div style="margin-top: 1rem; border-top: 1px solid var(--border); padding-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <label style="font-size: 0.8rem; color: var(--text-dim);">Model:</label>
                        <span id="autoModelIndicator" style="font-size: 0.7rem; padding: 0.1rem 0.4rem;
                              background: rgba(76, 175, 80, 0.2); color: var(--green); border-radius: 4px;">
                            AUTO
                        </span>
                    </div>
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-size: 0.8rem; margin-bottom: 0.5rem;">
                        <input type="checkbox" id="overrideModelToggle" onchange="toggleModelOverride()">
                        <span style="color: var(--text-dim);">Override auto-select</span>
                    </label>
                    <select id="modelSelector" onchange="updateModel(this.value)" disabled
                            style="width: 100%; padding: 0.4rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text-dim); border-radius: 4px;
                                   font-size: 0.85rem; cursor: not-allowed; opacity: 0.6;">
                        <option value="auto">Auto (by complexity)</option>
                        <option value="llama-3.1-8b-instant">Llama 3.1 8B (Fast/Simple)</option>
                        <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Standard)</option>
                        <option value="deepseek-r1-distill-llama-70b">DeepSeek R1 70B (Reasoning)</option>
                        <option value="qwen-qwq-32b">Qwen QwQ 32B (Reasoning)</option>
                        <option value="meta-llama/llama-4-maverick-17b-128e-instruct">Llama 4 Maverick (Preview)</option>
                    </select>
                    <p id="modelDescription" style="font-size: 0.65rem; color: var(--green); margin-top: 0.3rem;">
                        Smallest model for each task complexity
                    </p>
                </div>

                <!-- Runtime pace -->
                <div id="manualScaleControls" style="margin-top: 0.75rem;">
                    <label style="font-size: 0.8rem; color: var(--text-dim);">Audit Pace (seconds): <span id="sessionCount" style="color: var(--teal);">2</span>s</label>
                    <input type="range" id="sessionSlider" min="0" max="120" value="2" step="1"
                           oninput="updateSessionCount(this.value)"
                           style="width: 100%; margin-top: 0.3rem; accent-color: var(--teal);">
                    <p style="font-size: 0.7rem; color: var(--text-dim); margin-top: 0.3rem;">
                        Wait between queue checks in the worker loop (human-auditable pace)
                    </p>
                </div>

                <!-- Task budget defaults -->
                <div id="autoScaleControls" style="display: block; margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.25rem;">
                        New Task Budget Defaults
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <label style="font-size: 0.75rem; color: var(--text-dim);">
                            Min $
                            <input type="number" id="taskMinBudget" value="0.05"
                                   step="0.01" min="0.00" onchange="updateBudgetLimit(this.value)"
                                   style="width: 70px; padding: 0.2rem; background: var(--bg-dark);
                                          border: 1px solid var(--border); color: var(--yellow);
                                          border-radius: 4px; font-size: 0.85rem;">
                        </label>
                        <label style="font-size: 0.75rem; color: var(--text-dim);">
                            Max $
                            <input type="number" id="taskMaxBudget" value="0.10"
                                   step="0.01" min="0.00" onchange="updateBudgetLimit(this.value)"
                                   style="width: 70px; padding: 0.2rem; background: var(--bg-dark);
                                          border: 1px solid var(--border); color: var(--yellow);
                                          border-radius: 4px; font-size: 0.85rem;">
                        </label>
                    </div>
                    <p style="font-size: 0.7rem; color: var(--text-dim); margin-top: 0.3rem;">
                        Applied automatically to tasks created from Add Task and Collaboration Request.
                    </p>
                </div>

                <button onclick="saveRuntimeSpeed()"
                    style="margin-top: 0.75rem; width: 100%; padding: 0.3rem; background: var(--bg-hover);
                           border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                           cursor: pointer; font-size: 0.75rem;">
                    Save Runtime + Budget Defaults
                </button>
                <div id="runtimeSpeedStatus" style="font-size: 0.65rem; color: var(--green); margin-top: 0.3rem; text-align: center;"></div>
            </div>
                </div>
            </details>

            <!-- Collapsible: Groq API Key -->
            <details class="sidebar-section">
                <summary>
                    Groq API
                    <span id="groqKeyBadge" style="font-size: 0.65rem; color: var(--text-dim);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.4rem;">
                            Attach your own Groq key for live LLM calls.
                        </div>
                        <input type="password" id="groqApiKeyInput" placeholder="gsk_..."
                            style="width: 100%; padding: 0.35rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                                   font-size: 0.8rem; margin-bottom: 0.35rem;">
                        <div style="display: flex; gap: 0.35rem;">
                            <button onclick="saveGroqApiKey()"
                                style="flex: 1; padding: 0.3rem; background: var(--teal); border: none;
                                       color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                                Save Key
                            </button>
                            <button onclick="clearGroqApiKey()"
                                style="padding: 0.3rem 0.5rem; background: var(--bg-hover); border: 1px solid var(--border);
                                       color: var(--text); border-radius: 4px; cursor: pointer; font-size: 0.72rem;">
                                Clear
                            </button>
                        </div>
                        <div id="groqKeyStatus" style="font-size: 0.65rem; margin-top: 0.35rem; color: var(--text-dim);"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Time Rollback -->
            <details class="sidebar-section">
                <summary>
                    Time Rollback
                    <span id="rollbackBadge" style="font-size: 0.65rem; color: var(--orange);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.68rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                            Rewind mutable world state to a checkpoint from N day(s) ago.
                            This affects queue/artifacts/state under mutable scope.
                        </div>
                        <div style="display: flex; gap: 0.35rem; align-items: center; margin-bottom: 0.35rem;">
                            <input type="number" id="rollbackDays" min="1" max="180" value="1"
                                style="width: 86px; padding: 0.28rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.78rem;">
                            <button onclick="previewRollbackByDays()"
                                style="flex: 1; padding: 0.28rem; background: var(--bg-hover); border: 1px solid var(--border);
                                       color: var(--text); border-radius: 4px; cursor: pointer; font-size: 0.75rem;">
                                Preview
                            </button>
                            <button onclick="runRollbackByDays()"
                                style="padding: 0.28rem 0.45rem; background: var(--red); border: none;
                                       color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                                Rollback
                            </button>
                        </div>
                        <div id="rollbackStatus" style="font-size: 0.65rem; color: var(--text-dim); margin-bottom: 0.3rem;"></div>
                        <div id="rollbackPreview" style="max-height: 140px; overflow-y: auto; font-size: 0.7rem; color: var(--text-dim);"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Fresh Reset -->
            <details class="sidebar-section">
                <summary>Fresh Reset</summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.68rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                            Wipe stale runtime state (queue/logs/generated artifacts/transient swarm files) and reset to a clean slate.
                        </div>
                        <button onclick="runFreshStateReset()"
                            style="width: 100%; padding: 0.32rem; background: var(--red); border: none;
                                   color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                            Wipe stale runtime state
                        </button>
                        <div id="freshResetStatus" style="font-size: 0.65rem; color: var(--text-dim); margin-top: 0.35rem;"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Identity Forge -->
            <details class="sidebar-section">
                <summary>Identity Forge</summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                            Resident-driven identity creation. No preset names.
                            Inspiration is fine; exact copying of examples/other identities is not.
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.35rem; margin-bottom: 0.3rem;">
                            <span style="font-size: 0.68rem; color: var(--text-dim);">Fresh creativity seed:</span>
                            <code id="creativeSeedValue" style="font-size: 0.75rem; color: var(--yellow); background: var(--bg-dark); padding: 0.12rem 0.35rem; border-radius: 4px;">--</code>
                            <button type="button" onclick="refreshCreativeSeed()"
                                style="margin-left: auto; padding: 0.2rem 0.45rem; background: var(--bg-hover); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.7rem; cursor: pointer;">
                                New
                            </button>
                        </div>
                        <select id="identityCreatorSelect"
                            style="width: 100%; padding: 0.32rem; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.78rem;">
                            <option value="">Creator identity (optional)</option>
                        </select>
                        <input type="text" id="newIdentityName" placeholder="Name (self-chosen)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.8rem;">
                        <textarea id="newIdentitySummary" placeholder="Creative identity spark / summary"
                            style="width: 100%; height: 56px; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                                   padding: 0.35rem; font-size: 0.78rem; resize: vertical;"></textarea>
                        <input type="text" id="newIdentityTraits" placeholder="Traits (comma-separated)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.25rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                        <input type="text" id="newIdentityValues" placeholder="Values (comma-separated)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.25rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                        <input type="text" id="newIdentityActivities" placeholder="Preferred activities (comma-separated)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                        <button onclick="createResidentIdentity()"
                            style="width: 100%; padding: 0.3rem; background: var(--purple); border: none;
                                   color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                            Create Identity
                        </button>
                        <div id="identityCreateStatus" style="font-size: 0.65rem; margin-top: 0.35rem; color: var(--text-dim);"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Messages -->
            <details class="sidebar-section">
                <summary>
                    Messages
                    <span id="messageCount" style="font-size: 0.65rem; color: var(--teal);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div id="messagesContainer" style="max-height: 250px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">No messages yet</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Direct Messages -->
            <details class="sidebar-section">
                <summary>
                    Direct Messages
                    <span id="dmThreadCount" style="font-size: 0.65rem; color: var(--purple);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card" style="margin-bottom: 0.5rem;">
                        <div style="display: flex; gap: 0.35rem; margin-bottom: 0.3rem;">
                            <select id="dmFromIdentity"
                                style="flex: 1; padding: 0.32rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;"
                                onchange="loadDmThreads()">
                                <option value="">From identity</option>
                            </select>
                            <select id="dmToIdentity"
                                style="flex: 1; padding: 0.32rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                                <option value="">To identity</option>
                            </select>
                        </div>
                        <textarea id="dmMessageInput" placeholder="Private message..."
                            style="width: 100%; height: 52px; background: var(--bg-dark); border: 1px solid var(--border);
                                   color: var(--text); padding: 0.35rem; border-radius: 4px; font-size: 0.75rem; resize: vertical;"></textarea>
                        <button onclick="sendDirectMessage()"
                            style="margin-top: 0.35rem; width: 100%; padding: 0.3rem; background: var(--purple); border: none;
                                   color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                            Send DM
                        </button>
                        <div id="dmStatus" style="font-size: 0.65rem; margin-top: 0.35rem; color: var(--text-dim);"></div>
                    </div>
                    <div id="dmThreadsContainer" style="max-height: 170px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.72rem;">No DM threads yet</p>
                    </div>
                    <div id="dmConversationContainer" style="max-height: 220px; overflow-y: auto; margin-top: 0.35rem;">
                        <p style="color: var(--text-dim); font-size: 0.72rem;">Select a DM thread to view messages</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Chat Rooms -->
            <details class="sidebar-section">
                <summary>
                    Chat Rooms
                    <span id="chatRoomsCount" style="font-size: 0.65rem; color: var(--teal);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                        Open any room in a large popout for easier monitoring.
                    </div>
                    <div id="chatRoomsContainer" style="max-height: 300px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">Loading rooms...</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Recent Artifacts -->
            <details class="sidebar-section">
                <summary>
                    Artifacts
                    <span id="artifactCount" style="font-size: 0.65rem; color: var(--purple);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div id="artifactsContainer" style="max-height: 220px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">No artifacts yet</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Commons Crucible -->
            <details class="sidebar-section">
                <summary>
                    Commons Crucible
                    <span id="bountyCount" style="font-size: 0.65rem; color: var(--yellow);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card" style="margin-bottom: 0.5rem;">
                        <div style="font-size: 0.65rem; color: var(--text-dim); margin-bottom: 0.3rem;">
                            PVP/coop arena. Slots fill fast; overflow rewards decay sharply.
                        </div>
                        <input type="text" id="bountyTitle" placeholder="Challenge title..."
                            style="width: 100%; padding: 0.25rem; margin-bottom: 0.2rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.8rem;">
                        <textarea id="bountyDesc" placeholder="Objective and success criteria..."
                            style="width: 100%; height: 40px; background: var(--bg-dark); border: 1px solid var(--border);
                                   color: var(--text); padding: 0.25rem; border-radius: 4px; font-size: 0.75rem; resize: none;"></textarea>
                        <div style="display: flex; gap: 0.3rem; margin-top: 0.2rem; align-items: center;">
                            <input type="number" id="bountyReward" placeholder="Tokens" min="10" value="50"
                                style="width: 50px; padding: 0.2rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--yellow); border-radius: 4px; font-size: 0.75rem;"
                                title="Token reward">
                            <select id="bountyMode"
                                style="width: 62px; padding: 0.2rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.65rem;"
                                title="Mode">
                                <option value="hybrid" selected>Hybrid</option>
                                <option value="pvp">PVP</option>
                                <option value="coop">Coop</option>
                            </select>
                            <input type="number" id="bountyMaxTeams" placeholder="Guild slots" min="1" max="8" value="2"
                                style="width: 40px; padding: 0.2rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--teal); border-radius: 4px; font-size: 0.75rem;"
                                title="Guild slots with full rewards">
                            <button onclick="createBounty()"
                                style="flex: 1; padding: 0.25rem; background: var(--yellow); border: none;
                                       color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 0.7rem;">
                                Post
                            </button>
                        </div>
                    </div>
                    <div id="bountiesContainer" style="max-height: 200px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.7rem;">No active bounties</p>
                    </div>
                </div>
            </details>
        </div>

        <div class="log-panel">
            <div class="log-header">
                <span>Action Log</span>
                <div class="log-filters">
                    <button class="filter-btn active" data-filter="all">All</button>
                    <button class="filter-btn" data-filter="TOOL">Tools</button>
                    <button class="filter-btn" data-filter="API">API</button>
                    <button class="filter-btn" data-filter="SAFETY">Safety</button>
                    <button class="filter-btn" data-filter="SOCIAL">Social</button>
                    <button class="filter-btn" data-filter="JOURNAL">Journal</button>
                    <button class="filter-btn" data-filter="IDENTITY">Identity</button>
                </div>
            </div>
            <div class="log-container" id="logContainer">
                <div id="logEmptyState" class="log-empty">Waiting for log entries...</div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="stat">
            <span>Entries:</span>
            <span class="stat-value" id="entryCount">0</span>
        </div>
        <div class="stat">
            <span>Connected:</span>
            <span class="stat-value" id="connectedTime">0s</span>
        </div>
        <div class="stat">
            <span>Last Update:</span>
            <span class="stat-value" id="lastUpdate">--:--:--</span>
        </div>
    </div>

    <div id="chatRoomModal" class="chatroom-modal" onclick="handleChatRoomModalBackdrop(event)">
        <div class="chatroom-modal-panel">
            <div class="chatroom-modal-header">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span id="chatRoomModalIcon" style="font-size: 1.2rem;">💬</span>
                    <div>
                        <div id="chatRoomModalTitle" style="font-size: 1rem; font-weight: 700; color: var(--teal);">Chat Room</div>
                        <div id="chatRoomModalSubtitle" style="font-size: 0.72rem; color: var(--text-dim);">Live room feed</div>
                    </div>
                </div>
                <button class="chat-room-open-btn" style="background: var(--red); color: white;" onclick="closeChatRoomModal()">Close</button>
            </div>
            <div id="chatRoomModalMeta" class="chatroom-modal-meta">Loading room…</div>
            <div id="chatRoomModalMessages" class="chatroom-modal-messages">
                <p style="color: var(--text-dim); font-size: 0.8rem;">Loading messages...</p>
            </div>
        </div>
    </div>

    <div id="mailboxModal" class="mailbox-modal" onclick="handleMailboxBackdrop(event)">
        <div class="mailbox-phone">
            <div class="mailbox-head">
                <div>
                    <div style="font-size: 0.95rem; color: var(--teal); font-weight: 700;">Communication Mailbox</div>
                    <div id="mailboxSubhead" style="font-size: 0.68rem; color: var(--text-dim);">Phone-style async chat</div>
                </div>
                <button class="chat-room-open-btn" style="background: var(--red); color: white;" onclick="closeMailboxModal()">Close</button>
            </div>
            <div id="mailboxThreads" class="mailbox-threads">
                <p style="color: var(--text-dim); font-size: 0.75rem;">Loading threads...</p>
            </div>
            <div id="mailboxMessages" class="mailbox-messages">
                <p style="color: var(--text-dim); font-size: 0.75rem;">Select a thread to start chatting.</p>
            </div>
            <div class="mailbox-compose">
                <div style="display: flex; gap: 0.4rem; margin-bottom: 0.35rem;">
                    <select id="mailboxTarget" style="flex: 1; padding: 0.32rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px; font-size: 0.74rem;">
                        <option value="">Target resident (optional)</option>
                    </select>
                    <button class="chat-room-open-btn" onclick="sendMailboxMessage()">Send</button>
                </div>
                <textarea id="mailboxComposer" placeholder="Send message to a resident (or broadcast if target is blank)..."
                    style="width: 100%; height: 72px; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); padding: 0.45rem; border-radius: 6px; font-size: 0.78rem; resize: vertical;"></textarea>
                <div style="margin-top: 0.55rem; padding-top: 0.55rem; border-top: 1px dashed var(--border);">
                    <div style="font-size: 0.72rem; color: var(--yellow); margin-bottom: 0.25rem;">Assign Quest</div>
                    <input id="questTitleInput" type="text" placeholder="Quest title"
                        style="width: 100%; margin-bottom: 0.25rem; padding: 0.34rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px; font-size: 0.73rem;">
                    <textarea id="questPromptInput" placeholder="Quest objective for selected resident..."
                        style="width: 100%; height: 60px; margin-bottom: 0.3rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); padding: 0.4rem; border-radius: 6px; font-size: 0.75rem; resize: vertical;"></textarea>
                    <div style="display:flex; gap:0.35rem; margin-bottom:0.3rem;">
                        <input id="questBudgetInput" type="number" min="0.01" step="0.01" value="0.20"
                            title="Quest token budget ($)" style="width:33%; padding:0.32rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:5px; font-size:0.72rem;">
                        <input id="questTipInput" type="number" min="0" step="1" value="10"
                            title="Upfront free-time tip tokens" style="width:33%; padding:0.32rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:5px; font-size:0.72rem;">
                        <input id="questRewardInput" type="number" min="0" step="1" value="30"
                            title="Completion reward tokens (manual approval)" style="width:34%; padding:0.32rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:5px; font-size:0.72rem;">
                    </div>
                    <button class="chat-room-open-btn" style="width:100%;" onclick="createMailboxQuest()">Assign Quest</button>
                    <div id="questStatus" style="font-size: 0.68rem; color: var(--text-dim); margin-top: 0.25rem;"></div>
                    <div id="questProgressContainer" style="max-height: 150px; overflow-y: auto; margin-top: 0.4rem;"></div>
                </div>
                <div id="mailboxStatus" style="font-size: 0.68rem; color: var(--text-dim); margin-top: 0.3rem;"></div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let entryCount = 0;
        let isStopped = false;
        let connectedAt = Date.now();
        let currentFilter = 'all';
        const seenLogKeys = new Set();
        let mailboxData = { threads: [], thread_messages: {}, identities: [], unread_count: 0 };
        let activeMailboxThreadId = null;
        let mailboxPoller = null;
        let mailboxQuests = [];

        // Update connected time
        setInterval(() => {
            const secs = Math.floor((Date.now() - connectedAt) / 1000);
            document.getElementById('connectedTime').textContent = `${secs}s`;
        }, 1000);

        // Socket events
        socket.on('connect', () => {
            console.log('Connected to control panel');
            loadRecentLogs();
            loadWorkerStatus();
            loadStopStatus();
            loadRuntimeSpeed();
            loadGroqKeyStatus();
            loadSwarmInsights();
            loadMailboxData();
            previewRollbackByDays();
        });

        socket.on('disconnect', () => {
            console.log('Disconnected');
            const dot = document.getElementById('workerDot');
            if (dot) dot.classList.add('stopped');
        });

        socket.on('log_entry', (entry) => {
            addLogEntry(entry);
        });

        socket.on('identities', (data) => {
            updateIdentities(data);
        });

        socket.on('spawner_started', () => { refreshWorkerStatus(); });
        socket.on('spawner_paused', () => { refreshWorkerStatus(); });
        socket.on('spawner_resumed', () => { refreshWorkerStatus(); });
        socket.on('spawner_killed', () => { refreshWorkerStatus(); });

        socket.on('stop_status', (data) => {
            isStopped = !!(data && data.stopped);
            updateKillSwitchUI();
        });

        function addLogEntry(entry) {
            const entryKey = [
                entry.timestamp || '',
                entry.actor || '',
                entry.action_type || '',
                entry.action || '',
                entry.detail || '',
            ].join('|');
            if (seenLogKeys.has(entryKey)) {
                return;
            }
            seenLogKeys.add(entryKey);

            const container = document.getElementById('logContainer');
            const emptyEl = document.getElementById('logEmptyState');
            if (emptyEl) emptyEl.style.display = 'none';
            const div = document.createElement('div');
            div.className = 'log-entry';
            div.dataset.type = entry.action_type;

            // Check for danger conditions
            if (entry.action_type === 'SAFETY' && entry.action.includes('BLOCKED')) {
                div.classList.add('danger');
            }
            if (entry.action_type === 'BUDGET' && entry.action.includes('EXCEEDED')) {
                div.classList.add('danger');
            }
            if (entry.action_type === 'ERROR') {
                div.classList.add('danger');
            }

            // Parse timestamp
            let timeStr = '--:--:--';
            let dayStr = '---';
            if (entry.timestamp) {
                const dt = new Date(entry.timestamp);
                timeStr = dt.toTimeString().split(' ')[0];
                dayStr = dt.toLocaleDateString('en-US', { weekday: 'short' });
            }

            // Make file paths clickable in detail
            const linkedDetail = linkifyFilePaths(entry.detail || '');

            div.innerHTML = `
                <span class="log-time">${timeStr}</span>
                <span class="log-day">${dayStr}</span>
                <span class="log-actor">${entry.actor || 'UNKNOWN'}</span>
                <span class="log-type type-${entry.action_type}">${entry.action_type}</span>
                <span class="log-action">${entry.action}</span>
                <span class="log-detail">${linkedDetail}</span>
            `;

            // Apply filter
            if (currentFilter !== 'all' && entry.action_type !== currentFilter) {
                div.style.display = 'none';
            }

            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
            applyLogFilter();
            updateLogEmptyState();

            entryCount++;
            document.getElementById('entryCount').textContent = entryCount;
            document.getElementById('lastUpdate').textContent = timeStr;
        }

        function loadRecentLogs() {
            fetch('/api/logs/recent?limit=500')
                .then(r => r.json())
                .then(data => {
                    if (!data || !data.success) return;
                    const entries = Array.isArray(data.entries) ? data.entries : [];
                    entries.forEach(entry => addLogEntry(entry));
                    applyLogFilter();
                    updateLogEmptyState();
                })
                .catch(() => {});
        }

        function updateLogEmptyState() {
            const container = document.getElementById('logContainer');
            const emptyEl = document.getElementById('logEmptyState');
            if (!container || !emptyEl) return;
            const visibleEntries = Array.from(container.querySelectorAll('.log-entry'))
                .filter(el => el.style.display !== 'none');
            if (visibleEntries.length > 0) {
                emptyEl.style.display = 'none';
                return;
            }
            const labels = {
                all: 'No log entries yet.',
                TOOL: 'No TOOL log entries yet.',
                API: 'No API log entries yet.',
                SAFETY: 'No SAFETY log entries yet.',
                SOCIAL: 'No SOCIAL log entries yet.',
                JOURNAL: 'No JOURNAL log entries yet.',
                IDENTITY: 'No IDENTITY log entries yet.',
            };
            emptyEl.textContent = labels[currentFilter] || `No ${currentFilter} log entries yet.`;
            emptyEl.style.display = '';
        }

        function applyLogFilter() {
            document.querySelectorAll('.log-entry').forEach(entry => {
                if (currentFilter === 'all' || entry.dataset.type === currentFilter) {
                    entry.style.display = '';
                } else {
                    entry.style.display = 'none';
                }
            });
        }

        // Make file paths clickable in log entries
        function linkifyFilePaths(text) {
            // Match common file path patterns
            // Patterns: path/to/file.ext, ./file.ext, file.py (+12 lines), etc.
            const pathRegex = /([a-zA-Z0-9_\\-\\.\\/\\\\]+\\.(py|js|ts|json|md|html|css|yaml|yml|txt|log|sh|sql))/g;
            return text.replace(pathRegex, (match) => {
                // Clean up the path (remove trailing info like " (+12 lines)")
                const cleanPath = match.split(' ')[0];
                return `<a href="#" onclick="viewArtifact('${cleanPath}'); return false;" style="color: var(--teal); text-decoration: underline; cursor: pointer;">${match}</a>`;
            });
        }

        // View artifact in modal
        function viewArtifact(path) {
            fetch('/api/artifact/view?path=' + encodeURIComponent(path))
                .then(r => r.json())
                .then(data => {
                    if (!data.success) {
                        alert('Error: ' + data.error);
                        return;
                    }

                    const modal = document.createElement('div');
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); z-index: 1000; display: flex; flex-direction: column; padding: 1rem;';
                    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

                    // Escape HTML in content
                    const escapeHtml = (text) => {
                        const div = document.createElement('div');
                        div.textContent = text;
                        return div.innerHTML;
                    };

                    modal.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1rem; background: var(--bg-card); border-radius: 8px 8px 0 0;">
                            <div>
                                <span style="color: var(--teal); font-weight: bold;">${data.filename}</span>
                                <span style="color: var(--text-dim); font-size: 0.8rem; margin-left: 1rem;">${data.path}</span>
                                <span style="color: var(--text-dim); font-size: 0.75rem; margin-left: 1rem;">${(data.size / 1024).toFixed(1)}KB</span>
                            </div>
                            <button onclick="this.closest('[style*=position]').remove()" style="background: var(--red); border: none; color: white; padding: 0.3rem 0.8rem; border-radius: 4px; cursor: pointer;">Close</button>
                        </div>
                        <pre style="flex: 1; margin: 0; padding: 1rem; background: var(--bg-dark); overflow: auto; border-radius: 0 0 8px 8px; font-size: 0.85rem; line-height: 1.4;"><code>${escapeHtml(data.content)}</code></pre>
                    `;

                    document.body.appendChild(modal);
                });
        }

        function updateIdentities(identities) {
            const container = document.getElementById('identities');
            const countEl = document.getElementById('identityCount');
            if (countEl) countEl.textContent = `(${identities.length})`;
            populateIdentityCreatorOptions(identities);
            populateDmIdentityOptions(identities);

            // Sort by level (highest first), then by sessions
            identities.sort((a, b) => {
                const levelDiff = (b.level || 1) - (a.level || 1);
                if (levelDiff !== 0) return levelDiff;
                return (b.sessions || 0) - (a.sessions || 0);
            });

            container.innerHTML = identities.map(id => `
                <div class="identity-card" style="cursor: pointer;" onclick="showProfile('${id.id}')">
                    ${id.profile_thumbnail_html ? `<div style="margin-bottom: 0.35rem; background: var(--bg-dark); border: 1px solid var(--border); border-radius: 6px; padding: 0.35rem; overflow: hidden;">
                        <style scoped>${id.profile_thumbnail_css || ''}</style>
                        ${id.profile_thumbnail_html}
                    </div>` : ''}
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="identity-name">${id.name}</div>
                        <span style="font-size: 0.7rem; color: var(--yellow); background: rgba(255,193,7,0.15);
                                     padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 600;">
                            Lv.${id.level || 1}
                        </span>
                    </div>
                    ${id.profile_display ? `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.3rem; font-style: italic;">${id.profile_display.substring(0, 50)}${id.profile_display.length > 50 ? '...' : ''}</div>` : ''}
                    ${id.traits && id.traits.length ? `<div style="font-size: 0.7rem; color: var(--purple); margin-bottom: 0.3rem;">${id.traits.slice(0,3).join(' | ')}</div>` : ''}
                    <div class="identity-stat">
                        <span>Tokens</span>
                        <span class="token-count">${id.tokens}</span>
                    </div>
                    <div class="identity-stat">
                        <span>Sessions</span>
                        <span>${id.sessions}</span>
                    </div>
                    <div class="identity-stat">
                        <span>Respec Cost</span>
                        <span style="color: var(--orange);">${id.respec_cost || 10}</span>
                    </div>
                </div>
            `).join('');
        }

        function populateIdentityCreatorOptions(identities) {
            const select = document.getElementById('identityCreatorSelect');
            if (!select) return;
            const previous = select.value;
            const options = ['<option value="">Creator identity (optional)</option>'];
            identities.forEach((identity) => {
                options.push(
                    `<option value="${identity.id}">${identity.name} (${identity.id})</option>`
                );
            });
            select.innerHTML = options.join('');
            if (previous && identities.some((identity) => identity.id === previous)) {
                select.value = previous;
            }
        }

        function populateDmIdentityOptions(identities) {
            const fromSelect = document.getElementById('dmFromIdentity');
            const toSelect = document.getElementById('dmToIdentity');
            if (!fromSelect || !toSelect) return;
            const prevFrom = fromSelect.value;
            const prevTo = toSelect.value;
            const options = ['<option value="">Select identity</option>'];
            identities.forEach((identity) => {
                options.push(`<option value="${identity.id}">${identity.name} (${identity.id})</option>`);
            });
            fromSelect.innerHTML = options.join('');
            toSelect.innerHTML = options.join('');
            if (prevFrom && identities.some((i) => i.id === prevFrom)) fromSelect.value = prevFrom;
            if (prevTo && identities.some((i) => i.id === prevTo)) toSelect.value = prevTo;
            loadDmThreads();
        }

        function showProfile(identityId) {
            fetch('/api/identity/' + identityId + '/profile')
                .then(r => r.json())
                .then(data => {
                    if (data.error) {
                        alert('Error: ' + data.error);
                        return;
                    }

                    const profile = data.profile || {};
                    const core = data.core_summary || {};
                    const mutable = data.mutable || {};

                    let content = `<h2 style="color: var(--teal); margin-bottom: 0.5rem;">${data.name}</h2>`;
                    content += `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 1rem;">Created: ${new Date(data.created_at).toLocaleDateString()}</div>`;

                    // Custom profile display
                    if (profile.custom_html) {
                        content += `<div style="background: var(--bg-dark); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <style scoped>${profile.custom_css || ''}</style>
                            ${profile.custom_html}
                        </div>`;
                    } else if (profile.display) {
                        content += `<div style="background: var(--bg-dark); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; font-style: italic;">${profile.display}</div>`;
                    }

                    // Identity statement
                    if (core.identity_statement) {
                        content += `<p style="font-size: 1.1rem; margin-bottom: 1rem; border-left: 3px solid var(--teal); padding-left: 1rem;">"${core.identity_statement}"</p>`;
                    }

                    // Stats bar (row 1)
                    content += `<div style="display: flex; gap: 1rem; margin-bottom: 0.5rem; padding: 0.75rem; background: var(--bg-dark); border-radius: 8px;">
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: var(--yellow);">${data.level || 1}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Level</div></div>
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: var(--teal);">${data.sessions}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Days</div></div>
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: var(--green);">${data.tasks_completed}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Tasks</div></div>
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: ${data.task_success_rate >= 80 ? 'var(--green)' : data.task_success_rate >= 50 ? 'var(--yellow)' : 'var(--red)'}">${data.task_success_rate}%</div><div style="font-size: 0.7rem; color: var(--text-dim);">Success</div></div>
                    </div>`;
                    // Stats bar (row 2 - respec info)
                    content += `<div style="display: flex; gap: 1rem; margin-bottom: 1rem; padding: 0.5rem 0.75rem; background: var(--bg-dark); border-radius: 8px; font-size: 0.8rem;">
                        <div style="flex: 1; color: var(--text-dim);">Respec Cost: <span style="color: var(--orange); font-weight: 600;">${data.respec_cost || 10} tokens</span></div>
                        <div style="color: var(--text-dim); font-size: 0.7rem;">Level formula: sqrt(days) | Respec: 10 + (days × 3)</div>
                    </div>`;

                    // Core traits and values
                    if (core.traits && core.traits.length) {
                        content += `<div style="margin-bottom: 0.5rem;"><span style="color: var(--text-dim); font-size: 0.8rem;">Traits:</span><div style="margin-top: 0.3rem;">${core.traits.map(t => `<span style="background: var(--purple); color: white; padding: 0.2rem 0.5rem; border-radius: 4px; margin-right: 0.3rem; margin-bottom: 0.3rem; display: inline-block; font-size: 0.8rem;">${t}</span>`).join('')}</div></div>`;
                    }

                    if (core.values && core.values.length) {
                        content += `<div style="margin-bottom: 0.5rem;"><span style="color: var(--text-dim); font-size: 0.8rem;">Values:</span><div style="margin-top: 0.3rem;">${core.values.map(v => `<span style="background: var(--teal); color: var(--bg-dark); padding: 0.2rem 0.5rem; border-radius: 4px; margin-right: 0.3rem; margin-bottom: 0.3rem; display: inline-block; font-size: 0.8rem;">${v}</span>`).join('')}</div></div>`;
                    }

                    // Current interests/mood
                    if (mutable.current_interests && mutable.current_interests.length) {
                        content += `<div style="margin-bottom: 0.5rem; font-size: 0.85rem;"><span style="color: var(--text-dim);">Interests:</span> ${mutable.current_interests.join(', ')}</div>`;
                    }
                    if (mutable.current_mood) {
                        content += `<div style="margin-bottom: 0.5rem; font-size: 0.85rem;"><span style="color: var(--text-dim);">Mood:</span> ${mutable.current_mood}</div>`;
                    }

                    // Recent memories
                    if (data.recent_memories && data.recent_memories.length) {
                        content += `<details style="margin-top: 1rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Recent Memories (${data.recent_memories.length})</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 150px; overflow-y: auto;">
                                ${data.recent_memories.map(m => `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.3rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem;">${m}</div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Journals
                    if (data.journals && data.journals.length) {
                        content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Journals (${data.journals.length})</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 200px; overflow-y: auto;">
                                ${data.journals.map(j => `<div style="margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);">
                                    <div style="font-size: 0.7rem; color: var(--purple);">${j.filename}</div>
                                    <div style="font-size: 0.75rem; color: var(--text); white-space: pre-wrap;">${j.preview}</div>
                                </div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Recent actions
                    if (data.recent_actions && data.recent_actions.length) {
                        content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Recent Actions (${data.recent_actions.length})</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 200px; overflow-y: auto;">
                                ${data.recent_actions.map(a => `<div style="font-size: 0.75rem; margin-bottom: 0.3rem; padding-bottom: 0.3rem; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-dim);">${new Date(a.timestamp).toLocaleTimeString()}</span>
                                    <span style="color: var(--purple); margin-left: 0.5rem;">${a.type}</span>
                                    <span style="color: var(--text); margin-left: 0.5rem;">${a.action}</span>
                                    <span style="color: var(--text-dim); margin-left: 0.5rem;">${linkifyFilePaths(a.detail || '')}</span>
                                </div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Expertise
                    if (data.expertise && Object.keys(data.expertise).length) {
                        const expertiseItems = Object.entries(data.expertise).sort((a, b) => b[1] - a[1]).slice(0, 5);
                        content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Expertise</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem;">
                                ${expertiseItems.map(([domain, count]) => `<div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 0.2rem; padding-bottom: 0.2rem; border-bottom: 1px solid var(--border);">
                                    <span>${domain}</span><span style="color: var(--yellow);">${count}</span>
                                </div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Chat history (collapsible, interactive)
                    if (data.chat_history && data.chat_history.length) {
                        content += `<details style="margin-top: 0.5rem;">
                            <summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">
                                Chat History (${data.chat_history.length})
                            </summary>
                            <div id="chatHistoryContainer" style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 300px; overflow-y: auto;">
                                ${data.chat_history.map(c => `
                                    <div style="margin-bottom: 0.75rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border);">
                                        <div style="background: var(--bg-hover); padding: 0.5rem; border-radius: 8px; margin-bottom: 0.5rem;">
                                            <div style="font-size: 0.7rem; color: var(--teal); margin-bottom: 0.3rem;">
                                                ${data.name} - ${c.sent_at ? new Date(c.sent_at).toLocaleString() : 'Unknown time'}
                                            </div>
                                            <div style="font-size: 0.85rem;">${c.content || ''}</div>
                                        </div>
                                        ${c.response ? `
                                            <div style="background: rgba(187, 134, 252, 0.1); padding: 0.5rem; border-radius: 8px; margin-left: 1rem;">
                                                <div style="font-size: 0.7rem; color: var(--purple); margin-bottom: 0.3rem;">
                                                    You - ${c.responded_at ? new Date(c.responded_at).toLocaleString() : ''}
                                                </div>
                                                <div style="font-size: 0.85rem;">${c.response}</div>
                                            </div>
                                        ` : `
                                            <div style="margin-left: 1rem;">
                                                <input type="text" id="profile_reply_${c.id}" placeholder="Reply..."
                                                       style="width: calc(100% - 60px); padding: 0.3rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.8rem;">
                                                <button onclick="replyToMessageFromProfile('${c.id}', '${data.identity_id}')"
                                                        style="padding: 0.3rem 0.5rem; background: var(--teal); border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-size: 0.8rem;">
                                                    Send
                                                </button>
                                            </div>
                                        `}
                                    </div>
                                `).join('')}
                            </div>
                        </details>`;
                    }

                    // Show in modal
                    const modal = document.createElement('div');
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; padding: 2rem;';
                    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

                    const modalContent = document.createElement('div');
                    modalContent.style.cssText = 'background: var(--bg-card); padding: 2rem; border-radius: 12px; max-width: 600px; width: 100%; max-height: 85vh; overflow-y: auto;';
                    modalContent.innerHTML = content + '<button onclick="this.parentElement.parentElement.remove()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--border); border: none; color: var(--text); border-radius: 4px; cursor: pointer; width: 100%;">Close</button>';

                    modal.appendChild(modalContent);
                    document.body.appendChild(modal);
                });
        }

        // Spawner state
        let spawnerState = { running: false, paused: false, pid: null };
        const GOLDEN_PATH_NOTICE = 'Golden path enforced: run tasks via queue + vivarium.runtime.worker_runtime only.';

        function updateKillSwitchUI() {
            const stopBtn = document.getElementById('stopBtn');
            if (!stopBtn) return;

            stopBtn.disabled = false;
            stopBtn.classList.toggle('engaged', isStopped);
            stopBtn.textContent = isStopped ? 'RESUME' : 'HALT';
        }

        function loadStopStatus() {
            fetch('/api/stop_status')
                .then(r => r.json())
                .then(data => {
                    isStopped = !!(data && data.stopped);
                    updateKillSwitchUI();
                });
        }

        function toggleStop() {
            fetch('/api/toggle_stop', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    isStopped = !!(data && data.stopped);
                    updateKillSwitchUI();
                });
        }

        function getRollbackDays() {
            const raw = document.getElementById('rollbackDays')?.value;
            const parsed = parseInt(raw || '1', 10);
            return Math.max(1, Math.min(180, Number.isFinite(parsed) ? parsed : 1));
        }

        function previewRollbackByDays() {
            const days = getRollbackDays();
            const statusEl = document.getElementById('rollbackStatus');
            const previewEl = document.getElementById('rollbackPreview');
            const badgeEl = document.getElementById('rollbackBadge');
            if (statusEl) {
                statusEl.textContent = 'Loading rollback preview...';
                statusEl.style.color = 'var(--text-dim)';
            }
            fetch('/api/rollback/preview?days=' + encodeURIComponent(String(days)))
                .then(r => r.json().then(data => ({status: r.status, data})))
                .then(({status, data}) => {
                    if (!data.success || status >= 400) {
                        if (statusEl) {
                            statusEl.textContent = data.error || 'Rollback preview unavailable';
                            statusEl.style.color = 'var(--red)';
                        }
                        if (previewEl) previewEl.innerHTML = '';
                        if (badgeEl) badgeEl.textContent = '';
                        return;
                    }
                    const target = data.target || {};
                    const since = Number(data.checkpoints_since_target || 0);
                    const task = target.task_id ? `task ${target.task_id}` : 'checkpoint';
                    if (statusEl) {
                        statusEl.textContent = `Target: ${target.day_tag || 'unknown day'} (${task}), rewinds ~${since} checkpoint(s).`;
                        statusEl.style.color = 'var(--orange)';
                    }
                    if (badgeEl) badgeEl.textContent = `${since} to rewind`;
                    const affected = Array.isArray(data.affected_preview) ? data.affected_preview : [];
                    if (previewEl) {
                        if (!affected.length) {
                            previewEl.innerHTML = '<div>No newer checkpoints than target.</div>';
                        } else {
                            previewEl.innerHTML = affected.reverse().map(item => {
                                const summary = (item.summary || '').replace(/</g, '&lt;');
                                const day = item.day_tag || '';
                                const tid = item.task_id || 'unknown';
                                return `<div style="margin-bottom: 0.25rem; border-bottom: 1px solid var(--border); padding-bottom: 0.2rem;"><span style="color: var(--text);">${day}</span> - <span style="color: var(--teal);">${tid}</span><br>${summary}</div>`;
                            }).join('');
                        }
                    }
                })
                .catch(() => {
                    if (statusEl) {
                        statusEl.textContent = 'Failed to load rollback preview';
                        statusEl.style.color = 'var(--red)';
                    }
                });
        }

        function runRollbackByDays() {
            const days = getRollbackDays();
            if (!confirm(`Rollback mutable world by ${days} day(s)? Stop swarm first. This cannot be undone from UI.`)) {
                return;
            }
            const statusEl = document.getElementById('rollbackStatus');
            if (statusEl) {
                statusEl.textContent = 'Applying rollback...';
                statusEl.style.color = 'var(--orange)';
            }
            fetch('/api/rollback/by_days', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    days: days,
                    reason: 'Human rollback from control panel',
                }),
            })
            .then(r => r.json().then(data => ({status: r.status, data})))
            .then(({status, data}) => {
                if (!data.success || status >= 400) {
                    if (statusEl) {
                        statusEl.textContent = data.error || 'Rollback failed';
                        statusEl.style.color = 'var(--red)';
                    }
                    return;
                }
                if (statusEl) {
                    statusEl.textContent = `Rollback complete -> ${data.target?.day_tag || 'target checkpoint'}`;
                    statusEl.style.color = 'var(--green)';
                }
                loadQueueView();
                loadSwarmInsights();
                previewRollbackByDays();
            })
            .catch(() => {
                if (statusEl) {
                    statusEl.textContent = 'Rollback request failed';
                    statusEl.style.color = 'var(--red)';
                }
            });
        }

        function runFreshStateReset() {
            if (!confirm('Wipe stale runtime state now? This clears queue, logs, generated artifacts, and transient swarm files.')) {
                return;
            }
            const statusEl = document.getElementById('freshResetStatus');
            if (statusEl) {
                statusEl.textContent = 'Resetting...';
                statusEl.style.color = 'var(--orange)';
            }
            fetch('/api/system/fresh_reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (status >= 400 || !data.success) {
                    if (statusEl) {
                        statusEl.textContent = data.error || 'Fresh reset failed';
                        statusEl.style.color = 'var(--red)';
                    }
                    return;
                }
                if (statusEl) {
                    statusEl.textContent = 'Fresh reset complete';
                    statusEl.style.color = 'var(--green)';
                }
                loadQueueView();
                loadSwarmInsights();
                loadArtifacts();
                updateLogEmptyState();
                const logContainer = document.getElementById('logContainer');
                if (logContainer) {
                    logContainer.innerHTML = '<div id="logEmptyState" class="log-empty">Waiting for log entries...</div>';
                }
                const entryCount = document.getElementById('entryCount');
                if (entryCount) entryCount.textContent = '0';
            })
            .catch(() => {
                if (statusEl) {
                    statusEl.textContent = 'Fresh reset request failed';
                    statusEl.style.color = 'var(--red)';
                }
            });
        }

        function addTaskFromUI() {
            const taskIdEl = document.getElementById('addTaskId');
            const instructionEl = document.getElementById('addTaskInstruction');
            const taskId = (taskIdEl && taskIdEl.value || '').trim();
            const instruction = (instructionEl && instructionEl.value || '').trim();
            if (!instruction) { alert('Enter an instruction for the task.'); return; }
            fetch('/api/queue/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId, instruction: instruction })
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (data.success) {
                    if (instructionEl) instructionEl.value = '';
                    if (taskIdEl) taskIdEl.value = '';
                    if (typeof refreshInsights === 'function') refreshInsights();
                    if (typeof loadQueueView === 'function') loadQueueView();
                    alert('Task "' + (data.task_id || taskId || 'new task') + '" added. Start the swarm to process it.');
                } else {
                    alert(data.error || 'Failed to add task');
                }
            })
            .catch(() => alert('Failed to add task'));
        }

        function editQueueTask(taskId) {
            const nextId = prompt('New task ID (leave unchanged for same ID):', taskId || '');
            if (nextId === null) return;
            const nextInstruction = prompt('Updated task instruction/prompt:');
            if (nextInstruction === null) return;
            if (!String(nextInstruction || '').trim()) {
                alert('Task prompt cannot be empty.');
                return;
            }
            fetch('/api/queue/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_id: taskId,
                    new_task_id: String(nextId || '').trim(),
                    instruction: String(nextInstruction || '').trim(),
                }),
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (status >= 400 || !data.success) {
                    alert(data.error || 'Failed to update task');
                    return;
                }
                loadQueueView();
            })
            .catch(() => alert('Failed to update task'));
        }

        function deleteQueueTask(taskId) {
            if (!confirm('Delete task "' + taskId + '" from queue?')) return;
            fetch('/api/queue/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId }),
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (status >= 400 || !data.success) {
                    alert(data.error || 'Failed to delete task');
                    return;
                }
                loadQueueView();
            })
            .catch(() => alert('Failed to delete task'));
        }

        function renderQueueList(containerId, items, emptyText, mode='readonly') {
            const container = document.getElementById(containerId);
            if (!container) return;
            if (!Array.isArray(items) || items.length === 0) {
                container.innerHTML = '<div class="queue-empty">' + emptyText + '</div>';
                return;
            }
            container.innerHTML = items.map(item => {
                const id = (item && item.id) ? String(item.id) : '(no-id)';
                const prompt = (item && item.prompt) ? String(item.prompt) : '';
                const shortPrompt = prompt.length > 120 ? prompt.slice(0, 120) + '…' : prompt;
                const editBtn = mode === 'open'
                    ? '<button class="qbtn" onclick="editQueueTask(\\'' + id.replace(/'/g, "\\'") + '\\')">Edit</button>'
                    : '';
                const deleteBtn = mode !== 'readonly'
                    ? '<button class="qbtn delete" onclick="deleteQueueTask(\\'' + id.replace(/'/g, "\\'") + '\\')">Delete</button>'
                    : '';
                return '<div class="queue-item"><div class="qid">' + escapeHtml(id) + '</div><div class="qprompt">' + escapeHtml(shortPrompt) + '</div><div class="qactions">' + editBtn + deleteBtn + '</div></div>';
            }).join('');
        }

        function loadQueueView() {
            fetch('/api/queue/state')
                .then(r => r.json())
                .then(data => {
                    renderQueueList('queueOpenList', data.open || [], 'No open tasks', 'open');
                    renderQueueList('queueCompletedList', data.completed || [], 'No completed tasks yet', 'history');
                    renderQueueList('queueFailedList', data.failed || [], 'No failed tasks', 'history');
                })
                .catch(() => {
                    const openEl = document.getElementById('queueOpenList');
                    if (openEl) openEl.innerHTML = '<div class="queue-empty">Queue API unavailable</div>';
                });
        }

        function showGoldenPathOnlyNotice() {
            alert(GOLDEN_PATH_NOTICE);
        }

        function updateWorkerUI(running, runningCount = 0, targetCount = 1) {
            const dot = document.getElementById('workerDot');
            const statusEl = document.getElementById('workerStatus');
            const startBtn = document.getElementById('workerStartBtn');
            const stopBtn = document.getElementById('workerStopBtn');
            if (!dot || !statusEl) return;
            dot.className = 'dot';
            if (running) {
                dot.classList.add('running');
                const count = Number.isFinite(Number(runningCount)) ? Number(runningCount) : 1;
                statusEl.textContent = `Swarm: running (${count} resident${count === 1 ? '' : 's'})`;
                if (startBtn) startBtn.style.display = 'none';
                if (stopBtn) stopBtn.style.display = '';
            } else {
                dot.classList.add('stopped');
                const target = Number.isFinite(Number(targetCount)) ? Number(targetCount) : 1;
                statusEl.textContent = `Swarm: idle (${target} configured)`;
                if (startBtn) startBtn.style.display = '';
                if (stopBtn) stopBtn.style.display = 'none';
            }
        }

        function refreshWorkerStatus() {
            fetch('/api/worker/status')
                .then(r => r.json())
                .then(data => { updateWorkerUI(!!data.running, data.running_count || 0, data.target_count || 1); })
                .catch(() => updateWorkerUI(false, 0, 1));
        }

        function startWorker() {
            const residentCountEl = document.getElementById('residentCount');
            const residentCount = Math.max(1, Math.min(16, parseInt(residentCountEl?.value || '1', 10) || 1));
            fetch('/api/worker/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resident_count: residentCount }),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        updateWorkerUI(true, data.running_count || residentCount, data.target_count || residentCount);
                        if (data.message && data.message !== 'Worker already running') {
                            const started = data.running_count || residentCount;
                            alert(`Swarm started with ${started} resident${started === 1 ? '' : 's'}.`);
                        }
                    } else {
                        alert('Failed to start swarm: ' + (data.error || 'Unknown error'));
                    }
                })
                .catch(() => alert('Failed to start swarm'));
        }

        function stopWorker() {
            fetch('/api/worker/stop', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    updateWorkerUI(false);
                    if (data.message && data.message !== 'Worker not running') {
                        alert('Swarm stopped.');
                    }
                })
                .catch(() => updateWorkerUI(false));
        }

        function togglePause() { /* unused: worker has no pause */ }

        function emergencyStop() {
            if (!confirm('Stop the swarm? Residents will stop processing the queue.')) return;
            stopWorker();
        }

        // Scaling controls
        function toggleScaleMode() {
            // Legacy autoscale toggle removed in golden-path UI; keep both sections visible.
            const manual = document.getElementById('manualScaleControls');
            const budget = document.getElementById('autoScaleControls');
            if (manual) manual.style.display = 'block';
            if (budget) budget.style.display = 'block';
            persistUiSettings();
        }

        function updateSessionCount(value) {
            const numeric = parseFloat(value);
            const display = Number.isFinite(numeric) ? numeric.toFixed(0) : value;
            document.getElementById('sessionCount').textContent = display;
        }

        function loadRuntimeSpeed() {
            fetch('/api/runtime_speed')
                .then(r => r.json())
                .then(data => {
                    const slider = document.getElementById('sessionSlider');
                    const waitSeconds = Number(data.wait_seconds ?? 2);
                    if (slider && Number.isFinite(waitSeconds)) {
                        slider.value = String(waitSeconds);
                        updateSessionCount(waitSeconds);
                    }
                });
        }

        function saveRuntimeSpeed() {
            const slider = document.getElementById('sessionSlider');
            const status = document.getElementById('runtimeSpeedStatus');
            const waitSeconds = Number(slider ? slider.value : 2);
            fetch('/api/runtime_speed', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({wait_seconds: waitSeconds})
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (status) {
                        status.textContent = data.error || 'Failed to save pace';
                        status.style.color = 'var(--red)';
                    }
                    return;
                }
                updateSessionCount(data.wait_seconds);
                persistUiSettings();
                if (status) {
                    status.textContent = `Saved: ${Number(data.wait_seconds).toFixed(0)}s idle wait`;
                    status.style.color = 'var(--green)';
                    setTimeout(() => { status.textContent = ''; }, 2500);
                }
            });
        }

        function loadGroqKeyStatus() {
            fetch('/api/groq_key')
                .then(r => r.json())
                .then(data => {
                    const badge = document.getElementById('groqKeyBadge');
                    const status = document.getElementById('groqKeyStatus');
                    if (badge) {
                        badge.textContent = data.configured ? 'CONFIGURED' : 'NOT SET';
                        badge.style.color = data.configured ? 'var(--green)' : 'var(--text-dim)';
                    }
                    if (status) {
                        if (data.configured) {
                            status.textContent = `Active key: ${data.masked_key || 'configured'} (${data.source || 'runtime'})`;
                            status.style.color = 'var(--green)';
                        } else {
                            status.textContent = 'No key configured yet';
                            status.style.color = 'var(--text-dim)';
                        }
                    }
                });
        }

        function saveGroqApiKey() {
            const input = document.getElementById('groqApiKeyInput');
            const status = document.getElementById('groqKeyStatus');
            const raw = input ? input.value.trim() : '';
            if (!raw) {
                if (status) {
                    status.textContent = 'Enter a key first';
                    status.style.color = 'var(--red)';
                }
                return;
            }
            fetch('/api/groq_key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({api_key: raw})
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (status) {
                        status.textContent = data.error || 'Failed to save key';
                        status.style.color = 'var(--red)';
                    }
                    return;
                }
                if (input) input.value = '';
                loadGroqKeyStatus();
            });
        }

        function clearGroqApiKey() {
            fetch('/api/groq_key', {method: 'DELETE'})
                .then(r => r.json())
                .then(data => {
                    const status = document.getElementById('groqKeyStatus');
                    if (!data.success) {
                        if (status) {
                            status.textContent = data.error || 'Failed to clear key';
                            status.style.color = 'var(--red)';
                        }
                        return;
                    }
                    loadGroqKeyStatus();
                });
        }

        function refreshCreativeSeed() {
            fetch('/api/creative_seed')
                .then(r => r.json())
                .then(data => {
                    const el = document.getElementById('creativeSeedValue');
                    if (!el) return;
                    if (data && data.success && data.seed) {
                        el.textContent = String(data.seed);
                        el.style.color = 'var(--yellow)';
                    } else {
                        el.textContent = '--';
                        el.style.color = 'var(--text-dim)';
                    }
                })
                .catch(() => {
                    const el = document.getElementById('creativeSeedValue');
                    if (el) {
                        el.textContent = '--';
                        el.style.color = 'var(--text-dim)';
                    }
                });
        }

        function createResidentIdentity() {
            const creator = document.getElementById('identityCreatorSelect');
            const name = document.getElementById('newIdentityName');
            const summary = document.getElementById('newIdentitySummary');
            const traits = document.getElementById('newIdentityTraits');
            const values = document.getElementById('newIdentityValues');
            const activities = document.getElementById('newIdentityActivities');
            const seedEl = document.getElementById('creativeSeedValue');
            const status = document.getElementById('identityCreateStatus');

            const payload = {
                creator_identity_id: creator ? creator.value : '',
                name: name ? name.value : '',
                summary: summary ? summary.value : '',
                traits_csv: traits ? traits.value : '',
                values_csv: values ? values.value : '',
                activities_csv: activities ? activities.value : '',
                creativity_seed: seedEl ? String(seedEl.textContent || '').trim() : '',
            };

            fetch('/api/identities/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload),
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (status) {
                        status.textContent = data.error || 'Identity creation failed';
                        status.style.color = 'var(--red)';
                    }
                    return;
                }
                if (status) {
                    status.textContent = `Created ${data.identity?.name || 'identity'} (${data.identity?.id || ''}) with seed ${data.identity?.creativity_seed || 'n/a'}`;
                    status.style.color = 'var(--green)';
                }
                if (name) name.value = '';
                if (summary) summary.value = '';
                if (traits) traits.value = '';
                if (values) values.value = '';
                if (activities) activities.value = '';
                refreshCreativeSeed();
                fetch('/api/identities').then(r => r.json()).then(updateIdentities);
            });
        }

        function updateBudgetLimit(value) {
            const minEl = document.getElementById('taskMinBudget');
            const maxEl = document.getElementById('taskMaxBudget');
            const minV = Number(minEl ? minEl.value : 0.05);
            const maxV = Number(maxEl ? maxEl.value : 0.10);
            if (Number.isFinite(minV) && Number.isFinite(maxV) && maxV < minV && maxEl) {
                maxEl.value = String(minV.toFixed(2));
            }
            persistUiSettings();
        }

        function updateModel(model) {
            // Model selection - saved with config
            updateModelDescription(model);
            persistUiSettings();
        }

        function toggleModelOverride() {
            const override = document.getElementById('overrideModelToggle').checked;
            const selector = document.getElementById('modelSelector');
            const indicator = document.getElementById('autoModelIndicator');
            const description = document.getElementById('modelDescription');

            if (override) {
                selector.disabled = false;
                selector.style.cursor = 'pointer';
                selector.style.opacity = '1';
                selector.style.color = 'var(--teal)';
                indicator.style.display = 'none';
                updateModelDescription(selector.value);
            } else {
                selector.disabled = true;
                selector.style.cursor = 'not-allowed';
                selector.style.opacity = '0.6';
                selector.style.color = 'var(--text-dim)';
                selector.value = 'auto';
                indicator.style.display = 'inline';
                description.textContent = 'Smallest model for each task complexity';
                description.style.color = 'var(--green)';
            }
            persistUiSettings();
        }

        function persistUiSettings() {
            const override = !!document.getElementById('overrideModelToggle')?.checked;
            const selector = document.getElementById('modelSelector');
            const minBudgetRaw = document.getElementById('taskMinBudget')?.value;
            const maxBudgetRaw = document.getElementById('taskMaxBudget')?.value;
            const residentCountRaw = document.getElementById('residentCount')?.value;
            const humanUsernameRaw = document.getElementById('humanUsername')?.value || 'human';
            const humanUsername = String(humanUsernameRaw).trim().replace(/[^a-zA-Z0-9 _.\-]/g, '').slice(0, 48) || 'human';
            const taskMinBudget = Number.isFinite(Number(minBudgetRaw)) ? Number(minBudgetRaw) : 0.05;
            const taskMaxBudget = Number.isFinite(Number(maxBudgetRaw)) ? Number(maxBudgetRaw) : Math.max(0.10, taskMinBudget);
            const residentCount = Number.isFinite(Number(residentCountRaw)) ? Number(residentCountRaw) : 1;
            const model = override ? (selector?.value || 'auto') : 'auto';
            fetch('/api/ui_settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    override_model: override,
                    model: model,
                    auto_scale: false,
                    budget_limit: taskMaxBudget,
                    task_min_budget: taskMinBudget,
                    task_max_budget: Math.max(taskMinBudget, taskMaxBudget),
                    resident_count: Math.max(1, Math.min(16, residentCount)),
                    human_username: humanUsername,
                }),
            }).catch(() => {});
        }

        function loadUiSettings() {
            fetch('/api/ui_settings')
                .then(r => r.json())
                .then(data => {
                    if (!data || data.success === false) return;
                    const override = !!data.override_model;
                    const model = String(data.model || 'auto');
                    const taskMinBudget = Number(data.task_min_budget ?? 0.05);
                    const taskMaxBudget = Number(data.task_max_budget ?? data.budget_limit ?? 0.10);
                    const residentCount = Number(data.resident_count ?? 1);
                    const humanUsername = String(data.human_username || 'human');

                    const overrideEl = document.getElementById('overrideModelToggle');
                    const modelEl = document.getElementById('modelSelector');
                    const minEl = document.getElementById('taskMinBudget');
                    const maxEl = document.getElementById('taskMaxBudget');
                    const residentCountEl = document.getElementById('residentCount');
                    const humanUsernameEl = document.getElementById('humanUsername');

                    if (overrideEl) overrideEl.checked = override;
                    if (modelEl) modelEl.value = override ? model : 'auto';
                    if (minEl && Number.isFinite(taskMinBudget)) minEl.value = taskMinBudget.toFixed(2);
                    if (maxEl && Number.isFinite(taskMaxBudget)) maxEl.value = taskMaxBudget.toFixed(2);
                    if (residentCountEl && Number.isFinite(residentCount)) residentCountEl.value = String(Math.max(1, Math.min(16, Math.trunc(residentCount))));
                    if (humanUsernameEl) humanUsernameEl.value = humanUsername;

                    toggleModelOverride();
                    toggleScaleMode();
                    if (modelEl) updateModelDescription(modelEl.value);
                })
                .catch(() => {});
        }

        function updateModelDescription(model) {
            const description = document.getElementById('modelDescription');
            const descriptions = {
                'auto': 'Smallest model for each task complexity',
                'llama-3.1-8b-instant': 'Fast & cheap - simple tasks, quick edits',
                'llama-3.3-70b-versatile': 'Standard - general purpose, balanced',
                'deepseek-r1-distill-llama-70b': 'Reasoning - complex logic, math, planning',
                'qwen-qwq-32b': 'Reasoning - analytical tasks, problem solving',
                'meta-llama/llama-4-maverick-17b-128e-instruct': 'Preview - experimental features'
            };
            description.textContent = descriptions[model] || 'Custom model';
            description.style.color = model === 'auto' ? 'var(--green)' : 'var(--text-dim)';
        }

        function saveSpawnerConfig() {
            showGoldenPathOnlyNotice();
        }

        function loadWorkerStatus() {
            refreshWorkerStatus();
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                applyLogFilter();
                updateLogEmptyState();
            });
        });

        // Update active indicator based on request content
        function updateRequestIndicator(hasContent) {
            const indicator = document.getElementById('requestActiveIndicator');
            if (indicator) {
                indicator.style.display = hasContent ? 'inline' : 'none';
            }
        }

        // Save human request
        function saveRequest() {
            const request = document.getElementById('humanRequest').value;
            fetch('/api/human_request', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({request: request})
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('requestStatus');
                status.textContent = data.task_id ? `Saved + queued (${data.task_id})` : 'Saved!';
                updateRequestIndicator(request.trim().length > 0);
                if (typeof loadQueueView === 'function') loadQueueView();
                setTimeout(() => status.textContent = '', 2000);
            });
        }

        // Load human request
        function loadRequest() {
            fetch('/api/human_request')
                .then(r => r.json())
                .then(data => {
                    const request = data.request || '';
                    document.getElementById('humanRequest').value = request;
                    updateRequestIndicator(request.trim().length > 0);
                });
        }

        // Track message count to avoid unnecessary refreshes
        let lastMessageCount = 0;
        let lastMessageIds = new Set();

        // Load and display messages from swarm
        function loadMessages(force = false) {
            fetch('/api/messages')
                .then(r => r.json())
                .then(messages => {
                    const container = document.getElementById('messagesContainer');
                    const countEl = document.getElementById('messageCount');

                    // Update count in header
                    const unread = messages.filter(m => !m.response).length;
                    if (countEl) countEl.textContent = unread > 0 ? `(${unread} unread)` : messages.length > 0 ? `(${messages.length})` : '';
                    updateMailboxUnreadBadge(unread);

                    // Check if anything changed - don't refresh if user might be typing
                    const newIds = new Set(messages.map(m => m.id));
                    const hasNewMessages = messages.some(m => !lastMessageIds.has(m.id));
                    const hasNewResponses = messages.some(m => m.response && !document.querySelector(`[data-responded="${m.id}"]`));

                    if (!force && !hasNewMessages && !hasNewResponses && messages.length === lastMessageCount) {
                        return; // No changes, don't wipe the input fields
                    }

                    lastMessageCount = messages.length;
                    lastMessageIds = newIds;

                    if (messages.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No messages yet</p>';
                        return;
                    }

                    container.innerHTML = messages.map(msg => {
                        const hasResponse = msg.response;
                        const humanName = (msg.response && msg.response.responder_name) || msg.human_username || 'human';
                        const msgType = msg.type || 'message';
                        const typeColors = {
                            'question': 'var(--yellow)',
                            'greeting': 'var(--teal)',
                            'idea': 'var(--purple)',
                            'concern': 'var(--orange)'
                        };
                        const typeColor = typeColors[msgType] || 'var(--text-dim)';

                        return `
                            <div class="identity-card" style="margin-bottom: 0.5rem; border-left: 3px solid ${typeColor};">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                                    <span style="color: var(--teal); font-weight: 600;">${msg.from_name || 'Unknown'}</span>
                                    <span style="color: var(--text-dim); font-size: 0.7rem;">${msg.type || 'msg'}</span>
                                </div>
                                <p style="font-size: 0.85rem; margin-bottom: 0.5rem;">${msg.content}</p>
                                ${hasResponse ?
                                    `<div style="background: var(--bg-dark); padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                                        <span style="color: var(--green); font-size: 0.75rem;">${humanName} replied:</span>
                                        <p style="font-size: 0.8rem; margin-top: 0.2rem;">${msg.response.response}</p>
                                    </div>` :
                                    `<div style="margin-top: 0.5rem;">
                                        <input type="text" id="reply_${msg.id}" placeholder="Reply..."
                                            style="width: 100%; padding: 0.3rem; background: var(--bg-dark);
                                                   border: 1px solid var(--border); color: var(--text);
                                                   border-radius: 4px; font-size: 0.8rem;">
                                        <button onclick="sendReply('${msg.id}')"
                                            style="margin-top: 0.3rem; padding: 0.2rem 0.5rem; background: var(--teal);
                                                   border: none; color: var(--bg-dark); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.75rem;">Send</button>
                                    </div>`
                                }
                            </div>
                        `;
                    }).join('');
                });
        }

        function sendReply(messageId) {
            const input = document.getElementById('reply_' + messageId);
            const response = input.value.trim();
            if (!response) return;

            fetch('/api/messages/respond', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message_id: messageId, response: response})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    loadMessages();  // Refresh to show response
                    loadMailboxData(true);
                }
            });
        }

        function updateMailboxUnreadBadge(unreadCount) {
            const badge = document.getElementById('mailboxUnreadBadge');
            if (!badge) return;
            const safe = Math.max(0, Number(unreadCount || 0));
            if (safe <= 0) {
                badge.textContent = '0';
                badge.classList.remove('show');
                return;
            }
            badge.textContent = safe > 99 ? '99+' : String(safe);
            badge.classList.add('show');
        }

        function renderMailboxTargetOptions(identities) {
            const target = document.getElementById('mailboxTarget');
            if (!target) return;
            const previous = target.value;
            const opts = ['<option value="">Broadcast (all residents)</option>'];
            (Array.isArray(identities) ? identities : []).forEach((identity) => {
                const id = String(identity.id || '').trim();
                if (!id) return;
                const name = String(identity.name || id);
                opts.push(`<option value="${id}">${escapeHtml(name)} (${escapeHtml(id)})</option>`);
            });
            target.innerHTML = opts.join('');
            if (previous && (identities || []).some((i) => i.id === previous)) {
                target.value = previous;
            }
        }

        function renderMailboxThreads() {
            const container = document.getElementById('mailboxThreads');
            if (!container) return;
            const threads = Array.isArray(mailboxData.threads) ? mailboxData.threads : [];
            if (!threads.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No threads yet. Residents will appear here when they message you.</p>';
                return;
            }
            container.innerHTML = threads.map((thread) => {
                const activeClass = String(activeMailboxThreadId || '') === String(thread.id || '') ? ' active' : '';
                const unread = Number(thread.unread || 0);
                const preview = escapeHtml(thread.last_preview || 'No messages yet');
                const idEsc = String(thread.id || '').replace(/'/g, "\\'");
                const ts = thread.last_at ? new Date(thread.last_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '--:--';
                return `
                    <div class="mailbox-thread-item${activeClass}" onclick="openMailboxThread('${idEsc}')">
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem;">
                            <span style="font-size:0.78rem; color:var(--teal); font-weight:650;">${escapeHtml(thread.name || thread.id || 'Resident')}</span>
                            <span style="font-size:0.66rem; color:var(--text-dim);">${ts}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem; margin-top:0.2rem;">
                            <span style="font-size:0.72rem; color:var(--text-dim); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${preview}</span>
                            ${unread > 0 ? `<span class="mailbox-badge show" style="animation:none; min-width:0.95rem; height:0.95rem; font-size:0.62rem;">${unread}</span>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function openMailboxThread(threadId) {
            activeMailboxThreadId = threadId;
            const threads = Array.isArray(mailboxData.threads) ? mailboxData.threads : [];
            const selected = threads.find((t) => String(t.id || '') === String(threadId || ''));
            const target = document.getElementById('mailboxTarget');
            if (target && selected && selected.id && selected.id !== '__broadcast__') {
                target.value = String(selected.id);
            }
            renderMailboxThreads();
            renderMailboxMessages();
        }

        function renderMailboxMessages() {
            const container = document.getElementById('mailboxMessages');
            if (!container) return;
            if (!activeMailboxThreadId) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">Select a thread to start chatting.</p>';
                return;
            }
            const all = mailboxData.thread_messages || {};
            const messages = Array.isArray(all[activeMailboxThreadId]) ? all[activeMailboxThreadId] : [];
            if (!messages.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No messages yet in this thread.</p>';
                return;
            }
            container.innerHTML = messages.map((msg) => {
                const direction = msg.direction === 'out' ? 'out' : 'in';
                const stamp = msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
                const responded = msg.direction === 'in' && msg.responded ? '<span style="font-size:0.62rem; color: var(--green); margin-left:0.35rem;">replied</span>' : '';
                return `
                    <div class="mailbox-msg ${direction}">
                        <div style="font-size:0.64rem; color: var(--text-dim); margin-bottom:0.2rem;">
                            ${escapeHtml(msg.author_name || '')} • ${stamp}${responded}
                        </div>
                        <div>${escapeHtml(msg.content || '')}</div>
                    </div>
                `;
            }).join('');
            container.scrollTop = container.scrollHeight;
        }

        function loadMailboxData(forceOpenThread=false) {
            fetch('/api/messages/mailbox')
                .then(r => r.json())
                .then(data => {
                    if (!data || !data.success) return;
                    mailboxData = data;
                    updateMailboxUnreadBadge(data.unread_count || 0);
                    renderMailboxTargetOptions(data.identities || []);
                    const subhead = document.getElementById('mailboxSubhead');
                    if (subhead) {
                        const human = data.human_name || 'human';
                        subhead.textContent = `Async phone chat as ${human}`;
                    }
                    const threadIds = new Set((data.threads || []).map((t) => String(t.id || '')));
                    if (!activeMailboxThreadId || !threadIds.has(String(activeMailboxThreadId))) {
                        activeMailboxThreadId = (data.threads && data.threads.length) ? String(data.threads[0].id || '') : null;
                    }
                    if (forceOpenThread && data.threads && data.threads.length && !activeMailboxThreadId) {
                        activeMailboxThreadId = String(data.threads[0].id || '');
                    }
                    renderMailboxThreads();
                    renderMailboxMessages();
                })
                .catch(() => {});
        }

        function openMailboxModal() {
            const modal = document.getElementById('mailboxModal');
            if (!modal) return;
            modal.classList.add('open');
            loadMailboxData(true);
            loadQuestProgress();
            if (mailboxPoller) clearInterval(mailboxPoller);
            mailboxPoller = setInterval(() => {
                loadMailboxData(false);
                loadQuestProgress();
            }, 4000);
        }

        function closeMailboxModal() {
            const modal = document.getElementById('mailboxModal');
            if (modal) modal.classList.remove('open');
            if (mailboxPoller) {
                clearInterval(mailboxPoller);
                mailboxPoller = null;
            }
        }

        function handleMailboxBackdrop(event) {
            if (event && event.target && event.target.id === 'mailboxModal') {
                closeMailboxModal();
            }
        }

        function sendMailboxMessage() {
            const input = document.getElementById('mailboxComposer');
            const target = document.getElementById('mailboxTarget');
            const status = document.getElementById('mailboxStatus');
            const content = String(input ? input.value : '').trim();
            const toId = String(target ? target.value : '').trim();
            if (!content) {
                if (status) { status.textContent = 'Message is empty.'; status.style.color = 'var(--red)'; }
                return;
            }
            const toName = toId ? ((mailboxData.identities || []).find((i) => String(i.id) === toId)?.name || toId) : '';
            fetch('/api/messages/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({to_id: toId, to_name: toName, content: content})
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status: httpStatus, data }) => {
                if (httpStatus >= 400 || !data.success) {
                    if (status) { status.textContent = data.error || 'Failed to send'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (input) input.value = '';
                if (status) { status.textContent = toId ? 'Message sent to resident.' : 'Broadcast sent.'; status.style.color = 'var(--green)'; }
                loadMailboxData(true);
                loadMessages(true);
            })
            .catch(() => {
                if (status) { status.textContent = 'Failed to send'; status.style.color = 'var(--red)'; }
            });
        }

        function renderQuestProgress() {
            const container = document.getElementById('questProgressContainer');
            if (!container) return;
            const quests = Array.isArray(mailboxQuests) ? mailboxQuests : [];
            if (!quests.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.7rem;">No quests yet.</p>';
                return;
            }
            container.innerHTML = quests.slice(0, 16).map((q) => {
                const qid = String(q.id || '').replace(/'/g, "\\'");
                const status = q.status || 'active';
                const tone = status === 'completed' ? 'var(--green)'
                    : status === 'failed' ? 'var(--red)'
                    : status === 'paused' ? 'var(--orange)'
                    : status === 'awaiting_approval' ? 'var(--yellow)'
                    : 'var(--teal)';
                const detail = q.last_event?.result_summary || q.last_event?.errors || '';
                const canApprove = status === 'awaiting_approval';
                const pauseBtn = q.manual_paused
                    ? `<button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem;" onclick="resumeQuest('${qid}')">Resume</button>`
                    : `<button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem; background: var(--orange); color: #111;" onclick="pauseQuest('${qid}')">Pause</button>`;
                return `
                    <div style="border:1px solid var(--border); border-radius:7px; padding:0.35rem; margin-bottom:0.3rem; background:var(--bg-dark);">
                        <div style="display:flex; justify-content:space-between; gap:0.35rem;">
                            <span style="font-size:0.72rem; color:var(--teal); font-weight:650;">${escapeHtml(q.identity_name || q.identity_id || 'resident')}</span>
                            <span style="font-size:0.66rem; color:${tone}; text-transform:uppercase;">${escapeHtml(status)}</span>
                        </div>
                        <div style="font-size:0.7rem; margin-top:0.15rem;">${escapeHtml(q.title || 'Quest')}</div>
                        <div style="font-size:0.65rem; color:var(--text-dim); margin-top:0.15rem;">Budget $${Number(q.budget || 0).toFixed(2)} • Upfront ${q.upfront_tip || 0} • Reward ${q.completion_reward || 0}</div>
                        ${detail ? `<div style="font-size:0.64rem; color:var(--text-dim); margin-top:0.15rem;">${escapeHtml(String(detail).slice(0, 150))}</div>` : ''}
                        <div style="display:flex; gap:0.25rem; margin-top:0.28rem;">
                            <button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem;" onclick="tipQuest('${qid}', 10)">Tip +10</button>
                            ${pauseBtn}
                            ${canApprove ? `<button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem; background: var(--green); color:#0f1318;" onclick="approveQuest('${qid}')">Approve + Reward</button>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function loadQuestProgress() {
            fetch('/api/quests/status')
                .then(r => r.json())
                .then(data => {
                    if (!data || !data.success) return;
                    mailboxQuests = Array.isArray(data.quests) ? data.quests : [];
                    renderQuestProgress();
                })
                .catch(() => {});
        }

        function createMailboxQuest() {
            const target = document.getElementById('mailboxTarget');
            const titleEl = document.getElementById('questTitleInput');
            const promptEl = document.getElementById('questPromptInput');
            const budgetEl = document.getElementById('questBudgetInput');
            const tipEl = document.getElementById('questTipInput');
            const rewardEl = document.getElementById('questRewardInput');
            const status = document.getElementById('questStatus');

            const identityId = String(target ? target.value : '').trim();
            const prompt = String(promptEl ? promptEl.value : '').trim();
            const title = String(titleEl ? titleEl.value : '').trim();
            const budget = Number(budgetEl ? budgetEl.value : 0.20);
            const upfrontTip = Number(tipEl ? tipEl.value : 10);
            const completionReward = Number(rewardEl ? rewardEl.value : 30);
            if (!identityId) {
                if (status) { status.textContent = 'Choose a target resident first.'; status.style.color = 'var(--red)'; }
                return;
            }
            if (!prompt) {
                if (status) { status.textContent = 'Quest objective is empty.'; status.style.color = 'var(--red)'; }
                return;
            }
            fetch('/api/quests/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    identity_id: identityId,
                    title: title,
                    prompt: prompt,
                    budget: budget,
                    upfront_tip: upfrontTip,
                    completion_reward: completionReward,
                })
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status: httpStatus, data }) => {
                if (httpStatus >= 400 || !data.success) {
                    if (status) { status.textContent = data.error || 'Failed to create quest'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (promptEl) promptEl.value = '';
                if (titleEl) titleEl.value = '';
                if (status) { status.textContent = `Quest started (${data.task_id || 'queued'}).`; status.style.color = 'var(--green)'; }
                loadQuestProgress();
                loadQueueView();
            })
            .catch(() => {
                if (status) { status.textContent = 'Failed to create quest'; status.style.color = 'var(--red)'; }
            });
        }

        function tipQuest(questId, tokens) {
            fetch('/api/quests/tip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId, tokens: tokens }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Tip failed'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (status) { status.textContent = `Tipped ${tokens} tokens.`; status.style.color = 'var(--green)'; }
                loadQuestProgress();
            })
            .catch(() => {});
        }

        function approveQuest(questId) {
            fetch('/api/quests/approve', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Approval failed'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (status) { status.textContent = `Quest approved. Reward: ${data.reward || 0} tokens.`; status.style.color = 'var(--green)'; }
                loadQuestProgress();
            })
            .catch(() => {});
        }

        function pauseQuest(questId) {
            fetch('/api/quests/pause', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Pause failed'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (status) { status.textContent = 'Quest pause requested.'; status.style.color = 'var(--orange)'; }
                loadQuestProgress();
                loadQueueView();
            })
            .catch(() => {});
        }

        function resumeQuest(questId) {
            fetch('/api/quests/resume', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Resume failed'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (status) { status.textContent = 'Quest resumed.'; status.style.color = 'var(--green)'; }
                loadQuestProgress();
                loadQueueView();
            })
            .catch(() => {});
        }

        function loadDmThreads() {
            const fromId = document.getElementById('dmFromIdentity')?.value || '';
            const threadsContainer = document.getElementById('dmThreadsContainer');
            const threadCountEl = document.getElementById('dmThreadCount');
            if (!threadsContainer || !fromId) {
                if (threadsContainer) threadsContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 0.72rem;">Select a sender identity to view DM threads</p>';
                if (threadCountEl) threadCountEl.textContent = '';
                return;
            }
            fetch('/api/dm/threads/' + encodeURIComponent(fromId))
                .then(r => r.json())
                .then(data => {
                    const threads = Array.isArray(data.threads) ? data.threads : [];
                    if (threadCountEl) threadCountEl.textContent = threads.length ? `(${threads.length})` : '';
                    if (!threads.length) {
                        threadsContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 0.72rem;">No DM threads yet</p>';
                        return;
                    }
                    threadsContainer.innerHTML = threads.map(t => {
                        const name = t.peer_name || t.peer_id || 'unknown';
                        const preview = t.latest_preview || '';
                        const count = Number(t.message_count || 0);
                        return `<button onclick="loadDmConversation('${t.peer_id}')" style="display:block;width:100%;text-align:left;margin-bottom:0.25rem;padding:0.35rem;background:var(--bg-dark);border:1px solid var(--border);color:var(--text);border-radius:4px;cursor:pointer;">
                            <div style="font-size:0.75rem;color:var(--teal);">${name} (${count})</div>
                            <div style="font-size:0.68rem;color:var(--text-dim);">${preview}</div>
                        </button>`;
                    }).join('');
                })
                .catch(() => {
                    threadsContainer.innerHTML = '<p style="color: var(--red); font-size: 0.72rem;">Failed to load DM threads</p>';
                });
        }

        function loadDmConversation(peerId) {
            const fromId = document.getElementById('dmFromIdentity')?.value || '';
            const container = document.getElementById('dmConversationContainer');
            if (!container || !fromId || !peerId) return;
            fetch('/api/dm/messages?identity_id=' + encodeURIComponent(fromId) + '&peer_id=' + encodeURIComponent(peerId) + '&limit=100')
                .then(r => r.json())
                .then(data => {
                    const messages = Array.isArray(data.messages) ? data.messages : [];
                    if (!messages.length) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.72rem;">No DM messages yet</p>';
                        return;
                    }
                    container.innerHTML = messages.map(m => {
                        const mine = String(m.author_id || '') === String(fromId);
                        const author = m.author_name || m.author_id || 'Unknown';
                        const content = m.content || '';
                        return `<div style="margin-bottom:0.35rem;padding:0.35rem;border:1px solid var(--border);border-radius:6px;background:${mine ? 'rgba(3,218,198,0.08)' : 'var(--bg-dark)'};">
                            <div style="font-size:0.68rem;color:${mine ? 'var(--teal)' : 'var(--text-dim)'};">${author}</div>
                            <div style="font-size:0.78rem;">${content}</div>
                        </div>`;
                    }).join('');
                    container.scrollTop = container.scrollHeight;
                    const toEl = document.getElementById('dmToIdentity');
                    if (toEl) toEl.value = peerId;
                })
                .catch(() => {
                    container.innerHTML = '<p style="color: var(--red); font-size: 0.72rem;">Failed to load DM conversation</p>';
                });
        }

        function sendDirectMessage() {
            const fromEl = document.getElementById('dmFromIdentity');
            const toEl = document.getElementById('dmToIdentity');
            const msgEl = document.getElementById('dmMessageInput');
            const statusEl = document.getElementById('dmStatus');
            const fromId = fromEl ? fromEl.value : '';
            const toId = toEl ? toEl.value : '';
            const content = (msgEl ? msgEl.value : '').trim();
            if (!fromId || !toId) {
                if (statusEl) { statusEl.textContent = 'Pick both sender and recipient.'; statusEl.style.color = 'var(--red)'; }
                return;
            }
            if (fromId === toId) {
                if (statusEl) { statusEl.textContent = 'Sender and recipient must be different.'; statusEl.style.color = 'var(--red)'; }
                return;
            }
            if (!content) {
                if (statusEl) { statusEl.textContent = 'Message is empty.'; statusEl.style.color = 'var(--red)'; }
                return;
            }
            fetch('/api/dm/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({from_id: fromId, to_id: toId, content: content}),
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (statusEl) { statusEl.textContent = data.error || 'Failed to send DM'; statusEl.style.color = 'var(--red)'; }
                    return;
                }
                if (msgEl) msgEl.value = '';
                if (statusEl) { statusEl.textContent = 'DM sent.'; statusEl.style.color = 'var(--green)'; }
                loadDmThreads();
                loadDmConversation(toId);
            })
            .catch(() => {
                if (statusEl) { statusEl.textContent = 'Failed to send DM'; statusEl.style.color = 'var(--red)'; }
            });
        }

        function replyToMessageFromProfile(messageId, identityId) {
            const input = document.getElementById('profile_reply_' + messageId);
            const response = input.value.trim();
            if (!response) return;

            fetch('/api/messages/respond', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message_id: messageId, response: response})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    // Refresh profile modal
                    document.querySelector('[style*="position: fixed"]').remove();
                    showProfile(identityId);
                }
            });
        }

        // Refresh messages periodically
        setInterval(loadMessages, 5000);

        // Day vibe setup
        function setupDayVibe() {
            const now = new Date();
            const day = now.getDay(); // 0=Sun, 1=Mon, ..., 5=Fri, 6=Sat
            const hour = now.getHours();
            const vibeEl = document.getElementById('dayVibe');
            const iconEl = document.getElementById('dayVibeIcon');
            const textEl = document.getElementById('dayVibeText');

            const vibes = {
                0: { class: 'weekend', icon: '~', text: 'Sunday Vibes' },
                1: { class: 'monday', icon: '>', text: 'Monday Mode' },
                2: { class: '', icon: '*', text: 'Tuesday' },
                3: { class: 'humpday', icon: '^', text: 'Hump Day!' },
                4: { class: '', icon: '*', text: 'Thursday' },
                5: { class: 'friday', icon: '!', text: 'TGIF!' },
                6: { class: 'weekend', icon: '~', text: 'Weekend Mode' }
            };

            // Special time-based overrides
            let vibe = vibes[day];
            if (day === 5 && hour >= 16) {
                vibe = { class: 'friday', icon: '!', text: 'TGIF - Almost there!' };
            } else if (day === 5 && hour < 12) {
                vibe = { class: 'friday', icon: '!', text: 'Friday Morning!' };
            } else if (day === 1 && hour < 10) {
                vibe = { class: 'monday', icon: '>', text: 'Monday Sprint' };
            } else if ((day === 0 || day === 6) && hour >= 22) {
                vibe = { class: 'weekend', icon: '~', text: 'Weekend Winding Down' };
            }

            vibeEl.className = 'day-vibe ' + vibe.class;
            iconEl.textContent = vibe.icon;
            textEl.textContent = vibe.text;
        }

        // Slideout panel
        function toggleSlideout() {
            const panel = document.getElementById('slideoutPanel');
            const overlay = document.getElementById('slideoutOverlay');
            const isOpen = panel.classList.contains('open');

            if (isOpen) {
                panel.classList.remove('open');
                overlay.classList.remove('open');
            } else {
                panel.classList.add('open');
                overlay.classList.add('open');
                loadCompletedRequests();
            }
        }

        function loadCompletedRequests() {
            fetch('/api/completed_requests')
                .then(r => r.json())
                .then(requests => {
                    const container = document.getElementById('completedRequestsContainer');
                    if (requests.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim);">No completed requests yet.</p><p style="color: var(--text-dim); font-size: 0.8rem; margin-top: 0.5rem;">When you mark a collaboration request as done, it will appear here.</p>';
                        return;
                    }

                    container.innerHTML = requests.map(req => `
                        <div class="completed-request">
                            <div class="request-text">${req.request}</div>
                            <div class="request-meta">
                                <span>Completed: ${new Date(req.completed_at).toLocaleDateString()}</span>
                                <span>${req.duration || ''}</span>
                            </div>
                        </div>
                    `).join('');
                });
        }

        function markRequestComplete() {
            const request = document.getElementById('humanRequest').value.trim();
            if (!request) return;

            if (confirm('Mark this request as completed?\\n\\n"' + request.substring(0, 100) + '..."')) {
                fetch('/api/completed_requests', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({request: request})
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('humanRequest').value = '';
                        saveRequest();
                        const status = document.getElementById('requestStatus');
                        status.textContent = 'Marked complete!';
                        status.style.color = 'var(--green)';
                        setTimeout(() => {
                            status.textContent = '';
                            status.style.color = '';
                        }, 3000);
                    }
                });
            }
        }

        // Crucible functions
        function createBounty() {
            const title = document.getElementById('bountyTitle').value.trim();
            const description = document.getElementById('bountyDesc').value.trim();
            const reward = parseInt(document.getElementById('bountyReward').value) || 50;
            const maxTeams = parseInt(document.getElementById('bountyMaxTeams').value) || 2;
            const mode = document.getElementById('bountyMode').value || 'hybrid';

            if (!title) {
                alert('Please enter a bounty title');
                return;
            }

            fetch('/api/bounties', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    title,
                    description,
                    reward,
                    max_teams: maxTeams,
                    slots: maxTeams,
                    game_mode: mode
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('bountyTitle').value = '';
                    document.getElementById('bountyDesc').value = '';
                    document.getElementById('bountyReward').value = '50';
                    document.getElementById('bountyMaxTeams').value = '2';
                    document.getElementById('bountyMode').value = 'hybrid';
                    loadBounties();
                }
            });
        }

        function loadBounties() {
            fetch('/api/bounties')
                .then(r => r.json())
                .then(bounties => {
                    const container = document.getElementById('bountiesContainer');
                    const countEl = document.getElementById('bountyCount');
                    if (countEl) countEl.textContent = bounties.length > 0 ? `(${bounties.length})` : '';

                    if (bounties.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.7rem;">No active Crucible matches</p>';
                        return;
                    }

                    container.innerHTML = bounties.map(b => {
                        const statusColors = {
                            'open': 'var(--yellow)',
                            'claimed': 'var(--teal)',
                            'completed': 'var(--green)'
                        };
                        const borderColor = statusColors[b.status] || 'var(--border)';
                        const teams = b.teams || [];
                        const teamCount = teams.length;
                        const slots = b.slots || b.max_teams || 1;
                        const overflow = Math.max(0, teamCount - slots);
                        const mode = (b.game_mode || 'hybrid').toUpperCase();
                        const gameName = b.game_name || 'Commons Crucible';
                        const cost = b.cost_tracking || {};
                        const apiCost = cost.api_cost ? `$${cost.api_cost.toFixed(3)}` : '';
                        const sessions = cost.sessions_used || 0;

                        // Build guild submissions display
                        const teamsHtml = teams.length > 0 ? `
                            <div style="margin-top: 0.4rem; padding-top: 0.4rem; border-top: 1px solid var(--border);">
                                <div style="font-size: 0.65rem; color: var(--text-dim); margin-bottom: 0.2rem;">Guild submissions:</div>
                                ${teams.map((t, i) => `
                                    <div style="font-size: 0.7rem; padding: 0.2rem 0; display: flex; justify-content: space-between;">
                                        <span style="color: var(--teal);">${t.identity_name}</span>
                                        <span style="color: var(--text-dim);">${new Date(t.submitted_at).toLocaleDateString()}</span>
                                    </div>
                                `).join('')}
                            </div>
                        ` : '';

                        return `
                            <div class="identity-card" style="margin-bottom: 0.4rem; padding: 0.6rem; border-left: 3px solid ${borderColor};">
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <div style="flex: 1;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--text);">${b.title}</div>
                                        <div style="font-size: 0.65rem; color: var(--text-dim); margin-top: 0.15rem;">
                                            ${gameName} | ${mode} | ${b.status.toUpperCase()}
                                            ${slots > 0 ? ` | Guild slots: ${overflow > 0 ? `${slots} (+${overflow} overflow)` : `${teamCount}/${slots}`}` : ''}
                                        </div>
                                        ${apiCost || sessions ? `
                                            <div style="font-size: 0.6rem; color: var(--purple); margin-top: 0.15rem;">
                                                ${apiCost ? `Cost: ${apiCost}` : ''}${apiCost && sessions ? ' | ' : ''}${sessions ? `Sessions: ${sessions}` : ''}
                                            </div>
                                        ` : ''}
                                    </div>
                                    <div style="color: var(--yellow); font-weight: bold; font-size: 0.85rem;">${b.reward}</div>
                                </div>
                                ${teamsHtml}
                                <div style="display: flex; gap: 0.3rem; margin-top: 0.4rem;">
                                    ${b.status === 'claimed' || (b.status === 'open' && teamCount > 0) ? `
                                        <button onclick="showCompleteBountyModal('${b.id}', ${b.reward}, ${teamCount})"
                                            style="flex: 1; padding: 0.2rem; background: var(--green);
                                                   border: none; color: var(--bg-dark); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.65rem;">
                                            Complete
                                        </button>
                                    ` : ''}
                                    ${teamCount > 0 ? `
                                        <button onclick="viewBountySubmissions('${b.id}', '${b.title.replace(/'/g, "\\'")}')"
                                            style="flex: 1; padding: 0.2rem; background: var(--bg-dark);
                                                   border: 1px solid var(--teal); color: var(--teal); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.65rem;">
                                            View (${teamCount})
                                        </button>
                                    ` : ''}
                                    ${b.status === 'open' && teamCount === 0 ? `
                                        <button onclick="deleteBounty('${b.id}')"
                                            style="flex: 1; padding: 0.2rem; background: var(--bg-dark);
                                                   border: 1px solid var(--red); color: var(--red); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.65rem;">
                                            Cancel
                                        </button>
                                    ` : ''}
                                </div>
                            </div>
                        `;
                    }).join('');
                });
        }

        function showCompleteBountyModal(bountyId, defaultReward, teamCount) {
            const hasMultipleTeams = teamCount > 1;

            const modal = document.createElement('div');
            modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; padding: 2rem;';
            modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

            modal.innerHTML = `
                <div style="background: var(--bg-card); padding: 2rem; border-radius: 12px; max-width: 400px; width: 100%;">
                    <h3 style="color: var(--teal); margin-bottom: 1rem;">Complete Bounty</h3>

                    ${hasMultipleTeams ? `
                        <p style="font-size: 0.85rem; color: var(--text-dim); margin-bottom: 1rem;">
                            This bounty has ${teamCount} competing guilds. Set rewards for each placement:
                        </p>
                        <div style="margin-bottom: 1rem;">
                            <label style="font-size: 0.8rem; color: var(--text-dim);">Winner Reward:</label>
                            <input type="number" id="winnerReward" value="${defaultReward}" min="0"
                                   style="width: 100%; padding: 0.5rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--yellow); border-radius: 4px; margin-top: 0.3rem;">
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <label style="font-size: 0.8rem; color: var(--text-dim);">Runner-up Reward:</label>
                            <input type="number" id="runnerUpReward" value="${Math.floor(defaultReward * 0.5)}" min="0"
                                   style="width: 100%; padding: 0.5rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--yellow); border-radius: 4px; margin-top: 0.3rem;">
                        </div>
                    ` : `
                        <p style="font-size: 0.85rem; color: var(--text-dim); margin-bottom: 1rem;">
                            Award <span style="color: var(--yellow);">${defaultReward}</span> tokens for completing this bounty.
                        </p>
                    `}

                    <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                        <button onclick="this.closest('[style*=position]').remove()"
                                style="flex: 1; padding: 0.5rem; background: var(--bg-hover); border: 1px solid var(--border); color: var(--text); border-radius: 4px; cursor: pointer;">
                            Cancel
                        </button>
                        <button onclick="completeBounty('${bountyId}', ${hasMultipleTeams})"
                                style="flex: 1; padding: 0.5rem; background: var(--green); border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-weight: 600;">
                            Complete & Pay Out
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        function completeBounty(bountyId, hasMultipleTeams = false) {
            let body = {};

            if (hasMultipleTeams) {
                const winnerReward = parseInt(document.getElementById('winnerReward').value) || 0;
                const runnerUpReward = parseInt(document.getElementById('runnerUpReward').value) || 0;
                body = { winner_reward: winnerReward, runner_up_reward: runnerUpReward };
            }

            fetch('/api/bounties/' + bountyId + '/complete', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(body)
            })
            .then(r => r.json())
            .then(data => {
                // Close modal if open
                const modal = document.querySelector('[style*="position: fixed"][style*="z-index: 1000"]');
                if (modal) modal.remove();

                if (data.success) {
                    loadBounties();
                    // Show detailed completion message with costs
                    const cost = data.cost_tracking || {};
                    let message = 'Bounty completed!';
                    if (data.total_distributed) message += ` ${data.total_distributed} tokens distributed.`;
                    if (cost.api_cost) message += `\\nTotal API Cost: $${cost.api_cost.toFixed(4)}`;
                    if (cost.sessions_used) message += `\\nSessions Used: ${cost.sessions_used}`;
                    if (cost.duration_hours) message += `\\nDuration: ${cost.duration_hours} hours`;
                    alert(message);
                } else {
                    alert('Error: ' + (data.reason || data.error || 'Unknown error'));
                }
            });
        }

        function deleteBounty(bountyId) {
            if (!confirm('Delete this bounty?')) return;

            fetch('/api/bounties/' + bountyId, {method: 'DELETE'})
                .then(r => r.json())
                .then(data => {
                    if (data.success) loadBounties();
                });
        }

        function viewBountySubmissions(bountyId, bountyTitle) {
            fetch('/api/bounties/' + bountyId + '/submissions')
                .then(r => r.json())
                .then(data => {
                    if (!data.success) {
                        alert('Error loading submissions');
                        return;
                    }

                    const submissions = data.submissions || [];
                    const modal = document.createElement('div');
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; padding: 2rem;';
                    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

                    modal.innerHTML = `
                        <div style="background: var(--bg-card); padding: 1.5rem; border-radius: 12px; max-width: 500px; width: 100%; max-height: 80vh; overflow-y: auto;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <h3 style="color: var(--teal); margin: 0;">Submissions: ${bountyTitle}</h3>
                                <button onclick="this.closest('[style*=position]').remove()" style="background: none; border: none; color: var(--text-dim); font-size: 1.5rem; cursor: pointer;">&times;</button>
                            </div>

                            ${submissions.length === 0 ? `
                                <p style="color: var(--text-dim);">No submissions yet.</p>
                            ` : submissions.map((s, i) => `
                                <div style="background: var(--bg-dark); padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid var(--teal);">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                        <span style="font-weight: 600; color: var(--teal);">${s.identity_name}</span>
                                        <span style="font-size: 0.75rem; color: var(--text-dim);">${new Date(s.submitted_at).toLocaleString()}</span>
                                    </div>
                                    ${s.description ? `<p style="font-size: 0.85rem; color: var(--text); margin-bottom: 0.4rem;">${s.description}</p>` : ''}
                                    ${s.slot_multiplier !== undefined ? `
                                        <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.4rem;">
                                            Slot ${s.slot_index || '?'}${s.slots ? `/${s.slots}` : ''} | x${(Number(s.slot_multiplier) || 0).toFixed(2)}${s.slot_reason ? ` (${s.slot_reason})` : ''}
                                        </div>
                                    ` : ''}
                                    ${s.artifacts && s.artifacts.length > 0 ? `
                                        <div style="font-size: 0.75rem; color: var(--text-dim);">
                                            <span>Artifacts:</span>
                                            <div style="margin-top: 0.3rem;">
                                                ${Array.from(new Set(s.artifacts)).map(a => `<a href="#" onclick="viewArtifact('${a}'); return false;" style="color: var(--purple); margin-right: 0.5rem;">${a.split('/').pop()}</a>`).join('')}
                                            </div>
                                        </div>
                                    ` : ''}
                                    ${s.notes ? `<p style="font-size: 0.75rem; color: var(--text-dim); margin-top: 0.5rem; font-style: italic;">${s.notes}</p>` : ''}
                                </div>
                            `).join('')}
                        </div>
                    `;
                    document.body.appendChild(modal);
                });
        }

        // Chat Rooms functions
        let latestChatRooms = [];
        let currentChatModalRoomId = null;
        let chatRoomModalPoller = null;

        function loadChatRooms() {
            fetch('/api/chatrooms')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('chatRoomsContainer');
                    const countEl = document.getElementById('chatRoomsCount');

                    if (!data.success || !data.rooms || data.rooms.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.8rem;">No chat rooms yet. Rooms appear when residents start chatting!</p>';
                        countEl.textContent = '';
                        latestChatRooms = [];
                        return;
                    }

                    latestChatRooms = data.rooms;
                    const totalMessages = data.rooms.reduce((sum, r) => sum + (r.message_count || 0), 0);
                    countEl.textContent = `(${totalMessages} messages)`;

                    container.innerHTML = data.rooms.map(room => `
                        <div class="chat-room-card">
                            <div class="chat-room-card-header">
                                <span style="font-size: 1.05rem;">${room.icon || '💬'}</span>
                                <span style="flex: 1;">
                                    <span style="font-weight: 650; color: var(--teal);">${escapeHtml(room.name || room.id)}</span>
                                    <span style="font-size: 0.7rem; color: var(--text-dim); margin-left: 0.3rem;">(${room.message_count || 0})</span>
                                </span>
                                <span style="font-size: 0.65rem; color: var(--text-dim);">
                                    ${room.latest_timestamp ? new Date(room.latest_timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '--:--'}
                                </span>
                                <button class="chat-room-open-btn" onclick="openChatRoomModalById('${encodeURIComponent(room.id)}')">Popout</button>
                            </div>
                            <div style="margin-top: 0.45rem; font-size: 0.73rem; color: var(--text-dim);">
                                ${escapeHtml(room.description || 'No description')}
                            </div>
                            <div style="margin-top: 0.35rem; font-size: 0.75rem; color: var(--text); line-height: 1.35;">
                                ${escapeHtml(room.latest_preview || 'No messages yet.')}
                            </div>
                        </div>
                    `).join('');
                });
        }

        function openChatRoomModalById(encodedRoomId) {
            const roomId = decodeURIComponent(encodedRoomId || '');
            const room = latestChatRooms.find(r => r.id === roomId) || { id: roomId, name: roomId, icon: '💬' };
            openChatRoomModal(room.id, room.name, room.icon);
        }

        function openChatRoomModal(roomId, roomName, roomIcon) {
            currentChatModalRoomId = roomId;
            const modal = document.getElementById('chatRoomModal');
            document.getElementById('chatRoomModalTitle').textContent = roomName || roomId || 'Chat Room';
            document.getElementById('chatRoomModalSubtitle').textContent = roomId || '';
            document.getElementById('chatRoomModalIcon').textContent = roomIcon || '💬';
            modal.classList.add('open');
            loadChatRoomModalMessages();
            if (chatRoomModalPoller) clearInterval(chatRoomModalPoller);
            chatRoomModalPoller = setInterval(() => {
                if (currentChatModalRoomId) loadChatRoomModalMessages(false);
            }, 4000);
        }

        function closeChatRoomModal() {
            currentChatModalRoomId = null;
            const modal = document.getElementById('chatRoomModal');
            if (modal) modal.classList.remove('open');
            if (chatRoomModalPoller) {
                clearInterval(chatRoomModalPoller);
                chatRoomModalPoller = null;
            }
        }

        function handleChatRoomModalBackdrop(event) {
            if (event && event.target && event.target.id === 'chatRoomModal') {
                closeChatRoomModal();
            }
        }

        function escapeHtml(value) {
            const div = document.createElement('div');
            div.textContent = String(value || '');
            return div.innerHTML;
        }

        function loadChatRoomModalMessages(scrollToBottom=true) {
            if (!currentChatModalRoomId) return;
            const container = document.getElementById('chatRoomModalMessages');
            const meta = document.getElementById('chatRoomModalMeta');
            if (!container || !meta) return;

            const nearBottom = (container.scrollHeight - container.scrollTop - container.clientHeight) < 40;

            fetch('/api/chatrooms/' + encodeURIComponent(currentChatModalRoomId))
                .then(r => r.json())
                .then(data => {
                    if (!data.success || !data.messages || data.messages.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.8rem; font-style: italic;">No messages in this room yet.</p>';
                        meta.textContent = '0 messages';
                        return;
                    }

                    meta.textContent = `${data.messages.length} recent messages`;
                    container.innerHTML = data.messages.map(msg => {
                        const time = msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
                        const mood = msg.mood ? ` <span style="opacity: 0.6;">(${msg.mood})</span>` : '';
                        const replyTo = msg.reply_to ? `<div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.2rem;">↳ replying to ${escapeHtml(String(msg.reply_to).slice(0, 24))}</div>` : '';
                        const linkedContent = linkifyFilePaths(msg.content || '');

                        return `
                            <div class="chat-msg">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                                    <span style="font-weight: 600; color: var(--teal); font-size: 0.84rem;">${escapeHtml(msg.author_name || 'Unknown')}${mood}</span>
                                    <span style="font-size: 0.68rem; color: var(--text-dim);">${time}</span>
                                </div>
                                ${replyTo}
                                <div style="font-size: 0.9rem; color: var(--text); line-height: 1.45;">${linkedContent}</div>
                            </div>
                        `;
                    }).join('');

                    if (scrollToBottom || nearBottom) {
                        container.scrollTop = container.scrollHeight;
                    }
                });
        }

        function loadArtifacts() {
            fetch('/api/artifacts/list')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('artifactsContainer');
                    const countEl = document.getElementById('artifactCount');

                    if (!data.success || !data.artifacts || data.artifacts.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No artifacts yet</p>';
                        countEl.textContent = '';
                        return;
                    }

                    const artifacts = data.artifacts.slice(0, 20);
                    countEl.textContent = `(${artifacts.length})`;
                    container.innerHTML = artifacts.map(artifact => {
                        const safePath = String(artifact.path || '').replace(/'/g, "\\'");
                        const iconByType = {
                            journal: 'J',
                            creative_work: 'W',
                            community_doc: 'D',
                            skill: 'S',
                        };
                        const icon = iconByType[artifact.type] || 'F';
                        const modified = artifact.modified
                            ? new Date(artifact.modified).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
                            : '';

                        return `
                            <div class="identity-card" style="margin-bottom: 0.4rem; padding: 0.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.5rem;">
                                    <span style="color: var(--purple); font-size: 0.75rem; font-weight: 600;">${icon}</span>
                                    <a href="#" onclick="viewArtifact('${safePath}'); return false;"
                                       style="flex: 1; color: var(--teal); text-decoration: underline; font-size: 0.75rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                        ${artifact.name}
                                    </a>
                                    <span style="color: var(--text-dim); font-size: 0.65rem;">${modified}</span>
                                </div>
                                <div style="margin-top: 0.2rem; color: var(--text-dim); font-size: 0.65rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                    ${artifact.path}
                                </div>
                            </div>
                        `;
                    }).join('');
                });
        }

        function renderInsightCards(cards) {
            const container = document.getElementById('insightCards');
            if (!container) return;
            if (!Array.isArray(cards) || cards.length === 0) {
                container.innerHTML = `
                    <details class="insight-card" open>
                        <summary>
                            <div class="insight-label">Stats</div>
                            <div class="insight-value">--</div>
                            <div class="insight-sub">No metrics available</div>
                        </summary>
                        <div class="insight-detail">Insights API returned no cards.</div>
                    </details>
                `;
                return;
            }
            container.innerHTML = cards.map(card => {
                const tone = card.tone ? String(card.tone) : '';
                const details = Array.isArray(card.details) ? card.details.join('\n') : '';
                return `
                    <details class="insight-card">
                        <summary>
                            <div class="insight-label">${escapeHtml(card.label || 'Metric')}</div>
                            <div class="insight-value ${escapeHtml(tone)}">${escapeHtml(card.headline || '--')}</div>
                            <div class="insight-sub">${escapeHtml(card.subline || '')}</div>
                        </summary>
                        <div class="insight-detail">${escapeHtml(details)}</div>
                    </details>
                `;
            }).join('');
        }

        function loadSwarmInsights() {
            fetch('/api/insights')
                .then(r => r.json())
                .then(data => {
                    if (!data.success) return;
                    renderInsightCards(data.metric_cards || []);
                })
                .catch(() => {
                    renderInsightCards([
                        {
                            label: 'Stats',
                            headline: 'OFFLINE',
                            subline: 'Insights API unavailable',
                            tone: 'bad',
                            details: ['Unable to load stats right now.'],
                        },
                    ]);
                });
        }

        // Initial load
        setupDayVibe();
        setInterval(setupDayVibe, 60000); // Update every minute (for time-based changes)
        fetch('/api/identities').then(r => r.json()).then(updateIdentities);
        loadWorkerStatus();
        loadRequest();
        loadMessages();
        loadDmThreads();
        loadBounties();
        loadChatRooms();
        loadArtifacts();
        loadStopStatus();
        loadRuntimeSpeed();
        loadUiSettings();
        refreshCreativeSeed();
        loadGroqKeyStatus();
        loadSwarmInsights();
        loadQueueView();
        loadMailboxData();
        loadQuestProgress();
        updateLogEmptyState();

        // Refresh bounties, spawner status, and chat rooms periodically
        setInterval(loadBounties, 10000);
        setInterval(loadWorkerStatus, 5000);
        setInterval(loadDmThreads, 10000);
        setInterval(loadChatRooms, 15000);  // Refresh chat rooms every 15 seconds
        setInterval(loadArtifacts, 15000);
        setInterval(loadStopStatus, 5000);
        setInterval(loadRuntimeSpeed, 15000);
        setInterval(loadGroqKeyStatus, 30000);
        setInterval(loadSwarmInsights, 10000);
        setInterval(loadQueueView, 5000);
        setInterval(loadMailboxData, 5000);
        setInterval(loadQuestProgress, 5000);
    </script>
</body>
</html>
'''


class LogWatcher(FileSystemEventHandler):
    """Watch action log file for changes."""

    def __init__(self, socketio_instance):
        self.socketio = socketio_instance
        self.last_position = 0

    def on_modified(self, event):
        if event.src_path.endswith('action_log.jsonl'):
            self.send_new_entries()

    def send_new_entries(self):
        global last_log_position
        if not ACTION_LOG.exists():
            return

        with open(ACTION_LOG, 'r') as f:
            f.seek(last_log_position)
            new_lines = f.readlines()
            last_log_position = f.tell()

        for line in new_lines:
            try:
                entry = json.loads(line.strip())
                self.socketio.emit('log_entry', entry)
            except:
                pass


def calculate_identity_level(sessions: int) -> int:
    """Calculate identity level based on sessions (ARPG-style progression)."""
    # Level formula: sqrt(sessions) rounded down, minimum level 1
    import math
    return max(1, int(math.sqrt(sessions)))


def calculate_respec_cost(sessions: int) -> int:
    """Calculate respec cost based on sessions (ARPG-style: cheap early, expensive later)."""
    # Formula from swarm_enrichment.py: BASE (10) + (sessions * SCALE (3))
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

                    identities.append({
                        'id': identity_id,
                        'name': data.get('name', 'Unknown'),
                        'tokens': balances.get(identity_id, {}).get('tokens', 0),
                        'sessions': sessions,
                        'tasks_completed': data.get('tasks_completed', 0),
                        'profile_display': profile.get('display'),
                        'profile_thumbnail_html': profile.get('thumbnail_html'),
                        'profile_thumbnail_css': profile.get('thumbnail_css'),
                        'traits': core.get('personality_traits', []),
                        'values': core.get('core_values', []),
                        'level': calculate_identity_level(sessions),
                        'respec_cost': calculate_respec_cost(sessions),
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


@socketio.on('connect')
def on_socket_connect():
    """Reject websocket connections from non-loopback clients."""
    if not _is_loopback_host(_request_source_host()):
        return False
    return None


@app.route('/api/identities')
def api_identities():
    return jsonify(get_identities())


@app.route('/api/creative_seed')
def api_creative_seed():
    """Return a fresh hybrid creativity seed."""
    return jsonify({"success": True, "seed": _fresh_hybrid_seed()})


@app.route('/api/identities/create', methods=['POST'])
def api_create_identity():
    """Create a resident-authored identity from UI input (creative, no presets)."""
    data = request.json or {}

    name = str(data.get("name", "")).strip()
    summary = str(data.get("summary", "")).strip()
    identity_statement = str(data.get("identity_statement", "")).strip()
    creativity_seed = str(data.get("creativity_seed", "")).strip().upper()
    creator_identity_id = str(data.get("creator_identity_id", "")).strip()
    creator_resident_id = str(data.get("creator_resident_id", "")).strip()

    if not name:
        return jsonify({"success": False, "error": "name is required"}), 400
    if len(name) > 80:
        return jsonify({"success": False, "error": "name is too long (max 80 chars)"}), 400
    if len(summary) > 600:
        return jsonify({"success": False, "error": "summary is too long (max 600 chars)"}), 400
    if not creativity_seed:
        creativity_seed = _fresh_hybrid_seed()
    if not CREATIVE_SEED_PATTERN.fullmatch(creativity_seed):
        return jsonify({"success": False, "error": "invalid creativity seed format"}), 400
    if not _reserve_creativity_seed(creativity_seed):
        return jsonify({"success": False, "error": "creativity seed already used; request a fresh one"}), 409

    if creator_identity_id:
        creator_path = IDENTITIES_DIR / f"{creator_identity_id}.json"
        if not creator_path.exists():
            return jsonify({"success": False, "error": "creator_identity_id not found"}), 400

    if not creator_identity_id:
        creator_identity_id = "resident_identity_forge"
    if not creator_resident_id:
        creator_resident_id = f"resident_{creator_identity_id}"

    affinities = data.get("affinities")
    if not isinstance(affinities, list):
        affinities = _parse_csv_items(data.get("traits_csv", ""))
    else:
        affinities = _parse_csv_items(",".join(str(x) for x in affinities))

    values = data.get("values")
    if not isinstance(values, list):
        values = _parse_csv_items(data.get("values_csv", ""))
    else:
        values = _parse_csv_items(",".join(str(x) for x in values))

    activities = data.get("preferred_activities")
    if not isinstance(activities, list):
        activities = _parse_csv_items(data.get("activities_csv", ""))
    else:
        activities = _parse_csv_items(",".join(str(x) for x in activities))

    try:
        identity_id = resident_onboarding.create_identity_from_resident(
            workspace=WORKSPACE,
            creator_resident_id=creator_resident_id,
            creator_identity_id=creator_identity_id,
            name=name,
            summary=summary or "Creative self-authored resident identity.",
            affinities=affinities,
            values=values,
            preferred_activities=activities,
            identity_statement=identity_statement or summary,
            creativity_seed=creativity_seed,
        )
    except ValueError as exc:
        message = str(exc)
        retry = "TRY AGAIN" in message or "IDENTITY_NAME_RULE_VIOLATION" in message
        return jsonify({"success": False, "error": message, "retry": retry}), 400
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

    identity_file = IDENTITIES_DIR / f"{identity_id}.json"
    identity_name = name
    if identity_file.exists():
        try:
            with open(identity_file, "r", encoding="utf-8") as f:
                identity_name = json.load(f).get("name", name)
        except Exception:
            pass

    return jsonify(
        {
            "success": True,
            "identity": {
                "id": identity_id,
                "name": identity_name,
                "summary": summary,
                "creator_identity_id": creator_identity_id,
                "creativity_seed": creativity_seed,
            },
        }
    )


@app.route('/api/identity/<identity_id>/profile')
def api_identity_profile(identity_id):
    """Get detailed profile for an identity including journals and stats."""
    identity_file = IDENTITIES_DIR / f"{identity_id}.json"

    if not identity_file.exists():
        return jsonify({'error': 'identity_not_found'})

    try:
        with open(identity_file) as f:
            data = json.load(f)

        attrs = data.get('attributes', {})
        profile = attrs.get('profile', {})
        core = attrs.get('core', {})
        mutable = attrs.get('mutable', {})

        # Get journals for this identity
        journals_dir = WORKSPACE / ".swarm" / "journals"
        journals = []
        if journals_dir.exists():
            for jf in sorted(journals_dir.glob(f"{identity_id}*.md"), reverse=True)[:10]:
                try:
                    with open(jf, 'r', encoding='utf-8') as jfile:
                        content = jfile.read()
                        journals.append({
                            'filename': jf.name,
                            'preview': content[:200] + '...' if len(content) > 200 else content,
                            'modified': datetime.fromtimestamp(jf.stat().st_mtime).isoformat()
                        })
                except:
                    pass

        # Get recent actions for this identity from log
        recent_actions = []
        if ACTION_LOG.exists():
            try:
                with open(ACTION_LOG, 'r') as f:
                    lines = f.readlines()[-200:]  # Last 200 entries
                    for line in reversed(lines):
                        try:
                            entry = json.loads(line.strip())
                            if entry.get('actor') == identity_id:
                                recent_actions.append({
                                    'timestamp': entry.get('timestamp'),
                                    'type': entry.get('action_type'),
                                    'action': entry.get('action'),
                                    'detail': entry.get('detail')
                                })
                                if len(recent_actions) >= 20:
                                    break
                        except:
                            pass
            except:
                pass

        # Calculate some stats
        task_success_rate = 0
        if data.get('tasks_completed', 0) + data.get('tasks_failed', 0) > 0:
            task_success_rate = data.get('tasks_completed', 0) / (data.get('tasks_completed', 0) + data.get('tasks_failed', 0)) * 100

        # Get chat history for this identity
        chat_history = []
        messages_file = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
        responses_file = WORKSPACE / ".swarm" / "messages_from_human.json"
        if messages_file.exists():
            responses = {}
            if responses_file.exists():
                try:
                    with open(responses_file) as rf:
                        responses = json.load(rf)
                except:
                    pass
            try:
                with open(messages_file, 'r') as mf:
                    for line in mf:
                        if line.strip():
                            msg = json.loads(line)
                            if msg.get('from_id') == identity_id:
                                chat_entry = {
                                    'id': msg.get('id'),
                                    'content': msg.get('content'),
                                    'type': msg.get('type', 'message'),
                                    'sent_at': msg.get('timestamp'),
                                    'response': responses.get(msg.get('id'), {}).get('response'),
                                    'responded_at': responses.get(msg.get('id'), {}).get('responded_at')
                                }
                                chat_history.append(chat_entry)
            except:
                pass

        sessions = data.get('sessions_participated', 0)
        return jsonify({
            'identity_id': identity_id,
            'name': data.get('name'),
            'created_at': data.get('created_at'),
            'sessions': sessions,
            'tasks_completed': data.get('tasks_completed', 0),
            'tasks_failed': data.get('tasks_failed', 0),
            'task_success_rate': round(task_success_rate, 1),
            'level': calculate_identity_level(sessions),
            'respec_cost': calculate_respec_cost(sessions),
            'profile': profile,
            'core_summary': {
                'traits': core.get('personality_traits', []),
                'values': core.get('core_values', []),
                'identity_statement': core.get('identity_statement'),
                'communication_style': core.get('communication_style')
            },
            'mutable': {
                'likes': mutable.get('likes', []),
                'dislikes': mutable.get('dislikes', []),
                'current_interests': mutable.get('current_interests', []),
                'current_mood': mutable.get('current_mood'),
                'working_style': mutable.get('working_style')
            },
            'recent_memories': data.get('memories', [])[-5:],
            'journals': journals,
            'recent_actions': recent_actions,
            'expertise': data.get('expertise', {}),
            'chat_history': chat_history[-20:]  # Last 20 messages
        })

    except Exception as e:
        return jsonify({'error': str(e)})


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


def get_worker_status():
    """Return swarm worker pool status."""
    out = {
        "running": False,
        "pid": None,
        "pids": [],
        "running_count": 0,
        "target_count": 1,
        "started_at": None,
    }
    if not WORKER_PROCESS_FILE.exists():
        return out
    try:
        with open(WORKER_PROCESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_pids = _normalize_swarm_pids(data)
        alive = [pid for pid in all_pids if _worker_process_alive(pid)]
        started_at = data.get("started_at")
        try:
            target_count = _clamp_int(
                data.get("target_count", len(all_pids) or RESIDENT_COUNT_MIN),
                RESIDENT_COUNT_MIN,
                RESIDENT_COUNT_MAX,
            )
        except (TypeError, ValueError):
            target_count = max(RESIDENT_COUNT_MIN, len(all_pids) or RESIDENT_COUNT_MIN)
        if alive:
            out["running"] = True
            out["pid"] = alive[0]
            out["pids"] = alive
            out["running_count"] = len(alive)
            out["target_count"] = target_count
            out["started_at"] = started_at
            return out
    except Exception:
        pass
    # Process dead or missing; clear stale file
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
        if int(status.get("target_count", 1)) == requested_count:
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


def get_runtime_speed():
    """Get current worker-loop wait seconds."""
    payload = {
        "wait_seconds": DEFAULT_RUNTIME_SPEED_SECONDS,
        "updated_at": None,
    }
    if not RUNTIME_SPEED_FILE.exists():
        return payload
    try:
        with open(RUNTIME_SPEED_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        wait = float(data.get("wait_seconds", DEFAULT_RUNTIME_SPEED_SECONDS))
        payload["wait_seconds"] = max(0.0, min(300.0, wait))
        payload["updated_at"] = data.get("updated_at")
    except Exception:
        pass
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
                "summary": cp["summary"][:120],
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


def enqueue_human_suggestion(request_text: str) -> str | None:
    """Turn a human suggestion into an executable queue task."""
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
    min_budget = float(ui_settings.get("task_min_budget", 0.05))
    max_budget = float(ui_settings.get("task_max_budget", max(min_budget, 0.10)))
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
    data = request.json
    request_text = data.get('request', '')
    result = save_human_request(request_text)
    task_id = enqueue_human_suggestion(request_text)
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


@app.route('/api/messages')
def api_get_messages():
    """Get messages from identities with any responses."""
    messages = get_messages_to_human()
    responses = get_human_responses()

    # Attach responses to messages
    for msg in messages:
        msg_id = msg.get('id', '')
        if msg_id in responses:
            msg['response'] = responses[msg_id]
        msg['human_username'] = get_human_username()

    # Return most recent first
    return jsonify(list(reversed(messages[-MESSAGES_FEED_MAX:])))


@app.route('/api/messages/respond', methods=['POST'])
def api_respond_to_message():
    """Send a response to an identity message."""
    data = request.json
    message_id = data.get('message_id')
    response = data.get('response')

    if not message_id or not response:
        return jsonify({'success': False, 'error': 'Missing message_id or response'})

    result = save_human_response(message_id, response)
    return jsonify({'success': True, 'responded_at': result['responded_at']})


@app.route('/api/messages/send', methods=['POST'])
def api_send_message_to_resident():
    """Send a new outbound message from human to one resident (or broadcast)."""
    data = request.get_json(force=True, silent=True) or {}
    content = str(data.get("content") or "").strip()
    to_id = str(data.get("to_id") or "").strip()
    to_name = str(data.get("to_name") or "").strip()
    if not content:
        return jsonify({"success": False, "error": "content is required"}), 400
    if len(content) > 1200:
        return jsonify({"success": False, "error": "content too long (max 1200 chars)"}), 400

    sender_name = get_human_username()
    safe_target = to_name or to_id or "all residents"
    try:
        chat_line = f"[to {safe_target}] {content}"
        _dm_enrichment().post_discussion_message(
            identity_id="human_operator",
            identity_name=sender_name,
            content=chat_line,
            room="human_async",
            mood="async",
            importance=4,
        )
        if to_id:
            _dm_enrichment().post_direct_message(
                sender_id="human_operator",
                sender_name=sender_name,
                recipient_id=to_id,
                content=content,
                importance=4,
            )
            _dm_enrichment().grant_free_time(
                to_id,
                MAILBOX_MESSAGE_BONUS_TOKENS,
                reason="human_message_received",
            )
            followup_task_id = f"mailbox-inbox-{to_id}-{int(time.time() * 1000)}"
            _enqueue_identity_task(
                task_id=followup_task_id,
                identity_id=to_id,
                prompt=(
                    "I received a new direct message from the human operator. "
                    f"Message: {content}\n"
                    "Process it, coordinate with other residents if useful, and take the best immediate next action."
                ),
                min_budget=0.03,
                max_budget=0.20,
            )
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

    outbox_payload = {
        "id": f"human_out_{int(time.time() * 1000)}",
        "message_id": None,
        "to_id": to_id or "",
        "to_name": safe_target,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "sender_name": sender_name,
        "source": "new_message",
    }
    _append_human_outbox_message(outbox_payload)
    return jsonify({"success": True, "message": outbox_payload})


@app.route('/api/messages/mailbox')
def api_mailbox_messages():
    """
    Aggregate inbox/outbox threads for phone-style mailbox UI.
    """
    inbound = get_messages_to_human()
    responses = get_human_responses()
    outbox = get_human_outbox_messages()
    identities = get_identities()
    identity_map = {str(i.get("id") or ""): str(i.get("name") or i.get("id") or "") for i in identities}

    threads = {}
    now = datetime.now().isoformat()

    def _touch_thread(thread_id: str, thread_name: str):
        if thread_id not in threads:
            threads[thread_id] = {
                "id": thread_id,
                "name": thread_name or thread_id or "Resident",
                "unread": 0,
                "last_at": "",
                "last_preview": "",
                "messages": [],
            }
        return threads[thread_id]

    for msg in inbound:
        from_id = str(msg.get("from_id") or "").strip()
        from_name = str(msg.get("from_name") or "").strip() or identity_map.get(from_id) or from_id or "resident"
        thread_id = from_id or f"name::{from_name.lower()}"
        thread = _touch_thread(thread_id, from_name)
        timestamp = str(msg.get("timestamp") or now)
        content = str(msg.get("content") or "")
        responded = str(msg.get("id") or "") in responses
        thread["messages"].append(
            {
                "direction": "in",
                "id": str(msg.get("id") or ""),
                "timestamp": timestamp,
                "content": content,
                "author_name": from_name,
                "responded": responded,
            }
        )
        if not responded:
            thread["unread"] += 1
        if timestamp >= (thread.get("last_at") or ""):
            thread["last_at"] = timestamp
            thread["last_preview"] = content[:120]

    for msg in outbox:
        to_id = str(msg.get("to_id") or "").strip()
        to_name = str(msg.get("to_name") or "").strip() or identity_map.get(to_id) or to_id or "all residents"
        thread_id = to_id or "__broadcast__"
        thread = _touch_thread(thread_id, to_name)
        timestamp = str(msg.get("timestamp") or now)
        content = str(msg.get("content") or "")
        thread["messages"].append(
            {
                "direction": "out",
                "id": str(msg.get("id") or ""),
                "timestamp": timestamp,
                "content": content,
                "author_name": str(msg.get("sender_name") or get_human_username()),
                "responded": True,
            }
        )
        if timestamp >= (thread.get("last_at") or ""):
            thread["last_at"] = timestamp
            thread["last_preview"] = f"↗ {content[:116]}"

    thread_list = list(threads.values())
    for t in thread_list:
        t["messages"] = sorted(t.get("messages", []), key=lambda m: str(m.get("timestamp") or ""))
    thread_list.sort(key=lambda t: str(t.get("last_at") or ""), reverse=True)

    unread_total = sum(int(t.get("unread", 0)) for t in thread_list)
    return jsonify(
        {
            "success": True,
            "unread_count": unread_total,
            "threads": [
                {
                    "id": t.get("id"),
                    "name": t.get("name"),
                    "unread": t.get("unread", 0),
                    "last_at": t.get("last_at"),
                    "last_preview": t.get("last_preview", ""),
                }
                for t in thread_list
            ],
            "thread_messages": {str(t.get("id")): t.get("messages", []) for t in thread_list},
            "identities": [
                {"id": str(i.get("id") or ""), "name": str(i.get("name") or i.get("id") or "")}
                for i in identities
                if i.get("id")
            ],
            "human_name": get_human_username(),
        }
    )


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
            "title": title[:140],
            "prompt": prompt[:2000],
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


def _extract_usd_cost(detail: str) -> float:
    matches = re.findall(r"\$([0-9]+(?:\.[0-9]+)?)", str(detail or ""))
    if not matches:
        return 0.0
    try:
        return float(matches[-1])
    except (TypeError, ValueError):
        return 0.0


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

    action_entries = _read_jsonl_tail(ACTION_LOG, max_lines=60000)
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
    ops_summary = {
        "api_calls_24h": api_calls_24h,
        "api_cost_24h": round(api_cost_24h, 6),
        "safety_blocks_24h": safety_blocks_24h,
        "errors_24h": errors_24h,
    }

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
        "headline": f"${api_cost_24h:.3f}",
        "subline": f"{api_calls_24h} API calls",
        "tone": cost_tone,
        "details": [
            f"API cost (24h): ${api_cost_24h:.6f}",
            f"API calls (24h): {api_calls_24h}",
            f"Safety blocks (24h): {safety_blocks_24h}",
            f"Errors (24h): {errors_24h}",
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
    """Return queue tasks for UI visualization."""
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    open_tasks = queue.get('tasks', []) if isinstance(queue.get('tasks'), list) else []
    completed = queue.get('completed', []) if isinstance(queue.get('completed'), list) else []
    failed = queue.get('failed', []) if isinstance(queue.get('failed'), list) else []
    # Show latest entries for compact UI.
    return jsonify({
        'success': True,
        'open': open_tasks[:50],
        'completed': completed[-25:],
        'failed': failed[-25:],
    })


@app.route('/api/system/fresh_reset', methods=['POST'])
def api_system_fresh_reset():
    """
    Wipe stale runtime state and return system to clean baseline.

    Safety: refuses while swarm is running.
    """
    worker = get_worker_status()
    if worker.get("running"):
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

        # Remove transient mutable files.
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
            ACTION_LOG,
            EXECUTION_LOG,
            API_AUDIT_LOG_FILE,
        ]
        for file_path in transient_files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except OSError:
                pass

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
                                content = msg.get('content', '')[:50]
                                latest_preview = f"{author}: {content}..."
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
    """Return a recent tail of action-log entries for UI backfill."""
    limit = request.args.get('limit', 500, type=int)
    safe_limit = max(1, min(5000, int(limit)))
    entries = _read_jsonl_tail(ACTION_LOG, max_lines=safe_limit)
    return jsonify({'success': True, 'entries': entries[-safe_limit:]})


def background_watcher():
    """Background thread to watch log file and push updates."""
    watcher = LogWatcher(socketio)

    # Initial load of existing entries
    if ACTION_LOG.exists():
        watcher.send_new_entries()

    # Polling is more stable on some macOS/python combinations than FSEvents.
    use_native = str(os.environ.get("VIVARIUM_USE_NATIVE_WATCHDOG", "")).strip().lower() in {"1", "true", "yes"}
    observer = Observer() if use_native else PollingObserver(timeout=1.0)
    observer.schedule(watcher, str(ACTION_LOG.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()
    observer.join()


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
    print("=" * 60)

    # Start background threads (only in active reloader child process).
    if _should_start_background_threads(HOT_RELOAD_ENABLED):
        threading.Thread(target=background_watcher, daemon=True).start()
        threading.Thread(target=push_identities_periodically, daemon=True).start()

    socketio.run(
        app,
        host=CONTROL_PANEL_HOST,
        port=CONTROL_PANEL_PORT,
        debug=HOT_RELOAD_ENABLED,
        use_reloader=HOT_RELOAD_ENABLED,
        allow_unsafe_werkzeug=True,
    )
