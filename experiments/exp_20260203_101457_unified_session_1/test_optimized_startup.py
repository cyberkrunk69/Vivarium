#!/usr/bin/env python3
"""
Test script to benchmark the optimized grind spawner startup performance.
"""

import time
import sys
import subprocess
import json
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent.parent

def time_import(module_path):
    """Time how long it takes to import a Python module."""
    start = time.perf_counter()

    result = subprocess.run([
        sys.executable, '-c', f'import sys; sys.path.insert(0, "{WORKSPACE}"); import {module_path}'
    ], capture_output=True, cwd=WORKSPACE)

    duration = time.perf_counter() - start
    return duration, result.returncode == 0

def benchmark_startup():
    """Benchmark startup times."""
    print("=" * 60)
    print("  STARTUP OPTIMIZATION BENCHMARK")
    print("=" * 60)

    results = {}

    # Test original spawner
    print("[TEST] Original grind_spawner_unified...")
    duration, success = time_import("grind_spawner_unified")
    results["original"] = {"duration_ms": duration * 1000, "success": success}
    print(f"  Duration: {duration*1000:.2f}ms, Success: {success}")

    # Test optimized spawner
    print("[TEST] Optimized grind_spawner...")
    opt_path = Path(__file__).parent / "grind_spawner_optimized.py"
    if opt_path.exists():
        start = time.perf_counter()
        result = subprocess.run([
            sys.executable, str(opt_path), '--help'
        ], capture_output=True, cwd=WORKSPACE)
        duration = time.perf_counter() - start
        success = result.returncode == 0
        results["optimized"] = {"duration_ms": duration * 1000, "success": success}
        print(f"  Duration: {duration*1000:.2f}ms, Success: {success}")
    else:
        print("  Optimized spawner not found")
        results["optimized"] = {"duration_ms": -1, "success": False}

    # Calculate improvement
    if results["original"]["success"] and results["optimized"]["success"]:
        improvement = ((results["original"]["duration_ms"] - results["optimized"]["duration_ms"])
                      / results["original"]["duration_ms"]) * 100
        print(f"\n[RESULT] Improvement: {improvement:.1f}% faster")
        results["improvement_percent"] = improvement
    else:
        print("\n[RESULT] Could not calculate improvement due to errors")
        results["improvement_percent"] = None

    print("=" * 60)

    # Save results
    benchmark_file = Path(__file__).parent / "startup_benchmark.json"
    with open(benchmark_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Benchmark saved to: {benchmark_file}")

if __name__ == "__main__":
    benchmark_startup()