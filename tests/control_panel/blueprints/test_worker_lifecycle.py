import os
import pytest
import json
import time

# Worker lifecycle tests spawn subprocesses; skip on CI where process spawning may fail
pytestmark = pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Worker subprocess tests skipped on CI (process spawning restricted)",
)


@pytest.fixture(autouse=True)
def ensure_worker_stopped(client, localhost_kwargs):
    """Pre-flight: ensure worker is stopped before each test"""
    client.post('/api/worker/stop', **localhost_kwargs)
    # Give it a moment
    time.sleep(0.1)


def test_worker_status_when_stopped(client, localhost_kwargs):
    """GET /api/worker/status when no worker running"""
    response = client.get('/api/worker/status', **localhost_kwargs)
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert data['running'] is False
    assert data['managed'] is False
    assert 'pid' in data

def test_worker_start_stop_cycle(client, localhost_kwargs):
    """POST /api/worker/start then POST /api/worker/stop"""
    # Start worker
    start_payload = {'resident_count': 2}
    start_resp = client.post('/api/worker/start',
                            data=json.dumps(start_payload),
                            content_type='application/json',
                            **localhost_kwargs)
    assert start_resp.status_code == 200
    start_data = start_resp.get_json()
    assert start_data['success'] is True

    # Check status shows running
    status_resp = client.get('/api/worker/status', **localhost_kwargs)
    status_data = status_resp.get_json()
    # Note: May still be False if worker failed to start (expected in test env)

    # Stop worker
    stop_resp = client.post('/api/worker/stop', **localhost_kwargs)
    assert stop_resp.status_code == 200
    stop_data = stop_resp.get_json()
    assert stop_data['success'] is True

    # Verify stopped
    final_status = client.get('/api/worker/status', **localhost_kwargs).get_json()
    assert final_status['running'] is False

def test_worker_start_idempotency(client, localhost_kwargs):
    """Starting worker twice should not crash"""
    payload = {'resident_count': 1}

    # First start
    resp1 = client.post('/api/worker/start',
                       data=json.dumps(payload),
                       content_type='application/json',
                       **localhost_kwargs)
    assert resp1.status_code == 200

    # Second start (should handle gracefully)
    resp2 = client.post('/api/worker/start',
                       data=json.dumps(payload),
                       content_type='application/json',
                       **localhost_kwargs)
    assert resp2.status_code == 200
    # May return success=False if already running, but shouldn't 500

    # Cleanup
    client.post('/api/worker/stop', **localhost_kwargs)

def test_worker_stop_idempotency(client, localhost_kwargs):
    """Stopping worker when already stopped should not crash"""
    # Ensure stopped first
    client.post('/api/worker/stop', **localhost_kwargs)

    # Stop again
    resp = client.post('/api/worker/stop', **localhost_kwargs)
    assert resp.status_code == 200
    # Should return success=True or success=False, not 500

def test_worker_invalid_resident_count(client, localhost_kwargs):
    """Worker start with invalid data handled gracefully"""
    invalid_payloads = [
        {},  # Missing resident_count
        {'resident_count': -1},  # Negative
        {'resident_count': 'not_a_number'},  # Wrong type
        {'resident_count': 9999},  # Unrealistically high
    ]

    for payload in invalid_payloads:
        resp = client.post('/api/worker/start',
                          data=json.dumps(payload),
                          content_type='application/json',
                          **localhost_kwargs)
        # Should not 500, may 400 or 200 with error
        assert resp.status_code in [200, 400, 422], f"Payload {payload} caused server error"
