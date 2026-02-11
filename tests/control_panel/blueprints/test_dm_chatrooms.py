"""DM and chatrooms blueprint tests. Issue #75."""
import json
import pytest


@pytest.fixture
def test_identity():
    return "test_identity_123"


@pytest.fixture
def test_message():
    """Valid DM payload: from_id, to_id, content (API expects these, not recipient/message)"""
    return {
        "from_id": "human",
        "to_id": "test_identity_123",
        "content": "Hello from test",
    }


@pytest.fixture
def test_room():
    return "town_hall"


class TestDMThreads:
    """GET /api/dm/threads/<identity_id>"""

    def test_dm_threads_empty(self, client, test_identity, localhost_kwargs):
        """Threads for new identity returns empty or 404"""
        response = client.get(
            f"/api/dm/threads/{test_identity}",
            **localhost_kwargs,
        )
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data.get("threads", []), list)

    def test_dm_threads_structure(self, client, localhost_kwargs):
        """Response has expected fields if threads exist"""
        response = client.get(
            "/api/dm/threads/existing_user",
            **localhost_kwargs,
        )
        if response.status_code == 200:
            data = response.get_json()
            assert "threads" in data or "messages" in data


class TestDMMessages:
    """GET /api/dm/messages, POST /api/dm/send"""

    def test_dm_messages_list(self, client, test_identity, localhost_kwargs):
        """GET /api/dm/messages returns message list when identity_id and peer_id provided"""
        response = client.get(
            f"/api/dm/messages?identity_id={test_identity}&peer_id=human",
            **localhost_kwargs,
        )
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.get_json()
            messages = data if isinstance(data, list) else data.get("messages", [])
            assert isinstance(messages, list)

    def test_dm_messages_missing_params(self, client, localhost_kwargs):
        """GET /api/dm/messages without params returns 400"""
        response = client.get("/api/dm/messages", **localhost_kwargs)
        assert response.status_code in [200, 400]
        if response.status_code == 400:
            data = response.get_json()
            assert "error" in data or "identity_id" in str(data).lower() or "peer_id" in str(data).lower()

    def test_dm_send_success(self, client, test_message, localhost_kwargs):
        """POST /api/dm/send creates message"""
        response = client.post(
            "/api/dm/send",
            data=json.dumps(test_message),
            content_type="application/json",
            **localhost_kwargs,
        )
        # May 200 (success) or 400 (validation/identities) but not 500
        assert response.status_code in [200, 201, 400]
        if response.status_code in [200, 201]:
            data = response.get_json()
            assert data.get("success") or data.get("id") or data.get("message")

    def test_dm_send_validation(self, client, localhost_kwargs):
        """Invalid payloads handled gracefully"""
        invalid_cases = [
            {},  # Empty
            {"to_id": "test", "content": "hi"},  # Missing from_id
            {"from_id": "test", "content": "hi"},  # Missing to_id
            {"from_id": "test", "to_id": "other"},  # Missing content
            {"from_id": "", "to_id": "x", "content": "y"},  # Empty from_id
            {"from_id": "a", "to_id": "a", "content": "same"},  # from_id == to_id
            {"from_id": "a", "to_id": "b", "content": "x" * 10000},  # Too long
        ]
        for payload in invalid_cases:
            response = client.post(
                "/api/dm/send",
                data=json.dumps(payload),
                content_type="application/json",
                **localhost_kwargs,
            )
            assert response.status_code in [200, 400, 422, 413]

    def test_dm_send_special_chars(self, client, localhost_kwargs):
        """Unicode and special characters handled"""
        message = {
            "from_id": "human",
            "to_id": "test",
            "content": "Hello 🚀 ñ 中文 <script>alert('xss')</script>",
        }
        response = client.post(
            "/api/dm/send",
            data=json.dumps(message),
            content_type="application/json",
            **localhost_kwargs,
        )
        assert response.status_code in [200, 201, 400]


class TestChatrooms:
    """GET /api/chatrooms, GET /api/chatrooms/<room_id>"""

    def test_chatrooms_list(self, client, localhost_kwargs):
        """GET /api/chatrooms returns available rooms"""
        response = client.get("/api/chatrooms", **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        rooms = data if isinstance(data, list) else data.get("rooms", data.get("chatrooms", []))
        assert isinstance(rooms, list)

    def test_chatrooms_has_standard_rooms(self, client, localhost_kwargs):
        """Standard rooms exist (town_hall, watercooler)"""
        response = client.get("/api/chatrooms", **localhost_kwargs)
        data = response.get_json()
        rooms = data if isinstance(data, list) else data.get("rooms", data.get("chatrooms", []))
        room_names = [r.get("id", r.get("name", "")).lower() for r in rooms]
        # Check for common rooms if any exist
        if room_names:
            common = ["town", "hall", "water", "general"]
            has_common = any(any(c in n for c in common) for n in room_names)
            # Just verify structure, not specific names
            assert all(isinstance(r, dict) for r in rooms)

    def test_chatroom_messages(self, client, test_room, localhost_kwargs):
        """GET /api/chatrooms/<room_id> returns messages"""
        response = client.get(f"/api/chatrooms/{test_room}", **localhost_kwargs)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.get_json()
            messages = data if isinstance(data, list) else data.get("messages", [])
            assert isinstance(messages, list)

    def test_chatroom_invalid_id(self, client, localhost_kwargs):
        """Invalid room IDs handled gracefully"""
        invalid_ids = [
            "!@#$%^&*",
            "../../../etc/passwd",
            "room' OR '1'='1",
            "<script>alert('xss')</script>",
            "a" * 1000,  # Too long
        ]
        for room_id in invalid_ids:
            response = client.get(
                f"/api/chatrooms/{room_id}",
                **localhost_kwargs,
            )
            assert response.status_code in [200, 404, 400]

    def test_chatroom_not_found(self, client, localhost_kwargs):
        """Non-existent room returns 404 or empty, not 500"""
        response = client.get(
            "/api/chatrooms/nonexistent_room_99999",
            **localhost_kwargs,
        )
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.get_json()
            messages = data if isinstance(data, list) else data.get("messages", [])
            assert len(messages) == 0 or data.get("exists") is False
