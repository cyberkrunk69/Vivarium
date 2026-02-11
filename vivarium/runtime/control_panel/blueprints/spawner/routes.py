"""Spawner blueprint: status, start, pause, resume, kill, and config endpoints."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime

from flask import Blueprint, current_app, jsonify

bp = Blueprint("spawner", __name__, url_prefix="/api")


def _spawner_helpers():
    """Lazy import from control_panel_app when spawner is re-enabled.
    Expects: _load_queue, _save_queue, _trigger_spawn, _is_spawner_running
    """
    from vivarium.runtime.control_panel_app import (
        _load_queue,
        _save_queue,
        _trigger_spawn,
        _is_spawner_running,
    )
    return _load_queue, _save_queue, _trigger_spawn, _is_spawner_running


def _get_spawner_paths():
    """Get spawner paths from app config."""
    WORKSPACE = current_app.config["WORKSPACE"]
    return (
        WORKSPACE / ".swarm" / "spawner_process.json",
        WORKSPACE / ".swarm" / "spawner_config.json",
        WORKSPACE,
    )


def _get_spawner_status():
    """Get current spawner process status."""
    SPAWNER_PROCESS_FILE, SPAWNER_CONFIG_FILE, WORKSPACE = _get_spawner_paths()
    status = {
        "running": False,
        "paused": False,
        "pid": None,
        "started_at": None,
        "config": None,
    }

    if SPAWNER_PROCESS_FILE.exists():
        try:
            with open(SPAWNER_PROCESS_FILE) as f:
                data = json.load(f)
                status["pid"] = data.get("pid")
                status["started_at"] = data.get("started_at")
                status["running"] = data.get("running", False)

                if status["pid"] and status["running"]:
                    try:
                        result = subprocess.run(
                            ["tasklist", "/FI", f'PID eq {status["pid"]}'],
                            capture_output=True,
                            text=True,
                        )
                        if str(status["pid"]) not in result.stdout:
                            status["running"] = False
                    except Exception:
                        pass
        except Exception:
            pass

    pause_file = WORKSPACE / "PAUSE"
    if pause_file.exists():
        status["paused"] = True

    if SPAWNER_CONFIG_FILE.exists():
        try:
            with open(SPAWNER_CONFIG_FILE) as f:
                status["config"] = json.load(f)
        except Exception:
            pass

    return status


def _save_spawner_process(pid: int, running: bool, config: dict = None):
    """Save spawner process info."""
    SPAWNER_PROCESS_FILE, _, _ = _get_spawner_paths()
    SPAWNER_PROCESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "pid": pid,
        "running": running,
        "started_at": datetime.now().isoformat(),
        "config": config,
    }
    with open(SPAWNER_PROCESS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _save_spawner_config(config: dict):
    """Save spawner configuration."""
    _, SPAWNER_CONFIG_FILE, _ = _get_spawner_paths()
    SPAWNER_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    config["updated_at"] = datetime.now().isoformat()
    with open(SPAWNER_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def _sanitize_spawner_start_payload(data: dict):
    sessions = data.get("sessions", 3)
    budget_limit = data.get("budget_limit", 1.0)
    auto_scale = bool(data.get("auto_scale", False))
    model = str(data.get("model", "llama-3.3-70b-versatile")).strip()

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


@bp.route("/spawner/status", methods=["GET"])
def get_spawner_status():
    """GET /api/spawner/status - Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        "running": False,
        "paused": False,
        "pid": None,
        "config": None,
        "golden_path_only": True,
        "message": "Golden path enforced: run queue tasks through vivarium.runtime.worker_runtime.",
    })


@bp.route("/spawner/start", methods=["POST"])
def start_spawner():
    """POST /api/spawner/start - Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        "success": False,
        "golden_path_only": True,
        "error": "Detached spawner path is disabled. Use queue.json + python -m vivarium.runtime.worker_runtime run.",
    }), 410


@bp.route("/spawner/pause", methods=["POST"])
def pause_spawner():
    """POST /api/spawner/pause - Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        "success": False,
        "golden_path_only": True,
        "error": "Detached spawner path is disabled. Use runtime safety controls only.",
    }), 410


@bp.route("/spawner/resume", methods=["POST"])
def resume_spawner():
    """POST /api/spawner/resume - Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        "success": False,
        "golden_path_only": True,
        "error": "Detached spawner path is disabled. Use runtime safety controls only.",
    }), 410


@bp.route("/spawner/kill", methods=["POST"])
def kill_spawner():
    """POST /api/spawner/kill - Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        "success": False,
        "golden_path_only": True,
        "error": "Detached spawner path is disabled. Use runtime safety controls only.",
    }), 410


@bp.route("/spawner/config", methods=["POST"])
def update_spawner_config():
    """POST /api/spawner/config - Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        "success": False,
        "golden_path_only": True,
        "error": "Detached spawner path is disabled. Configuration updates are ignored.",
    }), 410
