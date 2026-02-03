#!/usr/bin/env python3
"""
Profile grind spawner startup time to identify bottlenecks
"""
import time
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def time_operation(name, func, *args, **kwargs):
    """Time a single operation and return result + elapsed time"""
    start = time.time()
    try:
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed, None
    except Exception as e:
        elapsed = time.time() - start
        return None, elapsed, str(e)

def profile_imports():
    """Profile import times"""
    import_times = {}

    # Time individual imports
    start = time.time()
    import argparse
    import_times['argparse'] = time.time() - start

    start = time.time()
    import json
    import_times['json'] = time.time() - start

    start = time.time()
    import subprocess
    import_times['subprocess'] = time.time() - start

    start = time.time()
    from pathlib import Path
    import_times['pathlib'] = time.time() - start

    # Time heavy imports
    start = time.time()
    from roles import RoleType, decompose_task, get_role, get_role_chain
    import_times['roles'] = time.time() - start

    start = time.time()
    from knowledge_graph import KnowledgeGraph, KnowledgeNode, NodeType
    import_times['knowledge_graph'] = time.time() - start

    start = time.time()
    from failure_patterns import FailurePatternDetector
    import_times['failure_patterns'] = time.time() - start

    start = time.time()
    from safety_gateway import SafetyGateway
    import_times['safety_gateway'] = time.time() - start

    start = time.time()
    from safety_network import scan_for_network_access
    import_times['safety_network'] = time.time() - start

    start = time.time()
    from memory_synthesis import MemorySynthesis
    import_times['memory_synthesis'] = time.time() - start

    return import_times

def profile_grind_session_init():
    """Profile GrindSession.__init__ timing"""
    from grind_spawner import GrindSession

    session_init_times = {}

    # Mock parameters for profiling
    workspace = Path(__file__).parent.parent

    start = time.time()
    session = GrindSession(
        session_id=1,
        model="haiku",
        budget=0.01,
        workspace=workspace,
        task="Profile test task",
        max_total_cost=None,
        synthesis_interval=5,
        critic_mode=False
    )
    session_init_times['total'] = time.time() - start

    return session_init_times

def main():
    print("=" * 60)
    print("  GRIND SPAWNER STARTUP PROFILING")
    print("=" * 60)

    # Profile imports
    print("\n1. IMPORT PROFILING:")
    print("-" * 40)
    import_times = profile_imports()

    total_import_time = sum(import_times.values())
    for module, elapsed in sorted(import_times.items(), key=lambda x: x[1], reverse=True):
        print(f"  {module:20s}: {elapsed*1000:6.1f}ms")
    print(f"  {'TOTAL IMPORTS':20s}: {total_import_time*1000:6.1f}ms")

    # Profile GrindSession initialization
    print("\n2. GRIND SESSION INITIALIZATION:")
    print("-" * 40)
    try:
        session_times = profile_grind_session_init()
        for component, elapsed in session_times.items():
            print(f"  {component:20s}: {elapsed*1000:6.1f}ms")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Profile file operations
    print("\n3. FILE OPERATIONS:")
    print("-" * 40)
    workspace = Path(__file__).parent.parent

    # Knowledge graph loading
    kg_file = workspace / "knowledge_graph.json"
    if kg_file.exists():
        start = time.time()
        content = kg_file.read_text()
        read_time = time.time() - start
        print(f"  {'kg read':20s}: {read_time*1000:6.1f}ms ({len(content)} chars)")

        start = time.time()
        data = json.loads(content)
        parse_time = time.time() - start
        print(f"  {'kg parse':20s}: {parse_time*1000:6.1f}ms")

    # Failure patterns loading
    failure_file = workspace / "failure_patterns.json"
    if failure_file.exists():
        start = time.time()
        content = failure_file.read_text()
        elapsed = time.time() - start
        print(f"  {'failure patterns':20s}: {elapsed*1000:6.1f}ms")

    # Demo injection loading
    demos_file = workspace / "demos.json"
    if demos_file.exists():
        start = time.time()
        content = demos_file.read_text()
        elapsed = time.time() - start
        print(f"  {'demos':20s}: {elapsed*1000:6.1f}ms")

    print("\n4. STARTUP BOTTLENECK ANALYSIS:")
    print("-" * 40)
    print("  Top bottlenecks identified:")

    # Analyze and suggest optimizations
    bottlenecks = []

    if total_import_time > 0.1:  # >100ms
        bottlenecks.append(f"Heavy imports: {total_import_time*1000:.1f}ms")

    if 'knowledge_graph' in import_times and import_times['knowledge_graph'] > 0.05:
        bottlenecks.append(f"Knowledge graph import: {import_times['knowledge_graph']*1000:.1f}ms")

    if 'safety_gateway' in import_times and import_times['safety_gateway'] > 0.05:
        bottlenecks.append(f"Safety gateway import: {import_times['safety_gateway']*1000:.1f}ms")

    if len(bottlenecks) == 0:
        print("  No major bottlenecks detected (all operations < 50ms)")
    else:
        for i, bottleneck in enumerate(bottlenecks, 1):
            print(f"  {i}. {bottleneck}")

    print("\n5. OPTIMIZATION RECOMMENDATIONS:")
    print("-" * 40)
    print("  1. Use lazy loading for KnowledgeGraph")
    print("  2. Defer safety gateway initialization until needed")
    print("  3. Cache file hash operations between runs")
    print("  4. Move heavy imports to function-level")
    print("  5. Use background threads for non-critical operations")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()