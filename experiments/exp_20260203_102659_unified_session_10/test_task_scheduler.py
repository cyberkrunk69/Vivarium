"""
Test script for task_scheduler.py

Demonstrates dependency detection, scheduling, and visualization.
"""

import json
import time
import logging
from task_scheduler import TaskScheduler, Task, TaskStatus

def mock_executor(task: Task):
    """Mock task executor for testing."""
    print(f"Executing task: {task.id} - {task.content}")
    time.sleep(0.5)  # Simulate work
    return f"Result for {task.id}"

def test_basic_scheduling():
    """Test basic task scheduling without dependencies."""
    print("=== Test: Basic Scheduling ===")

    scheduler = TaskScheduler(max_workers=2, executor_func=mock_executor)

    # Add independent tasks
    scheduler.add_task("task_1", "First independent task")
    scheduler.add_task("task_2", "Second independent task")
    scheduler.add_task("task_3", "Third independent task")

    print("Initial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    results = scheduler.run(timeout=10)

    print("\nFinal state:")
    print(scheduler.visualize_progress())

    return results

def test_dependency_chain():
    """Test tasks with explicit dependencies."""
    print("\n=== Test: Dependency Chain ===")

    scheduler = TaskScheduler(max_workers=3, executor_func=mock_executor)

    # Add tasks with explicit dependencies
    scheduler.add_task("init", "Initialize system")
    scheduler.add_task("load", "Load data, depends on init")
    scheduler.add_task("process", "Process data, requires load")
    scheduler.add_task("save", "Save results, after process")

    # Add manual dependencies
    scheduler.add_dependency("load", "init")
    scheduler.add_dependency("process", "load")
    scheduler.add_dependency("save", "process")

    print("Initial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    results = scheduler.run(timeout=15)

    print("\nFinal state:")
    print(scheduler.visualize_progress())

    return results

def test_parallel_branches():
    """Test parallel execution with converging dependencies."""
    print("\n=== Test: Parallel Branches ===")

    scheduler = TaskScheduler(max_workers=4, executor_func=mock_executor)

    # Create diamond dependency pattern
    scheduler.add_task("start", "Start task")
    scheduler.add_task("branch_a", "Branch A, depends on start")
    scheduler.add_task("branch_b", "Branch B, depends on start")
    scheduler.add_task("merge", "Merge branches, needs branch_a and branch_b")

    # Set up dependencies
    scheduler.add_dependency("branch_a", "start")
    scheduler.add_dependency("branch_b", "start")
    scheduler.add_dependency("merge", "branch_a")
    scheduler.add_dependency("merge", "branch_b")

    print("Initial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    results = scheduler.run(timeout=15)

    print("\nFinal state:")
    print(scheduler.visualize_progress())

    return results

def test_auto_dependency_detection():
    """Test automatic dependency detection from task content."""
    print("\n=== Test: Auto-Dependency Detection ===")

    scheduler = TaskScheduler(max_workers=2, executor_func=mock_executor)

    # Tasks with dependency keywords
    scheduler.add_task("setup", "Setup the environment")
    scheduler.add_task("build", "Build the project, depends on setup")
    scheduler.add_task("test", "Run tests, requires build")
    scheduler.add_task("deploy", "Deploy application after test")

    print("Dependencies detected automatically:")
    for task_id, task in scheduler.dependency_graph.tasks.items():
        if task.dependencies:
            print(f"  {task_id}: {list(task.dependencies)}")

    print("\nInitial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    results = scheduler.run(timeout=15)

    print("\nFinal state:")
    print(scheduler.visualize_progress())

    return results

def test_complex_workflow():
    """Test complex workflow with multiple dependency patterns."""
    print("\n=== Test: Complex Workflow ===")

    scheduler = TaskScheduler(max_workers=3, executor_func=mock_executor)

    # Complex workflow
    tasks = [
        ("config", "Load configuration"),
        ("db_setup", "Setup database, depends on config"),
        ("api_setup", "Setup API server, requires config"),
        ("auth_init", "Initialize auth, needs db_setup"),
        ("data_seed", "Seed initial data, after db_setup"),
        ("api_start", "Start API service, requires api_setup and auth_init"),
        ("health_check", "Health check, needs api_start"),
        ("integration_test", "Run integration tests, after health_check and data_seed")
    ]

    for task_id, content in tasks:
        scheduler.add_task(task_id, content)

    # Add some manual dependencies for completeness
    scheduler.add_dependency("integration_test", "health_check")
    scheduler.add_dependency("integration_test", "data_seed")

    print("Initial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    results = scheduler.run(timeout=20)

    print("\nFinal state:")
    print(scheduler.visualize_progress())

    return results

def test_failure_handling():
    """Test handling of task failures."""
    print("\n=== Test: Failure Handling ===")

    def failing_executor(task: Task):
        if "fail" in task.content.lower():
            raise Exception("Simulated task failure")
        time.sleep(0.2)
        return f"Success: {task.id}"

    scheduler = TaskScheduler(max_workers=2, executor_func=failing_executor)

    # Add tasks where one will fail
    scheduler.add_task("good_task", "This task will succeed")
    scheduler.add_task("fail_task", "This task will FAIL")
    scheduler.add_task("dependent", "This depends on fail_task")

    scheduler.add_dependency("dependent", "fail_task")

    print("Initial state:")
    print(scheduler.visualize_progress())

    # Run scheduler
    results = scheduler.run(timeout=10)

    print("\nFinal state:")
    print(scheduler.visualize_progress())

    print("\nFailure details:")
    for task_id, task_result in results["tasks"].items():
        if task_result["status"] == "failed":
            print(f"  {task_id}: {task_result['error']}")

    return results

def run_all_tests():
    """Run all test scenarios."""
    logging.basicConfig(level=logging.INFO)

    test_results = {}

    try:
        test_results["basic"] = test_basic_scheduling()
        test_results["chain"] = test_dependency_chain()
        test_results["parallel"] = test_parallel_branches()
        test_results["auto_deps"] = test_auto_dependency_detection()
        test_results["complex"] = test_complex_workflow()
        test_results["failures"] = test_failure_handling()

        print("\n" + "="*50)
        print("ALL TESTS COMPLETED")
        print("="*50)

        # Summary
        for test_name, result in test_results.items():
            summary = result["summary"]
            print(f"{test_name}: {summary['completed']}/{summary['total']} completed, "
                  f"{summary['failed']} failed")

        return test_results

    except Exception as e:
        print(f"Test execution failed: {e}")
        return None

if __name__ == "__main__":
    results = run_all_tests()

    # Save test results
    if results:
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\nTest results saved to test_results.json")