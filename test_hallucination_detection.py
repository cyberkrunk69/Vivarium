#!/usr/bin/env python3
"""
Test script to verify hallucination detection fix

This script tests the enhanced verification system using the actual Session 2 data
that demonstrated the hallucination bug.
"""

import json
import sys
from pathlib import Path
import hashlib

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from grind_spawner import verify_grind_completion
from tool_operation_logger import log_hallucination_detection

def test_session_2_hallucination():
    """Test hallucination detection using actual Session 2 data."""

    # Load Session 2 log that showed the hallucination bug
    session_log_file = Path("grind_logs/session_2_run_1.json")
    if not session_log_file.exists():
        print("ERROR: Session 2 log not found. Expected grind_logs/session_2_run_1.json")
        return False

    # Load the session log
    session_data = json.loads(session_log_file.read_text())

    # Extract the output that claimed file modifications
    output = session_data.get("result", "")
    returncode = 0  # Session reported success

    print("Testing Session 2 Hallucination Detection")
    print("=" * 60)
    print(f"Session output length: {len(output)} characters")
    print(f"Return code: {returncode}")

    # Check current dashboard.html hash
    dashboard_file = Path("dashboard.html")
    if dashboard_file.exists():
        current_hash = hashlib.md5(dashboard_file.read_bytes()).hexdigest()
        print(f"Current dashboard.html hash: {current_hash}")

    # Run the enhanced verification system
    verification_result = verify_grind_completion(
        session_id=2,
        run_num=1,
        output=output,
        returncode=returncode
    )

    print("\nVerification Results:")
    print("-" * 30)
    print(f"Verified: {verification_result['verified']}")
    print(f"Verification Status: {verification_result.get('verification_status', 'UNKNOWN')}")
    print(f"Hallucination Detected: {verification_result.get('hallucination_detected', False)}")
    print(f"Claimed Files: {verification_result.get('claimed_files', [])}")
    print(f"Verified Files: {verification_result.get('verified_files', [])}")
    print(f"Details: {verification_result.get('details', 'No details')}")

    # Test tool operation logging
    print("\nTesting Tool Operation Logger:")
    print("-" * 30)
    tool_summary = log_hallucination_detection(
        workspace=Path("."),
        session_id=2,
        run_num=1,
        claimed_files=verification_result.get("claimed_files", []),
        verified_files=verification_result.get("verified_files", [])
    )

    print(f"Hallucination Risk: {tool_summary.get('hallucination_risk', False)}")
    print(f"Claimed Operations: {tool_summary.get('claimed_operations', 0)}")
    print(f"Actual Operations: {tool_summary.get('actual_operations', 0)}")

    # Determine if fix worked
    expected_hallucination = True  # We expect this session to be flagged as hallucination
    actual_hallucination = verification_result.get('hallucination_detected', False)

    print("\nTest Results:")
    print("=" * 60)
    if actual_hallucination == expected_hallucination:
        print("[SUCCESS] Hallucination detection is working correctly!")
        print("   The system now properly detects when workers claim file modifications")
        print("   but don't actually modify files on disk.")
        return True
    else:
        print("[FAILURE] Hallucination detection did not work as expected")
        print(f"   Expected hallucination: {expected_hallucination}")
        print(f"   Actual hallucination: {actual_hallucination}")
        return False

def test_pattern_extraction():
    """Test that the enhanced pattern extraction catches file claims in text."""

    # Test output that contains file modification claims in text (like Session 2)
    test_output = """
    Files modified:
    - dashboard.html:1-544 - Complete brand transformation with Vivarium visual identity

    Changes summary:
    - CSS variables system with brand colors (--swarm-void, --swarm-neural, --swarm-emergence, --swarm-warning)
    - Typography system using Inter for UI and JetBrains Mono for code elements
    """

    print("\nTesting Pattern Extraction:")
    print("-" * 30)
    print("Test output contains: 'dashboard.html:1-544'")

    # Run verification with this test output
    verification = verify_grind_completion(
        session_id=999,  # Test session
        run_num=1,
        output=test_output,
        returncode=0
    )

    claimed_files = verification.get("claimed_files", [])
    print(f"Extracted claimed files: {claimed_files}")

    if "dashboard.html" in claimed_files:
        print("[SUCCESS] Pattern extraction correctly identified dashboard.html")
        return True
    else:
        print("[FAILURE] Pattern extraction missed the file claim")
        return False

if __name__ == "__main__":
    print("Hallucination Detection Fix Test")
    print("=" * 60)

    # Test 1: Pattern extraction
    pattern_test_passed = test_pattern_extraction()

    # Test 2: Full Session 2 verification
    session_test_passed = test_session_2_hallucination()

    # Overall result
    print("\nOverall Test Results:")
    print("=" * 60)

    if pattern_test_passed and session_test_passed:
        print("ALL TESTS PASSED!")
        print("The hallucination bug fix is working correctly.")
        print("\nKey improvements:")
        print("- Enhanced file pattern extraction from text claims")
        print("- Strict verification using content hashing")
        print("- Explicit hallucination detection and flagging")
        print("- Tool operation logging for audit trail")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED")
        print("The hallucination detection fix needs more work.")
        sys.exit(1)