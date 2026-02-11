"""Worker blueprint: start, stop, and status for the queue worker pool."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint('worker', __name__, url_prefix='/api')


def _worker_helpers():
    """Lazy import from control_panel_app to avoid circular imports."""
    from vivarium.runtime.control_panel_app import (
        _is_worker_running,
        _start_worker_pool,
        _stop_worker_pool,
        _load_worker_process,
        _save_worker_process,
    )
    return (
        _is_worker_running,
        _start_worker_pool,
        _stop_worker_pool,
        _load_worker_process,
        _save_worker_process,
    )


@bp.route('/worker/status', methods=['GET'])
def api_worker_status():
    """GET /api/worker/status - Return worker pool status."""
    _is_running, _start, _stop, _load, _save = _worker_helpers()
    status = _load()
    return jsonify({
        "success": True,
        "running": status.get("running", False),
        "managed": status.get("running_source") == "managed",
        "pid": status.get("pid"),
        "pids": status.get("pids", []),
        "unmanaged_pids": status.get("unmanaged_pids", []),
        "running_count": status.get("running_count", 0),
        "target_count": status.get("target_count", 1),
        "started_at": status.get("started_at"),
        "running_source": status.get("running_source"),
    })


@bp.route('/worker/start', methods=['POST'])
def api_worker_start():
    """POST /api/worker/start - Start the queue worker pool."""
    _is_running, _start, _stop, _load, _save = _worker_helpers()
    body = request.get_json(force=True, silent=True) or {}
    requested_count = body.get("resident_count")  # None => _start uses load_ui_settings default
    result = _start(requested_count)
    if result.get("success"):
        return jsonify(result)
    return jsonify(result), 500


@bp.route('/worker/stop', methods=['POST'])
def api_worker_stop():
    """POST /api/worker/stop - Stop the worker pool."""
    _is_running, _start, _stop, _load, _save = _worker_helpers()
    result = _stop()
    return jsonify(result)
