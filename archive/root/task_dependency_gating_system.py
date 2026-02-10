import json
import threading

class Task:
    def __init__(self, task_id, dependencies):
        self.task_id = task_id
        self.dependencies = dependencies

    def execute(self):
        # Execute the task
        print(f"Task {self.task_id} executed")

class ParallelExecutionScheduler:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.thread_pool = []

    def execute_task(self, task):
        # Execute task in a separate thread
        thread = threading.Thread(target=task.execute)
        self.thread_pool.append(thread)
        thread.start()

    def wait_for_completion(self):
        # Wait for all threads to complete
        for thread in self.thread_pool:
            thread.join()

class CompletionDetector:
    def __init__(self):
        self.completed_tasks = []

    def task_completed(self, task):
        self.completed_tasks.append(task)

    def get_completed_tasks(self):
        return self.completed_tasks

class DynamicReScheduler:
    def __init__(self, dependency_graph):
        self.dependency_graph = dependency_graph

    def re_schedule(self, completed_task):
        # Re-schedule tasks that depend on the completed task
        for task, dependencies in self.dependency_graph.items():
            if completed_task in dependencies:
                # Remove the completed task from the dependencies
                dependencies.remove(completed_task)
                # If the task has no more dependencies, execute it
                if not dependencies:
                    # Execute the task
                    pass

def main():
    # Create tasks
    task_a = Task("task_a", ["task_b", "task_c"])
    task_b = Task("task_b", ["task_d"])
    task_c = Task("task_c", [])
    task_d = Task("task_d", [])

    # Create dependency graph
    dependency_graph = {
        "task_a": ["task_b", "task_c"],
        "task_b": ["task_d"],
        "task_c": [],
        "task_d": []
    }

    # Create parallel execution scheduler
    scheduler = ParallelExecutionScheduler(4)

    # Execute tasks
    scheduler.execute_task(task_a)
    scheduler.execute_task(task_b)
    scheduler.execute_task(task_c)
    scheduler.execute_task(task_d)

    # Wait for completion
    scheduler.wait_for_completion()

if __name__ == "__main__":
    main()