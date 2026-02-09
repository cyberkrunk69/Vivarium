from typing import List, Dict

# Ordered from smallest to largest capability
_MODEL_CATALOG: List[Dict] = [
    {"name": "gpt-3.5-turbo", "max_complexity": 40},
    {"name": "gpt-4", "max_complexity": 80},
    {"name": "gpt-4-32k", "max_complexity": 120},
]

def select_model(complexity: int) -> str:
    """
    Choose the smallest model that can handle the given complexity.
    If complexity exceeds all entries, return the most capable model.
    """
    for entry in _MODEL_CATALOG:
        if complexity <= entry["max_complexity"]:
            return entry["name"]
    return _MODEL_CATALOG[-1]["name"]
class ModelSelector:
    """
    Maps a complexity tier to a concrete model identifier.
    The mapping can be overridden by editing `_model_map` or by loading
    a configuration file in the future.
    """
    _model_map = {
        'low':    'gpt-3.5-turbo',
        'medium': 'gpt-4',
        'high':   'gpt-4-32k'   # or any larger, more capable model you provision
    }

    @classmethod
    def select_model(cls, complexity: str) -> str:
        """Return the model name for the given complexity tier."""
        return cls._model_map.get(complexity, 'gpt-3.5-turbo')