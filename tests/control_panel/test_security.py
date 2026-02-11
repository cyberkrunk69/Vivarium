import pytest


def test_localhost_only_rejects_external(client):
    """Non-loopback requests get 403"""
    response = client.get('/api/identities',
                         headers={'X-Forwarded-For': '8.8.8.8'})
    assert response.status_code == 403
    data = response.get_json()
    assert 'localhost-only' in data.get('error', '').lower()


def test_security_headers_present(client):
    """All responses have security headers"""
    response = client.get('/')
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('Referrer-Policy') == 'no-referrer'


def test_root_route_serves_ui(client, localhost_kwargs):
    """GET / returns the control panel HTML"""
    response = client.get('/', **localhost_kwargs)
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_favicon_exists(client, localhost_kwargs):
    """Favicon route works"""
    response = client.get('/favicon.ico', **localhost_kwargs)
    # May 200, 204, or 404, but shouldn't 500
    assert response.status_code in [200, 204, 404]
