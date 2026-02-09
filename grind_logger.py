def get_error_category_stats() -> dict:
    """Return a snapshot of error category counts."""
    # Return a plain dict copy to avoid external mutation
    return dict(ERROR_CATEGORY_COUNTER)