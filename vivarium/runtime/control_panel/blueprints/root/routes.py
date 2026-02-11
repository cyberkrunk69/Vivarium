"""Root blueprint: index and favicon."""
from __future__ import annotations

from flask import Blueprint, render_template_string

from vivarium.runtime.control_panel.frontend_template import CONTROL_PANEL_HTML

bp = Blueprint("root", __name__)


@bp.route("/")
def index():
    return render_template_string(CONTROL_PANEL_HTML)


@bp.route("/favicon.ico")
def favicon():
    return ("", 204)
