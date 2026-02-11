import pytest
import json

# Define expected response schemas
ROUTE_CONTRACTS = {
    '/api/identities': {
        'required': ['success', 'identities'],
        'types': {'success': bool, 'identities': list}
    },
    '/api/messages/mailbox': {
        'required': ['success', 'threads', 'unread_count'],
        'types': {'success': bool, 'threads': list, 'unread_count': int}
    },
    '/api/logs/recent': {
        'required': ['success', 'entries', 'limit'],
        'types': {'success': bool, 'entries': list, 'limit': int}
    },
    '/api/queue/state': {
        'required': ['success', 'queue', 'one_time_tasks'],
        'types': {'success': bool, 'queue': list, 'one_time_tasks': list}
    },
    '/api/bounties': {
        'required': ['success', 'bounties'],
        'types': {'success': bool, 'bounties': list}
    },
    '/api/quests/status': {
        'required': ['success', 'quests'],
        'types': {'success': bool, 'quests': list}
    },
    '/api/worker/status': {
        'required': ['success', 'running', 'managed'],
        'types': {'success': bool, 'running': bool, 'managed': bool}
    },
    '/api/groq_key': {
        'required': ['success', 'configured'],
        'types': {'success': bool, 'configured': bool}
    },
    '/api/stop_status': {
        'required': ['stopped'],
        'types': {'stopped': bool}
    },
    '/api/runtime_speed': {
        'required': ['success', 'speed'],
        'types': {'success': bool, 'speed': (int, float)}
    }
}


@pytest.mark.parametrize("route,schema", [(k, v) for k, v in ROUTE_CONTRACTS.items()])
def test_route_contract(client, localhost_kwargs, route, schema):
    """Verify route returns expected JSON structure"""
    response = client.get(route, **localhost_kwargs)
    assert response.status_code == 200, f"{route} returned {response.status_code}"

    data = json.loads(response.data)

    # Check required fields
    for field in schema['required']:
        assert field in data, f"{route} missing field: {field}"

    # Check types
    for field, expected_type in schema['types'].items():
        if field in data:
            assert isinstance(data[field], expected_type), \
                f"{route}.{field} expected {expected_type}, got {type(data[field])}"
