import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import worker
from runtime_contract import normalize_queue


class _StubIntent:
    def __init__(self, original_text: str):
        self.goal = "Ship feature set"
        self.constraints = []
        self.preferences = []
        self.anti_goals = []
        self.clarifications = []
        self.original_text = original_text
        self.extracted_at = "2026-02-09T00:00:00"
        self.confidence = 0.9

    def to_dict(self):
        return {
            "goal": self.goal,
            "constraints": self.constraints,
            "preferences": self.preferences,
            "anti_goals": self.anti_goals,
            "clarifications": self.clarifications,
            "original_text": self.original_text,
            "extracted_at": self.extracted_at,
            "confidence": self.confidence,
        }


class _StubGatekeeper:
    def extract_intent(self, prompt: str):
        return _StubIntent(prompt)

    def inject_into_prompt(self, prompt: str, intent: _StubIntent) -> str:
        return f"##INTENT goal={intent.goal}\n{prompt}"


def test_phase4_gut_check_identifies_multi_clause_prompt():
    gut_check = worker._phase4_gut_check(
        "Implement auth API, add integration tests, and then update deployment docs."
    )
    assert gut_check["should_decompose"] is True
    assert gut_check["complexity_score"] >= 2
    assert "sequencing_connectors" in gut_check["signals"] or "compound_clauses" in gut_check["signals"]


def test_phase4_gut_check_identifies_comma_enumeration_prompt():
    gut_check = worker._phase4_gut_check(
        "Implement auth API, add integration tests, update deployment docs."
    )
    assert gut_check["should_decompose"] is True
    assert "comma_enumeration" in gut_check["signals"]


def test_phase4_feature_breakdown_splits_comma_delimited_actions():
    features = worker._phase4_feature_breakdown(
        "Implement auth API, add integration tests, update deployment docs.",
        "Ship feature set",
    )
    assert "Implement auth API" in features
    assert "add integration tests" in features
    assert "update deployment docs" in features


def test_phase4_feature_breakdown_preserves_descriptive_comma_clause():
    features = worker._phase4_feature_breakdown(
        "Implement auth API, with OAuth2 support and refresh tokens.",
        "Ship feature set",
    )
    assert any(feature.startswith("Implement auth API") for feature in features)
    assert all(not feature.lower().startswith("with oauth2 support") for feature in features)


def test_phase4_plan_compiles_subtasks_with_dependencies(monkeypatch, tmp_path):
    queue_path = tmp_path / "queue.json"
    monkeypatch.setattr(worker, "QUEUE_FILE", queue_path)
    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", _StubGatekeeper())

    queue = normalize_queue(
        {
            "tasks": [
                {
                    "id": "task_phase4_parent",
                    "prompt": "Create login endpoint and add integration tests, then update docs.",
                    "min_budget": 0.12,
                    "max_budget": 0.30,
                    "intensity": "high",
                }
            ]
        }
    )
    queue_path.write_text(json.dumps(queue), encoding="utf-8")

    task = queue["tasks"][0]
    plan = worker._maybe_compile_phase4_plan(task, queue)
    assert plan is not None
    assert plan["subtasks_added"] >= 2

    updated_queue = normalize_queue(json.loads(queue_path.read_text(encoding="utf-8")))
    tasks_by_id = {entry["id"]: entry for entry in updated_queue["tasks"]}
    parent = tasks_by_id["task_phase4_parent"]

    subtask_ids = parent["phase4_plan"]["subtasks"]
    assert len(subtask_ids) >= 2
    assert set(subtask_ids).issubset(set(parent["depends_on"]))
    assert parent["phase4_planned"] is True
    assert parent["phase4_intent"]["goal"] == "Ship feature set"

    first_subtask = tasks_by_id[subtask_ids[0]]
    second_subtask = tasks_by_id[subtask_ids[1]]
    assert first_subtask["phase4_generated"] is True
    assert first_subtask["phase4_parent_task"] == "task_phase4_parent"
    assert second_subtask["depends_on"] == [subtask_ids[0]]


def test_phase4_plan_uses_comma_delimited_feature_splitting(monkeypatch, tmp_path):
    queue_path = tmp_path / "queue.json"
    monkeypatch.setattr(worker, "QUEUE_FILE", queue_path)
    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", _StubGatekeeper())

    queue = normalize_queue(
        {
            "tasks": [
                {
                    "id": "task_phase4_comma_parent",
                    "prompt": "Implement auth API, add integration tests, update deployment docs.",
                    "min_budget": 0.12,
                    "max_budget": 0.30,
                    "intensity": "high",
                }
            ]
        }
    )
    queue_path.write_text(json.dumps(queue), encoding="utf-8")

    task = queue["tasks"][0]
    plan = worker._maybe_compile_phase4_plan(task, queue)
    assert plan is not None
    assert "add integration tests" in plan["features"]
    assert "update deployment docs" in plan["features"]
    assert plan["subtasks_added"] >= 3


def test_worker_execute_task_injects_intent_context(monkeypatch):
    captured = {}

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

        def post(self, url, json):
            captured["url"] = url
            captured["payload"] = json
            return _FakeResponse()

    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", _StubGatekeeper())
    monkeypatch.setattr(worker, "WORKER_TOOL_ROUTER", None)
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
            "id": "task_phase4_intent",
            "prompt": "Implement cache invalidation and then update tests.",
            "mode": "llm",
            "model": "llama-3.1-8b-instant",
        },
        api_endpoint="http://127.0.0.1:8420",
    )

    assert result["status"] == "completed"
    assert captured["url"].endswith("/grind")
    assert captured["payload"]["prompt"].startswith("##INTENT goal=Ship feature set")
