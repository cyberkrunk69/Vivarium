#!/usr/bin/env python3
"""
Test script to verify the hallucination bug fixes are working correctly.
"""

import json
import tempfile
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from grind_spawner import verify_grind_completion
from critic import CriticAgent
from logger import json_log


def test_hallucination_detection():
    """Test that the verification system correctly detects hallucination."""

    print("=== Testing Hallucination Detection ===")

    # Test Case 1: Worker claims to modify files but doesn't actually do it
    output_with_claims = json.dumps({
        "files_modified": ["test_file.py", "another_file.js"],
        "result": "Successfully modified 2 files as requested"
    })

    # Create a temporary directory to simulate workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        prev_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Don't actually create the files - simulate hallucination
            verification = verify_grind_completion(
                session_id=999,
                run_num=1,
                output=output_with_claims,
                returncode=0
            )
        finally:
            os.chdir(prev_cwd)

        print(f"Verification result: {verification['verification_status']}")
        print(f"Hallucination detected: {verification.get('hallucination_detected', False)}")
        print(f"Details: {verification['details']}")

        # Should detect hallucination
        assert verification.get('hallucination_detected') == True
        assert verification['verification_status'] == 'HALLUCINATION'
        assert not verification['verified']

        print("[OK] Hallucination detection works correctly")


def test_critic_enhanced_detection():
    """Test that the critic correctly penalizes hallucination."""

    print("\n=== Testing Enhanced Critic Detection ===")

    critic = CriticAgent()

    # Mock session data with hallucination
    context = {
        "session_id": 999,
        "run": 1,
        "files_claimed": ["file1.py", "file2.js"],
        "files_actually_modified": [],  # No files actually modified
        "file_verification_passed": False
    }

    # Code that claims to modify files
    code = """
    # Modified file1.py with new function
    # Updated file2.js with bug fixes
    print("Files modified successfully!")
    """

    review = critic.review(code, context)

    print(f"Quality score: {review['score']}")
    print(f"Issues found: {len(review['issues'])}")
    print(f"Passed: {review['passed']}")

    # Should find hallucination issues
    hallucination_issues = [i for i in review['issues'] if 'hallucination' in i.get('type', '').lower()]
    print(f"Hallucination issues: {len(hallucination_issues)}")

    for issue in hallucination_issues:
        print(f"  - {issue['type']}: {issue['message']}")

    assert len(hallucination_issues) > 0
    assert review['score'] < 0.5  # Should have very low score
    assert not review['passed']

    print("[OK] Enhanced critic detection works correctly")


def test_legitimate_file_creation():
    """Test that legitimate file creation is not flagged as hallucination."""

    print("\n=== Testing Legitimate File Creation ===")

    output_with_creation = json.dumps({
        "files_modified": ["new_file.py"],
        "result": "Successfully created new_file.py"
    })

    with tempfile.TemporaryDirectory() as temp_dir:
        prev_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Actually create the file
            test_file = Path("new_file.py")
            test_file.write_text("print('Hello, World!')")

            verification = verify_grind_completion(
                session_id=888,
                run_num=1,
                output=output_with_creation,
                returncode=0
            )
        finally:
            os.chdir(prev_cwd)

        print(f"Verification result: {verification['verification_status']}")
        print(f"Hallucination detected: {verification.get('hallucination_detected', False)}")
        print(f"Files verified: {verification.get('verified_files', [])}")

        # Should NOT detect hallucination
        assert not verification.get('hallucination_detected', False)
        assert verification['verification_status'] == 'VERIFIED'
        assert verification['verified']
        assert len(verification['verified_files']) > 0

        print("[OK] Legitimate file creation works correctly")


if __name__ == "__main__":
    try:
        test_hallucination_detection()
        test_critic_enhanced_detection()
        test_legitimate_file_creation()

        print("\n[SUCCESS] ALL TESTS PASSED - Hallucination bug fixes are working!")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)