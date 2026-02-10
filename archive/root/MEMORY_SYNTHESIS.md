# Memory Synthesis Implementation

Implements reflection synthesis for learned lessons based on arXiv:2304.03442 (Generative Agents).

## Features

### 1. Three-Level Reflection Hierarchy
- **Level 0**: Raw observations (individual lessons from `learned_lessons.json`)
- **Level 1**: Patterns (lessons appearing 3+ times synthesized into insights)
- **Level 2**: Principles (patterns spanning multiple categories - extensible)

### 2. Importance Scoring
Lessons scored on three dimensions:
- **Frequency** (30%): How often retrieved (`retrieval_count`)
- **Recency** (40%): Newer lessons weighted higher (decay over 10 days)
- **Impact** (30%): Success flag + explicit importance field

### 3. Automatic Synthesis
- Runs after every 10 grind sessions (configurable via `should_synthesize()`)
- Groups high-importance lessons (score >= 0.5)
- Generates higher-level insights from patterns
- Prunes redundant lessons

### 4. Memory Archiving
- Archives rarely-used lessons (retrieval_count < 1, older than 30 days)
- Preserves active lessons for dynamic retrieval

## Usage

```bash
# Run synthesis manually
python memory_synthesis.py

# Integrate with SOP executor (auto-trigger every 10 sessions)
python sop_executor.py my_sop.json learned_lessons.json --session-count 10
```

## API

```python
from memory_synthesis import MemorySynthesis, should_synthesize

# Initialize
synth = MemorySynthesis("learned_lessons.json")

# Core methods
lessons = synth.load_all_lessons()
score = synth.compute_importance(lesson)
reflection = synth.generate_reflection(lessons_batch)
synth.synthesize()
synth.archive_unused()

# Check if synthesis should run
if should_synthesize(session_count=10, interval=10):
    synth.synthesize()
```

## Lesson Schema

**Raw Lesson (Level 0)**
```json
{
  "id": "lesson_001",
  "lesson": "Always read files before proposing changes",
  "retrieval_count": 2,
  "timestamp": "2026-02-03"
}
```

**Synthesized Reflection (Level 1)**
```json
{
  "type": "level_1_pattern",
  "timestamp": "2026-02-03",
  "source_count": 3,
  "common_themes": ["lessons", "task"],
  "insight": "Pattern: lessons, task appears consistently",
  "level": 1,
  "category": "synthesis",
  "retrieval_count": 0,
  "importance": 0.5
}
```

## Key Insight

Per Generative Agents paper: "retrieve them dynamically to plan behavior"

The synthesis system enables agents to:
1. Accumulate raw observations over time
2. Synthesize patterns when sufficient evidence exists
3. Retrieve synthesized insights dynamically for future planning
4. Archive outdated lessons to maintain focus
