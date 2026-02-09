# ----------------------------------------------------------------------
# Auto‑inject relevant skills into a grind spawner.
# ----------------------------------------------------------------------
def auto_inject_into_spawner(self, spawner):
    """
    Register this registry’s skills with the given grind spawner.
    The spawner is expected to expose an ``add_skill`` method.
    """
    for skill_name, skill_obj in self.skills.items():
        try:
            spawner.add_skill(skill_name, skill_obj)
        except Exception as e:
            # Non‑critical – log and continue
            print(f"[SkillRegistry] Failed to inject skill '{skill_name}': {e}")
def _text_to_embedding(text: str) -> dict:
    """
    Simple TF‑IDF‑like embedding: normalized word frequency vector.
import re
import re
import math
# ----------------------------------------------------------------------
# Embedding utilities (simple TF‑IDF style word frequency vectors)
# ----------------------------------------------------------------------
import math
# ------------------------------------------------------------
# Automatic integration with grind_spawner:
# This patch monkey‑patches the prompt‑building function in
# grind_spawner so that any retrieved skill is injected into the
# prompt before execution.
# ------------------------------------------------------------
import importlib
import logging

_logger = logging.getLogger(__name__)

def _inject_skill_into_prompt(original_func):
    """Wrap ``original_func`` to prepend a relevant skill, if any."""
    def wrapper(*args, **kwargs):
        # Preserve original call signature – most prompt builders accept
        # a ``task_description`` (or similar) as the first positional arg.
        task_description = args[0] if args else kwargs.get('task_description', '')
        skill = retrieve_skill(task_description)  # <-- existing API
        if skill:
            # ``skill`` may be a dict like {'name': ..., 'code': ...}
            # or a tuple (name, code). Normalise it.
            if isinstance(skill, dict):
                skill_name = skill.get('name')
                skill_code = skill.get('code')
            else:
                # Assume (name, code)
                skill_name, skill_code = skill
            # Log the retrieval – Session number is taken from a
            # hypothetical ``session_id`` attribute if present.
            session_id = getattr(kwargs.get('context', {}), 'session_id', 'N')
            _logger.info(f"[Session {session_id}] Retrieved skill: {skill_name}")

            # Build the skill injection block.
            skill_block = f"RELEVANT SKILL: {skill_name}\\n{skill_code}\\n"
            # Call the original function to get the base prompt.
            base_prompt = original_func(*args, **kwargs)
            # Prepend the skill block.
            return skill_block + base_prompt
        # No skill found – just return the original prompt.
        return original_func(*args, **kwargs)
    return wrapper

def _patch_grind_spawner():
    try:
        grind_spawner = importlib.import_module('grind_spawner')
    except ImportError:
        _logger.debug("grind_spawner module not found – skipping skill injection.")
        return

    # Heuristic: look for a function that builds the prompt. Common names:
    candidate_names = ['build_prompt', 'create_prompt', 'generate_prompt']
    for name in candidate_names:
        original = getattr(grind_spawner, name, None)
        if callable(original):
            setattr(grind_spawner, name, _inject_skill_into_prompt(original))
            _logger.debug(f"Patched grind_spawner.{name} to inject skills.")
            break
    else:
        _logger.debug("No recognizable prompt‑building function found in grind_spawner.")

# Apply the patch at import time.
_patch_grind_spawner()
import collections
import json
import re
import os
# Load skill library and ensure each entry has an embedding vector
_SKILL_LIBRARY_PATH = os.path.join(os.path.dirname(__file__), "skill_library.json")
with open(_SKILL_LIBRARY_PATH, "r", encoding="utf-8") as _f:
    _skill_library = json.load(_f)

# Compute missing embeddings and persist them
_ensure_embeddings(_skill_library, _SKILL_LIBRARY_PATH)

def compute_embedding(text: str) -> dict:
    """
    Compute a normalized word‑frequency vector for the given text.
    Simple TF (term frequency) with L2 normalization.
    """
    # Tokenize: lower‑case alphanumerics
    words = [w.lower() for w in re.findall(r"\b\w+\b", text)]
    if not words:
        return {}
    freq = collections.Counter(words)
    # Convert to float frequencies
    total = sum(freq.values())
    vec = {word: count / total for word, count in freq.items()}
    # L2‑normalize
    norm = math.sqrt(sum(v * v for v in vec.values()))
    if norm == 0:
        return vec
    return {word: v / norm for word, v in vec.items()}

def cosine_similarity(vec1: dict, vec2: dict) -> float:
    """Cosine similarity between two sparse vectors represented as dicts."""
    # Dot product
    dot = sum(vec1.get(k, 0.0) * v for k, v in vec2.items())
    # Norms (vectors are already L2‑normalized, but compute for safety)
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def semantic_search(query: str, skills: list, top_k: int = 3) -> list:
    """
    Return the top_k skills whose embeddings are most similar to the query.
    Each skill dict is expected to contain an 'embedding' key.
    """
    query_emb = compute_embedding(query)
    scored = []
    for skill in skills:
        emb = skill.get("embedding")
        if not emb:
            continue
        sim = cosine_similarity(query_emb, emb)
        scored.append((sim, skill))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [skill for sim, skill in scored[:top_k] if sim > 0.3]

def _ensure_embeddings(skills: list, json_path: str):
    """
    Compute and store embeddings for all skills if missing,
    then persist back to the JSON file.
    """
    updated = False
    for skill in skills:
        if "embedding" not in skill:
            # Build a text source from name, description, and keywords (if any)
            parts = [skill.get("name", ""), skill.get("description", "")]
            parts.extend(skill.get("keywords", []))
            skill["embedding"] = compute_embedding(" ".join(parts))
            updated = True
    if updated:
        # Write back the enriched library
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)

def _log_lesson(message: str):
    """
    Append a simple lesson entry to learned_lessons.json.
    """
    lessons_path = os.path.join(os.path.dirname(__file__), "learned_lessons.json")
    entry = {"timestamp": __import__("datetime").datetime.utcnow().isoformat(),
             "lesson": message}
    try:
        if os.path.exists(lessons_path):
            with open(lessons_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except Exception:
        data = []
    data.append(entry)
    with open(lessons_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
from collections import Counter

def compute_embedding(text: str) -> dict:
    """
    Compute a simple normalized word‑frequency embedding for the given text.
    """
    # Basic tokenisation – lower‑case, keep alphabetic words
    tokens = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = sum(counts.values())
    # Normalised frequencies
    return {word: cnt / total for word, cnt in counts.items()}

def cosine_similarity(vec1: dict, vec2: dict) -> float:
    """
    Cosine similarity for two sparse frequency vectors represented as dicts.
    """
    # Dot product
    dot = sum(vec1.get(k, 0.0) * vec2.get(k, 0.0) for k in set(vec1) | set(vec2))
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
# --------------------------------------------------------------
# Embedding utilities – simple normalized word frequency vectors
# --------------------------------------------------------------
import math
from collections import Counter

def compute_embedding(text: str) -> dict:
    """
    Compute a normalized word‑frequency embedding for the given text.
    Returns a dict mapping token -> frequency (sum of frequencies = 1.0).
    """
    tokens = [t.lower() for t in text.split() if t]
    if not tokens:
        return {}
    counts = Counter(tokens)
# Ensure each skill has an embedding; compute and store if absent
updated = False
for skill in skill_library:
    if "embedding" not in skill:
        # Combine name and description for a richer representation
        text = f"{skill.get('name', '')} {skill.get('description', '')}"
        skill["embedding"] = compute_embedding(text)
        updated = True

# Write back the enriched library so embeddings are persisted
if updated:
    with open("skill_library.json", "w") as f:
        json.dump(skill_library, f, indent=2)
    total = sum(counts.values())
    return {word: cnt / total for word, cnt in counts.items()}

def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """
    Cosine similarity between two sparse vectors represented as dicts.
    """
    # dot product
    dot = sum(vec_a.get(k, 0.0) * vec_b.get(k, 0.0) for k in set(vec_a) | set(vec_b))
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def semantic_search(query: str, skills: list, top_k: int = 3) -> list:
    """
    Return the top_k skills whose embeddings are most similar to the query.
    """
    query_emb = compute_embedding(query)
    scored = [
        (skill, cosine_similarity(query_emb, skill.get("embedding", {})))
        for skill in skills
    ]
    # sort descending by similarity
    scored.sort(key=lambda x: x[1], reverse=True)
    return [skill for skill, _ in scored[:top_k]]
    return dot / (norm1 * norm2)

def semantic_search(query: str, skills: list, top_k: int = 3) -> list:
    """
    Return the top‑k skills whose embeddings are most similar to the query.
    Each skill dict is expected to have an ``embedding`` key.
    """
    query_emb = compute_embedding(query)
    # Compute similarity for each skill
    scored = [
        (skill, cosine_similarity(query_emb, skill.get("embedding", {})))
        for skill in skills
    ]
    # Sort by similarity descending and take top_k
    scored.sort(key=lambda x: x[1], reverse=True)
    return [skill for skill, _ in scored[:top_k] if _ > 0]
    """
    tokens = [t.lower() for t in text.split()]
    total = len(tokens) or 1
    freq = Counter(tokens)
    # Normalize frequencies
    return {word: count / total for word, count in freq.items()}


def _cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """
    Compute cosine similarity between two sparse vectors represented as dicts.
    """
    # Dot product
    dot = sum(vec_a.get(k, 0.0) * vec_b.get(k, 0.0) for k in set(vec_a) | set(vec_b))
    # Norms
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def compute_embedding_for_skill(skill: dict) -> None:
    """
    Compute and store an embedding for a skill dict if it does not already exist.
    The embedding is based on the skill's description (or name if description missing).
    """
def _tokenize(text: str) -> list:
    """Simple whitespace and punctuation tokenizer."""
    return re.findall(r"\b\w+\b", text.lower())

def compute_embedding(text: str) -> dict:
    """
    Compute a normalized word‑frequency (TF) vector for the given text.
    Returns a dict mapping token -> normalized frequency.
    """
    tokens = _tokenize(text)
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = sum(counts.values())
    # Normalized frequencies (L2 norm)
    norm = math.sqrt(sum((c / total) ** 2 for c in counts.values()))
    return {tok: (cnt / total) / norm for tok, cnt in counts.items()}

def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """Cosine similarity between two sparse vectors represented as dicts."""
    # dot product
    dot = sum(vec_a.get(k, 0.0) * v for k, v in vec_b.items())
    # magnitudes (vectors are already L2‑normalized, but compute safely)
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def semantic_search(query: str, skills: list, top_k: int = 3) -> list:
    """
    Return the top_k skills whose embeddings are most similar to the query.
    Each returned item is the original skill dict.
    """
    query_emb = compute_embedding(query)
    scored = []
    for skill in skills:
        emb = skill.get("embedding", {})
        score = cosine_similarity(query_emb, emb)
        scored.append((score, skill))
    # sort descending by similarity
    scored.sort(key=lambda x: x[0], reverse=True)
    return [skill for _, skill in scored[:top_k] if _ > 0]
    if "embedding" not in skill:
        source_text = skill.get("description", skill.get("name", ""))
        skill["embedding"] = _text_to_embedding(source_text)


def semantic_search(query: str, skills: list, top_k: int = 3) -> list:
    """
    Return the top‑k skills whose embeddings are most similar to the query embedding.
    """
    query_emb = _text_to_embedding(query)
    # Ensure every skill has an embedding
    for skill in skills:
        compute_embedding_for_skill(skill)

    # Compute similarities
    scored = [
        (skill, _cosine_similarity(query_emb, skill.get("embedding", {})))
        for skill in skills
    ]
    # Sort by similarity descending
    scored.sort(key=lambda x: x[1], reverse=True)
    # Return only the skill dicts (filter out zero‑similarity results if desired)
    return [skill for skill, _ in scored[:top_k] if _ > 0]
import json
import os
import math
from collections import Counter

def compute_embedding(text):
    """
    Compute a simple normalized word‑frequency embedding for the given text.
    Returns a dict mapping word -> normalized frequency (L2 norm = 1).
    """
    words = [w.lower() for w in text.split()]
    if not words:
        return {}
    freq = Counter(words)
    # convert counts to floats
    vec = {word: float(count) for word, count in freq.items()}
    # L2‑normalize
    norm = math.sqrt(sum(v * v for v in vec.values()))
    if norm == 0:
        return {}
    for word in vec:
        vec[word] /= norm
    return vec

def _cosine_similarity(vec1, vec2):
    """Cosine similarity for two sparse dict vectors (both assumed L2‑normalized)."""
    # dot product over the intersection
    return sum(vec1.get(k, 0.0) * vec2.get(k, 0.0) for k in vec1)

def semantic_search(query, skills, top_k=3):
    """
    Perform a semantic similarity search.
    - query: raw query string.
    - skills: list of skill dicts (each must contain an 'embedding' field).
    - Returns the top_k most similar skill dicts sorted by similarity descending.
    """
    query_emb = compute_embedding(query)
    # compute similarity for each skill
    scored = []
    for skill in skills:
        emb = skill.get("embedding")
        if not emb:
            continue
        sim = _cosine_similarity(query_emb, emb)
        scored.append((sim, skill))
    # sort by similarity descending and take top_k
    scored.sort(key=lambda x: x[0], reverse=True)
    return [skill for _, skill in scored[:top_k]]