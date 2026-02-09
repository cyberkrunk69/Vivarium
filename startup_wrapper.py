import time
import logging
from grind_spawner import main as spawner_main

logger = logging.getLogger("startup_total")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def run():
    start = time.perf_counter()
    spawner_main()
    elapsed = time.perf_counter() - start
    logger.info("Total grind spawner startup time: %.3f s", elapsed)

if __name__ == "__main__":
    run()