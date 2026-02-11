"""Human request blueprint: get/save human collaboration request."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint("human_request", __name__, url_prefix="/api")


def _app_helpers():
    from vivarium.runtime import control_panel_app as app
    return app.get_human_request, app.save_human_request, app.enqueue_human_suggestion


@bp.route("/human_request", methods=["GET"])
def api_get_human_request():
    get_human_request, _, _ = _app_helpers()
    return jsonify({"request": get_human_request()})


@bp.route("/human_request", methods=["POST"])
def api_save_human_request():
    get_human_request, save_human_request, enqueue_human_suggestion = _app_helpers()
    data = request.get_json(force=True, silent=True) or {}
    request_text = str(data.get("request", ""))
    try:
        result = save_human_request(request_text)
        task_id = enqueue_human_suggestion(request_text)
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
    return jsonify({"success": True, "updated_at": result["updated_at"], "task_id": task_id})
