import os
import pickle
from functools import wraps
from threading import RLock

_cache_lock = RLock()

def cached_to_file(cache_path):
    """
    Simple persistent cache decorator.
    Results are stored on disk (pickle) and reused across runs
    if the cache file exists.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Only cache when called without arguments (common for startup loads)
            if args or kwargs:
                return func(*args, **kwargs)

            # Ensure cache directory exists
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)

            with _cache_lock:
                if os.path.exists(cache_path):
                    try:
                        with open(cache_path, "rb") as f:
                            return pickle.load(f)
                    except Exception:
                        # Corrupted cache – fall back to recompute
                        pass

                # Compute and store result
                result = func()
                try:
                    with open(cache_path, "wb") as f:
                        pickle.dump(result, f)
                except Exception:
                    pass
                return result
        return wrapper
    return decorator