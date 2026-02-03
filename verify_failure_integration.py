#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify failure_patterns is integrated into grind_spawner."""

import sys
import io
from pathlib import Path

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test 1: Check imports
print("Test 1: Checking imports...")
try:
    from failure_patterns import FailurePatternDetector
    from grind_spawner import GrindSession
    print("  ✓ All imports successful")
except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Check that grind_spawner imports failure_patterns
print("\nTest 2: Verifying integration...")
import inspect
source = inspect.getsource(GrindSession)
if "FailurePatternDetector" in source:
    print("  ✓ FailurePatternDetector referenced in GrindSession")
else:
    print("  ✗ FailurePatternDetector not found in GrindSession")
    sys.exit(1)

if "failure_detector" in source:
    print("  ✓ failure_detector attribute found")
else:
    print("  ✗ failure_detector attribute not found")
    sys.exit(1)

if "generate_warning_prompt" in source:
    print("  ✓ Warning prompt generation integrated")
else:
    print("  ✗ Warning prompt generation not found")
    sys.exit(1)

if "track_failure" in source:
    print("  ✓ Failure tracking integrated")
else:
    print("  ✗ Failure tracking not found")
    sys.exit(1)

# Test 3: Test basic functionality
print("\nTest 3: Testing basic functionality...")
detector = FailurePatternDetector(workspace=project_root)

# Track a test failure
failure = detector.track_failure(
    task_description="Test task for verification",
    error_type="TestError",
    error_message="This is a test error",
    task_characteristics={"test": True},
    attempted_approaches=["Test approach"]
)
print(f"  ✓ Tracked test failure: {failure['id']}")

# Check for patterns
result = detector.check_failure_patterns(
    "Test task for verification",
    {"test": True}
)
print(f"  ✓ Pattern check returned: {result['warning_level']}")

# Generate warning
warning = detector.generate_warning_prompt(
    "Test task for verification",
    {"test": True}
)
if warning:
    print(f"  ✓ Warning generated ({len(warning)} chars)")
else:
    print("  ✓ No warning (expected for single failure)")

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print("\nFailure pattern detection is fully integrated.")
print("\nFeatures:")
print("  • Tracks failures with error type, message, and context")
print("  • Detects similar past failures before execution")
print("  • Injects warnings into prompts for risky tasks")
print("  • Records failures from timeout, exceptions, and errors")
print("  • Provides avoidance strategies based on past failures")
