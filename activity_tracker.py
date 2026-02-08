"""
activity_tracker.py
-------------------
Track concurrent activity by type and compute a novelty decay multiplier.

Purpose:
- Encourage novelty by reducing rewards when many residents do the same thing.
- Keep tracking lightweight and file-based (no external dependencies).
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Any

from utils import read_json, write_json, get_timestamp


WORKSPACE = Path(__file__).parent
STATE_FILE = WORKSPACE / ".swarm" / "activity_state.json"
LOCK_FILE = WORKSPACE / ".swarm" / "activity.lock"

LOCK_RETRIES = 25
LOCK_SLEEP_SECONDS = 0.05
STALE_SECONDS = 60 * 60  # 1 hour stale window

DECAY_RATE = 0.35
DECAY_FLOOR = 0.40


@contextmanager
def _activity_lock():
    acquired = False
    fd = None
    try:
        for _ in range(LOCK_RETRIES):
            try:
                fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                acquired = True
                break
            except FileExistsError:
                time.sleep(LOCK_SLEEP_SECONDS)
        if not acquired:
            # Best-effort: proceed without lock if contention persists
            yield
        else:
            yield
    finally:
        if acquired:
            try:
                if fd is not None:
                    os.close(fd)
                if LOCK_FILE.exists():
                    LOCK_FILE.unlink()
            except Exception:
                pass


def _load_state() -> Dict[str, Any]:
    return read_json(STATE_FILE, default={"entries": [], "updated_at": get_timestamp()})


def _save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = get_timestamp()
    write_json(STATE_FILE, state)


def _prune_stale(entries: list[dict], now_ts: float) -> list[dict]:
    fresh = []
    for entry in entries:
        started_at = entry.get("started_at_ts")
        if started_at is None:
            continue
        if now_ts - started_at <= STALE_SECONDS:
            fresh.append(entry)
    return fresh


def _decay_multiplier(concurrent_count: int) -> float:
    if concurrent_count <= 1:
        return 1.0
    return max(DECAY_FLOOR, 1.0 / (1.0 + DECAY_RATE * (concurrent_count - 1)))


def start_activity(identity_id: str, activity_type: str) -> Dict[str, Any]:
    """
    Register an active task and return concurrency + decay multiplier.
    """
    now_ts = time.time()
    with _activity_lock():
        state = _load_state()
        entries = _prune_stale(state.get("entries", []), now_ts)
        entries.append(
            {
                "identity_id": identity_id,
                "activity_type": activity_type,
                "started_at": get_timestamp(),
                "started_at_ts": now_ts,
            }
        )
        state["entries"] = entries
        _save_state(state)

    concurrent = sum(1 for e in entries if e.get("activity_type") == activity_type)
    return {
        "concurrent": concurrent,
        "decay_multiplier": _decay_multiplier(concurrent),
    }


def end_activity(identity_id: str, activity_type: str) -> None:
    """Remove an active task entry."""
    now_ts = time.time()
    with _activity_lock():
        state = _load_state()
        entries = _prune_stale(state.get("entries", []), now_ts)
        entries = [
            e for e in entries
            if not (e.get("identity_id") == identity_id and e.get("activity_type") == activity_type)
        ]
        state["entries"] = entries
        _save_state(state)


def get_concurrent(activity_type: str) -> int:
    now_ts = time.time()
    state = _load_state()
    entries = _prune_stale(state.get("entries", []), now_ts)
    return sum(1 for e in entries if e.get("activity_type") == activity_type)


__all__ = ["start_activity", "end_activity", "get_concurrent"]
