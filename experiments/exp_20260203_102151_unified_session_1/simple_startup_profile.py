#!/usr/bin/env python3
"""
Simple startup time profiler - just measure actual operations
"""
import time
import os
import sys
import json
from pathlib import Path

def measure_startup():
    """Measure actual grind_spawner startup time"""
    print("=" * 60)
    print("  STARTUP TIME MEASUREMENT")
    print("=" * 60)

    # Change to parent directory
    parent_dir = Path(__file__).parent.parent
    os.chdir(parent_dir)

    # Measure full startup time
    start_total = time.time()

    # Test minimal grind_spawner import/init
    cmd = [
        sys.executable, "-c",
        """
import time
start = time.time()
import sys
sys.path.append('.')

# Time individual operations
import_start = time.time()
from grind_spawner import GrindSession
import_time = time.time() - import_start

init_start = time.time()
session = GrindSession(1, "haiku", 0.01, ".", "test task")
init_time = time.time() - init_start

total_time = time.time() - start

print(f"IMPORT_TIME:{import_time:.3f}")
print(f"INIT_TIME:{init_time:.3f}")
print(f"TOTAL_TIME:{total_time:.3f}")
"""
    ]

    import subprocess
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'IMPORT_TIME:' in line:
                    import_time = float(line.split(':')[1])
                    print(f"  Import time:     {import_time*1000:6.1f}ms")
                elif 'INIT_TIME:' in line:
                    init_time = float(line.split(':')[1])
                    print(f"  Init time:       {init_time*1000:6.1f}ms")
                elif 'TOTAL_TIME:' in line:
                    total_time = float(line.split(':')[1])
                    print(f"  Total time:      {total_time*1000:6.1f}ms")
        else:
            print(f"  ERROR: {result.stderr}")
            return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

    return total_time

def analyze_files():
    """Analyze file sizes that might affect startup"""
    print("\n  FILE SIZE ANALYSIS:")
    print("-" * 40)

    files_to_check = [
        "knowledge_graph.json",
        "failure_patterns.json",
        "demos.json",
        "learned_lessons.json",
        "grind_tasks.json"
    ]

    total_size = 0
    for filename in files_to_check:
        filepath = Path(filename)
        if filepath.exists():
            size = filepath.stat().st_size
            total_size += size
            print(f"  {filename:20s}: {size:8d} bytes ({size/1024:.1f} KB)")
        else:
            print(f"  {filename:20s}: Not found")

    print(f"  {'Total data':20s}: {total_size:8d} bytes ({total_size/1024:.1f} KB)")

    return total_size

def main():
    startup_time = measure_startup()
    file_size = analyze_files()

    if startup_time:
        print("\n  OPTIMIZATION TARGETS:")
        print("-" * 40)

        if startup_time > 1.0:
            print(f"  1. Startup too slow ({startup_time*1000:.0f}ms) - target <500ms")

        if file_size > 100000:  # >100KB
            print(f"  2. Large data files ({file_size/1024:.1f}KB) - use lazy loading")

        print(f"  3. Knowledge graph should be loaded on-demand")
        print(f"  4. Safety checks can be deferred until execution")
        print(f"  5. File hashing can be cached/backgrounded")

if __name__ == "__main__":
    main()