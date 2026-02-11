"""Registry of Flask blueprints for the control panel. Each (bp, url_prefix) is registered on the app."""
from __future__ import annotations

BLUEPRINT_SPECS: list[tuple] = []

# [BLUEPRINTS_START]
from vivarium.runtime.control_panel.blueprints.identities import identities_bp
from vivarium.runtime.control_panel.blueprints.logs import logs_bp
from vivarium.runtime.control_panel.blueprints.messages import messages_bp

BLUEPRINT_SPECS.append((identities_bp, ""))
BLUEPRINT_SPECS.append((messages_bp, ""))
BLUEPRINT_SPECS.append((logs_bp, ""))
