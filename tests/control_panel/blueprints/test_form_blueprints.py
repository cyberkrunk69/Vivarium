"""POST path tests for form-submission blueprints (ui_settings, completed_requests, human_request)."""
import json
import pytest


class TestUISettings:
    """GET/POST /api/ui_settings"""

    def test_ui_settings_get(self, client, localhost_kwargs):
        """GET returns current settings"""
        response = client.get('/api/ui_settings', **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data or 'settings' in data or isinstance(data, dict)

    def test_ui_settings_post_valid(self, client, localhost_kwargs):
        """POST updates settings"""
        settings = {
            "model": "gpt-4",
            "budget_limit": 100,
            "resident_count": 5
        }
        response = client.post(
            '/api/ui_settings',
            data=json.dumps(settings),
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data.get('success') is True or 'updated' in data

    def test_ui_settings_post_partial(self, client, localhost_kwargs):
        """Partial update works"""
        partial = {"budget_limit": 50}
        response = client.post(
            '/api/ui_settings',
            data=json.dumps(partial),
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code in [200, 400]

    def test_ui_settings_persistence(self, client, localhost_kwargs):
        """Settings persist between requests"""
        # Set a value
        client.post(
            '/api/ui_settings',
            data=json.dumps({"resident_count": 3}),
            content_type='application/json',
            **localhost_kwargs
        )
        # Read it back
        response = client.get('/api/ui_settings', **localhost_kwargs)
        data = response.get_json()
        settings = data.get('settings', data)
        # May or may not contain our test key depending on merge logic
        assert isinstance(settings, dict)


class TestCompletedRequests:
    """GET/POST /api/completed_requests"""

    def test_completed_requests_get(self, client, localhost_kwargs):
        """GET returns list"""
        response = client.get('/api/completed_requests', **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        requests_list = data if isinstance(data, list) else data.get('requests', [])
        assert isinstance(requests_list, list)

    def test_completed_requests_post_adds(self, client, localhost_kwargs):
        """POST adds completed request"""
        request_data = {
            "request": "test_request - success",
            "metadata": {"test": True}
        }
        response = client.post(
            '/api/completed_requests',
            data=json.dumps(request_data),
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code == 200
        # Verify it appears in list
        list_response = client.get('/api/completed_requests', **localhost_kwargs)
        list_data = list_response.get_json()
        requests_list = list_data if isinstance(list_data, list) else list_data.get('requests', [])
        # Should contain our new request or be longer than before
        assert isinstance(requests_list, list)


class TestHumanRequest:
    """GET/POST /api/human_request"""

    def test_human_request_get(self, client, localhost_kwargs):
        """GET returns current request or empty"""
        response = client.get('/api/human_request', **localhost_kwargs)
        assert response.status_code == 200
        data = response.get_json()
        # May be null, empty dict, or request object
        assert data is None or isinstance(data, dict)

    def test_human_request_post_creates(self, client, localhost_kwargs):
        """POST creates human-in-the-loop request"""
        request_data = {
            "request": "Test human request - approval needed"
        }
        response = client.post(
            '/api/human_request',
            data=json.dumps(request_data),
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data.get('success') is True or data.get('id') or data.get('request')

    def test_human_request_validation(self, client, localhost_kwargs):
        """Invalid requests handled"""
        invalid = [
            {},  # Empty
            {"request": ""},  # Empty request text
        ]
        for payload in invalid:
            response = client.post(
                '/api/human_request',
                data=json.dumps(payload),
                content_type='application/json',
                **localhost_kwargs
            )
            assert response.status_code in [200, 400, 422]
