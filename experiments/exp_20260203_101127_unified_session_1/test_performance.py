#!/usr/bin/env python3
"""
Test performance comparison between original and optimized spawner.
"""

import time
import subprocess
import sys
from pathlib import Path

def test_spawner_performance(spawner_path, name, extra_args=None):
    """Test startup time of a spawner."""
    print(f"\nTesting {name}:")
    print(f"  Path: {spawner_path}")

    if not spawner_path.exists():
        print(f"  ERROR: File not found")
        return None

    args = [sys.executable, str(spawner_path), "--help"]
    if extra_args:
        args.extend(extra_args)

    # Time 3 runs for accuracy
    times = []
    for i in range(3):
        start = time.perf_counter()
        try:
            result = subprocess.run(args, capture_output=True, text=True,
                                  cwd=spawner_path.parent.parent.parent, timeout=30)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"  Run {i+1}: {elapsed:.3f}s (code: {result.returncode})")

            if result.returncode != 0 and i == 0:
                print(f"  Error: {result.stderr[:200]}")

        except Exception as e:
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"  Run {i+1}: {elapsed:.3f}s (FAILED: {e})")

    if times:
        avg_time = sum(times) / len(times)
        print(f"  Average: {avg_time:.3f}s")
        return avg_time

    return None

def main():
    print("=" * 60)
    print("  SPAWNER PERFORMANCE COMPARISON")
    print("=" * 60)

    workspace = Path(__file__).parent.parent.parent

    # Test original spawner
    original_path = workspace / "grind_spawner_groq.py"
    original_time = test_spawner_performance(original_path, "Original Spawner")

    # Test optimized spawner
    optimized_path = Path(__file__).parent / "grind_spawner_optimized.py"
    optimized_time = test_spawner_performance(optimized_path, "Optimized Spawner")

    # Test optimized spawner with --unsafe
    unsafe_time = test_spawner_performance(optimized_path, "Optimized Spawner (--unsafe)", ["--unsafe"])

    print("\n" + "=" * 60)
    print("  PERFORMANCE SUMMARY")
    print("=" * 60)

    if original_time and optimized_time:
        improvement = ((original_time - optimized_time) / original_time) * 100
        print(f"Original startup time:     {original_time:.3f}s")
        print(f"Optimized startup time:    {optimized_time:.3f}s")
        print(f"Improvement:               {improvement:.1f}% faster")

        if unsafe_time:
            unsafe_improvement = ((original_time - unsafe_time) / original_time) * 100
            print(f"Unsafe mode startup time:  {unsafe_time:.3f}s")
            print(f"Unsafe improvement:        {unsafe_improvement:.1f}% faster")

    print("\nOPTIMIZATIONS APPLIED:")
    print("  1. Lazy import of safety modules")
    print("  2. Cached knowledge graph loading")
    print("  3. Deferred non-critical initialization")
    print("  4. Cached network scans and file hashes")
    print("  5. Optional safety bypass (--unsafe)")

if __name__ == "__main__":
    main()