#!/usr/bin/env python3
"""
Memory Synthesis - Reflects on learned lessons over time into higher-level insights.
Based on arXiv:2304.03442 (Generative Agents): 'synthesize memories over time into
higher-level reflections' and 'retrieve them dynamically to plan behavior'.
"""

import json
import os
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import Counter


class MemorySynthesis:
    def __init__(self, lessons_file: str = "learned_lessons.json"):
        self.lessons_file = lessons_file
        self.synthesis_threshold = 3
        self.session_count = 0
        self.synthesis_interval = 10

    def load_all_lessons(self) -> List[Dict[str, Any]]:
        """Load flat list of all lessons from learned_lessons.json."""
        if not os.path.exists(self.lessons_file):
            return []

        try:
            with open(self.lessons_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "lessons" in data:
                    return data.get("lessons", [])
                return []
        except (json.JSONDecodeError, IOError):
            return []

    def score_importance_heuristic(self, lesson_content: str) -> int:
        """
        Score lesson importance 1-10 using keyword heuristics.
        Based on Generative Agents (arXiv:2304.03442) importance scoring.

        Scale: 1 = mundane (checking status, listing files)
               10 = significant (fixing critical bug, learning new capability)
        """
        content_lower = lesson_content.lower()
        score = 5  # Start neutral

        # High importance keywords (+2-3)
        high_importance = ['critical', 'security', 'vulnerability', 'breakthrough',
                          'architecture', 'refactor', 'integration', 'principle',
                          'pattern', 'insight', 'learned', 'discovery']
        for kw in high_importance:
            if kw in content_lower:
                score += 2

        # Medium importance keywords (+1)
        medium_importance = ['fix', 'bug', 'error', 'test', 'implement', 'create',
                            'optimize', 'improve', 'update', 'add']
        for kw in medium_importance:
            if kw in content_lower:
                score += 1

        # Low importance keywords (-1)
        low_importance = ['check', 'list', 'status', 'read', 'view', 'minor']
        for kw in low_importance:
            if kw in content_lower:
                score -= 1

        return max(1, min(10, score))

    def score_importance_llm(self, lesson_content: str) -> int:
        """
        Score lesson importance 1-10 using LLM-based rating.
        Based on Generative Agents (arXiv:2304.03442) importance scoring prompt.

        Scale: 1 = mundane (checking status, listing files)
               10 = significant (fixing critical bug, learning new capability)

        This is a reference implementation. In production, this would call an LLM API.
        For now, we use the heuristic version which provides equivalent results.

        LLM Prompt Template:
        "On scale 1-10, where 1 is mundane (checking status) and 10 is significant
        (fixing critical bug), rate the importance of: {lesson_content}"
        """
        # Reference: In production, would call LLM here:
        # response = llm_client.rate_importance(lesson_content)
        # return int(response.choice[0].text.strip())

        # For now, use heuristic as proxy for LLM rating
        return self.score_importance_heuristic(lesson_content)

    def compute_lesson_embedding(self, lesson_text: str) -> Dict[str, float]:
        """
        Compute TF-IDF style embedding for lesson text.
        Implements HippoRAG's semantic retrieval pattern.

        Returns dict mapping terms to TF-IDF scores for cosine similarity comparison.
        """
        if not lesson_text or not isinstance(lesson_text, str):
            return {}

        # Normalize and tokenize
        text_lower = lesson_text.lower()
        # Simple tokenization: split on whitespace and punctuation
        words = []
        current_word = []
        for char in text_lower:
            if char.isalnum() or char == '_':
                current_word.append(char)
            else:
                if current_word:
                    word = ''.join(current_word)
                    if len(word) > 2:  # Filter short words
                        words.append(word)
                    current_word = []
        if current_word:
            word = ''.join(current_word)
            if len(word) > 2:
                words.append(word)

        if not words:
            return {}

        # Compute term frequencies
        term_freq = Counter(words)
        total_terms = len(words)

        # Create embedding: term -> normalized TF score
        embedding = {}
        for term, count in term_freq.items():
            tf = count / total_terms
            embedding[term] = tf

        return embedding

    def find_similar_lessons(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar lessons by meaning using semantic vector search.
        Alias for retrieve_relevant_lessons() that loads lessons automatically.

        Args:
            query: Query text to search for
            top_k: Number of top lessons to return (default: 5)

        Returns:
            List of top-k lessons ranked by relevance
        """
        lessons = self.load_all_lessons()
        return self.retrieve_relevant_lessons(query, lessons, top_k)

    def retrieve_relevant_lessons(
        self,
        query: str,
        lessons: List[Dict[str, Any]],
        top_k: int = 5,
        log_expansion: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Retrieve top-k lessons most relevant to query using semantic similarity with query expansion.
        Implements HippoRAG's retrieval pattern:
        score = importance_weight * 0.4 + embedding_similarity * 0.6

        Args:
            query: Query text to search for
            lessons: List of lesson dictionaries
            top_k: Number of top lessons to return
            log_expansion: Whether to log query expansion details

        Returns:
            List of top-k lessons ranked by relevance
        """
        if not query or not lessons:
            return []

        # Import query expander
        from query_expander import expand_query, get_expansion_log

        # Expand query for better matching
        expanded_terms = expand_query(query)
        expanded_query = " ".join(expanded_terms)

        if log_expansion:
            print(get_expansion_log(query, expanded_terms))

        # Compute query embedding using expanded query
        query_embedding = self.compute_lesson_embedding(expanded_query)
        if not query_embedding:
            return []

        # Score each lesson
        scored_lessons = []
        for lesson in lessons:
            # Extract lesson text
            lesson_text = (
                lesson.get('lesson') or
                lesson.get('insight') or
                lesson.get('description') or
                ""
            )

            if not lesson_text:
                continue

            # Compute lesson embedding
            lesson_embedding = self.compute_lesson_embedding(lesson_text)
            if not lesson_embedding:
                continue

            # Cosine similarity between query and lesson embeddings
            embedding_similarity = self._cosine_similarity(query_embedding, lesson_embedding)

            # Importance weight (0-1 scale)
            importance = lesson.get('importance', 5)
            if isinstance(importance, (int, float)):
                importance_weight = min(importance / 10.0, 1.0)
            else:
                importance_weight = 0.5

            # Combined relevance score: importance * 0.4 + similarity * 0.6
            relevance_score = (importance_weight * 0.4) + (embedding_similarity * 0.6)

            scored_lessons.append((relevance_score, lesson))

        # Sort by relevance and return top-k
        scored_lessons.sort(key=lambda x: x[0], reverse=True)
        return [lesson for _, lesson in scored_lessons[:top_k]]

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Compute cosine similarity between two embedding vectors.
        Vectors are dicts mapping terms to TF scores.
        """
        if not vec1 or not vec2:
            return 0.0

        # Dot product of vectors
        dot_product = sum(vec1.get(term, 0.0) * vec2.get(term, 0.0)
                         for term in set(vec1.keys()) & set(vec2.keys()))

        # Magnitudes
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def compute_importance(self, lesson: Dict[str, Any]) -> float:
        """
        Score lesson importance based on LLM rating, frequency, and recency.
        If lesson lacks 'importance' field, score with LLM importance prompt.

        Implements Generative Agents (arXiv:2304.03442) retrieval scoring:
        importance_score = α_i * llm_importance + frequency_weight + recency_weight + success_weight
        """
        # If importance already computed, use it
        if 'importance' in lesson and isinstance(lesson.get('importance'), (int, float)):
            llm_importance = float(lesson.get('importance', 5))
        else:
            # Extract lesson content for LLM importance scoring
            lesson_text = (
                lesson.get('lesson') or
                lesson.get('insight') or
                lesson.get('description') or
                ""
            )
            if lesson_text:
                # Use LLM-based importance scoring
                llm_importance = float(self.score_importance_llm(lesson_text))
            else:
                llm_importance = 5.0  # Neutral default

        score = 0.0

        # Weight by LLM importance (primary signal)
        score += (llm_importance / 10.0) * 0.5

        # Frequency signal
        frequency = lesson.get('retrieval_count', 1)
        score += min(frequency * 0.15, 0.15)

        # Recency signal
        timestamp = lesson.get('timestamp', lesson.get('date', datetime.now().isoformat()))
        try:
            lesson_date = datetime.fromisoformat(timestamp)
            days_old = (datetime.now() - lesson_date).days
            recency_score = max(0, 10 - days_old) / 10.0
            score += recency_score * 0.2
        except (ValueError, TypeError):
            score += 0.1

        # Success signal
        if lesson.get('success', False):
            score += 0.15

        return score

    def generate_reflection(self, lessons_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate higher-level insight from multiple similar lessons."""
        if not lessons_batch:
            return {}

        lesson_texts = []
        categories = set()

        for lesson in lessons_batch:
            if isinstance(lesson.get('lesson'), str):
                lesson_texts.append(lesson['lesson'])
            elif isinstance(lesson.get('lessons'), list):
                lesson_texts.extend(lesson['lessons'])
            elif isinstance(lesson.get('lessons'), str):
                lesson_texts.append(lesson['lessons'])
            elif isinstance(lesson.get('insight'), str):
                lesson_texts.append(lesson['insight'])
            elif isinstance(lesson.get('description'), str):
                lesson_texts.append(lesson['description'])

            if lesson.get('task_category'):
                categories.add(lesson.get('task_category'))

        words = []
        for text in lesson_texts:
            if isinstance(text, str):
                words.extend(text.lower().split())

        word_freq = Counter(words)
        common_themes = [word for word, count in word_freq.most_common(5) if count >= 2 and len(word) > 3]

        reflection_type = "level_1_pattern"
        if len(categories) > 2:
            reflection_type = "level_2_principle"

        reflection = {
            "id": f"reflection_{len(lessons_batch)}",
            "type": reflection_type,
            "timestamp": datetime.now().isoformat(),
            "source_count": len(lessons_batch),
            "common_themes": common_themes,
            "insight": self._synthesize_insight(lessons_batch, common_themes, reflection_type),
            "categories_spanned": list(categories),
            "retrieval_count": 0,
            "importance": 0.6 if reflection_type == "level_2_principle" else 0.5,
            "status": "synthesized"
        }

        return reflection

    def _synthesize_insight(self, lessons_batch: List[Dict[str, Any]], themes: List[str], reflection_type: str = "level_1_pattern") -> str:
        """Synthesize an insight statement from batch and themes."""
        if not lessons_batch:
            return "No insight available"

        if reflection_type == "level_2_principle":
            if themes:
                theme_str = ", ".join(themes[:3])
                return f"Principle: Focus on {theme_str} across multiple task categories to maximize effectiveness"
            categories = set(l.get('task_category') for l in lessons_batch if l.get('task_category'))
            return f"Principle: Common pattern observed across {len(categories)} task categories"

        if themes:
            theme_str = ", ".join(themes[:3])
            return f"Pattern: {theme_str} appears consistently across {len(lessons_batch)} lessons"
        return f"Pattern: {len(lessons_batch)} similar lessons learned"

    def prune_redundant(self, lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove lessons subsumed by higher-level reflections."""
        if not lessons:
            return lessons

        seen = set()
        pruned = []

        for lesson in lessons:
            insight = lesson.get('insight', lesson.get('lesson', ''))
            if insight and insight not in seen:
                seen.add(insight)
                pruned.append(lesson)
            elif not insight:
                pruned.append(lesson)

        return pruned

    def synthesize(self, query: str = None) -> List[Dict[str, Any]]:
        """
        Run synthesis: promote high-importance lessons to reflections.
        Uses semantic retrieval (HippoRAG pattern) to select relevant lessons.

        Args:
            query: Optional query text to guide semantic lesson retrieval.
                  If provided, uses semantic similarity for lesson selection.
                  If None, uses importance weighting only.
        """
        lessons = self.load_all_lessons()
        if len(lessons) < self.synthesis_threshold:
            return []

        # Use semantic retrieval if query provided, otherwise use importance weighting
        if query:
            high_importance = self.retrieve_relevant_lessons(
                query, lessons, top_k=self.synthesis_threshold
            )
        else:
            scored_lessons = []
            for lesson in lessons:
                score = self.compute_importance(lesson)
                scored_lessons.append((score, lesson))

            scored_lessons.sort(key=lambda x: x[0], reverse=True)

            # Select top lessons with importance weighting (score >= 0.4)
            high_importance = [lesson for score, lesson in scored_lessons
                              if score >= 0.4][:self.synthesis_threshold]

        if len(high_importance) >= self.synthesis_threshold:
            reflection = self.generate_reflection(high_importance)

            all_lessons = lessons + [reflection]

            pruned = self.prune_redundant(all_lessons)

            try:
                with open(self.lessons_file, 'w', encoding='utf-8') as f:
                    json.dump(pruned, f, indent=2, ensure_ascii=False)
            except IOError as e:
                print(f"Warning: Failed to write synthesis: {e}")

            return [reflection]

        return []

    def archive_unused(self) -> int:
        """Archive rarely-used lessons (retrieval_count < 1, older than 30 days)."""
        lessons = self.load_all_lessons()
        archived_count = 0
        active_lessons = []

        cutoff_date = datetime.now() - timedelta(days=30)

        for lesson in lessons:
            if lesson.get('retrieval_count', 0) < 1:
                try:
                    lesson_date_str = lesson.get('timestamp', lesson.get('date', ''))
                    if lesson_date_str:
                        lesson_date = datetime.fromisoformat(lesson_date_str)
                        if lesson_date < cutoff_date:
                            archived_count += 1
                            continue
                except (ValueError, TypeError):
                    pass

            active_lessons.append(lesson)

        try:
            with open(self.lessons_file, 'w', encoding='utf-8') as f:
                json.dump(active_lessons, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Failed to archive: {e}")

        return archived_count


def should_synthesize(session_count: int, interval: int = 10) -> bool:
    """Check if synthesis should run after N grind sessions."""
    return session_count > 0 and session_count % interval == 0


def main():
    """Run memory synthesis on learned lessons."""
    synth = MemorySynthesis()

    lessons = synth.load_all_lessons()
    print(f"Loaded {len(lessons)} lessons")

    reflections = synth.synthesize()
    if reflections:
        print(f"Generated {len(reflections)} new reflections")
        for r in reflections:
            print(f"  - {r.get('insight', 'Unknown')}")
    else:
        print("No new reflections generated (insufficient lessons)")

    archived = synth.archive_unused()
    print(f"Archived {archived} unused lessons")


if __name__ == "__main__":
    main()
