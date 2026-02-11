import json
from pathlib import Path


def test_queue_survives_app_restart(app, client, localhost_kwargs):
    """Queue state persists to disk and reloads on restart"""
    from vivarium.runtime.control_panel_app import app as new_app_instance

    # Add task to queue via API (task_id + instruction)
    task = {
        "task_id": "persistent_test_task",
        "instruction": "test instruction for persistence",
    }
    add_resp = client.post(
        "/api/queue/add",
        data=json.dumps(task),
        content_type="application/json",
        **localhost_kwargs,
    )
    assert add_resp.status_code == 200
    assert add_resp.get_json()["success"] is True

    # Verify file exists and contains valid JSON
    queue_file = app.config["QUEUE_FILE"]
    assert queue_file.exists(), f"Queue file not found: {queue_file}"

    file_content = json.loads(queue_file.read_text())
    assert isinstance(file_content, (list, dict)), "Queue file should contain JSON array or object"

    # Simulate app restart by reconfiguring app with same paths and using new test client
    test_workspace = app.config["WORKSPACE"]

    new_app_instance.config["TESTING"] = True
    new_app_instance.config["WORKSPACE"] = test_workspace
    new_app_instance.config["QUEUE_FILE"] = queue_file
    new_app_instance.config["ACTION_LOG"] = app.config["ACTION_LOG"]
    new_app_instance.config["EXECUTION_LOG"] = app.config["EXECUTION_LOG"]
    new_app_instance.config["IDENTITIES_DIR"] = app.config["IDENTITIES_DIR"]
    new_app_instance.config["KILL_SWITCH"] = app.config["KILL_SWITCH"]
    new_app_instance.config["GROQ_API_KEY_FILE"] = app.config["GROQ_API_KEY_FILE"]
    new_app_instance.config["RUNTIME_SPEED_FILE"] = app.config["RUNTIME_SPEED_FILE"]
    new_app_instance.config["MAILBOX_QUESTS_FILE"] = app.config["MAILBOX_QUESTS_FILE"]

    with new_app_instance.test_client() as new_client:
        # Verify queue state survived
        state_resp = new_client.get("/api/queue/state", **localhost_kwargs)
        assert state_resp.status_code == 200

        state_data = state_resp.get_json()
        assert state_data["success"] is True

        # Task should exist in queue (API creates cycle tasks)
        queue_tasks = state_data.get("queue", [])
        task_ids = [t.get("id") for t in queue_tasks]
        assert "persistent_test_task" in task_ids, (
            f"Task not found in queue after restart. Tasks: {task_ids}"
        )


def test_one_time_task_survives_restart(app, client, localhost_kwargs):
    """One-time tasks persist across restarts"""
    from vivarium.runtime.control_panel_app import app as new_app_instance

    # Create one-time task (id, title, prompt, bonus_tokens required)
    task = {
        "id": "one_off_persistent",
        "title": "Test persistent task",
        "prompt": "Test persistent one-time task",
        "bonus_tokens": 5,
    }
    create_resp = client.post(
        "/api/one_time_tasks",
        data=json.dumps(task),
        content_type="application/json",
        **localhost_kwargs,
    )
    assert create_resp.status_code == 200
    create_data = create_resp.get_json()
    assert create_data["success"] is True

    # Get task ID from response
    task_id = create_data.get("task_id") or create_data.get("id")
    assert task_id is not None, "Created task should have task_id"

    # Restart simulation: reconfigure app with same paths
    new_app_instance.config.update(
        {
            "TESTING": True,
            "WORKSPACE": app.config["WORKSPACE"],
            "QUEUE_FILE": app.config["QUEUE_FILE"],
            "ACTION_LOG": app.config["ACTION_LOG"],
            "EXECUTION_LOG": app.config["EXECUTION_LOG"],
            "IDENTITIES_DIR": app.config["IDENTITIES_DIR"],
            "KILL_SWITCH": app.config["KILL_SWITCH"],
            "GROQ_API_KEY_FILE": app.config["GROQ_API_KEY_FILE"],
            "RUNTIME_SPEED_FILE": app.config["RUNTIME_SPEED_FILE"],
            "MAILBOX_QUESTS_FILE": app.config["MAILBOX_QUESTS_FILE"],
        }
    )

    with new_app_instance.test_client() as new_client:
        # List tasks and verify ours exists
        list_resp = new_client.get("/api/one_time_tasks", **localhost_kwargs)
        assert list_resp.status_code == 200
        list_data = list_resp.get_json()

        task_ids = [t.get("id") for t in list_data.get("tasks", [])]
        assert task_id in task_ids, f"One-time task {task_id} not found after restart"
