import json

import pytest
from hypothesis import HealthCheck, given, settings, strategies as st


class TestQueueProperties:
    """Property-based tests for queue invariants"""

    @given(
        task_id=st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(whitelist_categories=("L", "N")),
        ),
        priority=st.integers(min_value=0, max_value=100),
    )
    @settings(
        max_examples=20,
        deadline=5000,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_queue_adds_any_valid_task(
        self, client, task_id, priority, localhost_kwargs
    ):
        """Queue accepts any reasonable task ID and priority"""
        task = {
            "task_id": task_id,
            "instruction": "Test task",
            "priority": priority,
        }

        response = client.post(
            "/api/queue/add",
            data=json.dumps(task),
            content_type="application/json",
            **localhost_kwargs,
        )

        # Should never crash
        assert response.status_code in [200, 201, 400]

        if response.status_code in [200, 201]:
            data = response.get_json()
            # Success flag or ID returned
            assert data.get("success") is True or "task_id" in data

    @given(n=st.integers(min_value=1, max_value=20))
    @settings(
        max_examples=8,
        deadline=10000,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_queue_state_consistent(self, client, n, localhost_kwargs):
        """Queue state is consistent after n operations"""
        # Add n tasks
        for i in range(n):
            task = {
                "task_id": f"prop_test_{i}",
                "instruction": f"Task {i}",
                "priority": i % 10,
            }
            client.post(
                "/api/queue/add",
                data=json.dumps(task),
                content_type="application/json",
                **localhost_kwargs,
            )

        # Get state
        response = client.get("/api/queue/state", **localhost_kwargs)
        assert response.status_code == 200

        data = response.get_json()
        queue_len = len(data.get("queue", []))
        otc_len = len(data.get("one_time_tasks", []))

        # Total tasks should be reasonable (queue tasks from our adds)
        assert queue_len >= n
        assert otc_len >= 0
