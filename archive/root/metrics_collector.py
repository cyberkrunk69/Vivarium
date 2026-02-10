import time
import logging

def measure_execution(func):
    """
    Decorator that logs execution time and returns a tuple
    (result, elapsed_seconds) for later aggregation.
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logging.info("Executed %s in %.4f seconds", func.__name__, elapsed)
        return result, elapsed
    return wrapper