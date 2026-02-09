import json

def integrate_knowledge_packs(spawner, task_text):
    knowledge_packs = retrieve_knowledge_packs(task_text)

    # Inject knowledge packs into prompt context
    spawner.prompt_context.update(knowledge_packs)

# Example usage:
spawner = {}  # Initialize spawner object
task_text = "Use model-specific prompting patterns for optimal results"
integrate_knowledge_packs(spawner, task_text)
print(spawner.prompt_context)