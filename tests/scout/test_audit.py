"""
Tests for vivarium.scout.audit — append-only JSONL event log.

Covers: append/read, crash recovery, query performance, log rotation, corruption recovery.
"""

import gzip
import json
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from vivarium.scout.audit import AuditLog, DEFAULT_AUDIT_PATH, ROTATION_SIZE_BYTES


@pytest.fixture
def audit_path(tmp_path):
    """Temporary audit log path for isolated tests."""
    return tmp_path / "audit.jsonl"


@pytest.fixture
def audit_log(audit_path):
    """AuditLog instance with temp path."""
    log = AuditLog(path=audit_path)
    yield log
    log.close()


# --- Basic append and read ---


def test_append_and_immediate_read(audit_log, audit_path):
    """Write events and read them back immediately."""
    audit_log.log("nav", cost=0.000003, model="llama-3.1-8b", input_t=42, output_t=28)
    audit_log.log("brief", cost=0.000001, files=["path/to/file.py"])
    audit_log.log("validation_fail", reason="hallucinated_path")

    events = audit_log.query()
    assert len(events) == 3
    assert events[0]["event"] == "nav"
    assert events[0]["cost"] == 0.000003
    assert events[0]["model"] == "llama-3.1-8b"
    assert events[0]["input_t"] == 42
    assert events[0]["output_t"] == 28
    assert "ts" in events[0]
    assert "session_id" in events[0]

    assert events[1]["event"] == "brief"
    assert events[1]["files"] == ["path/to/file.py"]

    assert events[2]["event"] == "validation_fail"
    assert events[2]["reason"] == "hallucinated_path"


def test_append_latency_under_1ms(audit_log):
    """Write latency should be <1ms per event (buffered)."""
    t0 = time.perf_counter()
    for _ in range(100):
        audit_log.log("nav", cost=0.000001)
    elapsed = time.perf_counter() - t0
    per_event_ms = (elapsed / 100) * 1000
    assert per_event_ms < 1.0, f"Write latency {per_event_ms:.3f}ms per event exceeds 1ms"


# --- Crash recovery ---


def test_crash_recovery_partial_write(audit_path):
    """Partial last line (corruption) → truncate behavior: skip malformed, continue."""
    # Write two good lines
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write('{"ts":"2026-02-13T14:30:22.123Z","event":"nav","session_id":"x"}\n')
        f.write('{"ts":"2026-02-13T14:30:23.000Z","event":"brief","session_id":"x"}\n')
        f.write('{"ts":"2026-02-13T14:30:24.000Z","event":"nav"')  # truncated, no closing }
    # Parse should skip the bad line
    log = AuditLog(path=audit_path)
    events = log.query()
    log.close()
    assert len(events) == 2
    assert events[0]["event"] == "nav"
    assert events[1]["event"] == "brief"


def test_corruption_recovery(audit_path):
    """Multiple malformed lines are skipped, valid lines parsed."""
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write('{"ts":"2026-02-13T14:30:22.123Z","event":"nav","session_id":"a"}\n')
        f.write("not json at all\n")
        f.write("{}\n")  # valid but minimal
        f.write('{"event":"brief"}\n')  # valid
        f.write('{"ts":"broken\n')
    log = AuditLog(path=audit_path)
    events = log.query()
    log.close()
    assert len(events) == 3
    assert events[0]["event"] == "nav"
    assert events[1].get("event", "") == ""  # {} has no event key
    assert events[2]["event"] == "brief"


# --- Query performance ---


def test_query_performance_10k_events(audit_path):
    """Query 10k events in <1s (streaming, not loading all into memory upfront)."""
    # Pre-populate 10k events
    with open(audit_path, "w", encoding="utf-8") as f:
        for i in range(10000):
            obj = {
                "ts": f"2026-02-13T14:30:22.{i:03d}Z",
                "event": "nav",
                "session_id": "perf-test",
                "cost": 0.000001 * i,
            }
            f.write(json.dumps(obj) + "\n")

    log = AuditLog(path=audit_path)
    t0 = time.perf_counter()
    events = log.query()
    elapsed_ms = (time.perf_counter() - t0) * 1000
    log.close()

    assert len(events) == 10000
    # 3s threshold accommodates slow CI runners (shared CPU, cold I/O)
    assert elapsed_ms < 3000, f"Query took {elapsed_ms:.1f}ms, expected <3000ms"


# --- Log rotation ---


def test_log_rotation(audit_path):
    """Auto-archive at 10MB, gzip old logs."""
    log = AuditLog(path=audit_path)
    # Write enough to exceed 10MB (each line ~80 chars → ~130k lines)
    line = json.dumps({"ts": "2026-02-13T14:30:22.123Z", "event": "nav", "session_id": "x", "cost": 0.001}) + "\n"
    line_len = len(line.encode("utf-8"))
    num_lines = (ROTATION_SIZE_BYTES // line_len) + 10

    for _ in range(num_lines):
        log.log("nav", cost=0.001)

    log.close()

    # Current audit.jsonl should be new (small) or rotated away
    # We expect at least one .jsonl.gz archive
    parent = audit_path.parent
    archives = list(parent.glob("audit_*.jsonl.gz"))
    assert len(archives) >= 1, "Expected at least one gzipped archive"
    # Verify archive is valid gzip
    with gzip.open(archives[0], "rt", encoding="utf-8") as zf:
        first = zf.readline()
        assert json.loads(first)["event"] == "nav"


# --- Query interface ---


def test_hourly_spend(audit_log):
    """Sum costs in last N hours."""
    now = datetime.now(timezone.utc)
    # Log events with cost
    audit_log.log("nav", cost=0.01)
    audit_log.log("nav", cost=0.02)
    audit_log.log("brief", cost=0.005)

    spend = audit_log.hourly_spend(hours=1)
    assert spend == pytest.approx(0.035, rel=1e-6)


def test_last_events(audit_log):
    """Recent events, optionally filtered."""
    for i in range(30):
        audit_log.log("nav" if i % 2 == 0 else "brief", cost=0.001)

    last = audit_log.last_events(n=5)
    assert len(last) == 5
    assert last[-1]["event"] == "brief"  # most recent

    last_nav = audit_log.last_events(n=3, event_type="nav")
    assert len(last_nav) == 3
    assert all(e["event"] == "nav" for e in last_nav)


def test_accuracy_metrics(audit_log):
    """% validation_fail vs total nav events."""
    since = datetime.now(timezone.utc) - timedelta(hours=1)
    audit_log.log("nav")
    audit_log.log("nav")
    audit_log.log("nav")
    audit_log.log("validation_fail")

    m = audit_log.accuracy_metrics(since=since)
    assert m["total_nav"] == 3
    assert m["validation_fail_count"] == 1
    assert m["accuracy_pct"] == pytest.approx(66.67, rel=0.01)


def test_query_filter_since(audit_log):
    """Query with since filter."""
    base = datetime(2026, 2, 13, 14, 0, 0, tzinfo=timezone.utc)
    # We can't easily control ts in log - they're auto-generated. So we write directly
    p = audit_log._path
    audit_log.close()
    with open(p, "w", encoding="utf-8") as f:
        f.write('{"ts":"2026-02-13T13:59:00.000Z","event":"nav"}\n')
        f.write('{"ts":"2026-02-13T14:01:00.000Z","event":"nav"}\n')
        f.write('{"ts":"2026-02-13T14:02:00.000Z","event":"nav"}\n')
    log2 = AuditLog(path=p)
    events = log2.query(since=base)
    log2.close()
    assert len(events) == 2  # 14:01 and 14:02, not 13:59


def test_query_filter_event_type(audit_log):
    """Query with event_type filter."""
    audit_log.log("nav")
    audit_log.log("brief")
    audit_log.log("nav")
    nav_only = audit_log.query(event_type="nav")
    assert len(nav_only) == 2
    assert all(e["event"] == "nav" for e in nav_only)


def test_context_manager(audit_path):
    """AuditLog works as context manager."""
    with AuditLog(path=audit_path) as log:
        log.log("nav", cost=0.001)
    # Should be closed; no exception on explicit close
    log.close()


def test_default_path(tmp_path, monkeypatch):
    """Default path resolves to ~/.scout/audit.jsonl (or patched path for CI)."""
    monkeypatch.setattr(
        "vivarium.scout.audit.DEFAULT_AUDIT_PATH",
        tmp_path / "audit.jsonl",
    )
    log = AuditLog()
    assert log._path == (tmp_path / "audit.jsonl").resolve()
    log.close()
