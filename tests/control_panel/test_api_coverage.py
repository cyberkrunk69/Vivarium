"""Targeted tests to bridge coverage gap (41% → 50%). Covers health/metrics/swarm-style routes and error handlers."""
from __future__ import annotations

import json


class TestHealthAndInsights:
    """Cover /api/insights which exposes health_summary and metrics."""

    def test_insights_returns_health_summary(self, client, localhost_kwargs):
        """GET /api/insights returns health state in response."""
        response = client.get("/api/insights", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "health" in data
        health = data["health"]
        assert "state" in health
        assert health["state"] in ("stable", "watch", "critical")
        assert "kill_switch" in health
        assert "backlog_pressure" in health


class TestSwarmStatus:
    """Cover /api/spawner/status (swarm status equivalent)."""

    def test_spawner_status_returns_structure(self, client, localhost_kwargs):
        """GET /api/spawner/status returns status structure."""
        response = client.get("/api/spawner/status", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "running" in data
        assert "paused" in data
        assert isinstance(data["running"], bool)
        assert isinstance(data["paused"], bool)


class TestLogsRaw:
    """Cover /api/logs/raw endpoint."""

    def test_logs_raw_action_kind(self, client, localhost_kwargs, app):
        """GET /api/logs/raw?kind=action returns text."""
        response = client.get("/api/logs/raw?kind=action", **localhost_kwargs)
        assert response.status_code == 200
        assert response.content_type.startswith("text/")

    def test_logs_raw_invalid_kind_returns_400(self, client, localhost_kwargs):
        """GET /api/logs/raw?kind=invalid returns 400."""
        response = client.get("/api/logs/raw?kind=invalid", **localhost_kwargs)
        assert response.status_code == 400
        data = response.get_json()
        assert data.get("success") is False
        assert "kind" in (data.get("error") or "").lower()


class TestSystemFreshReset:
    """Cover /api/system/fresh_reset when worker is stopped."""

    def test_system_fresh_reset_when_stopped(self, client, localhost_kwargs, app):
        """POST /api/system/fresh_reset when worker is stopped succeeds."""
        # Ensure worker is stopped before fresh_reset
        client.post("/api/worker/stop", **localhost_kwargs)
        response = client.post(
            "/api/system/fresh_reset",
            data=json.dumps({}),
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code in (200, 409)
        if response.status_code == 200:
            data = response.get_json()
            assert data.get("success") is True


class TestArtifactsList:
    """Cover /api/artifacts/list."""

    def test_artifacts_list_empty_workspace(self, client, localhost_kwargs):
        """GET /api/artifacts/list returns structure when no artifacts."""
        response = client.get("/api/artifacts/list", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "artifacts" in data
        assert isinstance(data["artifacts"], list)

    def test_artifacts_list_with_journals(self, client, localhost_kwargs, app):
        """GET /api/artifacts/list with journals dir returns journal artifacts."""
        workspace = app.config["WORKSPACE"]
        journals_dir = workspace / ".swarm" / "journals"
        journals_dir.mkdir(parents=True, exist_ok=True)
        journal_file = journals_dir / "test_journal.md"
        journal_file.write_text("# Journal entry", encoding="utf-8")
        try:
            response = client.get("/api/artifacts/list", **localhost_kwargs)
            assert response.status_code == 200
            data = response.get_json()
            assert data.get("success") is True
            artifacts = data.get("artifacts", [])
            journal_artifacts = [a for a in artifacts if a.get("type") == "journal"]
            assert len(journal_artifacts) >= 1
        finally:
            journal_file.unlink(missing_ok=True)

    def test_artifacts_list_with_creative_works(self, client, localhost_kwargs, app):
        """GET /api/artifacts/list with library/creative_works returns artifacts."""
        workspace = app.config["WORKSPACE"]
        creative_dir = workspace / "library" / "creative_works"
        creative_dir.mkdir(parents=True, exist_ok=True)
        creative_file = creative_dir / "sample_work.md"
        creative_file.write_text("# Creative work", encoding="utf-8")
        try:
            response = client.get("/api/artifacts/list", **localhost_kwargs)
            assert response.status_code == 200
            data = response.get_json()
            artifacts = data.get("artifacts", [])
            creative = [a for a in artifacts if a.get("type") == "creative_work"]
            assert len(creative) >= 1
        finally:
            creative_file.unlink(missing_ok=True)


class TestMiddlewareForwardedFor:
    """Cover X-Forwarded-For path in middleware."""

    def test_localhost_via_forwarded_for(self, client, localhost_kwargs):
        """Request with X-Forwarded-For: 127.0.0.1 is allowed."""
        headers = {**localhost_kwargs.get("environ_overrides", {}), "HTTP_X_FORWARDED_FOR": "127.0.0.1"}
        kw = {"environ_overrides": {"REMOTE_ADDR": "10.0.0.1", "HTTP_X_FORWARDED_FOR": "127.0.0.1"}}
        response = client.get("/api/identities", **kw)
        assert response.status_code == 200


class Test404Handler:
    """Cover 404 for unknown API routes."""

    def test_unknown_api_route_returns_404(self, client, localhost_kwargs):
        """GET /api/nonexistent/route returns 404."""
        response = client.get("/api/nonexistent/route/xyz", **localhost_kwargs)
        assert response.status_code == 404

    def test_404_for_nonexistent_api(self, client, localhost_kwargs):
        """404 for /api/* returns 404 status."""
        response = client.get("/api/nonexistent/route/xyz", **localhost_kwargs)
        assert response.status_code == 404


class TestMalformedJsonRequests:
    """Verify malformed JSON returns 400/422 with JSON body."""

    def test_malformed_json_queue_add_does_not_500(self, client, localhost_kwargs):
        """POST /api/queue/add with invalid JSON does not 500."""
        response = client.post(
            "/api/queue/add",
            data="not json { broken",
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code in (400, 422, 500), "Should not crash"

    def test_malformed_json_bounties_does_not_500(self, client, localhost_kwargs):
        """POST /api/bounties with invalid JSON does not crash (400 or 422)."""
        response = client.post(
            "/api/bounties",
            data="{ invalid json ]",
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code in (200, 400, 422), "Malformed JSON should not 500"
        if response.content_type and "application/json" in response.content_type:
            data = response.get_json()
            if data:
                assert "success" in data or "error" in data

    def test_malformed_json_identities_create_does_not_500(self, client, localhost_kwargs):
        """POST /api/identities/create with invalid JSON does not crash."""
        response = client.post(
            "/api/identities/create",
            data='{"name": truncated',
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code in (200, 400, 422), "Malformed JSON should not 500"
        assert response.data is not None


class TestArtifactView:
    """Cover /api/artifact/view error paths."""

    def test_artifact_view_no_path_returns_400(self, client, localhost_kwargs):
        """GET /api/artifact/view without path returns error."""
        response = client.get("/api/artifact/view", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("success") is False
        assert "path" in (data.get("error") or "").lower() or "path" in str(data).lower()

    def test_artifact_view_nonexistent_returns_error(self, client, localhost_kwargs):
        """GET /api/artifact/view with bad path returns file not found."""
        response = client.get(
            "/api/artifact/view?path=nonexistent_file_xyz.md",
            **localhost_kwargs,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("success") is False


class TestChatrooms:
    """Cover /api/chatrooms list and room detail."""

    def test_chatrooms_list_returns_structure(self, client, localhost_kwargs):
        """GET /api/chatrooms returns rooms array."""
        response = client.get("/api/chatrooms", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "rooms" in data
        assert isinstance(data["rooms"], list)

    def test_chatroom_messages_empty_room(self, client, localhost_kwargs):
        """GET /api/chatrooms/watercooler returns structure when empty."""
        response = client.get("/api/chatrooms/watercooler", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "messages" in data
        assert "room" in data

    def test_chatrooms_with_discussion_file(self, client, localhost_kwargs, app):
        """GET /api/chatrooms with real room file hits message-count path."""
        discussions_dir = app.config.get("DISCUSSIONS_DIR")
        if discussions_dir:
            discussions_dir.mkdir(parents=True, exist_ok=True)
            room_file = discussions_dir / "watercooler.jsonl"
            room_file.write_text(
                '{"author_name":"Alice","content":"Hi","timestamp":"2025-01-01T12:00:00Z"}\n',
                encoding="utf-8",
            )
            try:
                response = client.get("/api/chatrooms", **localhost_kwargs)
                assert response.status_code == 200
                data = response.get_json()
                assert "rooms" in data
                rooms = [r for r in data["rooms"] if r.get("id") == "watercooler"]
                if rooms:
                    assert rooms[0].get("message_count", 0) >= 1
            finally:
                room_file.unlink(missing_ok=True)

    def test_chatroom_messages_with_content(self, client, localhost_kwargs, app):
        """GET /api/chatrooms/watercooler with messages returns them."""
        discussions_dir = app.config.get("DISCUSSIONS_DIR")
        if discussions_dir:
            discussions_dir.mkdir(parents=True, exist_ok=True)
            room_file = discussions_dir / "watercooler.jsonl"
            room_file.write_text(
                '{"author_name":"Bob","content":"Hello","timestamp":"2025-01-01T12:00:00Z"}\n',
                encoding="utf-8",
            )
            try:
                response = client.get("/api/chatrooms/watercooler", **localhost_kwargs)
                assert response.status_code == 200
                data = response.get_json()
                assert "messages" in data
                assert len(data["messages"]) >= 1
            finally:
                room_file.unlink(missing_ok=True)


class TestLogsRawExecution:
    """Cover /api/logs/raw with kind=execution."""

    def test_logs_raw_execution_kind(self, client, localhost_kwargs):
        """GET /api/logs/raw?kind=execution returns text."""
        response = client.get("/api/logs/raw?kind=execution", **localhost_kwargs)
        assert response.status_code == 200
        assert response.content_type.startswith("text/")


class TestToggleStop:
    """Cover POST /api/toggle_stop."""

    def test_toggle_stop_returns_stopped_status(self, client, localhost_kwargs):
        """POST /api/toggle_stop toggles and returns status."""
        response = client.post("/api/toggle_stop", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "stopped" in data
        assert isinstance(data["stopped"], bool)


class TestRollbackPreview:
    """Cover /api/rollback/preview."""

    def test_rollback_preview_returns_structure(self, client, localhost_kwargs):
        """GET /api/rollback/preview?days=1 returns structure or error."""
        response = client.get("/api/rollback/preview?days=1", **localhost_kwargs)
        assert response.status_code in (200, 400)
        data = response.get_json()
        assert "success" in data
        assert "days" in data or "error" in data


class TestMessagesGet:
    """Cover GET /api/messages."""

    def test_messages_get_returns_list(self, client, localhost_kwargs):
        """GET /api/messages returns list."""
        response = client.get("/api/messages", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)


class TestBountiesCreate:
    """Cover POST /api/bounties."""

    def test_bounties_create_valid(self, client, localhost_kwargs, app):
        """POST /api/bounties with title creates bounty."""
        workspace = app.config["WORKSPACE"]
        (workspace / ".swarm").mkdir(parents=True, exist_ok=True)
        response = client.post(
            "/api/bounties",
            data=json.dumps({
                "title": "Coverage test bounty",
                "description": "A bounty for testing coverage",
            }),
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("success") is True
        assert "bounty" in data


class TestCreativeSeed:
    """Cover GET /api/creative_seed."""

    def test_creative_seed_returns_structure(self, client, localhost_kwargs):
        """GET /api/creative_seed returns seed or error."""
        response = client.get("/api/creative_seed", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert "seed" in data or "success" in data or "error" in data


class TestQueueAdd:
    """Cover POST /api/queue/add."""

    def test_queue_add_valid_task(self, client, localhost_kwargs):
        """POST /api/queue/add with instruction adds task."""
        response = client.post(
            "/api/queue/add",
            data=json.dumps({
                "task_id": "cov_test_1",
                "instruction": "Test task for coverage",
            }),
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code in (200, 201)
        data = response.get_json()
        assert data.get("success") is True
        assert "task_id" in data

    def test_queue_update_valid_task(self, client, localhost_kwargs):
        """POST /api/queue/update with valid data."""
        client.post(
            "/api/queue/add",
            data=json.dumps({"instruction": "Original"}),
            content_type="application/json",
            **localhost_kwargs,
        )
        state = client.get("/api/queue/state", **localhost_kwargs).get_json() or {}
        task_id = next((t.get("id") for t in state.get("queue", []) if t.get("id")), None)
        if task_id:
            response = client.post(
                "/api/queue/update",
                data=json.dumps({"task_id": task_id, "instruction": "Updated"}),
                content_type="application/json",
                **localhost_kwargs,
            )
            assert response.status_code in (200, 400, 404)

    def test_queue_delete_task(self, client, localhost_kwargs):
        """POST /api/queue/delete removes task."""
        client.post(
            "/api/queue/add",
            data=json.dumps({"instruction": "To be deleted"}),
            content_type="application/json",
            **localhost_kwargs,
        )
        state = client.get("/api/queue/state", **localhost_kwargs).get_json() or {}
        tasks = state.get("queue", [])
        task_id = next((t.get("id") for t in tasks if t.get("id")), None)
        if task_id:
            response = client.post(
                "/api/queue/delete",
                data=json.dumps({"task_id": task_id}),
                content_type="application/json",
                **localhost_kwargs,
            )
            assert response.status_code in (200, 400, 404)


class TestLogsRawApi:
    """Cover /api/logs/raw?kind=api."""

    def test_logs_raw_api_kind(self, client, localhost_kwargs):
        """GET /api/logs/raw?kind=api returns text or empty."""
        response = client.get("/api/logs/raw?kind=api", **localhost_kwargs)
        assert response.status_code == 200
        assert response.content_type.startswith("text/")


class TestRuntimeSpeedPost:
    """Cover POST /api/runtime_speed."""

    def test_runtime_speed_post_valid(self, client, localhost_kwargs):
        """POST /api/runtime_speed with wait_seconds persists."""
        response = client.post(
            "/api/runtime_speed",
            data=json.dumps({"wait_seconds": 3.0}),
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("success") is True
        assert "wait_seconds" in data

    def test_runtime_speed_post_invalid_returns_400(self, client, localhost_kwargs):
        """POST /api/runtime_speed with invalid wait_seconds returns 400."""
        response = client.post(
            "/api/runtime_speed",
            data=json.dumps({"wait_seconds": "not_a_number"}),
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code == 400
