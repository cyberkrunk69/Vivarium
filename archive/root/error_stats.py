# Simple in‑memory counters for error categories
_error_counts = {}

def increment_error_count(category: str):
    _error_counts[category] = _error_counts.get(category, 0) + 1

def get_error_counts():
    return dict(_error_counts)