import json
import os
from datetime import datetime
from collections import Counter

# Path to the self experiences file
SELF_EXPERIENCES_PATH = os.path.join(os.path.dirname(__file__), "self_experiences.json")
# Path to the self patterns log file
SELF_PATTERNS_PATH = os.path.join(os.path.dirname(__file__), "self_patterns.json")

def _load_json(path):
    """Utility to safely load a JSON file."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_json(path, data):
    """Utility to write JSON data to a file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _extract_trait_keywords(text):
    """
    Very simple keyword extractor for trait mentions.
    Extend this list with the traits your persona uses.
    """
    traits = [
        "patience", "confidence", "curiosity", "empathy",
        "discipline", "creativity", "optimism", "resilience"
    ]
    found = []
    lowered = text.lower()
    for trait in traits:
        if trait in lowered:
            found.append(trait)
    return found

def analyze_and_suggest():
    """
    Reads the last 100 self:experience entries, analyses trait mentions,
    and logs suggestions for persona_memory trait updates to self:patterns.
    """
    experiences = _load_json(SELF_EXPERIENCES_PATH)

    # Ensure we have a list of entries
    if not isinstance(experiences, list):
        experiences = []

    # Take the last 100 entries
    recent = experiences[-100:]

    # Aggregate trait mentions
    trait_counter = Counter()
    for entry in recent:
        # Expect each entry to be a dict with a 'text' field containing the experience description
        text = entry.get("text", "")
        traits_found = _extract_trait_keywords(text)
        trait_counter.update(traits_found)

    # Determine suggestions based on simple frequency thresholds
    suggestions = {}
    total_mentions = sum(trait_counter.values()) or 1  # avoid division by zero
    for trait, count in trait_counter.items():
        frequency = count / total_mentions
        # If a trait appears in more than 10% of the recent experiences, suggest strengthening it
        if frequency > 0.10:
            suggestions[trait] = {
                "action": "strengthen",
                "reason": f"appears in {frequency:.0%} of recent experiences"
            }
        # If a trait appears in less than 2% of recent experiences, suggest reviewing it
        elif frequency < 0.02:
            suggestions[trait] = {
                "action": "review",
                "reason": f"rarely appears ({frequency:.0%}) in recent experiences"
            }

    # Prepare the log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": "trait_adjustment_suggestion",
        "suggestions": suggestions,
        "source": "trait_adjuster",
        "sample_size": len(recent)
    }

    # Append the suggestion to the self:patterns log
    patterns = _load_json(SELF_PATTERNS_PATH)
    if not isinstance(patterns, list):
        patterns = []
    patterns.append(log_entry)
    _save_json(SELF_PATTERNS_PATH, patterns)

# If this module is imported by a scheduler, expose a callable entry point
def run():
    """Entry point for the scheduled task."""
    analyze_and_suggest()
import json
from pathlib import Path
from datetime import datetime

def _load_experiences() -> list:
    """
    Load the self_experiences.json file and return its content as a list.
    Returns an empty list if the file does not exist or cannot be parsed.
    """
    experiences_path = Path(__file__).parent / "self_experiences.json"
    if not experiences_path.is_file():
        return []
    try:
        with experiences_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def _analyze_patterns(experiences: list) -> dict:
    """
    Very lightweight pattern analysis:
    - Count occurrences of any trait listed under the key ``detected_traits`` in each experience.
    - If a trait appears at least 5 times in the sampled window, generate a suggestion
      to strengthen that trait.
    Returns a dictionary mapping trait names to suggestion strings.
    """
    trait_counts = {}
    for exp in experiences:
        traits = exp.get("detected_traits", [])
        for trait in traits:
            trait_counts[trait] = trait_counts.get(trait, 0) + 1

    suggestions = {}
    for trait, count in trait_counts.items():
        if count >= 5:
            suggestions[trait] = (
                f"Consider strengthening '{trait}' (observed {count} times in the last 100 experiences)."
            )
    return suggestions

def _log_suggestions(suggestions: dict):
    """
    Append the generated suggestions to the ``self_patterns.json`` file under a
    timestamp key. The file acts as a simple log for all pattern‑analysis runs.
    """
    log_path = Path(__file__).parent / "self_patterns.json"
    # Load existing log if present
    if log_path.is_file():
        try:
            with log_path.open("r", encoding="utf-8") as f:
                log_data = json.load(f)
        except Exception:
            log_data = {}
    else:
        log_data = {}

    timestamp = datetime.utcnow().isoformat() + "Z"
    log_data[timestamp] = suggestions

    with log_path.open("w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

def run_trait_adjuster():
    """
    Entry point for the scheduled task.
    - Reads the last 100 self‑experience entries.
    - Analyzes them for recurring traits.
    - Logs any adjustment suggestions.
    """
    experiences = _load_experiences()
    if not experiences:
        return  # Nothing to process

    # Take the most recent 100 entries
    recent = experiences[-100:] if len(experiences) > 100 else experiences
    suggestions = _analyze_patterns(recent)
    if suggestions:
        _log_suggestions(suggestions)

if __name__ == "__main__":
    run_trait_adjuster()