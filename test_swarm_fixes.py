#!/usr/bin/env python3
"""
Test script for swarm communication fixes.
Tests the four implemented fixes:
1. Task phrasing normalization (interrogative -> declarative)
2. Verification system (detects when files aren't actually changed)
3. Indentation preservation in code extraction
4. Grounding instructions (prevent hallucination)
"""

import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent))

from grind_spawner_unified import UnifiedGrindSession, EngineType
from groq_code_extractor import GroqArtifactExtractor
from verification_fix import verify_file_changed, APPLIED, FAILED


def test_task_normalization():
    """Test Fix #1: Task phrasing normalization."""
    print("=" * 60)
    print("TEST 1: Task Phrasing Normalization")
    print("=" * 60)

    # Create a session with an interrogative task
    session = UnifiedGrindSession(
        session_id=999,
        task="Write to test_output.txt: Why does the swarm hallucinate?",
        budget=0.01,
        workspace=Path(__file__).parent,
        force_engine=EngineType.GROQ
    )

    # Check that task was normalized
    normalized = session._normalize_analysis_task(session.task)
    print(f"Original task: {session.task}")
    print(f"Normalized task: {normalized}")

    expected = "Create analysis file at test_output.txt that answers: Why does the swarm hallucinate?"
    if expected in normalized:
        print("✓ Task normalization working correctly")
        return True
    else:
        print("✗ Task normalization failed")
        return False


def test_indentation_preservation():
    """Test Fix #3: Indentation preservation in code extraction."""
    print("\n" + "=" * 60)
    print("TEST 2: Indentation Preservation")
    print("=" * 60)

    extractor = GroqArtifactExtractor(workspace_root=str(Path(__file__).parent))

    # Test code with indentation
    test_code = """
    <artifact type="file" path="test_indent.py">
def hello():
    if True:
        print("indented")
        if True:
            print("double indented")
    </artifact>
    """

    artifacts = extractor.extract_artifacts(test_code)
    if artifacts:
        content = artifacts[0].content
        print(f"Extracted content:\n{content}")

        # Check that indentation is preserved
        if "    print(\"indented\")" in content and "        print(\"double indented\")" in content:
            print("✓ Indentation preserved correctly")
            return True
        else:
            print("✗ Indentation not preserved")
            return False
    else:
        print("✗ Failed to extract artifact")
        return False


def test_verification_system():
    """Test Fix #2: Verification system."""
    print("\n" + "=" * 60)
    print("TEST 3: Verification System")
    print("=" * 60)

    # Create a test file
    test_file = Path(__file__).parent / "test_verify.txt"
    test_file.write_text("This is a test file with unique content ABC123")

    # Test successful verification
    result1 = verify_file_changed(str(test_file), "unique content ABC123")
    print(f"Verify with correct snippet: {result1}")

    # Test failed verification
    result2 = verify_file_changed(str(test_file), "THIS TEXT DOES NOT EXIST")
    print(f"Verify with wrong snippet: {result2}")

    # Test nonexistent file
    result3 = verify_file_changed("nonexistent_file.txt", "anything")
    print(f"Verify nonexistent file: {result3}")

    # Cleanup
    test_file.unlink()

    if result1 == APPLIED and result2 == FAILED and result3 == FAILED:
        print("✓ Verification system working correctly")
        return True
    else:
        print("✗ Verification system failed")
        return False


def test_grounding_instructions():
    """Test Fix #4: Grounding instructions presence."""
    print("\n" + "=" * 60)
    print("TEST 4: Grounding Instructions")
    print("=" * 60)

    session = UnifiedGrindSession(
        session_id=999,
        task="Fix the bug in example.py",
        budget=0.01,
        workspace=Path(__file__).parent,
        force_engine=EngineType.GROQ
    )

    prompt = session.get_prompt()

    # Check that grounding rules are in the prompt
    grounding_checks = [
        "CRITICAL GROUNDING RULES",
        "READ THE FILE FIRST",
        "NEVER make up function names",
        "NEVER guess data structures"
    ]

    found_all = all(check in prompt for check in grounding_checks)

    if found_all:
        print("✓ Grounding instructions present in prompt")
        print(f"Prompt length: {len(prompt)} chars")
        return True
    else:
        print("✗ Grounding instructions missing")
        for check in grounding_checks:
            if check not in prompt:
                print(f"  Missing: {check}")
        return False


def main():
    """Run all tests."""
    print("\nSWARM COMMUNICATION FIX TESTS")
    print("=" * 60)

    results = []

    try:
        results.append(("Task Normalization", test_task_normalization()))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Task Normalization", False))

    try:
        results.append(("Indentation Preservation", test_indentation_preservation()))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Indentation Preservation", False))

    try:
        results.append(("Verification System", test_verification_system()))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Verification System", False))

    try:
        results.append(("Grounding Instructions", test_grounding_instructions()))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Grounding Instructions", False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
