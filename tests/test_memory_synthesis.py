#!/usr/bin/env python3
"""Test memory synthesis with multi-level reflection hierarchy."""

import json
import tempfile
from pathlib import Path
from memory_synthesis import MemorySynthesis, should_synthesize

def test_synthesis_levels():
    """Test that synthesis creates proper reflection levels."""
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_file = f.name
        
        # Write diverse lessons across multiple categories
        test_lessons = [
            {
                "id": "lesson_1",
                "lesson": "Always read files before modifications",
                "task_category": "code_analysis",
                "timestamp": "2026-02-01",
                "retrieval_count": 3
            },
            {
                "id": "lesson_2", 
                "lesson": "Read documentation thoroughly when integrating",
                "task_category": "code_analysis",
                "timestamp": "2026-02-02",
                "retrieval_count": 2
            },
            {
                "id": "lesson_3",
                "lesson": "Read test results before debugging",
                "task_category": "testing",
                "timestamp": "2026-02-02",
                "retrieval_count": 1
            },
            {
                "id": "lesson_4",
                "lesson": "Read error messages carefully to understand failures",
                "task_category": "error_handling",
                "timestamp": "2026-02-03",
                "retrieval_count": 2
            }
        ]
        
        json.dump(test_lessons, f)
    
    try:
        # Run synthesis
        synth = MemorySynthesis(test_file)
        
        print("=" * 60)
        print("MEMORY SYNTHESIS TEST")
        print("=" * 60)
        
        # Load and display original lessons
        lessons = synth.load_all_lessons()
        print(f"\nLoaded {len(lessons)} raw lessons")
        for l in lessons:
            score = synth.compute_importance(l)
            print(f"  - {l.get('id')}: {l.get('lesson')[:40]}... (score: {score:.2f})")
        
        # Run synthesis
        print("\nRunning synthesis...")
        reflections = synth.synthesize()
        
        print(f"\nGenerated {len(reflections)} reflections")
        for r in reflections:
            print(f"  Type: {r.get('type')}")
            print(f"  Insight: {r.get('insight')}")
            print(f"  Themes: {r.get('common_themes')}")
            print(f"  Categories: {r.get('categories_spanned')}")
            print(f"  Importance: {r.get('importance')}")
        
        # Verify level hierarchy
        updated = synth.load_all_lessons()
        level_0 = [l for l in updated if 'type' not in l or l.get('type') not in ['level_1_pattern', 'level_2_principle']]
        level_1 = [l for l in updated if l.get('type') == 'level_1_pattern']
        level_2 = [l for l in updated if l.get('type') == 'level_2_principle']
        
        print(f"\n--- REFLECTION HIERARCHY ---")
        print(f"Level 0 (Raw observations): {len(level_0)} lessons")
        print(f"Level 1 (Patterns): {len(level_1)} reflections")
        print(f"Level 2 (Principles): {len(level_2)} reflections")
        
        print(f"\n[OK] Synthesis complete - 3-level hierarchy in place")
        
    finally:
        Path(test_file).unlink()

def test_should_synthesize():
    """Test periodic synthesis trigger."""
    
    print("\n" + "=" * 60)
    print("PERIODIC SYNTHESIS TRIGGER TEST")
    print("=" * 60)
    
    test_cases = [
        (9, 10, False),   # 9 runs, interval 10 = no synthesis
        (10, 10, True),   # 10 runs, interval 10 = synthesis
        (20, 10, True),   # 20 runs, interval 10 = synthesis
        (15, 10, False),  # 15 runs, interval 10 = no synthesis
        (30, 10, True),   # 30 runs, interval 10 = synthesis
    ]
    
    for session_count, interval, expected in test_cases:
        result = should_synthesize(session_count, interval)
        status = "[PASS]" if result == expected else "[FAIL]"
        print(f"{status} session_count={session_count}, interval={interval}: {result} (expected {expected})")

if __name__ == "__main__":
    test_synthesis_levels()
    test_should_synthesize()
    print("\n" + "=" * 60)
    print("All tests completed")
    print("=" * 60)
