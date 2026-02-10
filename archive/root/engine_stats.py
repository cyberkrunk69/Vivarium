import threading
from collections import defaultdict
from typing import Optional

# Thread‑safe in‑memory store for engine performance metrics.
# Structure: {task_type: {engine_name: {"success": int, "total": int}}}
_stats_lock = threading.Lock()
_engine_stats: defaultdict = defaultdict(lambda: defaultdict(lambda: {"success": 0, "total": 0}))

def record_engine_result(engine_name: str, task_type: str, success: bool) -> None:
    """
    Update the statistics for a given engine / task_type pair.
    """
    with _stats_lock:
        entry = _engine_stats[task_type][engine_name]
        entry["total"] += 1
        if success:
            entry["success"] += 1

def get_best_engine(task_type: str) -> Optional[str]:
    """
    Return the engine with the highest success rate for the supplied task_type.
    If multiple engines share the same rate, the one with the most executions is chosen.
    Returns None if no data is available for the task_type.
    """
    with _stats_lock:
        engines = _engine_stats.get(task_type, {})
        if not engines:
            return None

        # Compute success rate and pick the best
        best_engine = None
        best_rate = -1.0
        best_total = -1
        for engine, data in engines.items():
            total = data["total"]
            if total == 0:
                continue
            rate = data["success"] / total
            if (rate > best_rate) or (rate == best_rate and total > best_total):
                best_engine = engine
                best_rate = rate
                best_total = total
        return best_engine
import json
import os
from collections import defaultdict
from threading import Lock

_STATS_FILE = os.path.join(os.path.dirname(__file__), "engine_stats.json")
_LOCK = Lock()

def _load_stats():
    if not os.path.exists(_STATS_FILE):
        return {}
    with open(_STATS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_stats(stats):
    with open(_STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

class EngineStats:
    """
    Tracks success/failure counts per engine per task type.
    Provides a simple success‑rate based recommendation.
    """
    def __init__(self):
        self.stats = defaultdict(lambda: {"success": 0, "total": 0})
        self._load()

    def _load(self):
        raw = _load_stats()
        for key, val in raw.items():
            self.stats[key] = val

    def _persist(self):
        # Serialize only simple dicts
        raw = {k: v for k, v in self.stats.items()}
        _save_stats(raw)

    def record(self, engine_name: str, task_type: str, success: bool):
        """
        Record the outcome of a task run.
        """
        key = f"{engine_name}||{task_type}"
        with _LOCK:
            self.stats[key]["total"] += 1
            if success:
                self.stats[key]["success"] += 1
            self._persist()

    def success_rate(self, engine_name: str, task_type: str) -> float:
        key = f"{engine_name}||{task_type}"
        data = self.stats.get(key, {"success": 0, "total": 0})
        if data["total"] == 0:
            return 0.0
        return data["success"] / data["total"]

    def best_engine(self, task_type: str, candidate_engines):
        """
        Return the engine with the highest success rate for the given task_type.
        If none have history, fall back to the first candidate.
        """
        best = None
        best_rate = -1.0
        for engine in candidate_engines:
            rate = self.success_rate(engine, task_type)
            if rate > best_rate:
                best_rate = rate
                best = engine
        return best or (candidate_engines[0] if candidate_engines else None)

# Global singleton for easy import
engine_stats = EngineStats()