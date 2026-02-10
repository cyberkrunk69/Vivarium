import json
import os
from datetime import datetime
from founding_memory import FOUNDING_PRINCIPLES  # assumes this constant exists

class PersonaMemory:
    def __init__(self, storage_path='persona_memory.json'):
        self.storage_path = storage_path
        self.state = {
            'core_traits': {},
            'relationship_history': [],
            'emotional_continuity': [],
            'principles': FOUNDING_PRINCIPLES
        }
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self.state = json.load(f)

    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.state, f, indent=2)

    # Core traits management
    def set_core_trait(self, name, value):
        self.state['core_traits'][name] = value
        self._save()

    def get_core_trait(self, name, default=None):
        return self.state['core_traits'].get(name, default)

    # Relationship history
    def add_interaction(self, partner_id, summary):
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'partner_id': partner_id,
            'summary': summary
        }
        self.state['relationship_history'].append(entry)
        self._save()

    # Emotional continuity
    def record_emotion(self, emotion, intensity=1.0):
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'emotion': emotion,
            'intensity': intensity
        }
        self.state['emotional_continuity'].append(entry)
        self._save()

    # Retrieval helpers
    def recent_interactions(self, limit=5):
        return self.state['relationship_history'][-limit:]

    def recent_emotions(self, limit=5):
        return self.state['emotional_continuity'][-limit:]

# Global instance for easy access
persona_memory = PersonaMemory()
import json
import os
from datetime import datetime
from typing import Any, Dict, List

_PERSONA_FILE = os.path.join(os.path.dirname(__file__), "persona_memory.json")

class PersonaMemory:
    """
    Persistent memory for the agent's persona:
    - core traits
    - relationship history
    - emotional continuity
    Aligns with founding_memory principles.
    """

    def __init__(self):
        self.state: Dict[str, Any] = {
            "core_traits": {},
            "relationships": [],
            "emotional_log": []
        }
        self._load()

    # ------------------------------------------------------------------
    # Core Trait Management
    # ------------------------------------------------------------------
    def set_core_trait(self, name: str, value: Any) -> None:
        self.state["core_traits"][name] = value
        self._save()

    def get_core_trait(self, name: str, default: Any = None) -> Any:
        return self.state["core_traits"].get(name, default)

    # ------------------------------------------------------------------
    # Relationship History
    # ------------------------------------------------------------------
    def add_relationship_event(self, partner_id: str, description: str) -> None:
        event = {
            "partner_id": partner_id,
            "description": description,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.state["relationships"].append(event)
        self._save()

    def get_relationships(self) -> List[Dict[str, Any]]:
        return self.state["relationships"]

    # ------------------------------------------------------------------
    # Emotional Continuity
    # ------------------------------------------------------------------
    def log_emotion(self, emotion: str, intensity: float = 1.0) -> None:
        entry = {
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.state["emotional_log"].append(entry)
        self._save()

    def recent_emotions(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.state["emotional_log"][-limit:]

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load(self) -> None:
        if os.path.exists(_PERSONA_FILE):
            with open(_PERSONA_FILE, "r", encoding="utf-8") as f:
                try:
                    self.state = json.load(f)
                except json.JSONDecodeError:
                    pass  # keep defaults if corrupted

    def _save(self) -> None:
        with open(_PERSONA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

# Initialize a global instance for easy import elsewhere
persona_memory = PersonaMemory()