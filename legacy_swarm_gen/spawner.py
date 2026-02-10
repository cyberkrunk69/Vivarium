import json
from retrieval_api import retrieve_lessons, get_lessons

def spawn_task(task_text):
    domain = retrieve_lessons(task_text)
    if domain:
        lessons = get_lessons(domain)
        # Inject lessons into prompt context
        print(f"Injecting {len(lessons)} lessons into prompt context")
    else:
        print("No lessons found for this task")

def main():
    task_text = input("Enter task text: ")
    spawn_task(task_text)

if __name__ == "__main__":
    main()