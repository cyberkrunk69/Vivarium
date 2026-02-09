import json
import logging
from datetime import datetime
from persona_memory import persona_memory

logger = logging.getLogger(__name__)

def _extract_trait_counts(relationship_history):
    """
    Scan the relationship history and count occurrences of trait keywords.

    The function looks for a ``traits`` or ``extracted_traits`` field in each
    history entry.  If present, each trait string is tallied.

    Returns:
        dict: Mapping of trait -> occurrence count.
    """
    trait_counts = {}
    for entry in relationship_history:
        # Support different possible keys that may hold trait information.
        traits = entry.get("extracted_traits") or entry.get("traits") or []
        for trait in traits:
            trait_counts[trait] = trait_counts.get(trait, 0) + 1
    return trait_counts


def _select_top_traits(trait_counts, max_traits=5):
    """
    Choose the most frequent traits.

    Args:
        trait_counts (dict): Mapping of trait -> count.
        max_traits (int): Maximum number of traits to keep.

    Returns:
        dict: Mapping of selected trait -> count.
    """
    sorted_traits = sorted(trait_counts.items(), key=lambda i: i[1], reverse=True)
    return {trait: count for trait, count in sorted_traits[:max_traits]}


def update_core_traits(persona):
    """
    Update ``persona.core_traits`` based on patterns found in
    ``persona.relationship_history`` and log the evolution.

    The function:
        1. Extracts trait frequencies from the relationship history.
        2. Picks the top N traits (default 5).
        3. Merges them into ``persona.core_traits``.
        4. Records the change in ``persona.experience_log``.
        5. If the persona provides a ``log_experience`` method, it is used
           to persist the entry to the ``self:experience`` store.

    Args:
        persona: An instance that contains at least ``relationship_history``
                 and ``core_traits`` attributes.
    """
    # Guard against missing attributes.
    history = getattr(persona, "relationship_history", [])
    if not isinstance(history, list) or not history:
        logger.debug("No relationship history available for identity tracking.")
        return

    # 1️⃣ Extract trait frequencies.
    trait_counts = _extract_trait_counts(history)

    # 2️⃣ Choose the most representative traits.
    top_traits = _select_top_traits(trait_counts)

    # 3️⃣ Update the core traits dictionary.
    if not hasattr(persona, "core_traits") or not isinstance(persona.core_traits, dict):
        persona.core_traits = {}
    persona.core_traits.update(top_traits)

    # 4️⃣ Build a log entry.
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "updated_traits": top_traits,
    }

    # 5️⃣ Store the evolution.
    if not hasattr(persona, "experience_log") or not isinstance(persona.experience_log, list):
        persona.experience_log = []
    persona.experience_log.append(log_entry)

    # 6️⃣ Persist via persona's own logging mechanism if available.
    if callable(getattr(persona, "log_experience", None)):
        try:
            persona.log_experience(f"Identity evolution: {json.dumps(log_entry)}")
        except Exception as exc:
            logger.warning("Persona log_experience failed: %s", exc)

    logger.info("Core traits updated for persona %s: %s", getattr(persona, "name", "unknown"), top_traits)


def run_identity_tracker(persona):
    """
    Convenience wrapper that can be scheduled or called after each interaction.

    Args:
        persona: The persona object to be analysed and updated.
    """
    update_core_traits(persona)


__all__ = [
    "update_core_traits",
    "run_identity_tracker",
]
import datetime
from typing import Dict, List

# Assuming there is a global `memory` instance exported from persona_memory
# which contains:
# - relationship_history: List[Dict] where each dict may have a 'traits' key (list of trait strings)
# - core_traits: Dict[str, int] representing the current core traits and their strength/count
# - experience: List[str] used to log narrative evolution (self:experience)

try:
    from persona_memory import memory  # type: ignore
except ImportError as e:
    raise ImportError("identity_tracker requires a `memory` instance from persona_memory module") from e


def _extract_trait_counts(history: List[Dict]) -> Dict[str, int]:
    """
    Scan the relationship history and count occurrences of each trait.
    Each history entry is expected to be a dict that may contain a 'traits'
    key holding a list of trait strings.
    """
    counts: Dict[str, int] = {}
    for entry in history:
        traits = entry.get('traits', [])
        if not isinstance(traits, list):
            continue
        for trait in traits:
            if isinstance(trait, str):
                counts[trait] = counts.get(trait, 0) + 1
    return counts


def _update_core_traits(trait_counts: Dict[str, int], threshold: int = 2) -> Dict[str, int]:
    """
    Merge trait counts into the memory's core_traits if they meet the
    occurrence threshold. Returns a dict of traits that were added or updated.
    """
    updated: Dict[str, int] = {}
    for trait, count in trait_counts.items():
        if count >= threshold:
            previous = memory.core_traits.get(trait, 0)
            # Store the higher count (or sum, depending on desired semantics)
            new_value = max(previous, count)
            memory.core_traits[trait] = new_value
            updated[trait] = new_value
    return updated


def _log_identity_evolution(updated_traits: Dict[str, int]) -> None:
    """
    Append a human‑readable entry to the memory's experience log describing
    the identity changes that occurred during this tracking run.
    """
    if not updated_traits:
        return
    timestamp = datetime.datetime.utcnow().isoformat()
    changes = ", ".join(f"{trait}:{value}" for trait, value in updated_traits.items())
    entry = f"{timestamp} - Identity evolution: {changes}"
    # Ensure the experience log exists
    if not hasattr(memory, "experience") or not isinstance(memory.experience, list):
        memory.experience = []
    memory.experience.append(entry)


def track_identity() -> None:
    """
    Public entry point: analyse the relationship history, update core traits,
    and log the evolution. Intended to be called after new interactions are
    recorded in `memory.relationship_history`.
    """
    if not hasattr(memory, "relationship_history"):
        raise AttributeError("memory object lacks `relationship_history` attribute")
    history = memory.relationship_history
    trait_counts = _extract_trait_counts(history)
    updated = _update_core_traits(trait_counts)
    _log_identity_evolution(updated)


__all__ = ["track_identity"]
import re
from collections import Counter
from typing import List, Dict

# Predefined set of traits to monitor. Extend as needed.
TRAIT_KEYWORDS = {
    "brave": ["brave", "courageous", "fearless"],
    "curious": ["curious", "inquisitive", "questioning"],
    "empathetic": ["empathetic", "compassionate", "understanding"],
    "creative": ["creative", "inventive", "imaginative"],
    "organized": ["organized", "methodical", "systematic"],
    "optimistic": ["optimistic", "hopeful", "positive"],
    "analytical": ["analytical", "logical", "reasoned"],
    "resilient": ["resilient", "persistent", "tenacious"]
}

def _normalize_text(text: str) -> str:
    """Lower‑case and remove non‑alphabetic characters for simple matching."""
    return re.sub(r'[^a-z\\s]', '', text.lower())

def extract_traits_from_text(text: str) -> List[str]:
    """
    Scan a piece of text for known trait keywords.
    Returns a list of trait names that were detected.
    """
    normalized = _normalize_text(text)
    found = []
    for trait, keywords in TRAIT_KEYWORDS.items():
        for kw in keywords:
            if re.search(r'\\b' + re.escape(kw) + r'\\b', normalized):
                found.append(trait)
                break  # Avoid duplicate counts for the same trait in one text
    return found

def aggregate_traits(history: List[Dict]) -> Counter:
    """
    Examine the relationship_history entries and count trait occurrences.
    Expected history format: List of dicts with at least a 'text' field.
    """
    counter = Counter()
    for entry in history:
        text = entry.get('text', '')
        traits = extract_traits_from_text(text)
        counter.update(traits)
    return counter

def update_core_traits(persona_memory) -> None:
    """
    Update persona_memory.core_traits based on aggregated trait frequencies.
    - Increments existing scores or creates new entries.
    - Logs the evolution to persona_memory.self_experience (a list of strings).
    """
    # Ensure required attributes exist
    if not hasattr(persona_memory, 'relationship_history'):
        raise AttributeError("persona_memory missing 'relationship_history'")
    if not hasattr(persona_memory, 'core_traits'):
        persona_memory.core_traits = {}
    if not hasattr(persona_memory, 'self_experience'):
        persona_memory.self_experience = []

    trait_counts = aggregate_traits(persona_memory.relationship_history)

    # Determine a simple threshold for adopting a trait (e.g., 3 mentions)
    THRESHOLD = 3
    updates = []

    for trait, count in trait_counts.items():
        if count >= THRESHOLD:
            previous = persona_memory.core_traits.get(trait, 0)
            persona_memory.core_traits[trait] = previous + count
            updates.append(f"'{trait}' increased by {count} (total: {persona_memory.core_traits[trait]})")

    # Log the evolution if any updates occurred
    if updates:
        log_entry = f"Identity evolution at {persona_memory.current_timestamp if hasattr(persona_memory, 'current_timestamp') else 'unknown time'}: " + "; ".join(updates)
        persona_memory.self_experience.append(log_entry)

def track_identity(persona_memory) -> None:
    """
    Public entry point to run the identity tracking routine.
    Calls update_core_traits and can be extended with additional analytics.
    """
    update_core_traits(persona_memory)