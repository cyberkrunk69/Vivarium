"""Stop toggle blueprint: kill switch for runtime (emergency stop)."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, jsonify

bp = Blueprint('stop_toggle', __name__, url_prefix='/api')


def _get_kill_switch_path() -> Path:
    return current_app.config['KILL_SWITCH']


def get_stop_status() -> bool:
    """Check if kill switch is engaged."""
    path = _get_kill_switch_path()
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
                return data.get('halt', False)
        except Exception:
            pass
    return False


def set_stop_status(stopped: bool) -> bool:
    """Set kill switch status."""
    path = _get_kill_switch_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'halt': stopped,
        'reason': 'Manual stop from control panel' if stopped else None,
        'timestamp': datetime.now().isoformat(),
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    return stopped


def _get_reason() -> str | None:
    """Read reason from kill switch file if stopped."""
    path = _get_kill_switch_path()
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
                return data.get('reason')
        except Exception:
            pass
    return None


@bp.route('/stop_status', methods=['GET'])
def api_stop_status():
    """GET /api/stop_status - Check if runtime is stopped."""
    stopped = get_stop_status()
    reason = _get_reason() if stopped else None
    return jsonify({'stopped': stopped, 'reason': reason})


@bp.route('/toggle_stop', methods=['POST'])
def api_toggle_stop():
    """POST /api/toggle_stop - Toggle kill switch."""
    current = get_stop_status()
    new_status = set_stop_status(not current)
    socketio = current_app.config.get('SOCKETIO')
    if socketio:
        socketio.emit('stop_status', {'stopped': new_status})
    return jsonify({'stopped': new_status})
