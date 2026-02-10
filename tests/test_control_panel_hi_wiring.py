import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime import control_panel_app as cp
from vivarium.runtime import swarm_enrichment


def _localhost_request_kwargs():
    return {"environ_overrides": {"REMOTE_ADDR": "127.0.0.1"}}


def _configure_control_panel_paths(monkeypatch, tmp_path):
    swarm_dir = tmp_path / ".swarm"

    monkeypatch.setattr(cp, "WORKSPACE", tmp_path)
    monkeypatch.setattr(cp, "ACTION_LOG", tmp_path / "action_log.jsonl")
    monkeypatch.setattr(cp, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(cp, "QUEUE_FILE", tmp_path / "queue.json")
    monkeypatch.setattr(cp, "KILL_SWITCH", swarm_dir / "kill_switch.json")
    monkeypatch.setattr(cp, "FREE_TIME_BALANCES", swarm_dir / "free_time_balances.json")
    monkeypatch.setattr(cp, "IDENTITIES_DIR", swarm_dir / "identities")
    monkeypatch.setattr(cp, "HUMAN_REQUEST_FILE", swarm_dir / "human_request.json")
    monkeypatch.setattr(cp, "MESSAGES_TO_HUMAN", swarm_dir / "messages_to_human.jsonl")
    monkeypatch.setattr(cp, "MESSAGES_FROM_HUMAN", swarm_dir / "messages_from_human.json")
    monkeypatch.setattr(cp, "COMPLETED_REQUESTS_FILE", swarm_dir / "completed_requests.json")
    monkeypatch.setattr(cp, "BOUNTIES_FILE", swarm_dir / "bounties.json")
    monkeypatch.setattr(cp, "DISCUSSIONS_DIR", swarm_dir / "discussions")

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
    assert payload["execution"]["completed_24h"] == 2
    assert payload["execution"]["failed_24h"] == 1
    assert payload["execution"]["pending_review_24h"] == 1
    assert payload["ops"]["api_calls_24h"] == 1
    assert payload["ops"]["api_cost_24h"] == 0.125
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
