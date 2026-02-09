from knowledge_packs import get_relevant_packs
from grind_spawner import GrindSpawner

class SpawnerWrapper:
    def __init__(self):
        self.spawner = GrindSpawner()

    def execute_task(self, task_text):
        relevant_packs = get_relevant_packs(task_text)
        print(f'Relevant packs: {relevant_packs}')
        # Inject relevant lessons into prompt
        prompt = task_text
        for pack in relevant_packs:
            for lesson in pack.lessons:
                prompt += f' {lesson}'
        self.spawner.execute_task(prompt)