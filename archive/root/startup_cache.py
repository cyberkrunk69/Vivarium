import pickle
import os

class StartupCache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
        self.save_cache()

if __name__ == "__main__":
    cache = StartupCache('startup_cache.pkl')
    print(cache.get('knowledge_graph'))
import functools
import threading

def lazy_cache(func):
    """Cache the result of a function after first successful call.
    Thread‑safe for use during startup."""
    lock = threading.Lock()
    cached = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'result' in cached:
            return cached['result']
        with lock:
            if 'result' in cached:   # double‑checked locking
                return cached['result']
            result = func(*args, **kwargs)
            cached['result'] = result
            return result
    return wrapper