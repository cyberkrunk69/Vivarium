#!/usr/bin/env python3
"""
Simple test for LAN Session Manager - ASCII only
"""

import json
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lan_session_manager import LANSessionManager, SecurityError

def simple_test():
    print("Testing LAN Session Manager")
    print("=" * 40)

    # Create session manager
    session_manager = LANSessionManager("test_sessions")

    # Test basic functionality
    print("\n1. Creating sessions...")
    session1 = session_manager.create_session("192.168.1.100")
    session2 = session_manager.create_session("192.168.1.101")
    print(f"   Session 1: {session1.workspace}")
    print(f"   Session 2: {session2.workspace}")

    # Test task creation
    print("\n2. Starting tasks...")
    task1 = session_manager.start_user_task("192.168.1.100", "Test task 1")
    task2 = session_manager.start_user_task("192.168.1.101", "Test task 2")
    print(f"   Task 1: {task1}")
    print(f"   Task 2: {task2}")

    # Test dashboard data
    print("\n3. Getting dashboard data...")
    dashboard1 = session_manager.get_user_dashboard_data("192.168.1.100")
    dashboard2 = session_manager.get_user_dashboard_data("192.168.1.101")

    print(f"   User 1 active tasks: {len(dashboard1['activity']['my_tasks'])}")
    print(f"   User 2 active tasks: {len(dashboard2['activity']['my_tasks'])}")

    # Test task isolation
    print("\n4. Testing isolation...")
    user1_task_ids = {t['task_id'] for t in dashboard1['activity']['my_tasks']}
    user2_task_ids = {t['task_id'] for t in dashboard2['activity']['my_tasks']}

    assert task1 in user1_task_ids, "User 1 should see own task"
    assert task2 in user2_task_ids, "User 2 should see own task"
    assert task1 not in user2_task_ids, "User 2 should not see User 1's task"
    assert task2 not in user1_task_ids, "User 1 should not see User 2's task"
    print("   Task isolation: PASS")

    # Test security
    print("\n5. Testing security...")
    try:
        session_manager.complete_user_task(task1, "192.168.1.101")  # Wrong user
        print("   Security test: FAIL - should have blocked")
        return False
    except SecurityError:
        print("   Security test: PASS")

    # Complete tasks properly
    print("\n6. Completing tasks...")
    session_manager.complete_user_task(task1, "192.168.1.100")
    session_manager.complete_user_task(task2, "192.168.1.101")
    print("   Tasks completed successfully")

    # Cleanup
    print("\n7. Cleaning up...")
    session_manager.cleanup_session("192.168.1.100")
    session_manager.cleanup_session("192.168.1.101")
    print("   Cleanup complete")

    print("\nALL TESTS PASSED!")
    return True

if __name__ == "__main__":
    try:
        simple_test()
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)