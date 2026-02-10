import json
import os
from datetime import datetime, timedelta

from memory_synthesis import MemorySynthesis

LESSONS_PATH = os.path.join(os.path.dirname(__file__), "learned_lessons.json")

def load_lessons():
    if not os.path.exists(LESSONS_PATH):
        return []
    with open(LESSONS_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def recent_than_4_hours(lesson):
    ts = lesson.get("timestamp")
    if not ts:
        return False
    try:
        lesson_time = datetime.fromisoformat(ts)
    except ValueError:
        return False
    return datetime.utcnow() - lesson_time < timedelta(hours=4)

def maybe_reflect(session_count: int):
    lessons = load_lessons()
    recent = [l for l in lessons if recent_than_4_hours(l)]
    importance_sum = sum(l.get("importance", 5) for l in recent)

    # Generative‑Agents threshold
    if importance_sum > 150:
        synth = MemorySynthesis()
        new_reflections = synth.synthesize()
        if new_reflections:
            # Append generated reflections to the lessons file
            lessons.extend(new_reflections)
            with open(LESSONS_PATH, "w", encoding="utf-8") as f:
                json.dump(lessons, f, ensure_ascii=False, indent=2)

            print(f"[ReflectionTrigger] Generated {len(new_reflections)} reflections "
                  f"after {session_count} grind sessions.")
        else:
            print("[ReflectionTrigger] No new reflections were generated.")
```