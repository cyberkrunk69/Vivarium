"""
Integration module for task_scheduler.py with grind_spawner.py

Provides dependency-aware task scheduling for the grind spawner system.
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from task_scheduler import TaskScheduler, Task, TaskStatus

class GrindTaskScheduler:
    """Integration layer between task scheduler and grind spawner."""

    def __init__(self, max_workers: int = 4):
        self.scheduler = TaskScheduler(max_workers=max_workers, executor_func=self._execute_grind_task)
        self.grind_results: Dict[str, Any] = {}

    def _execute_grind_task(self, task: Task) -> Any:
        """Execute a grind task using subprocess."""
        import subprocess

        try:
            # Parse task content for grind parameters
            task_info = self._parse_task_content(task.content)

            # Build grind command
            cmd = self._build_grind_command(task_info)

            # Execute grind spawner
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=task_info.get('timeout', 300)  # 5 min default
            )

            # Parse result
            grind_result = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }

            self.grind_results[task.id] = grind_result

            if result.returncode != 0:
                raise Exception(f"Grind task failed: {result.stderr}")

            return grind_result

        except Exception as e:
            raise Exception(f"Failed to execute grind task {task.id}: {str(e)}")

    def _parse_task_content(self, content: str) -> Dict[str, Any]:
        """Parse task content to extract grind parameters."""
        task_info = {
            'task': content,
            'sessions': 1,
            'model': 'sonnet',
            'budget': 0.05,
            'timeout': 300
        }

        # Extract parameters from content
        lines = content.split('\n')
        for line in lines:
            line = line.strip().lower()

            if 'sessions:' in line or 'workers:' in line:
                try:
                    task_info['sessions'] = int(line.split(':')[1].strip())
                except:
                    pass

            if 'model:' in line:
                model = line.split(':')[1].strip()
                if model in ['opus', 'sonnet', 'haiku']:
                    task_info['model'] = model

            if 'budget:' in line:
                try:
                    task_info['budget'] = float(line.split(':')[1].strip())
                except:
                    pass

            if 'timeout:' in line:
                try:
                    task_info['timeout'] = int(line.split(':')[1].strip())
                except:
                    pass

        return task_info

    def _build_grind_command(self, task_info: Dict[str, Any]) -> List[str]:
        """Build grind spawner command."""
        cmd = [
            sys.executable,
            'grind_spawner.py',
            '--sessions', str(task_info['sessions']),
            '--model', task_info['model'],
            '--budget', str(task_info['budget']),
            '--task', task_info['task']
        ]

        return cmd

    def add_grind_task(self, task_id: str, task_content: str, dependencies: Set[str] = None) -> Task:
        """Add a grind task with dependencies."""
        return self.scheduler.add_task(task_id, task_content, dependencies)

    def load_tasks_from_json(self, tasks_file: str = "grind_tasks.json") -> List[Task]:
        """Load tasks from JSON file with dependency detection."""
        try:
            with open(tasks_file, 'r') as f:
                tasks_data = json.load(f)
        except FileNotFoundError:
            return []

        loaded_tasks = []

        for task_data in tasks_data:
            task_id = task_data.get('id', f"task_{len(loaded_tasks)}")
            content = task_data.get('content', task_data.get('task', ''))
            dependencies = set(task_data.get('dependencies', []))

            task = self.add_grind_task(task_id, content, dependencies)
            loaded_tasks.append(task)

        return loaded_tasks

    def run_grind_session(self, timeout: Optional[float] = None) -> Dict[str, Any]:
        """Run the grind session with dependency awareness."""
        print("Starting dependency-aware grind session...")
        print(self.get_progress_visualization())

        results = self.scheduler.run(timeout)

        print("\nGrind session complete!")
        print(self.get_progress_visualization())

        # Add grind-specific results
        results['grind_results'] = self.grind_results

        return results

    def get_progress_visualization(self) -> str:
        """Get visual progress of grind tasks."""
        return self.scheduler.visualize_progress()

    def save_results(self, output_file: str = "grind_results_with_dependencies.json"):
        """Save results to file."""
        results = self.scheduler.get_results()
        results['grind_results'] = self.grind_results

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to {output_file}")

def create_sample_dependency_tasks():
    """Create sample tasks with dependencies for testing."""
    tasks = [
        {
            "id": "setup_env",
            "content": "Setup development environment\nSessions: 1\nModel: haiku\nBudget: 0.02",
            "dependencies": []
        },
        {
            "id": "run_tests",
            "content": "Run all unit tests after setup_env\nSessions: 2\nModel: sonnet\nBudget: 0.05",
            "dependencies": ["setup_env"]
        },
        {
            "id": "fix_bugs",
            "content": "Fix identified bugs requires run_tests\nSessions: 3\nModel: sonnet\nBudget: 0.10",
            "dependencies": ["run_tests"]
        },
        {
            "id": "optimize_perf",
            "content": "Optimize performance needs setup_env\nSessions: 2\nModel: opus\nBudget: 0.08",
            "dependencies": ["setup_env"]
        },
        {
            "id": "final_test",
            "content": "Final integration tests after fix_bugs and optimize_perf\nSessions: 1\nModel: sonnet\nBudget: 0.03",
            "dependencies": ["fix_bugs", "optimize_perf"]
        }
    ]

    with open("grind_tasks_with_deps.json", 'w') as f:
        json.dump(tasks, f, indent=2)

    print("Created grind_tasks_with_deps.json with sample dependency tasks")

def main():
    """Main entry point for dependency-aware grind execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Dependency-aware grind spawner")
    parser.add_argument("--tasks-file", default="grind_tasks_with_deps.json",
                       help="JSON file with tasks and dependencies")
    parser.add_argument("--max-workers", type=int, default=4,
                       help="Maximum parallel grind sessions")
    parser.add_argument("--timeout", type=int, default=1800,
                       help="Total timeout in seconds")
    parser.add_argument("--create-sample", action="store_true",
                       help="Create sample tasks file")
    parser.add_argument("--visualize-only", action="store_true",
                       help="Only show task visualization, don't execute")

    args = parser.parse_args()

    if args.create_sample:
        create_sample_dependency_tasks()
        return

    # Create grind task scheduler
    grind_scheduler = GrindTaskScheduler(max_workers=args.max_workers)

    # Load tasks
    tasks = grind_scheduler.load_tasks_from_json(args.tasks_file)

    if not tasks:
        print(f"No tasks found in {args.tasks_file}")
        print("Use --create-sample to create a sample tasks file")
        return

    print(f"Loaded {len(tasks)} tasks with dependencies")

    if args.visualize_only:
        print("\nTask dependency visualization:")
        print(grind_scheduler.get_progress_visualization())
        return

    # Run grind session
    results = grind_scheduler.run_grind_session(timeout=args.timeout)

    # Save results
    grind_scheduler.save_results()

    # Print summary
    summary = results['summary']
    print(f"\nExecution Summary:")
    print(f"Total tasks: {summary['total']}")
    print(f"Completed: {summary['completed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Blocked: {summary['blocked']}")

if __name__ == "__main__":
    main()