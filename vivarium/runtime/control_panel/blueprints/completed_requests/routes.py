"""Completed requests blueprint: history of completed collaboration requests."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint("completed_requests", __name__, url_prefix="/api")


def _app_helpers():
    from vivarium.runtime import control_panel_app as app
    return app.get_completed_requests, app.add_completed_request


@bp.route("/completed_requests", methods=["GET"])
def api_get_completed_requests():
    """Get completed requests history."""
    get_completed_requests, _ = _app_helpers()
    return jsonify(get_completed_requests())


@bp.route("/completed_requests", methods=["POST"])
def api_add_completed_request():
    """Mark a request as completed."""
    get_completed_requests, add_completed_request = _app_helpers()
    data = request.json or {}
    request_text = data.get("request", "").strip()
    if not request_text:
        return jsonify({"success": False, "error": "No request text"})
    result = add_completed_request(request_text)
    return jsonify({"success": True, "completed": result})
