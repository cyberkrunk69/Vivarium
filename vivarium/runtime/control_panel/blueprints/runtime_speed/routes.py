"""Runtime speed blueprint: read/write worker-loop wait seconds from file."""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint('runtime_speed', __name__, url_prefix='/api')

REFERENCE_WEEKDAY_NAMES = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


def _get_runtime_speed_file() -> Path:
    return current_app.config['RUNTIME_SPEED_FILE']


def _default_wait_seconds() -> float:
    raw = os.environ.get("VIVARIUM_RUNTIME_WAIT_SECONDS")
    if raw is None:
        return 2.0
    try:
        return max(0.0, float(raw))
    except (TypeError, ValueError):
        return 2.0


def _get_runtime_speed():
    """Get current worker-loop wait seconds and resident day length (scaled with speed)."""
    from vivarium.runtime import resident_onboarding

    cycle_seconds = float(resident_onboarding.get_resident_cycle_seconds())
    cycle_id = int(time.time() // cycle_seconds) if cycle_seconds > 0 else int(time.time())
    weekday_idx = cycle_id % 7
    default_wait = _default_wait_seconds()
    payload = {
        "wait_seconds": default_wait,
        "updated_at": None,
        "current_cycle_id": cycle_id,
        "reference_weekday_index": weekday_idx,
        "reference_weekday_name": REFERENCE_WEEKDAY_NAMES[weekday_idx],
    }
    speed_file = _get_runtime_speed_file()
    if not speed_file.exists():
        payload["cycle_seconds"] = round(cycle_seconds, 1)
        return payload
    try:
        with open(speed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        wait = float(data.get("wait_seconds", default_wait))
        payload["wait_seconds"] = max(0.0, min(300.0, wait))
        payload["updated_at"] = data.get("updated_at")
    except Exception:
        pass
    payload["cycle_seconds"] = round(cycle_seconds, 1)
    return payload


def _save_runtime_speed(wait_seconds: float):
    """Persist worker-loop wait seconds for auditable pacing."""
    clamped = max(0.0, min(300.0, float(wait_seconds)))
    payload = {
        "wait_seconds": clamped,
        "updated_at": datetime.now().isoformat(),
    }
    speed_file = _get_runtime_speed_file()
    speed_file.parent.mkdir(parents=True, exist_ok=True)
    with open(speed_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return payload


@bp.route('/runtime_speed', methods=['GET'])
def get_runtime_speed():
    """GET /api/runtime_speed - Return current speed multiplier and cycle info."""
    payload = _get_runtime_speed()
    # Normalize to contract: success + speed (wait_seconds = inverse of speed)
    speed = 1.0 / max(0.001, float(payload.get("wait_seconds", 2.0)))
    return jsonify({"success": True, "speed": speed, **payload})


@bp.route('/runtime_speed', methods=['POST'])
def set_runtime_speed():
    """POST /api/runtime_speed - Set wait seconds."""
    data = request.json or {}
    raw = data.get("wait_seconds", _default_wait_seconds())
    try:
        wait_seconds = float(raw)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "wait_seconds must be a number"}), 400
    saved = _save_runtime_speed(wait_seconds)
    return jsonify({"success": True, **saved})
