"""
Automated benchmark tracking utility.

Intended usage:
    python benchmark_tracker.py   # runs the full suite and updates history/report
"""

import subprocess
import sys
import os

def run_suite():
    # Execute the benchmark suite as a subprocess to capture stdout/stderr
    result = subprocess.run([sys.executable, "agi_benchmark_suite.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Benchmark suite failed:", result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    run_suite()