import time
import atexit

_start_time = time.perf_counter()

def _log_startup_time():
    elapsed = (time.perf_counter() - _start_time) * 1000  # ms
    print(f"[STARTUP] Total elapsed time: {elapsed:.1f} ms")

atexit.register(_log_startup_time)