#!/usr/bin/env python3
"""Quick test for failure_patterns.py functionality."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from failure_patterns import FailurePatternDetector


def test_failure_tracking():
    """Test basic failure tracking."""
    print("Testing FailurePatternDetector...")

    # Use test file to avoid polluting real data
    detector = FailurePatternDetector(failures_file="test_failure_patterns.json")

    # Track a failure
    failure = detector.track_failure(
        task_description="Implement vector embeddings with sentence-transformers",
        error_type="ImportError",
        error_message="No module named 'sentence_transformers'",
        task_characteristics={
            "domain": "embeddings",
            "complexity": "medium",
            "requires_external_lib": True
        },
        attempted_approaches=[
            "Direct import",
            "pip install sentence-transformers"
        ],
        context={"model": "sonnet", "duration": 120}
    )

    print(f"[OK] Tracked failure: {failure['id']}")

    # Track another similar failure
    failure2 = detector.track_failure(
        task_description="Add semantic embeddings to skill retrieval",
        error_type="ImportError",
        error_message="Module sentence_transformers not found",
        task_characteristics={
            "domain": "embeddings",
            "complexity": "medium",
            "requires_external_lib": True
        },
        attempted_approaches=[
            "Import transformers library",
            "Use huggingface models"
        ]
    )

    print(f"[OK] Tracked failure: {failure2['id']}")

    # Check for patterns on a similar task
    print("\nChecking for failure patterns on similar task...")
    result = detector.check_failure_patterns(
        task_description="Create embeddings for lesson retrieval using transformers",
        task_characteristics={
            "domain": "embeddings",
            "complexity": "medium"
        }
    )

    print(f"Warning Level: {result['warning_level']}")
    print(f"Similar Failures Found: {len(result['similar_failures'])}")

    if result['similar_failures']:
        print("\nSimilar Failures:")
        for sf in result['similar_failures']:
            print(f"  - [{sf['error_type']}] {sf['task'][:60]}...")

    print("\nSuggested Strategies:")
    for strategy in result['suggested_strategies']:
        print(f"  * {strategy}")

    # Test warning prompt generation
    print("\n" + "="*60)
    print("Testing warning prompt generation:")
    print("="*60)
    warning = detector.generate_warning_prompt(
        "Upgrade skill retrieval with vector embeddings",
        {"domain": "embeddings"}
    )
    print(warning)

    # Test error stats
    print("\n" + "="*60)
    print("Error Type Statistics:")
    print("="*60)
    stats = detector.get_error_type_stats()
    for error_type, count in stats.items():
        print(f"  {error_type}: {count}")

    print("\n[OK] All tests passed!")

    # Cleanup test file
    test_file = Path("test_failure_patterns.json")
    if test_file.exists():
        test_file.unlink()
        print("[OK] Cleaned up test file")


if __name__ == "__main__":
    test_failure_tracking()
