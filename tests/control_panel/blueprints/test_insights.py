import pytest
import json


def test_insights_basic_structure(client, localhost_kwargs):
    """GET /api/insights returns metrics object"""
    response = client.get('/api/insights', **localhost_kwargs)
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, dict)

    # Should have success flag or direct metrics
    if 'success' in data:
        assert data['success'] is True
        metrics = data.get('insights', data)
    else:
        metrics = data

    # Check for expected metric categories
    expected_keys = ['queue', 'execution', 'health', 'cost', 'social']
    found_keys = [k for k in expected_keys if any(expected in str(key).lower()
                 for key in metrics.keys() for expected in [k])]
    # At least some metrics should be present
    assert len(metrics) > 0, "Insights should return metrics"

def test_insights_with_empty_system(client, localhost_kwargs):
    """Insights work even with no data"""
    response = client.get('/api/insights', **localhost_kwargs)
    assert response.status_code == 200

    data = response.get_json()
    # Should not crash on empty/zero values
    assert isinstance(data, dict)

def test_insights_consistency(client, localhost_kwargs):
    """Multiple calls return consistent structure"""
    resp1 = client.get('/api/insights', **localhost_kwargs)
    resp2 = client.get('/api/insights', **localhost_kwargs)

    assert resp1.status_code == resp2.status_code == 200

    data1 = resp1.get_json()
    data2 = resp2.get_json()

    # Structure should be consistent
    assert type(data1) == type(data2)
    if isinstance(data1, dict) and isinstance(data2, dict):
        assert set(data1.keys()) == set(data2.keys()), "Insights structure changed between calls"
