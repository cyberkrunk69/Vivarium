#!/usr/bin/env python3
"""
Real startup profiler - times actual grind spawner startup operations.
"""

import time
import subprocess
import sys
import os
from pathlib import Path

def time_startup_sequence():
    """Time the actual startup sequence by running spawner with --help."""
    print("=" * 60)
    print("  GRIND SPAWNER STARTUP TIMING")
    print("=" * 60)

    workspace = Path(__file__).parent.parent
    spawner_path = workspace / "grind_spawner_groq.py"

    print(f"Testing: {spawner_path}")

    # Time import and basic initialization with --help
    start_time = time.perf_counter()

    try:
        result = subprocess.run([
            sys.executable, str(spawner_path), "--help"
        ], capture_output=True, text=True, cwd=workspace, timeout=30)

        elapsed = time.perf_counter() - start_time

        print(f"\nStartup time: {elapsed:.3f}s")
        print(f"Return code: {result.returncode}")

        if result.returncode != 0:
            print(f"Error: {result.stderr}")

        return elapsed

    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start_time
        print(f"TIMEOUT after {elapsed:.3f}s")
        return elapsed

    except Exception as e:
        elapsed = time.perf_counter() - start_time
        print(f"EXCEPTION after {elapsed:.3f}s: {e}")
        return elapsed

def analyze_imports_in_spawner():
    """Analyze import structure in grind_spawner_groq.py."""
    print("\n" + "=" * 60)
    print("  IMPORT ANALYSIS")
    print("=" * 60)

    workspace = Path(__file__).parent.parent
    spawner_path = workspace / "grind_spawner_groq.py"

    try:
        with open(spawner_path, 'r') as f:
            content = f.read()

        imports = []
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if line.startswith('from ') or line.startswith('import '):
                if not line.startswith('#'):
                    imports.append((line_num, line))

        print(f"Found {len(imports)} import statements:")

        # Categorize imports
        safety_imports = []
        core_imports = []
        std_imports = []

        for line_num, imp in imports:
            if 'safety_' in imp or 'Safety' in imp:
                safety_imports.append((line_num, imp))
            elif any(module in imp for module in ['knowledge_graph', 'roles', 'groq_', 'git_automation']):
                core_imports.append((line_num, imp))
            else:
                std_imports.append((line_num, imp))

        print(f"\nStandard library ({len(std_imports)} imports):")
        for line_num, imp in std_imports[:5]:
            print(f"  L{line_num}: {imp}")
        if len(std_imports) > 5:
            print(f"  ... and {len(std_imports) - 5} more")

        print(f"\nSafety modules ({len(safety_imports)} imports):")
        for line_num, imp in safety_imports:
            print(f"  L{line_num}: {imp}")

        print(f"\nCore modules ({len(core_imports)} imports):")
        for line_num, imp in core_imports:
            print(f"  L{line_num}: {imp}")

        return safety_imports, core_imports, std_imports

    except Exception as e:
        print(f"Error analyzing imports: {e}")
        return [], [], []

def identify_optimization_opportunities():
    """Identify specific optimization opportunities."""
    print("\n" + "=" * 60)
    print("  OPTIMIZATION OPPORTUNITIES")
    print("=" * 60)

    opportunities = [
        {
            "area": "Safety Module Imports",
            "impact": "HIGH",
            "description": "6+ safety modules loaded on startup - can be lazy loaded",
            "solution": "Import safety modules only when creating sessions"
        },
        {
            "area": "Knowledge Graph Loading",
            "impact": "MEDIUM",
            "description": "KG loaded and parsed on every session init",
            "solution": "Cache loaded KG, only reload if file changed"
        },
        {
            "area": "File Hash Capture",
            "impact": "MEDIUM",
            "description": "Pre-hashes captured synchronously on startup",
            "solution": "Move to background thread or defer until needed"
        },
        {
            "area": "Network Isolation Scan",
            "impact": "LOW",
            "description": "Network scanning happens for every prompt",
            "solution": "Cache scan results for identical prompts"
        },
        {
            "area": "Demo Injection",
            "impact": "LOW",
            "description": "Demo patterns loaded from JSON on every session",
            "solution": "Load once and cache in memory"
        }
    ]

    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp['area']} ({opp['impact']} impact)")
        print(f"   Problem: {opp['description']}")
        print(f"   Solution: {opp['solution']}")
        print()

    return opportunities

def main():
    # Time current startup
    startup_time = time_startup_sequence()

    # Analyze import structure
    safety_imports, core_imports, std_imports = analyze_imports_in_spawner()

    # Identify optimization opportunities
    opportunities = identify_optimization_opportunities()

    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"Current startup time: {startup_time:.3f}s")
    print(f"Safety imports: {len(safety_imports)}")
    print(f"Core imports: {len(core_imports)}")
    print(f"Optimization opportunities: {len(opportunities)}")

    target_time = max(0.5, startup_time * 0.3)  # Aim for 70% reduction
    print(f"Target startup time: {target_time:.3f}s")

if __name__ == "__main__":
    main()