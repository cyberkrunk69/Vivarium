class ModelDescriptor:
    """Lightweight container for model metadata."""
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id


class ModelPool:
    """
    Holds references to the available LLM back‑ends.
    Extend this class to load models from config files or environment vars.
    """
    def __init__(self):
        # Example placeholders – replace with real model identifiers.
        self.default = ModelDescriptor(name="small‑model", id="gpt-3.5-turbo")
        self.medium = ModelDescriptor(name="medium‑model", id="gpt-4")
        self.large = ModelDescriptor(name="large‑model", id="gpt-4-32k")

    def get_default_model(self):
        return self.default

    def get_medium_model(self):
        return self.medium

    def get_largest_model(self):
        return self.large