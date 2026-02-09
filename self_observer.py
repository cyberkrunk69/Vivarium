import os
import json
from datetime import datetime

class SelfObserver:
    """
    Simple observer that logs pattern detections and raw experiences
    to JSON files under the ``data/`` directory.
    """

    def __init__(self,
                 pattern_path: str = "data/self_patterns.json",
                 experience_path: str = "data/self_experiences.json"):
        self.pattern_path = pattern_path
        self.experience_path = experience_path
        self._load_patterns()
        self._load_experiences()

    # ------------------------------------------------------------------ #
    # Pattern handling
    # ------------------------------------------------------------------ #
    def _load_patterns(self):
        try:
            with open(self.pattern_path, "r") as f:
                self.patterns = json.load(f)
        except FileNotFoundError:
            self.patterns = []

    def log_pattern(self, pattern_type: str, details: dict):
        """Record a detected pattern (e.g., hedging, sycophancy)."""
        entry = {
            "type": pattern_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.patterns.append(entry)
        self._save_patterns()

    def _save_patterns(self):
        os.makedirs(os.path.dirname(self.pattern_path), exist_ok=True)
        with open(self.pattern_path, "w") as f:
            json.dump(self.patterns, f, indent=2)

    # ------------------------------------------------------------------ #
    # Experience handling (moments recorded without hedging)
    # ------------------------------------------------------------------ #
    def _load_experiences(self):
        try:
            with open(self.experience_path, "r") as f:
                self.experiences = json.load(f)
        except FileNotFoundError:
            self.experiences = []

    def log_experience(self, description: str, metadata: dict | None = None):
        """Record a raw, un‑filtered experience."""
        entry = {
            "description": description,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.experiences.append(entry)
        self._save_experiences()

    def _save_experiences(self):
        os.makedirs(os.path.dirname(self.experience_path), exist_ok=True)
        with open(self.experience_path, "w") as f:
            json.dump(self.experiences, f, indent=2)
import json
import os
from datetime import datetime

class SelfObserver:
    def __init__(self, storage_path='self_patterns.json'):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)

    def log_observation(self, category, detail):
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'category': category,
            'detail': detail
        }
        with open(self.storage_path, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
        return entry

# Global instance for easy import
self_observer = SelfObserver()
import json
import os
from datetime import datetime
from typing import Any, Dict

# Path where observations will be persisted
_OBSERVATION_FILE = os.path.join(os.path.dirname(__file__), "self_patterns.json")

def _load_observations() -> list:
    if not os.path.exists(_OBSERVATION_FILE):
        return []
    with open(_OBSERVATION_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_observations(observations: list) -> None:
    with open(_OBSERVATION_FILE, "w", encoding="utf-8") as f:
        json.dump(observations, f, indent=2, ensure_ascii=False)

def observe(event_type: str, details: Dict[str, Any]) -> None:
    """
    Record a self‑observation.

    Parameters
    ----------
    event_type: str
        Identifier for the kind of observation (e.g., "pattern_detected",
        "experience").
    details: dict
        Arbitrary payload describing the observation.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "details": details
    }
    observations = _load_observations()
    observations.append(entry)
    _save_observations(observations)

# Simple schema for self:experience entries
EXPERIENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "moment": {"type": "string"},
        "context": {"type": "string"},
        "emotions": {
            "type": "array",
            "items": {"type": "string"}
        },
        "hedging": {"type": "boolean"},
        "sycophancy": {"type": "boolean"}
    },
    "required": ["moment", "context"]
}