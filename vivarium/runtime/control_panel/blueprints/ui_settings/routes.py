"""UI settings blueprint: get/set persisted UI defaults."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint("ui_settings", __name__, url_prefix="/api")


def _app_helpers():
    from vivarium.runtime import control_panel_app as app
    return app.load_ui_settings, app.save_ui_settings


@bp.route("/ui_settings", methods=["GET"])
def api_get_ui_settings():
    """Get persisted UI defaults (local, gitignored)."""
    load_ui_settings, _ = _app_helpers()
    return jsonify({"success": True, **load_ui_settings()})


@bp.route("/ui_settings", methods=["POST"])
def api_set_ui_settings():
    """Persist UI defaults (local, gitignored)."""
    load_ui_settings, save_ui_settings = _app_helpers()
    data = request.get_json(force=True, silent=True) or {}
    allowed = {
        "override_model", "model", "auto_scale", "budget_limit",
        "task_min_budget", "task_max_budget", "resident_count", "human_username",
    }
    updates = {k: data[k] for k in allowed if k in data}
    saved = save_ui_settings(updates)
    return jsonify({"success": True, **saved})
