# grind_spawner.py
def execute_task(task_text, pack_manager):
    relevant_packs = get_relevant_packs(task_text)
    # Execute the task with the relevant packs