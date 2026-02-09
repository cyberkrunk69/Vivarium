"""
knowledge_packs.py

Core implementation of the Knowledge Pack system.

Features
--------
- KnowledgePack: container for a category, its lessons and (optional) embeddings.
- PackManager: load/save/search knowledge packs from the `knowledge_packs/` folder.
- auto_categorize_lesson: very light‑weight heuristic categorisation.
- get_relevant_packs: retrieve the most relevant packs for a given task prompt.

During import the module will attempt to migrate any existing lessons from
`learned_lessons.json` into the appropriate category packs.  This migration is
idempotent – it will only run once per session.
"""

import json
import os
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

BASE_DIR = Path(__file__).parent
PACKS_DIR = BASE_DIR / "knowledge_packs"
LEARNED_LESSONS_PATH = BASE_DIR / "learned_lessons.json"

# Ensure the packs directory exists
PACKS_DIR.mkdir(exist_ok=True)

# Simple logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #


def _simple_text_vector(text: str) -> Dict[str, int]:
    """
    Very naive “embedding”: a bag‑of‑words frequency dictionary.
    Used only for intra‑process similarity scoring – not meant to be
    production‑grade.
    """
    tokens = [
        token.lower()
        for token in text.split()
        if token.isalpha()
    ]
    freq: Dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


def _cosine_similarity(v1: Dict[str, int], v2: Dict[str, int]) -> float:
    """Cosine similarity for two bag‑of‑words dict vectors."""
    # Intersection
    intersect = set(v1.keys()) & set(v2.keys())
    dot = sum(v1[t] * v2[t] for t in intersect)

    norm1 = sum(val * val for val in v1.values()) ** 0.5
    norm2 = sum(val * val for val in v2.values()) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


# --------------------------------------------------------------------------- #
# Core data structures
# --------------------------------------------------------------------------- #


class KnowledgePack:
    """
    A KnowledgePack groups lessons under a logical *category*.
    Optionally it can hold pre‑computed embeddings for each lesson.
    """

    def __init__(self, category: str, lessons: List[str] = None):
        self.category = category
        self.lessons: List[str] = lessons or []
        # Lazy embeddings – generated on demand
        self._embeddings: List[Dict[str, int]] | None = None

    @property
    def embeddings(self) -> List[Dict[str, int]]:
        """Compute (or retrieve) simple bag‑of‑words embeddings."""
        if self._embeddings is None:
            self._embeddings = [_simple_text_vector(l) for l in self.lessons]
        return self._embeddings

    def add_lesson(self, lesson: str) -> None:
        self.lessons.append(lesson)
        # Invalidate embeddings cache
        self._embeddings = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "lessons": self.lessons,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "KnowledgePack":
        return KnowledgePack(category=data["category"], lessons=data.get("lessons", []))


# --------------------------------------------------------------------------- #
# Pack manager
# --------------------------------------------------------------------------- #


class PackManager:
    """
    Handles persistence and retrieval of KnowledgePack objects.
    Packs are stored as JSON files under `knowledge_packs/`.
    """

    def __init__(self, packs_dir: Path = PACKS_DIR):
        self.packs_dir = packs_dir
        self._cache: Dict[str, KnowledgePack] = {}

    # ------------------------------------------------------------------- #
    # Loading / saving
    # ------------------------------------------------------------------- #

    def load_pack(self, category: str) -> KnowledgePack:
        """Load a pack from disk (cached after first load)."""
        if category in self._cache:
            return self._cache[category]

        pack_path = self.packs_dir / f"{category}.json"
        if not pack_path.is_file():
            # Create an empty pack on‑the‑fly
            pack = KnowledgePack(category=category)
            self._cache[category] = pack
            return pack

        with open(pack_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pack = KnowledgePack.from_dict(data)
        self._cache[category] = pack
        return pack

    def save_pack(self, pack: KnowledgePack) -> None:
        """Write a pack to its JSON file."""
        pack_path = self.packs_dir / f"{pack.category}.json"
        with open(pack_path, "w", encoding="utf-8") as f:
            json.dump(pack.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info(f"Saved knowledge pack '{pack.category}' with {len(pack.lessons)} lessons.")

    def all_packs(self) -> List[KnowledgePack]:
        """Load every JSON file in the packs directory."""
        packs: List[KnowledgePack] = []
        for file in self.packs_dir.glob("*.json"):
            category = file.stem
            packs.append(self.load_pack(category))
        return packs

    # ------------------------------------------------------------------- #
    # Search
    # ------------------------------------------------------------------- #

    def search(self, query: str, top_k: int = 3) -> List[Tuple[KnowledgePack, float]]:
        """
        Return the `top_k` packs most relevant to `query` based on average
        cosine similarity between the query vector and each lesson vector.
        """
        query_vec = _simple_text_vector(query)
        scored: List[Tuple[KnowledgePack, float]] = []

        for pack in self.all_packs():
            if not pack.lessons:
                continue
            # Average similarity across all lessons in the pack
            sims = [_cosine_similarity(query_vec, emb) for emb in pack.embeddings]
            avg_sim = sum(sims) / len(sims)
            scored.append((pack, avg_sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


# --------------------------------------------------------------------------- #
# Categorisation heuristics
# --------------------------------------------------------------------------- #


CATEGORY_KEYWORDS = {
    "claude": ["claude", "anthropic", "prompt", "llm", "conversation"],
    "groq": ["groq", "llama", "mixtral", "groq api"],
    "safety": ["safety", "ethics", "harm", "policy", "restricted"],
    "general": [],  # fallback
}


def auto_categorize_lesson(lesson_text: str) -> str:
    """
    Very lightweight rule‑based categorisation.
    Returns the first matching category; defaults to 'general'.
    """
    lowered = lesson_text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return category
    return "general"


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #


def get_relevant_packs(task_text: str, top_k: int = 3) -> List[KnowledgePack]:
    """
    Retrieve the most relevant knowledge packs for a given task description.
    """
    manager = PackManager()
    results = manager.search(task_text, top_k=top_k)
    packs = [pack for pack, _score in results]
    logger.info(
        f"Relevant packs for task '{task_text[:30]}...': {[p.category for p in packs]}"
    )
    return packs


# --------------------------------------------------------------------------- #
# Migration from legacy lessons (run once on import)
# --------------------------------------------------------------------------- #


def _migrate_legacy_lessons() -> None:
    """
    Read `learned_lessons.json`, auto‑categorise each lesson and store it
    in the appropriate category pack.  The function is safe to call multiple
    times – it will not duplicate lessons.
    """
    if not LEARNED_LESSONS_PATH.is_file():
        logger.warning("No legacy lessons file found at %s", LEARNED_LESSONS_PATH)
        return

    with open(LEARNED_LESSONS_PATH, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse learned_lessons.json: %s", exc)
            return

    # Expected format: list of {"lesson": "..."} or list of strings
    lessons: List[str] = []
    if isinstance(raw, list):
        for entry in raw:
            if isinstance(entry, dict) and "lesson" in entry:
                lessons.append(entry["lesson"])
            elif isinstance(entry, str):
                lessons.append(entry)
    else:
        logger.error("Unexpected structure in learned_lessons.json")
        return

    manager = PackManager()
    added = 0
    for lesson in lessons:
        category = auto_categorize_lesson(lesson)
        pack = manager.load_pack(category)
        if lesson not in pack.lessons:
            pack.add_lesson(lesson)
            manager.save_pack(pack)
            added += 1

    logger.info("Migrated %d lessons into knowledge packs.", added)


# Run migration on import (only if there are lessons to migrate)
_migrate_legacy_lessons()