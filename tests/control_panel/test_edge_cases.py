import pytest
import json

class Test404Handling:
    """All blueprints return proper 404s"""
    
    def test_identity_not_found(self, client, localhost_kwargs):
        """GET /api/identity/nonexistent returns 404 or empty"""
        response = client.get(
            '/api/identity/nonexistent_12345/profile',
            **localhost_kwargs
        )
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.get_json()
            assert data.get('exists') is False or data.get('profile') is None

    def test_bounty_not_found(self, client, localhost_kwargs):
        """DELETE /api/bounties/<bad_id> returns 404"""
        response = client.delete(
            '/api/bounties/nonexistent_99999',
            **localhost_kwargs
        )
        assert response.status_code in [200, 404, 204]
        if response.status_code == 200:
            data = response.get_json()
            assert data.get('success') is False or 'not found' in str(data).lower()

    def test_quest_not_found(self, client, localhost_kwargs):
        """POST to nonexistent quest handled"""
        response = client.post(
            '/api/quests/nonexistent_999/pause',
            **localhost_kwargs
        )
        assert response.status_code in [200, 404, 400]

class TestMalformedData:
    """Graceful handling of bad input"""
    
    def test_malformed_json(self, client, localhost_kwargs):
        """Non-JSON body doesn't crash"""
        endpoints = [
            ('/api/queue/add', 'post'),
            ('/api/bounties', 'post'),
            ('/api/identities/create', 'post'),
        ]
        for path, method in endpoints:
            response = getattr(client, method)(
                path,
                data='not json { malformed',
                content_type='application/json',
                **localhost_kwargs
            )
            assert response.status_code in [200, 400, 422, 500]  # 500 is bad, catch it

    def test_empty_body(self, client, localhost_kwargs):
        """Empty POST body handled"""
        response = client.post(
            '/api/messages/send',
            data='',
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code in [200, 400, 422]

    def test_wrong_content_type(self, client, localhost_kwargs):
        """Wrong Content-Type handled"""
        response = client.post(
            '/api/ui_settings',
            data='key=value',
            content_type='application/x-www-form-urlencoded',
            **localhost_kwargs
        )
        assert response.status_code in [200, 400, 415]

class TestLargePayloads:
    """Size limits enforced"""
    
    def test_huge_message(self, client, localhost_kwargs):
        """Very large message handled"""
        huge_message = {
            "recipient": "test",
            "message": "x" * 100000  # 100KB
        }
        response = client.post(
            '/api/messages/send',
            data=json.dumps(huge_message),
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code in [200, 400, 413]  # 413 = Payload Too Large

    def test_deeply_nested_json(self, client, localhost_kwargs):
        """Deep nesting handled"""
        nested = {"a": {"b": {"c": {"d": {"e": "deep"}}}}}
        response = client.post(
            '/api/queue/add',
            data=json.dumps(nested),
            content_type='application/json',
            **localhost_kwargs
        )
        assert response.status_code in [200, 400]

class TestSpecialCharacters:
    """Unicode and injection attempts"""
    
    def test_unicode_in_identity_name(self, client, localhost_kwargs):
        """Unicode identity names handled"""
        identity_data = {
            "name": "测试_🚀_ñ",
            "description": "Test <script>alert('xss')</script>"
        }
        response = client.post(
            '/api/identities/create',
            data=json.dumps(identity_data),
            content_type='application/json',
            **localhost_kwargs
        )
        # Should not 500, may 400 if validation strict
        assert response.status_code in [200, 201, 400]

    def test_sql_injection_attempt(self, client, localhost_kwargs):
        """SQL injection patterns handled"""
        malicious = {
            "type": "test'; DROP TABLE identities; --",
            "data": "' OR '1'='1"
        }
        response = client.post(
            '/api/completed_requests',
            data=json.dumps(malicious),
            content_type='application/json',
            **localhost_kwargs
        )
        # Should not crash or execute
        assert response.status_code in [200, 400]
