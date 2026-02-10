"""
rlif_rules.py
-------------
Rule extraction, formatting and persistent storage for RLIF.

Rules are stored in JSON format under the experiment directory:
    learned_lessons.json
Each entry is a dict:
{
    "timestamp": "<ISO‑8601>",
    "rule": "<text>"
}
"""

import json
import os
from datetime import datetime
from typing import List, Dict

# Path is relative to the experiment folder.
_LESSONS_FILE = os.path.join(
    os.path.dirname(__file__), "learned_lessons.json"
)


def _load_rules() -> List[Dict]:
    if not os.path.exists(_LESSONS_FILE):
        return []
    with open(_LESSONS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_rules(rules: List[Dict]) -> None:
    with open(_LESSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)


def add_rule(rule_text: str) -> None:
    """
    Append a new rule to the persistent lesson store.

    Parameters
    ----------
    rule_text: str
        Human‑readable rule description.
    """
    rule_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "rule": rule_text.strip(),
    }

    rules = _load_rules()
    # Avoid exact duplicates.
    if any(r["rule"] == rule_entry["rule"] for r in rules):
        return

    rules.append(rule_entry)
    _save_rules(rules)


def get_all_rules() -> List[Dict]:
    """Return the full list of learned rules."""
    return _load_rules()