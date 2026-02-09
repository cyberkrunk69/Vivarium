def detect_complexity(task_description: str) -> str:
    """
    Determine the appropriate Groq model for a given task description.

    SIMPLIFIED: Always returns groq/compound which auto-selects the best model
    based on task complexity internally.
    """
    # Groq Compound handles complexity detection internally
    # It routes to GPT-OSS 120B, Llama 4 Scout, or Llama 3.3 70B as needed
    return "groq/compound"
