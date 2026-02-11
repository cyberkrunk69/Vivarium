import pytest
from vivarium.runtime.control_panel.blueprints_registry import BLUEPRINT_SPECS


def test_all_blueprints_registered():
    """Every blueprint in specs is valid"""
    assert len(BLUEPRINT_SPECS) > 0, "No blueprints registered"

    for blueprint, url_prefix in BLUEPRINT_SPECS:
        assert blueprint is not None, "Blueprint is None"
        assert hasattr(blueprint, "name"), "Blueprint missing name"
        assert hasattr(blueprint, "url_prefix") or url_prefix is not None, (
            f"Blueprint {blueprint.name} has no URL prefix"
        )


def test_no_duplicate_blueprint_names():
    """All blueprint names are unique"""
    names = [bp.name for bp, _ in BLUEPRINT_SPECS]
    assert len(names) == len(set(names)), f"Duplicate blueprint names: {names}"


def test_blueprint_routes_accessible(client, localhost_kwargs):
    """Sample routes from each blueprint are accessible"""
    # Test a route from each major blueprint
    test_routes = [
        "/api/identities",
        "/api/messages/mailbox",
        "/api/logs/recent",
        "/api/queue/state",
        "/api/bounties",
        "/api/quests/status",
        "/api/worker/status",
        "/api/groq_key",
        "/api/stop_status",
        "/api/runtime_speed",
    ]

    for route in test_routes:
        response = client.get(route, **localhost_kwargs)
        # Should not 404 (means blueprint not registered)
        assert response.status_code != 404, f"Blueprint route not found: {route}"
        # Should not 500 (means blueprint crashed)
        assert response.status_code != 500, f"Blueprint crashed: {route}"
