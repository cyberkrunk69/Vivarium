"""
Simple test to verify safety_sandbox.py functionality.

Tests:
1. Path within workspace is allowed
2. Path outside workspace is blocked
3. Sensitive file patterns are blocked
4. Audit log captures operations
"""

from pathlib import Path
from safety_sandbox import WorkspaceSandbox

def test_sandbox():
    workspace = Path(__file__).parent
    sandbox = WorkspaceSandbox(str(workspace))

    print("Testing WorkspaceSandbox...")

    # Test 1: Path within workspace should be allowed
    test_file = workspace / "test_file.txt"
    assert sandbox.is_path_allowed(str(test_file)), "Test 1 Failed: Valid path rejected"
    print("[OK] Test 1: Path within workspace allowed")

    # Test 2: Path outside workspace should be blocked
    outside_path = "/etc/passwd"
    assert not sandbox.is_path_allowed(outside_path), "Test 2 Failed: Outside path allowed"
    print("[OK] Test 2: Path outside workspace blocked")

    # Test 3: Sensitive file patterns should be blocked
    sensitive_file = workspace / ".env"
    assert not sandbox.is_path_allowed(str(sensitive_file)), "Test 3 Failed: Sensitive file allowed"
    print("[OK] Test 3: Sensitive file pattern blocked")

    # Test 4: Audit log should capture operations
    audit = sandbox.get_audit_log()
    assert len(audit) > 0, "Test 4 Failed: No audit entries"
    print(f"[OK] Test 4: Audit log captured {len(audit)} operations")

    # Test 5: validate_write helper
    assert sandbox.validate_write(str(workspace / "allowed.json")), "Test 5 Failed: Valid write rejected"
    assert not sandbox.validate_write(str(workspace / "credentials.txt")), "Test 5 Failed: Sensitive write allowed"
    print("[OK] Test 5: validate_write helper works correctly")

    print("\n[SUCCESS] All tests passed!")
    print(f"\nAudit log entries: {len(sandbox.get_audit_log())}")

if __name__ == "__main__":
    test_sandbox()
