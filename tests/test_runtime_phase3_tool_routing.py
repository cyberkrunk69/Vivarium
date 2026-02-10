import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime import tool_router
import worker
from skills.skill_registry import compose_skills, register_skill


class _RouteResult:
    def __init__(self, tool, route: str, confidence: float):
        self.tool = tool
        self.route = route
        self.confidence = confidence

    @property
    def found(self) -> bool:
        return self.tool is not None


def test_tool_router_imports_and_routes_exact_skill(tmp_path):
    register_skill(
        name="phase3_exact_skill",
        code="def phase3_exact_skill():\n    return 'ok'",
        description="Exact route probe for phase 3",
        keywords=["exact", "phase3"],
    )
    store_path = tmp_path / "tool_store.json"
    store_path.write_text("{}", encoding="utf-8")

    router = tool_router.ToolRouter(tool_store_path=str(store_path))
    result = router.route("Please run phase3_exact_skill on this task.")

    assert result.found is True
    assert result.route == "exact"
    assert result.tool["name"] == "phase3_exact_skill"


def test_skill_registry_can_compose_multiple_skills():
    register_skill(
        name="phase3_compose_alpha",
        code="def phase3_compose_alpha(x):\n    return x + 1",
        description="Alpha compose skill",
        keywords=["alpha", "compose"],
    )
    register_skill(
        name="phase3_compose_beta",
        code="def phase3_compose_beta(x):\n    return x * 2",
        description="Beta compose skill",
        keywords=["beta", "compose"],
    )

    composed = compose_skills(["phase3_compose_alpha", "phase3_compose_beta"])
    assert composed is not None
    assert composed["name"].startswith("composed_")
    assert composed["components"] == ["phase3_compose_alpha", "phase3_compose_beta"]
    assert "Skill: phase3_compose_alpha" in composed["code"]
    assert "Skill: phase3_compose_beta" in composed["code"]


def test_worker_execute_task_injects_tool_context(monkeypatch):
    captured = {}

    class _StubRouter:
        def route(self, prompt, context=None):
            return _RouteResult(
                tool={
                    "name": "phase3_injected_tool",
                    "description": "Reusable helper for routing",
                    "code": "def phase3_injected_tool():\n    return 'ok'",
                },
                route="semantic",
                confidence=0.91,
            )

    class _FakeResponse:
        status_code = 200

        @staticmethod
        def json():
            return {
                "result": "done",
                "model": "llama-3.1-8b-instant",
                "safety_report": {"passed": True},
            }

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def post(self, url, json, headers=None):
            captured["url"] = url
            captured["payload"] = json
            captured["headers"] = headers
            return _FakeResponse()

    monkeypatch.setattr(worker, "WORKER_TOOL_ROUTER", _StubRouter())
    monkeypatch.setattr(worker, "validate_model_id", lambda _model: None)
    monkeypatch.setattr(
        worker,
        "_run_worker_safety_check",
        lambda task_id, prompt, command, mode: (
            True,
            {"passed": True, "task_id": task_id, "checks": {}},
        ),
    )
    monkeypatch.setattr(worker.httpx, "Client", _FakeClient)

    result = worker.execute_task(
        {
            "id": "task_phase3_route",
            "prompt": "Improve authentication tests",
            "mode": "llm",
            "model": "llama-3.1-8b-instant",
        },
        api_endpoint="http://127.0.0.1:8420",
    )

    assert result["status"] == "completed"
    assert result["tool_route"] == "semantic"
    assert result["tool_name"] == "phase3_injected_tool"
    assert result["tool_confidence"] == pytest.approx(0.91)
    assert captured["url"].endswith("/cycle")
    assert captured["headers"]["X-Vivarium-Internal-Token"]
    assert "RELEVANT TOOL CONTEXT" in captured["payload"]["prompt"]
    assert "phase3_injected_tool" in captured["payload"]["prompt"]
    assert "TASK:\nImprove authentication tests" in captured["payload"]["prompt"]
