"""Reflexion episodic memory utilities (arXiv:2303.11366)

Transforms verbal reflection into retrievable episodic memory with:
- Trial number tracking
- Task feedback capture (error/output signal)
- Self-verification (did lesson work?)
- Retrieval cues for context matching
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


LEARNED_LESSONS_PATH = Path(__file__).parent.parent / "learned_lessons.json"


def add_reflection(
    task_id: str,
    feedback_signal: str,
    verbal_reflection: str,
    verification_result: bool,
    retrieval_cues: Optional[List[str]] = None,
    trial_number: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Add a reflection to episodic memory.

    Args:
        task_id: Identifier for the task/problem being learned
        feedback_signal: The actual error message or output that triggered reflection
        verbal_reflection: Natural language summary of the lesson learned
        verification_result: Did applying this lesson work in subsequent trials?
        retrieval_cues: Keywords for context-based retrieval
        trial_number: Which attempt this insight came from (auto-incremented if None)

    Returns:
        The added reflection entry
    """
    if retrieval_cues is None:
        retrieval_cues = []

    lessons = _load_lessons()

    if trial_number is None:
        trial_number = len(lessons) + 1

    reflection = {
        "id": task_id,
        "trial_number": trial_number,
        "timestamp": datetime.utcnow().isoformat(),
        "task_feedback": feedback_signal,
        "lesson": verbal_reflection,
        "self_verification": verification_result,
        "retrieval_cues": retrieval_cues,
    }

    lessons.append(reflection)
    _save_lessons(lessons)

    return reflection


def retrieve_relevant_lessons(task_description: str, log_expansion: bool = False) -> List[Dict[str, Any]]:
    """
    Retrieve lessons matching task description via retrieval cues with query expansion.

    Args:
        task_description: Description of current task/problem
        log_expansion: Whether to log query expansion details

    Returns:
        List of lessons with matching retrieval_cues, sorted by verification score
    """
    # Import query expander
    from query_expander import expand_query, get_expansion_log

    lessons = _load_lessons()

    # Expand query for better matching
    expanded_terms = expand_query(task_description)
    task_words = set(expanded_terms)

    if log_expansion:
        print(get_expansion_log(task_description, expanded_terms))

    relevant = []
    for lesson in lessons:
        # Skip pattern entries and other non-lesson items
        if "retrieval_cues" not in lesson or "lesson" not in lesson:
            continue

        cues = set(cue.lower() for cue in lesson.get("retrieval_cues", []))
        match_score = len(task_words & cues)

        if match_score > 0:
            relevant.append({
                **lesson,
                "_match_score": match_score,
            })

    # Sort by: verification (True first), then match score (highest first), then trial number
    relevant.sort(
        key=lambda x: (
            not x.get("self_verification", False),
            -x.get("_match_score", 0),
            -x.get("trial_number", 0),
        )
    )

    return relevant


def synthesize_lessons(lessons: List[Dict[str, Any]]) -> str:
    """
    Synthesize retrieved lessons into prompt injection.

    Condenses multiple lessons into natural language experience summary
    for injecting into prompts (Reflexion key insight).

    Args:
        lessons: Retrieved lessons from retrieve_relevant_lessons()

    Returns:
        Synthesized prompt text for inclusion in next attempt
    """
    if not lessons:
        return ""

    synthesis = "=== LEARNED LESSONS FROM PREVIOUS ATTEMPTS ===\n\n"

    for i, lesson in enumerate(lessons, 1):
        synthesis += f"Lesson {i} (Trial {lesson.get('trial_number')}):\n"
        synthesis += f"  Problem: {lesson.get('task_feedback', 'N/A')}\n"
        synthesis += f"  Learning: {lesson.get('lesson', 'N/A')}\n"
        synthesis += f"  Verified: {'YES' if lesson.get('self_verification') else 'NO'}\n"
        synthesis += f"  Keywords: {', '.join(lesson.get('retrieval_cues', []))}\n\n"

    synthesis += "Apply these lessons to improve your solution.\n"
    return synthesis


def _load_lessons() -> List[Dict[str, Any]]:
    """Load learned_lessons.json, return empty list if missing."""
    if not LEARNED_LESSONS_PATH.exists():
        return []

    try:
        with open(LEARNED_LESSONS_PATH, "r") as f:
            data = json.load(f)
            # Handle both list and dict formats
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get("reflexion_episodic_memory", [])
            return []
    except (json.JSONDecodeError, IOError):
        return []


def _save_lessons(lessons: List[Dict[str, Any]]) -> None:
    """Save lessons to learned_lessons.json."""
    LEARNED_LESSONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEARNED_LESSONS_PATH, "w") as f:
        json.dump(lessons, f, indent=2)
