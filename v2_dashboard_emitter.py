"""
V2 Dashboard Event Emitter

Sends V2 Swarm Architecture events to the dashboard server.
Non-blocking, fire-and-forget HTTP posts.
"""

import threading
import json
from typing import Optional, Dict, Any, List


DASHBOARD_URL = "http://localhost:8420"


def _post_async(endpoint: str, data: Dict[str, Any]):
    """Fire-and-forget HTTP POST to dashboard."""
    def do_post():
        try:
            import urllib.request
            url = f"{DASHBOARD_URL}{endpoint}"
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            urllib.request.urlopen(req, timeout=2)
        except Exception:
            pass  # Silent fail - dashboard may not be running

    threading.Thread(target=do_post, daemon=True).start()


def emit_tool_hit(route: str, tool_name: str, confidence: float = 1.0, cost_saved: float = 0.01):
    """Emit a tool hit event to the dashboard."""
    _post_async('/api/v2/tool-hit', {
        'route': route,
        'tool': tool_name,
        'confidence': confidence,
        'cost_saved': cost_saved
    })


def emit_tool_miss():
    """Emit a tool miss event to the dashboard."""
    _post_async('/api/v2/tool-miss', {})


def emit_rlif_rule(rule: str, trigger: str = "", scope: str = ""):
    """Emit an RLIF rule creation event to the dashboard."""
    _post_async('/api/v2/rlif-rule', {
        'rule': rule,
        'trigger': trigger,
        'scope': scope
    })


def emit_drift(node_id: str, reason: str):
    """Emit an intent drift event to the dashboard."""
    _post_async('/api/v2/drift', {
        'nodeId': node_id,
        'reason': reason
    })


def emit_approval(approved: bool, confidence: float = 1.0, concerns: Optional[List[str]] = None):
    """Emit a user proxy approval event to the dashboard."""
    _post_async('/api/v2/approval', {
        'approved': approved,
        'confidence': confidence,
        'concerns': concerns or []
    })


def emit_v2_stats(tool_hit_rate: float = None, rlif_rules: int = None,
                  drift_incidents: int = None, approval_rate: float = None):
    """Emit a full V2 stats update to the dashboard."""
    data = {}
    if tool_hit_rate is not None:
        data['toolHitRate'] = tool_hit_rate
    if rlif_rules is not None:
        data['rlifRules'] = rlif_rules
    if drift_incidents is not None:
        data['driftIncidents'] = drift_incidents
    if approval_rate is not None:
        data['approvalRate'] = approval_rate

    if data:
        _post_async('/api/v2/stats', data)
