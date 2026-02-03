"""
Task Scheduler Integration with Grind Spawner
Provides integration layer between the task scheduler and existing grind spawner system.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import grind_spawner
sys.path.append(str(Path(__file__).parent.parent.parent))

from task_scheduler import TaskScheduler, Task, TaskStatus
import json
import threading
import time
from typing import Dict, List, Optional, Any


class GrindSchedulerIntegration:
    """Integration class that connects TaskScheduler with grind_spawner functionality."""

    def __init__(self, max_concurrent_sessions: int = 4, workspace: Optional[str] = None):
        self.scheduler = TaskScheduler(max_concurrent_tasks=max_concurrent_sessions)
        self.workspace = workspace or os.getcwd()
        self.session_logs: Dict[str, List[str]] = {}
        self.task_results: Dict[str, Any] = {}

        # Setup completion callback
        self.scheduler.add_completion_callback(self._on_task_complete)

    def _on_task_complete(self, task: Task):
        """Callback when a task completes."""
        print(f"[SCHEDULER] Task {task.id} completed: {task.status.value}")
        if task.error:
            print(f"[SCHEDULER] Error: {task.error}")

    def add_grind_task(self, task_id: str, description: str,
                      dependencies: Optional[List[str]] = None,
                      model: str = "sonnet",
                      budget: float = 0.05,
                      metadata: Optional[Dict] = None) -> Task:
        """Add a grind task with Claude spawner execution."""

        def grind_executor(task: Task) -> Dict[str, Any]:
            """Execute a grind task by spawning Claude session."""
            import subprocess
            import tempfile

            task_metadata = task.metadata.get('grind_config', {})
            model = task_metadata.get('model', 'sonnet')
            budget = task_metadata.get('budget', 0.05)
            workspace = task_metadata.get('workspace', self.workspace)

            # Create a temporary task file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                task_config = {
                    "task": task.description,
                    "model": model,
                    "budget": budget,
                    "workspace": workspace,
                    "dependencies": list(task.dependencies)
                }
                json.dump(task_config, f, indent=2)
                task_file = f.name

            try:
                # Execute grind spawner for this single task
                cmd = [
                    sys.executable,
                    os.path.join(self.workspace, 'grind_spawner.py'),
                    '--sessions', '1',
                    '--model', model,
                    '--budget', str(budget),
                    '--task', task.description,
                    '--workspace', workspace
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minute timeout
                )

                execution_result = {
                    'success': result.returncode == 0,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode,
                    'task_file': task_file
                }

                # Store logs for this session
                self.session_logs[task.id] = result.stdout.split('\n')

                if result.returncode != 0:
                    raise Exception(f"Grind spawner failed: {result.stderr}")

                return execution_result

            except subprocess.TimeoutExpired:
                raise Exception("Task execution timed out")
            except Exception as e:
                raise Exception(f"Failed to execute grind task: {str(e)}")
            finally:
                # Clean up temporary file
                try:
                    os.unlink(task_file)
                except:
                    pass

        # Combine provided metadata with grind config
        combined_metadata = metadata or {}
        combined_metadata['grind_config'] = {
            'model': model,
            'budget': budget,
            'workspace': self.workspace
        }

        return self.scheduler.add_task(
            task_id=task_id,
            description=description,
            dependencies=dependencies,
            executor_func=grind_executor,
            metadata=combined_metadata
        )

    def add_task_batch(self, tasks: List[Dict[str, Any]]) -> List[Task]:
        """Add multiple tasks at once."""
        created_tasks = []

        for task_config in tasks:
            task = self.add_grind_task(
                task_id=task_config['id'],
                description=task_config['description'],
                dependencies=task_config.get('dependencies'),
                model=task_config.get('model', 'sonnet'),
                budget=task_config.get('budget', 0.05),
                metadata=task_config.get('metadata')
            )
            created_tasks.append(task)

        return created_tasks

    def load_tasks_from_file(self, file_path: str) -> List[Task]:
        """Load tasks from a JSON configuration file."""
        with open(file_path, 'r') as f:
            config = json.load(f)

        if 'tasks' in config:
            return self.add_task_batch(config['tasks'])
        else:
            # Single task file
            return [self.add_grind_task(
                task_id=config.get('id', 'task_1'),
                description=config['description'],
                dependencies=config.get('dependencies'),
                model=config.get('model', 'sonnet'),
                budget=config.get('budget', 0.05),
                metadata=config.get('metadata')
            )]

    def start_execution(self):
        """Start the task scheduler."""
        print("[SCHEDULER] Starting dependency-aware task execution...")
        self.scheduler.start()

    def wait_for_completion(self, timeout: Optional[float] = None):
        """Wait for all tasks to complete."""
        try:
            self.scheduler.wait_for_completion(timeout=timeout)
            print("[SCHEDULER] All tasks completed!")
        except TimeoutError:
            print("[SCHEDULER] Tasks timed out!")

    def stop_execution(self):
        """Stop the task scheduler."""
        print("[SCHEDULER] Stopping task execution...")
        self.scheduler.stop()

    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report."""
        status = self.scheduler.get_status()
        history = self.scheduler.get_task_history()

        return {
            'scheduler_status': status,
            'task_history': history,
            'session_logs': self.session_logs,
            'dependency_graph': status['dependency_graph']
        }

    def export_results(self, output_file: str):
        """Export execution results to file."""
        results = self.get_status_report()

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"[SCHEDULER] Results exported to {output_file}")


def create_example_task_config():
    """Create an example task configuration file."""
    example_config = {
        "tasks": [
            {
                "id": "setup_env",
                "description": "Setup development environment and install dependencies",
                "model": "sonnet",
                "budget": 0.03
            },
            {
                "id": "run_tests",
                "description": "Run test suite requires setup_env",
                "dependencies": ["setup_env"],
                "model": "sonnet",
                "budget": 0.05
            },
            {
                "id": "fix_bugs",
                "description": "Fix any bugs found in tests depends on run_tests",
                "dependencies": ["run_tests"],
                "model": "opus",
                "budget": 0.10
            },
            {
                "id": "update_docs",
                "description": "Update documentation after setup_env",
                "dependencies": ["setup_env"],
                "model": "sonnet",
                "budget": 0.04
            },
            {
                "id": "final_validation",
                "description": "Final validation needs fix_bugs and update_docs",
                "dependencies": ["fix_bugs", "update_docs"],
                "model": "opus",
                "budget": 0.06
            }
        ]
    }

    with open('example_tasks.json', 'w') as f:
        json.dump(example_config, f, indent=2)

    print("Created example_tasks.json")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dependency-aware grind task scheduler")
    parser.add_argument('--tasks-file', help="JSON file containing task definitions")
    parser.add_argument('--sessions', type=int, default=4, help="Max concurrent sessions")
    parser.add_argument('--workspace', help="Target workspace directory")
    parser.add_argument('--timeout', type=int, default=3600, help="Execution timeout in seconds")
    parser.add_argument('--output', help="Output file for results")
    parser.add_argument('--create-example', action='store_true', help="Create example task config")

    args = parser.parse_args()

    if args.create_example:
        create_example_task_config()
        sys.exit(0)

    if not args.tasks_file:
        print("Error: --tasks-file is required")
        sys.exit(1)

    # Create integration instance
    integration = GrindSchedulerIntegration(
        max_concurrent_sessions=args.sessions,
        workspace=args.workspace
    )

    try:
        # Load tasks from file
        tasks = integration.load_tasks_from_file(args.tasks_file)
        print(f"[SCHEDULER] Loaded {len(tasks)} tasks")

        # Start execution
        integration.start_execution()

        # Wait for completion
        integration.wait_for_completion(timeout=args.timeout)

        # Export results if requested
        if args.output:
            integration.export_results(args.output)
        else:
            # Print status report
            report = integration.get_status_report()
            print("\n[SCHEDULER] Final Status Report:")
            print(json.dumps(report['scheduler_status'], indent=2))

    except KeyboardInterrupt:
        print("\n[SCHEDULER] Interrupted by user")
        integration.stop_execution()
    except Exception as e:
        print(f"[SCHEDULER] Error: {e}")
        integration.stop_execution()
        sys.exit(1)