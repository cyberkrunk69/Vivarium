#!/usr/bin/env python3
"""
Startup Performance Profiler for grind_spawner.py

Profiles the startup time of grind_spawner to identify bottlenecks.
"""

import time
import cProfile
import pstats
import io
import sys
import json
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

# Monkey patch imports to profile them
original_import = __import__
import_times = {}

def profile_import(name, *args, **kwargs):
    """Profile import time for each module."""
    start = time.time()
    result = original_import(name, *args, **kwargs)
    elapsed = time.time() - start

    if elapsed > 0.001:  # Only track imports > 1ms
        import_times[name] = elapsed

    return result

# Replace built-in import with profiling version
import builtins
builtins.__import__ = profile_import

@contextmanager
def timer(operation_name):
    """Context manager to time operations."""
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"[PROFILE] {operation_name}: {elapsed:.3f}s")

def profile_startup():
    """Profile the startup sequence of grind_spawner."""
    print("=" * 60)
    print("GRIND SPAWNER STARTUP PROFILER")
    print("=" * 60)

    startup_start = time.time()

    # Profile the main imports and initialization
    with timer("Total startup time"):
        with timer("Core imports"):
            import argparse
            import json
            import subprocess
            import threading
            import os
            import hashlib
            from pathlib import Path
            from concurrent.futures import ThreadPoolExecutor
            from datetime import datetime

        with timer("Role system imports"):
            try:
                from roles import RoleType, decompose_task, get_role, get_role_chain, format_handoff, RoleExecutor
            except ImportError as e:
                print(f"[PROFILE] Warning: Could not import roles: {e}")

        with timer("Memory and knowledge imports"):
            try:
                from memory_synthesis import MemorySynthesis, should_synthesize
                from knowledge_graph import KnowledgeGraph, KnowledgeNode, NodeType
            except ImportError as e:
                print(f"[PROFILE] Warning: Could not import memory/knowledge: {e}")

        with timer("Safety system imports"):
            try:
                from safety_sandbox import initialize_sandbox
                from failure_patterns import FailurePatternDetector
                from safety_network import scan_for_network_access
                from safety_constitutional import ConstitutionalChecker as ConstitutionalCheckerStandalone
                from safety_gateway import SafetyGateway
                from safety_sanitize import sanitize_task, detect_injection_attempt
                from safety_killswitch import get_kill_switch, get_circuit_breaker
            except ImportError as e:
                print(f"[PROFILE] Warning: Could not import safety systems: {e}")

        with timer("Skills and performance tracking"):
            try:
                from skills.skill_registry import retrieve_skill
                from critic import CriticAgent
                from performance_tracker import PerformanceTracker
            except ImportError as e:
                print(f"[PROFILE] Warning: Could not import skills/performance: {e}")

        with timer("Utility imports"):
            try:
                from utils import read_json, write_json
                from logger import json_log
                from config import validate_config
                from lesson_recorder import (
                    record_prompt_optimization_lesson,
                    record_error_categorization_lesson,
                    record_role_decomposition_lesson,
                    record_reflection_trigger_lesson,
                    record_skill_integration_lesson,
                    record_self_verification_lesson,
                    record_adaptive_complexity_lesson,
                    record_reflection_automation_lesson,
                    record_critic_feedback_lesson
                )
                from prompt_optimizer import collect_demonstrations, get_relevant_demonstrations, optimize_prompt
                from message_pool import get_message_pool
                from skill_extractor import extract_skill_from_session, auto_register_skill
                from connect_tracker_to_suggester import post_wave_analysis
                from context_builder import ContextBuilder
                from multi_path_executor import MultiPathExecutor, ExecutionPath, PathResult
                from cost_tracker import get_cost_tracker
            except ImportError as e:
                print(f"[PROFILE] Warning: Could not import utilities: {e}")

        # Profile startup operations that would happen during GrindSession creation
        workspace = Path(__file__).parent
        cache_dir = workspace / ".grind_cache"

        with timer("Cache directory creation"):
            cache_dir.mkdir(exist_ok=True)

        with timer("Config validation"):
            try:
                validate_config()
            except Exception as e:
                print(f"[PROFILE] Config validation failed: {e}")

        with timer("Sandbox initialization"):
            try:
                initialize_sandbox(str(workspace))
            except Exception as e:
                print(f"[PROFILE] Sandbox initialization failed: {e}")

        # Simulate expensive operations that happen during startup
        with timer("Knowledge Graph initialization"):
            try:
                kg = KnowledgeGraph()
                kg_file = workspace / "knowledge_graph.json"
                if kg_file.exists():
                    kg.load_json(str(kg_file))
                    print(f"[PROFILE] KG loaded with {len(kg.nodes)} nodes")
                else:
                    print("[PROFILE] KG file not found, would populate from codebase")
            except Exception as e:
                print(f"[PROFILE] KG initialization failed: {e}")

        with timer("Failure Pattern Detector initialization"):
            try:
                detector = FailurePatternDetector(workspace=workspace)
                print("[PROFILE] Failure detector initialized")
            except Exception as e:
                print(f"[PROFILE] Failure detector initialization failed: {e}")

        with timer("Safety Gateway initialization"):
            try:
                gateway = SafetyGateway(workspace=workspace)
                print("[PROFILE] Safety gateway initialized")
            except Exception as e:
                print(f"[PROFILE] Safety gateway initialization failed: {e}")

        with timer("Demonstration collection (cached)"):
            try:
                from grind_spawner import StartupCache
                cache = StartupCache(cache_dir)
                cached_demos = cache.get_cached("demonstrations", workspace)
                if cached_demos:
                    print(f"[PROFILE] Found cached demonstrations: {len(cached_demos)} items")
                else:
                    print("[PROFILE] No cached demonstrations, would collect from logs")
            except Exception as e:
                print(f"[PROFILE] Demonstration collection failed: {e}")

    total_time = time.time() - startup_start

    print("\n" + "=" * 60)
    print("IMPORT TIMING BREAKDOWN")
    print("=" * 60)

    # Sort imports by time
    sorted_imports = sorted(import_times.items(), key=lambda x: x[1], reverse=True)
    for name, elapsed in sorted_imports[:10]:  # Top 10 slowest imports
        print(f"[IMPORT] {name:30s}: {elapsed:.3f}s")

    print(f"\nTotal tracked import time: {sum(import_times.values()):.3f}s")
    print(f"Total startup time: {total_time:.3f}s")

    return {
        "total_startup_time": total_time,
        "import_times": import_times,
        "timestamp": datetime.now().isoformat(),
        "top_slow_imports": sorted_imports[:10]
    }

def save_profile_results(results):
    """Save profiling results to a JSON file."""
    output_file = Path(__file__).parent / "startup_profile_results.json"

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[PROFILE] Results saved to {output_file}")
    return output_file

if __name__ == "__main__":
    print("Profiling grind_spawner startup...")

    # Enable detailed profiling
    profiler = cProfile.Profile()
    profiler.enable()

    # Run the startup profiling
    results = profile_startup()

    profiler.disable()

    # Save results
    output_file = save_profile_results(results)

    # Generate detailed cProfile report
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(20)  # Top 20 functions

    profile_report = s.getvalue()
    print("\n" + "=" * 60)
    print("TOP 20 SLOWEST FUNCTIONS")
    print("=" * 60)
    print(profile_report)

    # Save detailed profile to file
    profile_file = Path(__file__).parent / "startup_profile_detailed.txt"
    with open(profile_file, 'w') as f:
        f.write(profile_report)

    print(f"\n[PROFILE] Detailed profile saved to {profile_file}")

    # Summary recommendations
    print("\n" + "=" * 60)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("=" * 60)

    if results["total_startup_time"] > 5.0:
        print("❌ SLOW: Startup time > 5s - significant optimization needed")
    elif results["total_startup_time"] > 2.0:
        print("⚠️  MODERATE: Startup time > 2s - some optimization recommended")
    else:
        print("✅ FAST: Startup time < 2s - minimal optimization needed")

    # Identify specific bottlenecks
    top_imports = results["top_slow_imports"]
    if top_imports:
        slowest_import, slowest_time = top_imports[0]
        if slowest_time > 1.0:
            print(f"\n🐌 Slowest import: {slowest_import} ({slowest_time:.3f}s)")
            print("   Consider lazy loading this module")

    total_import_time = sum(results["import_times"].values())
    if total_import_time > results["total_startup_time"] * 0.7:
        print(f"\n📦 Import overhead: {total_import_time:.3f}s ({total_import_time/results['total_startup_time']*100:.1f}%)")
        print("   Consider deferring non-critical imports")