"""
Task Dependency Scheduler for Autonomous AI Swarm

Implements dependency-aware task scheduling with:
- Automatic dependency detection from task text
- Parallel execution of independent tasks  
- Blocking on unmet dependencies
- Progress tracking with dependency visualization
"""

import re
import json
import time
import threading
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import networkx as nx

class TaskStatus(Enum):
    PENDING = "pending"
    READY = "ready" 
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

@dataclass
class Task:
    """Represents a single task with dependencies"""
    id: str
    description: str
    priority: int = 0
    status: TaskStatus = TaskStatus.PENDING
    dependencies: Set[str] = field(default_factory=set)
    dependents: Set[str] = field(default_factory=set)
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    result: Any = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

class DependencyGraph:
    """Manages task dependencies using a directed acyclic graph"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.tasks: Dict[str, Task] = {}
        
    def add_task(self, task: Task) -> None:
        """Add a task to the dependency graph"""
        self.tasks[task.id] = task
        self.graph.add_node(task.id)
        
    def add_dependency(self, task_id: str, dependency_id: str) -> None:
        """Add a dependency relationship between tasks"""
        if task_id not in self.tasks or dependency_id not in self.tasks:
            raise ValueError(f"Both tasks must exist before adding dependency")
            
        # Add edge from dependency to task (dependency -> task)
        self.graph.add_edge(dependency_id, task_id)
        self.tasks[task_id].dependencies.add(dependency_id)
        self.tasks[dependency_id].dependents.add(task_id)
        
        # Check for cycles
        if not nx.is_directed_acyclic_graph(self.graph):
            # Remove the edge that created the cycle
            self.graph.remove_edge(dependency_id, task_id)
            self.tasks[task_id].dependencies.remove(dependency_id)
            self.tasks[dependency_id].dependents.remove(task_id)
            raise ValueError(f"Adding dependency would create cycle")
    
    def get_ready_tasks(self) -> List[str]:
        """Get all tasks that are ready to run (dependencies satisfied)"""
        ready_tasks = []
        
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are completed
                deps_satisfied = all(
                    self.tasks[dep_id].status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )
                
                if deps_satisfied:
                    ready_tasks.append(task_id)
                    task.status = TaskStatus.READY
                    
        return ready_tasks
    
    def get_blocked_tasks(self) -> List[str]:
        """Get tasks blocked by failed dependencies"""
        blocked_tasks = []
        
        for task_id, task in self.tasks.items():
            if task.status in [TaskStatus.PENDING, TaskStatus.READY]:
                # Check if any dependency failed
                has_failed_dep = any(
                    self.tasks[dep_id].status == TaskStatus.FAILED
                    for dep_id in task.dependencies
                )
                
                if has_failed_dep:
                    task.status = TaskStatus.BLOCKED
                    blocked_tasks.append(task_id)
                    
        return blocked_tasks
    
    def topological_sort(self) -> List[str]:
        """Return tasks in topological order"""
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXError:
            raise ValueError("Graph contains cycles")
    
    def get_visualization(self) -> Dict:
        """Get dependency graph visualization data"""
        nodes = []
        edges = []
        
        for task_id, task in self.tasks.items():
            nodes.append({
                'id': task_id,
                'label': task.description[:50] + "..." if len(task.description) > 50 else task.description,
                'status': task.status.value,
                'priority': task.priority
            })
            
        for edge in self.graph.edges():
            edges.append({
                'from': edge[0], 
                'to': edge[1]
            })
            
        return {'nodes': nodes, 'edges': edges}

class TaskScheduler:
    """Manages task scheduling with dependency resolution"""
    
    def __init__(self, max_concurrent_tasks: int = 4):
        self.dependency_graph = DependencyGraph()
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[str, threading.Thread] = {}
        self.task_queue = deque()
        self.scheduler_running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        
        # Dependency detection patterns
        self.dependency_patterns = [
            # "after X", "once X is done"
            (r'(?:after|once)\s+([^,\n]+?)(?:\s+is\s+(?:done|complete|finished))?', 'after'),
            # "requires X", "needs X", "depends on X"
            (r'(?:requires?|needs?|depends?\s+on)\s+([^,\n]+)', 'requires'),
            # "prerequisite: X", "prereq: X"
            (r'(?:prerequisite|prereq):\s*([^,\n]+)', 'prerequisite'),
            # "before X", "prior to X" (reverse dependency)
            (r'(?:before|prior\s+to)\s+([^,\n]+)', 'before'),
            # File dependencies "using file.py", "reads data.json"
            (r'(?:using|reads?|loads?|imports?)\s+([a-zA-Z_][a-zA-Z0-9_]*\.(?:py|json|txt|csv))', 'file_dep')
        ]
    
    def auto_detect_dependencies(self, task_description: str, all_task_descriptions: List[str]) -> Set[str]:
        """Automatically detect dependencies from task description"""
        dependencies = set()
        
        for pattern, dep_type in self.dependency_patterns:
            matches = re.finditer(pattern, task_description, re.IGNORECASE)
            
            for match in matches:
                dep_text = match.group(1).strip()
                
                # Try to match against other task descriptions
                best_match = self._find_best_task_match(dep_text, all_task_descriptions)
                if best_match:
                    dependencies.add(best_match)
                    
        return dependencies
    
    def _find_best_task_match(self, dependency_text: str, task_descriptions: List[str]) -> Optional[str]:
        """Find the best matching task for a dependency text"""
        dependency_words = set(dependency_text.lower().split())
        best_score = 0
        best_match = None
        
        for task_desc in task_descriptions:
            task_words = set(task_desc.lower().split())
            
            # Calculate word overlap
            overlap = len(dependency_words & task_words)
            score = overlap / len(dependency_words) if dependency_words else 0
            
            # Bonus for exact substring match
            if dependency_text.lower() in task_desc.lower():
                score += 0.5
                
            if score > best_score and score > 0.3:  # Minimum threshold
                best_score = score
                best_match = task_desc
                
        return best_match
    
    def add_task(self, task_id: str, description: str, priority: int = 0, 
                 explicit_dependencies: Optional[List[str]] = None) -> Task:
        """Add a task with automatic dependency detection"""
        
        task = Task(
            id=task_id,
            description=description, 
            priority=priority
        )
        
        # Add explicit dependencies
        if explicit_dependencies:
            for dep_id in explicit_dependencies:
                if dep_id in self.dependency_graph.tasks:
                    task.dependencies.add(dep_id)
        
        self.dependency_graph.add_task(task)
        
        # Auto-detect dependencies from all existing tasks
        existing_descriptions = [t.description for t in self.dependency_graph.tasks.values() if t.id != task_id]
        auto_deps = self.auto_detect_dependencies(description, existing_descriptions)
        
        # Map descriptions back to task IDs
        desc_to_id = {t.description: t.id for t in self.dependency_graph.tasks.values()}
        for dep_desc in auto_deps:
            if dep_desc in desc_to_id:
                dep_id = desc_to_id[dep_desc]
                try:
                    self.dependency_graph.add_dependency(task_id, dep_id)
                except ValueError:
                    # Skip circular dependencies
                    pass
        
        return task
    
    def start_scheduler(self) -> None:
        """Start the task scheduler in a background thread"""
        if self.scheduler_running:
            return
            
        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def stop_scheduler(self) -> None:
        """Stop the task scheduler"""
        self.scheduler_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
    
    def _scheduler_loop(self) -> None:
        """Main scheduler loop"""
        while self.scheduler_running:
            try:
                with self.lock:
                    # Clean up completed threads
                    self._cleanup_completed_tasks()
                    
                    # Get ready tasks
                    ready_tasks = self.dependency_graph.get_ready_tasks()
                    
                    # Start tasks up to concurrency limit
                    available_slots = self.max_concurrent_tasks - len(self.running_tasks)
                    
                    # Sort by priority
                    ready_tasks.sort(key=lambda tid: self.dependency_graph.tasks[tid].priority, reverse=True)
                    
                    for task_id in ready_tasks[:available_slots]:
                        self._start_task(task_id)
                    
                    # Update blocked tasks
                    self.dependency_graph.get_blocked_tasks()
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(1)
    
    def _cleanup_completed_tasks(self) -> None:
        """Remove completed task threads"""
        completed = []
        for task_id, thread in self.running_tasks.items():
            if not thread.is_alive():
                completed.append(task_id)
                
        for task_id in completed:
            del self.running_tasks[task_id]
    
    def _start_task(self, task_id: str) -> None:
        """Start executing a task in a thread"""
        task = self.dependency_graph.tasks[task_id]
        task.status = TaskStatus.RUNNING
        task.start_time = time.time()
        
        thread = threading.Thread(target=self._execute_task, args=(task_id,))
        self.running_tasks[task_id] = thread
        thread.start()
    
    def _execute_task(self, task_id: str) -> None:
        """Execute a task (placeholder - override in subclass)"""
        task = self.dependency_graph.tasks[task_id]
        
        try:
            # Placeholder execution - implement actual task execution here
            print(f"Executing task: {task.description}")
            time.sleep(1)  # Simulate work
            
            # Mark as completed
            task.status = TaskStatus.COMPLETED
            task.completion_time = time.time()
            task.result = f"Completed: {task.description}"
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completion_time = time.time()
            print(f"Task failed: {task.description} - {e}")
    
    def get_status(self) -> Dict:
        """Get current scheduler status"""
        with self.lock:
            status_counts = defaultdict(int)
            for task in self.dependency_graph.tasks.values():
                status_counts[task.status.value] += 1
                
            return {
                'total_tasks': len(self.dependency_graph.tasks),
                'running_tasks': len(self.running_tasks),
                'status_counts': dict(status_counts),
                'dependency_graph': self.dependency_graph.get_visualization()
            }
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """Wait for all tasks to complete"""
        start_time = time.time()
        
        while True:
            with self.lock:
                incomplete_tasks = [
                    task for task in self.dependency_graph.tasks.values()
                    if task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.BLOCKED]
                ]
                
                if not incomplete_tasks:
                    return True
                    
            if timeout and (time.time() - start_time) > timeout:
                return False
                
            time.sleep(0.1)

# Example usage and integration helper
class GrindTaskScheduler(TaskScheduler):
    """Grind-specific task scheduler with execution integration"""
    
    def __init__(self, grind_spawner, max_concurrent_tasks: int = 4):
        super().__init__(max_concurrent_tasks)
        self.grind_spawner = grind_spawner
    
    def _execute_task(self, task_id: str) -> None:
        """Execute grind task using spawner"""
        task = self.dependency_graph.tasks[task_id]
        
        try:
            # Extract task details from metadata
            task_config = task.metadata.get('grind_config', {})
            
            # Execute via grind spawner
            result = self.grind_spawner.execute_task(task_config)
            
            task.status = TaskStatus.COMPLETED
            task.completion_time = time.time()
            task.result = result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completion_time = time.time()

def integrate_with_grind_spawner():
    """Integration example for grind_spawner.py"""
    integration_code = '''
# Add to grind_spawner.py:

from task_scheduler import GrindTaskScheduler, Task

class EnhancedGrindSpawner:
    def __init__(self):
        # ... existing init code ...
        self.task_scheduler = GrindTaskScheduler(self, max_concurrent_tasks=4)
        self.task_scheduler.start_scheduler()
    
    def schedule_tasks_with_dependencies(self, task_list):
        """Schedule multiple tasks with dependency detection"""
        
        # Add all tasks first
        for i, task_config in enumerate(task_list):
            task_id = f"task_{i}"
            description = task_config.get('description', f"Task {i}")
            priority = task_config.get('priority', 0)
            
            task = self.task_scheduler.add_task(
                task_id=task_id,
                description=description,
                priority=priority
            )
            task.metadata['grind_config'] = task_config
        
        # Wait for completion
        success = self.task_scheduler.wait_for_completion(timeout=3600)
        
        return self.task_scheduler.get_status()
'''
    
    return integration_code

if __name__ == "__main__":
    # Demo usage
    scheduler = TaskScheduler(max_concurrent_tasks=2)
    
    # Add some demo tasks
    scheduler.add_task("setup", "Initialize project setup")
    scheduler.add_task("download", "Download required data files")  
    scheduler.add_task("process", "Process data after download", explicit_dependencies=["download"])
    scheduler.add_task("analyze", "Analyze processed data requires setup", explicit_dependencies=["setup"])
    scheduler.add_task("report", "Generate report after analysis and processing")
    
    # Start scheduler
    scheduler.start_scheduler()
    
    # Wait and show status
    time.sleep(5)
    print(json.dumps(scheduler.get_status(), indent=2))
    
    scheduler.stop_scheduler()