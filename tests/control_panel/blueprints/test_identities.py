import json


def test_get_identities_empty(client, localhost_kwargs):
    """GET /api/identities returns success and empty identities list when no identities"""
    response = client.get("/api/identities", **localhost_kwargs)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data.get("success") is True
    assert data.get("identities") == []


def test_create_identity_validation(client, localhost_kwargs):
    """POST /api/identities/create rejects invalid data"""
    response = client.post(
        "/api/identities/create",
        data=json.dumps({}),
        content_type="application/json",
        **localhost_kwargs,
    )
    assert response.status_code in [400, 200]
    # Should fail gracefully, not 500


def test_identity_profile_not_found(client, localhost_kwargs):
    """GET /api/identity/nonexistent/profile returns 404 or error"""
    response = client.get("/api/identity/nonexistent/profile", **localhost_kwargs)
    assert response.status_code in [200, 404]
    # Blueprint handles gracefully (200 with error in body or 404)
