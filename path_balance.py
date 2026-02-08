"""
path_balance.py
---------------
Track task origin mix and provide balanced path multipliers.

Goal:
- Bias toward user requests & bounties.
- Keep other paths viable by granting small boosts when underrepresented.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

from utils import read_json, write_json, get_timestamp


WORKSPACE = Path(__file__).parent
STATE_FILE = WORKSPACE / ".swarm" / "path_balance.json"

WINDOW_DAYS = 7
MAX_EVENTS = 500

TARGET_MIX = {
    "user_request": 0.40,
    "bounty": 0.30,
    "maintenance": 0.20,
    "explore": 0.10,
}

BASE_BIAS = {
    "user_request": 1.05,
    "bounty": 1.03,
    "maintenance": 1.00,
    "explore": 0.98,
}

MIN_MULTIPLIER = 0.85
MAX_MULTIPLIER = 1.15


def _load_state() -> Dict[str, Any]:
    return read_json(STATE_FILE, default={"events": [], "updated_at": get_timestamp()})


def _save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = get_timestamp()
    write_json(STATE_FILE, state)


def _prune_events(events: list[dict]) -> list[dict]:
    cutoff = datetime.utcnow() - timedelta(days=WINDOW_DAYS)
    pruned = []
    for event in events:
        ts = event.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt >= cutoff:
            pruned.append(event)
    return pruned[-MAX_EVENTS:]


def record_path(origin: str) -> None:
    """Record a task origin event for balance tracking."""
    state = _load_state()
    events = _prune_events(state.get("events", []))
    events.append({"origin": origin, "timestamp": get_timestamp()})
    state["events"] = events[-MAX_EVENTS:]
    _save_state(state)


def get_path_multiplier(origin: str) -> float:
    """
    Return a multiplier based on how represented this origin is vs target.
    """
    state = _load_state()
    events = _prune_events(state.get("events", []))
    if not events:
        return BASE_BIAS.get(origin, 1.0)

    counts: Dict[str, int] = {}
    for e in events:
        counts[e.get("origin", "unknown")] = counts.get(e.get("origin", "unknown"), 0) + 1

    total = sum(counts.values()) or 1
    actual_ratio = counts.get(origin, 0) / total
    target_ratio = TARGET_MIX.get(origin, 0.05)

    if actual_ratio == 0:
        mix_multiplier = MAX_MULTIPLIER
    else:
        ratio = target_ratio / actual_ratio
        mix_multiplier = ratio ** 0.5  # dampen swings

    mix_multiplier *= BASE_BIAS.get(origin, 1.0)

    return max(MIN_MULTIPLIER, min(MAX_MULTIPLIER, mix_multiplier))


__all__ = ["record_path", "get_path_multiplier"]
