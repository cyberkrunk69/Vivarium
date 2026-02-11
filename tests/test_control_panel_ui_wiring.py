import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime import control_panel_app as cp
from vivarium.runtime import swarm_enrichment


def _localhost_request_kwargs():
    return {"environ_overrides": {"REMOTE_ADDR": "127.0.0.1"}}


def _configure_control_panel_paths(monkeypatch, tmp_path):
    swarm_dir = tmp_path / ".swarm"
    audit_dir = tmp_path / "audit"

    monkeypatch.setattr(cp, "WORKSPACE", tmp_path)
    monkeypatch.setattr(cp, "ACTION_LOG", tmp_path / "action_log.jsonl")
    monkeypatch.setattr(cp, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(cp, "API_AUDIT_LOG_FILE", audit_dir / "api_audit.log")
    monkeypatch.setattr(cp, "LEGACY_API_AUDIT_LOG_FILE", tmp_path / "legacy_api_audit.log")
    monkeypatch.setattr(cp, "QUEUE_FILE", tmp_path / "queue.json")
    monkeypatch.setattr(cp, "KILL_SWITCH", swarm_dir / "kill_switch.json")
    monkeypatch.setattr(cp, "FREE_TIME_BALANCES", swarm_dir / "free_time_balances.json")
    monkeypatch.setattr(cp, "IDENTITIES_DIR", swarm_dir / "identities")
    monkeypatch.setattr(cp, "HUMAN_REQUEST_FILE", swarm_dir / "human_request.json")
    monkeypatch.setattr(cp, "MESSAGES_TO_HUMAN", swarm_dir / "messages_to_human.jsonl")
    monkeypatch.setattr(cp, "MESSAGES_FROM_HUMAN", swarm_dir / "messages_from_human.json")
    monkeypatch.setattr(cp, "MESSAGES_FROM_HUMAN_OUTBOX", swarm_dir / "messages_from_human_outbox.jsonl")
    monkeypatch.setattr(cp, "COMPLETED_REQUESTS_FILE", swarm_dir / "completed_requests.json")
    monkeypatch.setattr(cp, "BOUNTIES_FILE", swarm_dir / "bounties.json")
    monkeypatch.setattr(cp, "DISCUSSIONS_DIR", swarm_dir / "discussions")
    monkeypatch.setattr(cp, "RUNTIME_SPEED_FILE", swarm_dir / "runtime_speed.json")
    monkeypatch.setattr(cp, "GROQ_API_KEY_FILE", tmp_path / "security" / "groq_api_key.txt")
    monkeypatch.setattr(cp.runtime_config, "GROQ_API_KEY_FILE", cp.GROQ_API_KEY_FILE)
    cp.runtime_config.set_groq_api_key(None)

    # Sync paths to app.config so blueprints (e.g. identities) use test paths
    cp.app.config["WORKSPACE"] = tmp_path
    cp.app.config["ACTION_LOG"] = tmp_path / "action_log.jsonl"
    cp.app.config["EXECUTION_LOG"] = tmp_path / "execution_log.jsonl"
    cp.app.config["IDENTITIES_DIR"] = swarm_dir / "identities"
    cp.app.config["FREE_TIME_BALANCES"] = swarm_dir / "free_time_balances.json"

    cp.app.config["TESTING"] = True
    return cp.app.test_client()


def test_kill_switch_toggle_api_round_trip(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    initial = client.get("/api/stop_status", **_localhost_request_kwargs()).get_json()
    assert initial["stopped"] is False

    toggled = client.post("/api/toggle_stop", **_localhost_request_kwargs()).get_json()
    assert toggled["stopped"] is True
    assert cp.KILL_SWITCH.exists()

    final = client.get("/api/stop_status", **_localhost_request_kwargs()).get_json()
    assert final["stopped"] is True


def test_artifacts_listing_api_returns_workspace_artifacts(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    journals_dir = tmp_path / ".swarm" / "journals"
    creative_dir = tmp_path / "library" / "creative_works"
    skills_dir = tmp_path / "skills"
    journals_dir.mkdir(parents=True, exist_ok=True)
    creative_dir.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)

    (journals_dir / "entry.md").write_text("journal", encoding="utf-8")
    (creative_dir / "poem.md").write_text("creative", encoding="utf-8")
    (skills_dir / "builder.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")

    response = client.get("/api/artifacts/list", **_localhost_request_kwargs()).get_json()
    assert response["success"] is True
    names = {artifact["name"] for artifact in response["artifacts"]}
    assert "entry.md" in names
    assert "poem.md" in names
    assert "builder.py" in names


def test_bounty_submission_records_members_and_claimed_by(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    created = client.post(
        "/api/bounties",
        json={"title": "Ship profile loop", "description": "Connect profile panels", "reward": 90, "slots": 2},
        **_localhost_request_kwargs(),
    ).get_json()
    assert created["success"] is True
    bounty_id = created["bounty"]["id"]

    submitted = client.post(
        f"/api/bounties/{bounty_id}/submit",
        json={
            "identity_id": "identity_alice",
            "identity_name": "Alice",
            "description": "Implemented and tested the profile endpoint wiring.",
        },
        **_localhost_request_kwargs(),
    ).get_json()
    assert submitted["success"] is True
    assert submitted["submission"]["members"] == ["identity_alice"]

    bounty_state = cp.load_bounties()[0]
    assert bounty_state["status"] == "claimed"
    assert bounty_state["claimed_by"]["type"] == "individual"
    assert bounty_state["claimed_by"]["id"] == "identity_alice"


def test_bounty_complete_multi_team_distributes_rewards(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    created = client.post(
        "/api/bounties",
        json={"title": "Ship support inbox", "description": "Wire support messaging", "reward": 100, "slots": 2},
        **_localhost_request_kwargs(),
    ).get_json()
    bounty_id = created["bounty"]["id"]

    client.post(
        f"/api/bounties/{bounty_id}/submit",
        json={
            "identity_id": "identity_one",
            "identity_name": "One",
            "description": "Submission one with enough detail to pass minimum contribution checks.",
        },
        **_localhost_request_kwargs(),
    )
    client.post(
        f"/api/bounties/{bounty_id}/submit",
        json={
            "identity_id": "identity_two",
            "identity_name": "Two",
            "description": "Submission two with enough detail to pass minimum contribution checks.",
        },
        **_localhost_request_kwargs(),
    )

    class _StubEnrichment:
        def __init__(self):
            self.calls = []

        def grant_free_time(self, identity_id, tokens, reason):
            self.calls.append((identity_id, tokens, reason))

        @staticmethod
        def distribute_bounty(_bounty_id):
            return {"success": True, "total_distributed": 0, "distributed": []}

    enrichment = _StubEnrichment()
    monkeypatch.setattr(swarm_enrichment, "get_enrichment", lambda _workspace=None: enrichment)

    completed = client.post(
        f"/api/bounties/{bounty_id}/complete",
        json={"winner_reward": 100, "runner_up_reward": 40},
        **_localhost_request_kwargs(),
    ).get_json()

    assert completed["success"] is True
    assert completed["total_distributed"] == 140
    identities = {identity for identity, _, _ in enrichment.calls}
    assert identities == {"identity_one", "identity_two"}

    bounty_state = cp.load_bounties()[0]
    assert bounty_state["status"] == "completed"


def test_insights_api_aggregates_runtime_signals(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    now = datetime.now(timezone.utc).isoformat()

    cp.QUEUE_FILE.write_text(
        json.dumps(
            {
                "tasks": [{"id": "t1"}, {"id": "t2"}],
                "completed": [{"id": "done_1"}],
                "failed": [{"id": "fail_1"}],
            }
        ),
        encoding="utf-8",
    )

    cp.EXECUTION_LOG.write_text(
        "\n".join(
            [
                json.dumps({"timestamp": now, "status": "approved"}),
                json.dumps({"timestamp": now, "status": "completed"}),
                json.dumps({"timestamp": now, "status": "failed"}),
                json.dumps({"timestamp": now, "status": "pending_review"}),
                json.dumps({"timestamp": now, "status": "completed", "budget_used": 0.042}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    cp.ACTION_LOG.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "timestamp": now,
                        "action_type": "API",
                        "action": "call",
                        "detail": "1523 tokens | $0.125",
                        "actor": "identity_alpha",
                    }
                ),
                json.dumps(
                    {
                        "timestamp": now,
                        "action_type": "SAFETY",
                        "action": "BLOCKED_WRITE",
                        "detail": "blocked by policy",
                        "actor": "identity_alpha",
                    }
                ),
                json.dumps(
                    {
                        "timestamp": now,
                        "action_type": "ERROR",
                        "action": "runtime_error",
                        "detail": "task crashed",
                        "actor": "identity_beta",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    cp.MESSAGES_TO_HUMAN.parent.mkdir(parents=True, exist_ok=True)
    cp.MESSAGES_TO_HUMAN.write_text(
        "\n".join(
            [
                json.dumps({"id": "m1", "from_id": "identity_alpha", "from_name": "Alpha", "timestamp": now}),
                json.dumps({"id": "m2", "from_id": "identity_beta", "from_name": "Beta", "timestamp": now}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    cp.MESSAGES_FROM_HUMAN.write_text(json.dumps({"m1": {"response": "ok"}}), encoding="utf-8")

    cp.BOUNTIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    cp.BOUNTIES_FILE.write_text(
        json.dumps(
            [
                {"id": "b1", "status": "open"},
                {"id": "b2", "status": "claimed"},
                {"id": "b3", "status": "completed"},
            ]
        ),
        encoding="utf-8",
    )

    cp.DISCUSSIONS_DIR.mkdir(parents=True, exist_ok=True)
    (cp.DISCUSSIONS_DIR / "watercooler.jsonl").write_text(
        json.dumps({"timestamp": now, "author_name": "Alpha", "content": "hello"}) + "\n",
        encoding="utf-8",
    )

    cp.IDENTITIES_DIR.mkdir(parents=True, exist_ok=True)
    (cp.IDENTITIES_DIR / "identity_alpha.json").write_text(
        json.dumps({"id": "identity_alpha", "name": "Alpha", "attributes": {}, "sessions_participated": 2}),
        encoding="utf-8",
    )
    (cp.IDENTITIES_DIR / "identity_beta.json").write_text(
        json.dumps({"id": "identity_beta", "name": "Beta", "attributes": {}, "sessions_participated": 3}),
        encoding="utf-8",
    )

    payload = client.get("/api/insights", **_localhost_request_kwargs()).get_json()
    assert payload["success"] is True
    assert payload["queue"]["open"] == 2
    assert payload["execution"]["completed_24h"] == 3  # 2 from original + 1 with budget_used
    assert payload["execution"]["failed_24h"] == 1
    assert payload["execution"]["pending_review_24h"] == 1
    assert payload["ops"]["api_calls_24h"] == 1
    # api_cost_24h = action_log API ($0.125) + execution_log budget_used ($0.042)
    assert payload["ops"]["api_cost_24h"] == pytest.approx(0.167, rel=1e-6)
    # all-time cost now aggregates both execution and action logs.
    assert payload["ops"]["api_cost_all_time"] == pytest.approx(0.167, rel=1e-6)
    assert payload["ops"]["safety_blocks_24h"] == 1
    assert payload["ops"]["errors_24h"] == 1
    assert payload["social"]["unread_messages"] == 1
    assert payload["social"]["open_bounties"] == 1
    assert payload["social"]["claimed_bounties"] == 1
    assert payload["social"]["completed_bounties"] == 1
    assert payload["social"]["chat_messages_24h"] == 1
    assert payload["identities"]["active_24h"] == 2
    assert payload["identities"]["top_actor"]["id"] == "identity_alpha"
    assert payload["health"]["state"] == "watch"
    card_ids = {card.get("id") for card in payload.get("metric_cards", [])}
    assert "spend_queue" in card_ids


def test_runtime_speed_api_round_trip(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    default_payload = client.get("/api/runtime_speed", **_localhost_request_kwargs()).get_json()
    assert "wait_seconds" in default_payload
    assert "cycle_seconds" in default_payload
    assert "current_cycle_id" in default_payload
    assert default_payload["reference_weekday_name"] in {
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    }

    update = client.post(
        "/api/runtime_speed",
        json={"wait_seconds": 11},
        **_localhost_request_kwargs(),
    ).get_json()
    assert update["success"] is True
    assert update["wait_seconds"] == 11

    refreshed = client.get("/api/runtime_speed", **_localhost_request_kwargs()).get_json()
    assert refreshed["wait_seconds"] == 11


def test_worker_start_replaces_unmanaged_processes_with_managed_pool(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    worker_process_file = tmp_path / ".swarm" / "worker_process.json"
    monkeypatch.setattr(cp, "MUTABLE_SWARM_DIR", worker_process_file.parent)
    monkeypatch.setattr(cp, "WORKER_PROCESS_FILE", worker_process_file)
    monkeypatch.setattr(
        cp,
        "get_worker_status",
        lambda: {
            "running": True,
            "pid": 43210,
            "pids": [43210],
            "unmanaged_pids": [43210],
            "running_count": 1,
            "target_count": 1,
            "started_at": None,
            "running_source": "unmanaged",
        },
    )

    killed: list[tuple[int, int]] = []
    monkeypatch.setattr(cp.os, "kill", lambda pid, sig: killed.append((pid, sig)))

    popen_envs: list[dict] = []

    class _Proc:
        pid = 54321

    def _fake_popen(cmd, cwd, env, stdout, stderr, start_new_session, **_kwargs):
        popen_envs.append(dict(env))
        return _Proc()

    monkeypatch.setattr(cp.subprocess, "Popen", _fake_popen)

    payload = client.post("/api/worker/start", json={"resident_count": 1}, **_localhost_request_kwargs()).get_json()
    assert payload["success"] is True
    assert killed == [(43210, 15)]
    assert len(popen_envs) == 1
    assert popen_envs[0]["VIVARIUM_WORKER_DAEMON"] == "1"
    assert worker_process_file.exists()


def test_identity_profile_exposes_full_identity_document(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    cp.IDENTITIES_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": "identity_alpha",
        "name": "Alpha",
        "summary": "Identity summary",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "attributes": {
            "core": {
                "identity_statement": "I am Alpha.",
                "personality_traits": ["curious"],
                "core_values": ["clarity"],
                "communication_style": "direct",
            },
            "mutable": {
                "current_mood": "focused",
                "current_focus": "debugging",
            },
            "profile": {},
        },
    }
    (cp.IDENTITIES_DIR / "identity_alpha.json").write_text(json.dumps(payload), encoding="utf-8")

    response = client.get("/api/identity/identity_alpha/profile", **_localhost_request_kwargs()).get_json()
    assert response["identity_id"] == "identity_alpha"
    assert response["identity_document"]["id"] == "identity_alpha"
    assert response["mutable"]["current_focus"] == "debugging"


def test_logs_recent_includes_hat_and_usage_metadata(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    now = datetime.now(timezone.utc).isoformat()
    cp.EXECUTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    cp.EXECUTION_LOG.write_text(
        json.dumps(
            {
                "timestamp": now,
                "task_id": "task_hat_1",
                "status": "subtask_started",
                "identity_id": "identity_alpha",
                "subtask_id": "phase4_01",
                "focus": "review",
                "hat_name": "Reviewer",
                "total_tokens": 321,
                "budget_used": 0.012345,
                "model": "llama-3.3-70b-versatile",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    payload = client.get("/api/logs/recent?limit=50", **_localhost_request_kwargs()).get_json()
    entries = payload["entries"]
    target = next(e for e in entries if e.get("action_type") == "EXECUTION")
    assert target["metadata"]["task_id"] == "task_hat_1"
    assert target["metadata"]["hat_name"] == "Reviewer"
    assert target["metadata"]["total_tokens"] == 321
    assert "hat=Reviewer" in target["detail"]
    assert "321 tokens" in target["detail"]


def test_logs_recent_includes_api_audit_entries_when_action_log_missing(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    now = datetime.now(timezone.utc).isoformat()
    cp.API_AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    cp.API_AUDIT_LOG_FILE.write_text(
        json.dumps(
            {
                "timestamp": now,
                "event": "API_CALL_SUCCESS",
                "user": "swarm_api",
                "model": "llama-3.1-8b-instant",
                "cost": 0.00123,
                "input_tokens": 1000,
                "output_tokens": 230,
                "call_type": "identity_generation",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    payload = client.get("/api/logs/recent?limit=50", **_localhost_request_kwargs()).get_json()
    assert payload["success"] is True
    api_entries = [e for e in payload["entries"] if e.get("action_type") == "API"]
    assert api_entries, "expected API entries mapped from api_audit.log"
    assert any(e.get("metadata", {}).get("usd_cost") == pytest.approx(0.00123) for e in api_entries)
    assert any(e.get("metadata", {}).get("call_type") == "identity_generation" for e in api_entries)


def test_insights_uses_api_audit_fallback_when_action_log_missing(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    now = datetime.now(timezone.utc).isoformat()
    cp.API_AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    cp.API_AUDIT_LOG_FILE.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "timestamp": now,
                        "event": "API_CALL_SUCCESS",
                        "user": "swarm_api",
                        "model": "llama-3.1-8b-instant",
                        "cost": 0.002,
                        "input_tokens": 800,
                        "output_tokens": 200,
                    }
                ),
                json.dumps(
                    {
                        "timestamp": now,
                        "event": "API_CALL_SUCCESS",
                        "user": "swarm_api",
                        "model": "llama-3.3-70b-versatile",
                        "cost": 0.003,
                        "input_tokens": 1200,
                        "output_tokens": 350,
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    payload = client.get("/api/insights", **_localhost_request_kwargs()).get_json()
    assert payload["success"] is True
    assert payload["ops"]["api_calls_24h"] == 2
    assert payload["ops"]["api_cost_24h"] == pytest.approx(0.005, rel=1e-6)
    assert payload["ops"]["api_cost_all_time"] == pytest.approx(0.005, rel=1e-6)


def test_send_message_does_not_auto_spawn_worker_when_paused(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    def _raise_if_called(*_args, **_kwargs):
        raise AssertionError("should not auto-spawn worker on message send")

    monkeypatch.setattr(cp, "_spawn_one_off_worker_if_paused", _raise_if_called)
    response = client.post(
        "/api/messages/send",
        json={"content": "hello", "to_id": "identity_alpha", "to_name": "Alpha"},
        **_localhost_request_kwargs(),
    ).get_json()
    assert response["success"] is True


def test_groq_key_api_round_trip_and_clear(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    initial = client.get("/api/groq_key", **_localhost_request_kwargs()).get_json()
    assert initial["configured"] is False

    saved = client.post(
        "/api/groq_key",
        json={"api_key": "gsk_test_key_1234567890"},
        **_localhost_request_kwargs(),
    ).get_json()
    assert saved["success"] is True
    assert saved["configured"] is True
    assert cp.GROQ_API_KEY_FILE.exists()

    loaded = client.get("/api/groq_key", **_localhost_request_kwargs()).get_json()
    assert loaded["configured"] is True
    assert loaded["masked_key"].startswith("gsk_")

    cleared = client.delete("/api/groq_key", **_localhost_request_kwargs()).get_json()
    assert cleared["success"] is True
    assert cleared["configured"] is False
    assert not cp.GROQ_API_KEY_FILE.exists()


def test_identity_create_api_creates_resident_authored_identity(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)

    created = client.post(
        "/api/identities/create",
        json={
            "name": "EchoFlux",
            "summary": "A curious mapper of swarm behavior and creative prompts.",
            "traits_csv": "curious, collaborative, reflective",
            "values_csv": "clarity, generosity",
            "activities_csv": "journal writing, bounty strategy",
        },
        **_localhost_request_kwargs(),
    ).get_json()
    assert created["success"] is True
    identity_id = created["identity"]["id"]

    identity_path = cp.IDENTITIES_DIR / f"{identity_id}.json"
    assert identity_path.exists()
    data = json.loads(identity_path.read_text(encoding="utf-8"))
    assert data["name"] == "EchoFlux"
    assert data["origin"] == "resident_authored"
    assert data["meta"]["creative_self_authored"] is True
    assert "curious" in data["attributes"]["core"]["personality_traits"]


def test_chatrooms_api_lists_and_reads_town_hall_messages(monkeypatch, tmp_path):
    client = _configure_control_panel_paths(monkeypatch, tmp_path)
    cp.DISCUSSIONS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    (cp.DISCUSSIONS_DIR / "town_hall.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "m1",
                        "author_id": "identity_alpha",
                        "author_name": "Alpha",
                        "content": "I reviewed the docs pass and propose two changes.",
                        "timestamp": now,
                        "room": "town_hall",
                    }
                ),
                json.dumps(
                    {
                        "id": "m2",
                        "author_id": "identity_beta",
                        "author_name": "Beta",
                        "content": "Replying with implementation notes.",
                        "timestamp": now,
                        "room": "town_hall",
                        "reply_to": "m1",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    rooms = client.get("/api/chatrooms", **_localhost_request_kwargs()).get_json()
    assert rooms["success"] is True
    town_hall = next((room for room in rooms["rooms"] if room["id"] == "town_hall"), None)
    assert town_hall is not None
    assert town_hall["message_count"] == 2

    payload = client.get("/api/chatrooms/town_hall", **_localhost_request_kwargs()).get_json()
    assert payload["success"] is True
    assert payload["room"] == "town_hall"
    assert len(payload["messages"]) == 2
    assert payload["messages"][1]["reply_to"] == "m1"
