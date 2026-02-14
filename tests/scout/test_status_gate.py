"""
TICKET-10: Gate metrics in scout-status.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from vivarium.scout.audit import AuditLog
from vivarium.scout.cli.status import run_status


def test_gate_metrics_empty(tmp_path):
    """No gate events → gate_metrics returns zeros."""
    audit = AuditLog(path=tmp_path / "audit.jsonl")
    gate = audit.gate_metrics(last_n=10)
    assert gate["total"] == 0
    assert gate["pass_rate_pct"] == 0.0
    assert gate["avg_confidence"] == 0.0
    assert gate["last_queries"] == []


def test_gate_metrics_with_events(tmp_path):
    """Gate events → correct pass rate, avg confidence, last queries."""
    audit = AuditLog(path=tmp_path / "audit.jsonl")
    # Simulate 8 pass, 2 escalate
    for i in range(8):
        audit.log(
            "gate_compress",
            confidence=80 + i,
            config={"gaps": [], "attempt": 1},
        )
    audit.log("gate_compress", reason="stale_cascade", confidence=0)
    audit.log("gate_escalate", reason="max_retries", config={"last_error": "low confidence"})

    gate = audit.gate_metrics(last_n=10)
    assert gate["total"] == 10
    assert gate["pass_count"] == 8
    assert gate["escalate_count"] == 2
    assert gate["pass_rate_pct"] == 80.0
    assert 0.80 <= gate["avg_confidence"] <= 0.87
    assert gate["escalate_rate_pct"] == 20.0
    assert len(gate["last_queries"]) == 10


def test_status_includes_gate_health(tmp_path, monkeypatch):
    """run_status includes Gate Health section."""
    monkeypatch.setattr(
        "vivarium.scout.audit.DEFAULT_AUDIT_PATH",
        tmp_path / "audit.jsonl",
    )
    # Create audit with gate events
    audit = AuditLog(path=tmp_path / "audit.jsonl")
    audit.log("gate_compress", confidence=85, config={})
    audit.log("gate_compress", confidence=78, config={})
    audit.close()

    output = run_status(tmp_path)
    assert "Gate Health" in output
    assert "pass rate" in output or "no gate_compress events" in output
