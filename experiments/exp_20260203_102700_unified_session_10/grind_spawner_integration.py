"""
Task Scheduler Integration for grind_spawner.py

This module provides integration functions to add dependency-aware scheduling
to the existing grind_spawner system.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Set
from task_scheduler import TaskScheduler, Task, TaskStatus

class GrindTaskScheduler:
    """Grind-specific task scheduler wrapper"""
    
    def __init__(self, max_concurrent: int = 3):
        self.scheduler = TaskScheduler(max_concurrent)
        self.grind_sessions: Dict[str, Any] = {}
        
    def add_grind_task(self, task_data: Dict[str, Any]) -> str:
        """Add a grind task with auto-detected dependencies"""
        task_id = task_data.get("id", f"grind_task_{len(self.scheduler.graph.tasks)}")
        description = task_data.get("task", "")
        explicit_deps = set(task_data.get("dependencies", []))
        
        # Store grind-specific data
        self.grind_sessions[task_id] = {
            "model": task_data.get("model", "haiku"),
            "budget": task_data.get("budget", 0.10),
            "workspace": task_data.get("workspace", "."),
            "original_data": task_data
        }
        
        # Create executor function for grind task
        async def grind_executor(task: Task):
            return await self._execute_grind_task(task_id, task)
        
        self.scheduler.add_task(task_id, description, explicit_deps, grind_executor)
        return task_id
    
    async def _execute_grind_task(self, task_id: str, task: Task):
        """Execute a grind task using the existing GrindSession logic"""
        session_config = self.grind_sessions[task_id]
        
        # Import here to avoid circular imports
        from grind_spawner import GrindSession
        
        # Create and run grind session
        session = GrindSession(
            session_id=hash(task_id) % 10000,  # Generate numeric ID
            model=session_config["model"],
            budget=session_config["budget"],
            workspace=Path(session_config["workspace"]),
            task=task.description
        )
        
        result = session.run_once()
        return result
    
    async def execute_all_grind_tasks(self) -> Dict[str, Any]:
        """Execute all grind tasks with dependency resolution"""
        return await self.scheduler.execute_all()
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get detailed execution status"""
        status = self.scheduler.get_status()
        
        # Add grind-specific information
        status["grind_sessions"] = {}
        for task_id in self.grind_sessions:
            task = self.scheduler.graph.tasks.get(task_id)
            if task:
                status["grind_sessions"][task_id] = {
                    "status": task.status.value,
                    "model": self.grind_sessions[task_id]["model"],
                    "budget": self.grind_sessions[task_id]["budget"],
                    "duration": task.duration(),
                    "result": str(task.result)[:100] if task.result else None
                }
        
        return status

def parse_grind_tasks_with_dependencies(tasks_file: Path) -> List[Dict[str, Any]]:
    """Parse grind_tasks.json with dependency support"""
    if not tasks_file.exists():
        return []
    
    with open(tasks_file, 'r') as f:
        tasks_data = json.load(f)
    
    # Enhance task data with dependency detection
    enhanced_tasks = []
    for i, task_data in enumerate(tasks_data):
        # Ensure task has an ID
        if "id" not in task_data:
            task_data["id"] = f"task_{i}"
        
        # Auto-detect dependencies from task description
        dependencies = extract_task_dependencies(task_data.get("task", ""), 
                                                [t.get("id", f"task_{j}") for j, t in enumerate(tasks_data) if j != i])
        
        # Merge with explicit dependencies
        if "dependencies" in task_data:
            dependencies.update(task_data["dependencies"])
        
        task_data["dependencies"] = list(dependencies)
        enhanced_tasks.append(task_data)
    
    return enhanced_tasks

def extract_task_dependencies(task_description: str, available_task_ids: List[str]) -> Set[str]:
    """Extract dependencies from task description text"""
    import re
    
    dependencies = set()
    description_lower = task_description.lower()
    
    # Dependency patterns
    patterns = [
        r"after\s+(\w+)",
        r"requires?\s+(\w+)",
        r"depends?\s+on\s+(\w+)",
        r"once\s+(\w+)\s+is\s+(?:done|complete)",
        r"when\s+(\w+)\s+(?:completes?|finishes?)",
        r"following\s+(\w+)",
        r"building\s+on\s+(\w+)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description_lower)
        for match in matches:
            # Find matching task ID
            for task_id in available_task_ids:
                if match in task_id.lower() or task_id.lower() in match:
                    dependencies.add(task_id)
                    break
    
    return dependencies

async def run_grind_with_dependencies(tasks_file: Path, max_concurrent: int = 3) -> Dict[str, Any]:
    """Run grind spawner with dependency-aware scheduling"""
    
    # Parse tasks with dependency detection
    tasks_data = parse_grind_tasks_with_dependencies(tasks_file)
    
    if not tasks_data:
        return {"error": "No tasks found"}
    
    # Create scheduler and add tasks
    grind_scheduler = GrindTaskScheduler(max_concurrent)
    
    for task_data in tasks_data:
        task_id = grind_scheduler.add_grind_task(task_data)
        print(f"Added task '{task_id}': {task_data.get('task', '')[:50]}...")
        if task_data.get('dependencies'):
            print(f"  Dependencies: {task_data['dependencies']}")
    
    # Check for dependency cycles
    if grind_scheduler.scheduler.graph.has_cycles():
        return {"error": "Dependency cycle detected in tasks"}
    
    # Execute with dependency resolution
    print(f"\nExecuting {len(tasks_data)} tasks with dependency resolution...")
    print(f"Max concurrent sessions: {max_concurrent}")
    
    result = await grind_scheduler.execute_all_grind_tasks()
    
    # Save execution log
    log_file = Path("grind_dependency_execution.json")
    grind_scheduler.scheduler.save_execution_log(str(log_file))
    print(f"\nExecution log saved to: {log_file}")
    
    return result

# CLI integration
def add_dependency_arguments(parser):
    """Add dependency-related arguments to grind_spawner argument parser"""
    parser.add_argument("--dependencies", action="store_true", 
                       help="Enable dependency-aware task scheduling")
    parser.add_argument("--max-concurrent", type=int, default=3,
                       help="Maximum concurrent tasks when using dependency scheduling")
    parser.add_argument("--dependency-viz", action="store_true",
                       help="Generate dependency visualization graph")

if __name__ == "__main__":
    # Test the dependency scheduler
    import asyncio
    
    async def test_dependency_scheduler():
        # Create test tasks file
        test_tasks = [
            {
                "id": "setup",
                "task": "Initialize project environment and dependencies",
                "model": "haiku",
                "budget": 0.05
            },
            {
                "id": "compile", 
                "task": "Compile the source code after setup is complete",
                "dependencies": ["setup"],
                "model": "haiku",
                "budget": 0.05
            },
            {
                "id": "test_unit",
                "task": "Run unit tests requires compile to be done first",
                "model": "sonnet",
                "budget": 0.10
            },
            {
                "id": "test_integration",
                "task": "Run integration tests depends on compile",
                "model": "sonnet", 
                "budget": 0.10
            },
            {
                "id": "deploy",
                "task": "Deploy to production after test_unit and test_integration",
                "model": "opus",
                "budget": 0.20
            }
        ]
        
        test_file = Path("test_grind_tasks_deps.json")
        with open(test_file, 'w') as f:
            json.dump(test_tasks, f, indent=2)
        
        # Run with dependencies
        result = await run_grind_with_dependencies(test_file, max_concurrent=2)
        print(json.dumps(result, indent=2))
        
        # Cleanup
        test_file.unlink()
    
    asyncio.run(test_dependency_scheduler())