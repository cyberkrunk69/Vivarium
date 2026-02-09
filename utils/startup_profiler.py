import time
import logging
from functools import wraps

logger = logging.getLogger("startup_profiler")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def profile_startup(func):
    """Decorator to log the execution time of startup‑related functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("Startup step %s completed in %.3f s", func.__name__, elapsed)
        return result
    return wrapper