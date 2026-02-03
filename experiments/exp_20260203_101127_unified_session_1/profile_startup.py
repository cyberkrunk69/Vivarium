#!/usr/bin/env python3
"""
Startup profiler for grind_spawner_groq.py
Measures timing of each initialization component.
"""

import time
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def time_operation(name, operation):
    """Time a single operation and return elapsed time."""
    print(f"Timing {name}...", end=" ", flush=True)
    start = time.perf_counter()
    try:
        result = operation()
        elapsed = time.perf_counter() - start
        print(f"{elapsed:.3f}s")
        return elapsed, result, None
    except Exception as e:
        elapsed = time.perf_counter() - start
        print(f"FAILED in {elapsed:.3f}s - {e}")
        return elapsed, None, str(e)

def profile_imports():
    """Profile import timing."""
    results = {}

    # Profile each major import group
    results['groq_client'] = time_operation("groq_client imports",
        lambda: __import__('groq_client'))

    results['safety_sandbox'] = time_operation("safety_sandbox import",
        lambda: __import__('safety_sandbox'))

    results['safety_gateway'] = time_operation("safety_gateway import",
        lambda: __import__('safety_gateway'))

    results['safety_sanitize'] = time_operation("safety_sanitize import",
        lambda: __import__('safety_sanitize'))

    results['safety_killswitch'] = time_operation("safety_killswitch import",
        lambda: __import__('safety_killswitch'))

    results['safety_network'] = time_operation("safety_network import",
        lambda: __import__('safety_network'))

    results['safety_constitutional'] = time_operation("safety_constitutional import",
        lambda: __import__('safety_constitutional'))

    results['experiments_sandbox'] = time_operation("experiments_sandbox import",
        lambda: __import__('experiments_sandbox'))

    results['roles'] = time_operation("roles import",
        lambda: __import__('roles'))

    results['knowledge_graph'] = time_operation("knowledge_graph import",
        lambda: __import__('knowledge_graph'))

    results['groq_code_extractor'] = time_operation("groq_code_extractor import",
        lambda: __import__('groq_code_extractor'))

    results['git_automation'] = time_operation("git_automation import",
        lambda: __import__('git_automation'))

    return results

def profile_initialization():
    """Profile initialization timing after imports."""
    from safety_sandbox import initialize_sandbox
    from safety_gateway import SafetyGateway
    from knowledge_graph import KnowledgeGraph
    from groq_client import get_groq_engine
    from safety_constitutional import ConstitutionalChecker
    from experiments_sandbox import ExperimentSandbox, create_experiment
    from utils import read_json

    results = {}
    workspace = Path.cwd()

    # Sandbox initialization
    results['sandbox_init'] = time_operation("sandbox initialization",
        lambda: initialize_sandbox(str(workspace)))

    # Safety gateway
    results['safety_gateway_init'] = time_operation("safety gateway init",
        lambda: SafetyGateway(workspace=workspace))

    # Knowledge graph loading
    results['kg_init'] = time_operation("knowledge graph init",
        lambda: KnowledgeGraph())

    def load_kg():
        kg = KnowledgeGraph()
        kg_file = workspace / "knowledge_graph.json"
        if kg_file.exists():
            kg.load_json(str(kg_file))
        return kg

    results['kg_load'] = time_operation("knowledge graph load", load_kg)

    # Groq engine
    results['groq_engine'] = time_operation("groq engine init",
        lambda: get_groq_engine())

    # Constitutional checker
    results['constitutional_checker'] = time_operation("constitutional checker init",
        lambda: ConstitutionalChecker(constraints_path=str(workspace / "SAFETY_CONSTRAINTS.json")))

    # Experiment sandbox
    results['experiment_sandbox'] = time_operation("experiment sandbox init",
        lambda: ExperimentSandbox())

    # File hash capture (simulated)
    def capture_hashes():
        time.sleep(0.1)  # Simulate file system scanning
        return "hashes_captured"

    results['file_hashes'] = time_operation("file hash capture", capture_hashes)

    return results

def main():
    print("=" * 60)
    print("  GRIND SPAWNER STARTUP PROFILER")
    print("=" * 60)

    total_start = time.perf_counter()

    print("\n1. IMPORT TIMING")
    print("-" * 30)
    import_results = profile_imports()

    print("\n2. INITIALIZATION TIMING")
    print("-" * 30)
    init_results = profile_initialization()

    total_elapsed = time.perf_counter() - total_start

    print("\n" + "=" * 60)
    print("  SUMMARY REPORT")
    print("=" * 60)

    # Calculate totals
    import_total = sum(r[0] for r in import_results.values() if r[1] is not None)
    init_total = sum(r[0] for r in init_results.values() if r[1] is not None)

    print(f"Total startup time:     {total_elapsed:.3f}s")
    print(f"Import time:           {import_total:.3f}s ({import_total/total_elapsed*100:.1f}%)")
    print(f"Initialization time:   {init_total:.3f}s ({init_total/total_elapsed*100:.1f}%)")

    print("\nSLOWEST OPERATIONS:")
    all_ops = [(name, timing[0]) for name, timing in {**import_results, **init_results}.items() if timing[1] is not None]
    all_ops.sort(key=lambda x: x[1], reverse=True)

    for name, elapsed in all_ops[:10]:
        print(f"  {name:<25} {elapsed:.3f}s")

    print("\nFAILED OPERATIONS:")
    failures = [(name, timing[2]) for name, timing in {**import_results, **init_results}.items() if timing[2] is not None]
    for name, error in failures:
        print(f"  {name}: {error}")

if __name__ == "__main__":
    main()