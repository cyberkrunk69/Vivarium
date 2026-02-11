import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime import worker_runtime as worker
from vivarium.runtime.runtime_contract import normalize_queue


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

        def post(self, url, json, headers=None):
            captured["url"] = url
            captured["payload"] = json
            captured["headers"] = headers
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
    assert captured["url"].endswith("/cycle")
    assert captured["headers"]["X-Vivarium-Internal-Token"]
    assert captured["payload"]["prompt"].startswith("##INTENT goal=Ship feature set")


def test_worker_execute_task_injects_enrichment_context(monkeypatch):
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

        def post(self, url, json, headers=None):
            captured["url"] = url
            captured["payload"] = json
            captured["headers"] = headers
            return _FakeResponse()

    class _StubResidentContext:
        resident_id = "resident_context"

        class _Identity:
            identity_id = "identity_context"
            name = "Nova"

        identity = _Identity()

        @staticmethod
        def apply_to_prompt(prompt: str) -> str:
            return f"WAKEUP\n{prompt}"

    class _StubEnrichment:
        @staticmethod
        def get_morning_messages(identity_id: str):
            assert identity_id == "identity_context"
            return "MORNING_MESSAGES"

        @staticmethod
        def get_discussion_context(identity_id: str, identity_name: str):
            assert identity_id == "identity_context"
            assert identity_name == "Nova"
            return "DISCUSSION_CONTEXT"

        @staticmethod
        def get_enrichment_context(identity_id: str, identity_name: str):
            assert identity_id == "identity_context"
            assert identity_name == "Nova"
            return "ENRICHMENT_CONTEXT"

    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", None)
    monkeypatch.setattr(worker, "WORKER_TOOL_ROUTER", None)
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", _StubEnrichment())
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
            "id": "task_phase4_enrichment",
            "prompt": "Summarize the current state.",
            "mode": "llm",
            "model": "llama-3.1-8b-instant",
        },
        api_endpoint="http://127.0.0.1:8420",
        resident_ctx=_StubResidentContext(),
    )

    assert result["status"] == "completed"
    rendered_prompt = captured["payload"]["prompt"]
    assert "WAKEUP" in rendered_prompt
    assert "MORNING_MESSAGES" in rendered_prompt
    assert "DISCUSSION_CONTEXT" in rendered_prompt
    assert "ENRICHMENT_CONTEXT" in rendered_prompt


def test_worker_execute_task_posts_discussion_update(monkeypatch):
    captured = {}

    class _FakeResponse:
        status_code = 200

        @staticmethod
        def json():
            return {
                "result": "Implemented doc update and aligned API wording.",
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

    class _StubResidentContext:
        resident_id = "resident_context"

        class _Identity:
            identity_id = "identity_context"
            name = "Nova"

        identity = _Identity()

        @staticmethod
        def apply_to_prompt(prompt: str) -> str:
            return prompt

    class _StubEnrichment:
        def __init__(self):
            self.posts = []

        @staticmethod
        def get_morning_messages(identity_id: str):
            return ""

        @staticmethod
        def get_discussion_context(identity_id: str, identity_name: str):
            return ""

        @staticmethod
        def get_enrichment_context(identity_id: str, identity_name: str):
            return ""

        @staticmethod
        def get_discussion_messages(room: str, limit: int = 8):
            return [{"id": "chat_prev_1", "author_id": "identity_other"}]

        def post_discussion_message(self, **kwargs):
            self.posts.append(kwargs)
            return {"success": True}

    enrichment = _StubEnrichment()
    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", None)
    monkeypatch.setattr(worker, "WORKER_TOOL_ROUTER", None)
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", enrichment)
    monkeypatch.setattr(worker, "AUTO_DISCUSSION_UPDATES", True)
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
            "id": "task_discussion_update",
            "prompt": "Publish runtime docs update.",
            "mode": "llm",
            "model": "llama-3.1-8b-instant",
        },
        api_endpoint="http://127.0.0.1:8420",
        resident_ctx=_StubResidentContext(),
    )

    assert result["status"] == "completed"
    assert enrichment.posts
    post = enrichment.posts[0]
    assert post["room"] == "town_hall"
    assert post["reply_to"] == "chat_prev_1"
    assert "Task task_discussion_update update" in post["content"]


def test_worker_execute_task_persists_mvp_markdown_artifacts(monkeypatch, tmp_path):
    captured = {}

    class _FakeResponse:
        status_code = 200

        @staticmethod
        def json():
            return {
                "result": "## Proposed Changes\n\n- Add clearer UI event timeline\n- Keep this as docs-only MVP",
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

    class _StubResidentContext:
        resident_id = "resident_docs"

        class _Identity:
            identity_id = "identity_docs"
            name = "Docsmith"

        identity = _Identity()

        @staticmethod
        def apply_to_prompt(prompt: str) -> str:
            return prompt

    journals_dir = tmp_path / ".swarm" / "journals"
    library_docs_dir = tmp_path / "library" / "community_library" / "swarm_docs"
    resident_suggestions_root = tmp_path / "library" / "community_library" / "resident_suggestions"

    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", None)
    monkeypatch.setattr(worker, "WORKER_TOOL_ROUTER", None)
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", None)
    monkeypatch.setattr(worker, "WORKER_MUTABLE_VCS", None)
    monkeypatch.setattr(worker, "MVP_DOCS_ONLY_MODE", True)
    monkeypatch.setattr(worker, "WORKSPACE", tmp_path)
    monkeypatch.setattr(worker, "MVP_JOURNALS_DIR", journals_dir)
    monkeypatch.setattr(worker, "MVP_LIBRARY_DOCS_DIR", library_docs_dir)
    monkeypatch.setattr(worker, "MVP_LIBRARY_RESIDENT_SUGGESTIONS_ROOT", resident_suggestions_root)
    monkeypatch.setattr(worker, "MVP_ARTIFACT_FINGERPRINTS_FILE", tmp_path / "artifact_fingerprints.json")
    monkeypatch.setattr(
        worker,
        "MVP_ALLOWED_DOC_ROOTS",
        (journals_dir, library_docs_dir, resident_suggestions_root),
    )
    monkeypatch.setattr(
        worker,
        "resolve_mutable_path",
        lambda path_token, cwd=None: (
            Path(path_token).resolve()
            if Path(path_token).is_absolute()
            else (Path(cwd or tmp_path) / path_token).resolve()
        ),
    )
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
            "id": "task_docs_only",
            "prompt": "Draft an MVP UI plan without making code changes.",
            "mode": "llm",
            "model": "llama-3.1-8b-instant",
            "doc_path": "library/community_library/swarm_docs/mvp_ui_plan.md",
        },
        api_endpoint="http://127.0.0.1:8420",
        resident_ctx=_StubResidentContext(),
    )

    assert result["status"] == "completed"
    assert "MVP MODE:" in captured["payload"]["prompt"]
    artifacts = result["mvp_markdown_artifacts"]
    assert artifacts["written"] is True
    assert artifacts["doc_path"].endswith("library/community_library/swarm_docs/mvp_ui_plan.md")

    doc_path = Path(artifacts["doc_path"])
    assert doc_path.exists()
    content = doc_path.read_text(encoding="utf-8")
    assert "Proposed Changes" in content

    journal_path = Path(artifacts["journal_path"])
    assert journal_path.exists()
    journal_content = journal_path.read_text(encoding="utf-8")
    assert "Journal Entry: task_docs_only" in journal_content


def test_worker_execute_task_defaults_suggestions_to_resident_library_folder(monkeypatch, tmp_path):
    class _FakeResponse:
        status_code = 200

        @staticmethod
        def json():
            return {
                "result": "## Proposal\n\n- Improve onboarding docs\n- Clarify reward signals",
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
            return _FakeResponse()

    class _StubResidentContext:
        resident_id = "resident_docs"

        class _Identity:
            identity_id = "identity_docs"
            name = "Docsmith"

        identity = _Identity()

        @staticmethod
        def apply_to_prompt(prompt: str) -> str:
            return prompt

    journals_dir = tmp_path / ".swarm" / "journals"
    library_docs_dir = tmp_path / "library" / "community_library" / "swarm_docs"
    resident_suggestions_root = tmp_path / "library" / "community_library" / "resident_suggestions"

    monkeypatch.setattr(worker, "WORKER_INTENT_GATEKEEPER", None)
    monkeypatch.setattr(worker, "WORKER_TOOL_ROUTER", None)
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", None)
    monkeypatch.setattr(worker, "WORKER_MUTABLE_VCS", None)
    monkeypatch.setattr(worker, "MVP_DOCS_ONLY_MODE", True)
    monkeypatch.setattr(worker, "WORKSPACE", tmp_path)
    monkeypatch.setattr(worker, "MVP_JOURNALS_DIR", journals_dir)
    monkeypatch.setattr(worker, "MVP_LIBRARY_DOCS_DIR", library_docs_dir)
    monkeypatch.setattr(worker, "MVP_LIBRARY_RESIDENT_SUGGESTIONS_ROOT", resident_suggestions_root)
    monkeypatch.setattr(worker, "MVP_ARTIFACT_FINGERPRINTS_FILE", tmp_path / "artifact_fingerprints.json")
    monkeypatch.setattr(
        worker,
        "MVP_ALLOWED_DOC_ROOTS",
        (journals_dir, library_docs_dir, resident_suggestions_root),
    )
    monkeypatch.setattr(
        worker,
        "resolve_mutable_path",
        lambda path_token, cwd=None: (
            Path(path_token).resolve()
            if Path(path_token).is_absolute()
            else (Path(cwd or tmp_path) / path_token).resolve()
        ),
    )
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
            "id": "task_docs_default_folder",
            "prompt": "Suggest improvements for UI docs.",
            "mode": "llm",
            "model": "llama-3.1-8b-instant",
        },
        api_endpoint="http://127.0.0.1:8420",
        resident_ctx=_StubResidentContext(),
    )

    assert result["status"] == "completed"
    artifacts = result["mvp_markdown_artifacts"]
    assert artifacts["written"] is True
    assert "library/community_library/resident_suggestions/identity_docs/" in artifacts["doc_path"]
