"""Registry of Flask blueprints for the control panel. Each (bp, url_prefix) is registered on the app."""
from __future__ import annotations

# [BLUEPRINTS_START]
from vivarium.runtime.control_panel.blueprints.artifacts import artifacts_bp
from vivarium.runtime.control_panel.blueprints.bounties import bounties_bp
from vivarium.runtime.control_panel.blueprints.chatrooms import chatrooms_bp
from vivarium.runtime.control_panel.blueprints.completed_requests import completed_requests_bp
from vivarium.runtime.control_panel.blueprints.dm import dm_bp
from vivarium.runtime.control_panel.blueprints.groq_key import groq_key_bp
from vivarium.runtime.control_panel.blueprints.human_request import human_request_bp
from vivarium.runtime.control_panel.blueprints.identities import identities_bp
from vivarium.runtime.control_panel.blueprints.insights import insights_bp
from vivarium.runtime.control_panel.blueprints.logs import logs_bp
from vivarium.runtime.control_panel.blueprints.messages import messages_bp
from vivarium.runtime.control_panel.blueprints.quests import quests_bp
from vivarium.runtime.control_panel.blueprints.queue import queue_bp
from vivarium.runtime.control_panel.blueprints.rollback import rollback_bp
from vivarium.runtime.control_panel.blueprints.runtime_speed import runtime_speed_bp
from vivarium.runtime.control_panel.blueprints.spawner import spawner_bp
from vivarium.runtime.control_panel.blueprints.stop_toggle import stop_toggle_bp
from vivarium.runtime.control_panel.blueprints.ui_settings import ui_settings_bp
from vivarium.runtime.control_panel.blueprints.worker import worker_bp
from vivarium.runtime.control_panel.blueprints.root import root_bp
from vivarium.runtime.control_panel.blueprints.system import system_bp

BLUEPRINT_SPECS: list[tuple] = [
    (root_bp, ""),
    (artifacts_bp, ""),
    (bounties_bp, ""),
    (chatrooms_bp, ""),
    (completed_requests_bp, ""),
    (dm_bp, ""),
    (groq_key_bp, ""),
    (human_request_bp, ""),
    (identities_bp, ""),
    (insights_bp, ""),
    (logs_bp, ""),
    (messages_bp, ""),
    (quests_bp, ""),
    (queue_bp, ""),
    (rollback_bp, ""),
    (runtime_speed_bp, ""),
    (spawner_bp, ""),
    (stop_toggle_bp, ""),
    (ui_settings_bp, ""),
    (worker_bp, ""),
    (system_bp, ""),
]


def register_blueprints(app):
    """Register all control panel blueprints on the Flask app."""
    for bp, url_prefix in BLUEPRINT_SPECS:
        kwargs = {"url_prefix": url_prefix} if url_prefix else {}
        app.register_blueprint(bp, **kwargs)
