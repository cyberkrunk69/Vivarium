import json
import os
from collections import defaultdict
from datetime import datetime

# Paths to data files – adjust if they are located elsewhere
CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "checkpoint.json")
GRIND_LOGS_PATH = os.path.join(os.path.dirname(__file__), "grind_logs.json")

def _load_entries():
    """Load task entries from checkpoint and grind logs."""
    entries = []
    for path in (CHECKPOINT_PATH, GRIND_LOGS_PATH):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    # Expect a list of dicts; if a dict with a key "entries", use it
                    if isinstance(data, dict) and "entries" in data:
                        data = data["entries"]
                    if isinstance(data, list):
                        entries.extend(data)
                except json.JSONDecodeError:
                    # Skip malformed files but continue processing the other source
                    continue
    return entries

def compute_cost_breakdown():
    """
    Compute cost aggregation by:
      * task file
      * phase
      * day (derived from timestamp)

    Returns a dictionary suitable for JSON serialization:
    {
        "by_file": {"file1.py": 12.34, ...},
        "by_phase": {"phaseA": 23.45, ...},
        "by_day": {"2023-09-01": 34.56, ...}
    }
    """
    entries = _load_entries()

    by_file = defaultdict(float)
    by_phase = defaultdict(float)
    by_day = defaultdict(float)

    for entry in entries:
        # Expected keys: task_file, phase, timestamp, cost
        file_name = entry.get("task_file", "unknown")
        phase = entry.get("phase", "unknown")
        cost = float(entry.get("cost", 0))

        # Timestamp handling – assume ISO format; fallback to current day if missing/invalid
        ts = entry.get("timestamp")
        try:
            day = datetime.fromisoformat(ts).date().isoformat() if ts else datetime.utcnow().date().isoformat()
        except (ValueError, TypeError):
            day = datetime.utcnow().date().isoformat()

        by_file[file_name] += cost
        by_phase[phase] += cost
        by_day[day] += cost

    # Convert defaultdicts to plain dicts for JSON serialization
    return {
        "by_file": dict(by_file),
        "by_phase": dict(by_phase),
        "by_day": dict(by_day)
    }