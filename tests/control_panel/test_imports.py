"""Tests for blueprint import structure — ensure no circular imports with control_panel_app."""
import ast
import pytest
from pathlib import Path

# Project root for path resolution
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_blueprints_import_without_app():
    """Blueprints can be imported without control_panel_app"""
    # This would fail if blueprints import from app at module level
    from vivarium.runtime.control_panel.blueprints.identities import identities_bp
    from vivarium.runtime.control_panel.blueprints.messages import messages_bp
    from vivarium.runtime.control_panel.blueprints.logs import logs_bp
    from vivarium.runtime.control_panel.blueprints.queue import queue_bp
    from vivarium.runtime.control_panel.blueprints.bounties import bounties_bp
    from vivarium.runtime.control_panel.blueprints.quests import quests_bp

    # If we get here, no circular imports at module level
    assert identities_bp.name == "identities"
    assert messages_bp.name == "messages"


def test_routes_use_lazy_imports():
    """Verify lazy import pattern in complex blueprints"""
    import inspect
    from vivarium.runtime.control_panel.blueprints import queue, messages, bounties

    # Check that _helpers functions exist (indicates lazy import pattern)
    for module in [queue, messages, bounties]:
        if hasattr(module.routes, "_queue_helpers"):
            source = inspect.getsource(module.routes._queue_helpers)
            assert "control_panel_app" in source, f"{module} missing lazy import"
        elif hasattr(module.routes, "_app_helpers"):
            source = inspect.getsource(module.routes._app_helpers)
            assert "control_panel_app" in source, f"{module} missing lazy import"


def test_no_app_imports_in_blueprint_modules():
    """Blueprint modules don't import app at module level"""
    blueprints_dir = _PROJECT_ROOT / "vivarium" / "runtime" / "control_panel" / "blueprints"

    for bp_dir in blueprints_dir.iterdir():
        if bp_dir.is_dir() and (bp_dir / "routes.py").exists():
            routes_file = bp_dir / "routes.py"
            source = routes_file.read_text()
            tree = ast.parse(source)

            for stmt in tree.body:
                if isinstance(stmt, ast.ImportFrom):
                    if stmt.module and "control_panel_app" in stmt.module:
                        pytest.fail(
                            f"{routes_file.relative_to(_PROJECT_ROOT)}: "
                            f"module-level import from control_panel_app (line {stmt.lineno}) "
                            "causes circular imports — use lazy import inside a function"
                        )
