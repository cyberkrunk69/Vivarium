#!/usr/bin/env python3
"""
Startup performance profiler for grind_spawner.py
Measures time taken by different initialization components.
"""

import time
import cProfile
import io
import pstats
from pathlib import Path
import json
from datetime import datetime

def profile_imports():
    """Profile import time for all modules."""
    start = time.time()

    # Core imports (fast)
    import argparse
    import subprocess
    import sys
    import threading
    import os
    from concurrent.futures import ThreadPoolExecutor

    core_time = time.time() - start

    # Heavy imports (potentially slow)
    heavy_start = time.time()

    from resident_facets import decompose_task
    from prompt_optimizer import collect_demonstrations, get_relevant_demonstrations, optimize_prompt
    from memory_synthesis import MemorySynthesis, should_synthesize
    from message_pool import get_message_pool
    from skills.skill_registry import retrieve_skill
    from critic import CriticAgent
    from knowledge_graph import KnowledgeGraph, KnowledgeNode, NodeType
    from performance_tracker import PerformanceTracker
    from utils import read_json, write_json
    from logger import json_log
    from config import validate_config
    from lesson_recorder import record_prompt_optimization_lesson
    from safety_sandbox import initialize_sandbox
    from failure_patterns import FailurePatternDetector
    from skill_extractor import extract_skill_from_session, auto_register_skill
    from connect_tracker_to_suggester import post_wave_analysis
    from context_builder import ContextBuilder
    from multi_path_executor import MultiPathExecutor, ExecutionPath, PathResult
    from safety_network import scan_for_network_access
    from safety_constitutional import ConstitutionalChecker as ConstitutionalCheckerStandalone
    from safety_gateway import SafetyGateway
    from safety_sanitize import sanitize_task, detect_injection_attempt
    from safety_killswitch import get_kill_switch, get_circuit_breaker
    from cost_tracker import get_cost_tracker

    heavy_time = time.time() - heavy_start
    total_time = time.time() - start

    return {
        "core_imports": core_time,
        "heavy_imports": heavy_time,
        "total_imports": total_time
    }

def profile_grind_session_init():
    """Profile GrindSession initialization."""
    workspace = Path(__file__).parent

    # Time each major component
    times = {}

    # Mock initialization steps from GrindSession.__init__
    start = time.time()

    # Task sanitization
    sanitize_start = time.time()
    from safety_sanitize import sanitize_task, detect_injection_attempt
    task_dict = {"task": "Test optimization task"}
    sanitized = sanitize_task(task_dict)
    detect_injection_attempt("Test optimization task")
    times["task_sanitization"] = time.time() - sanitize_start

    # Task decomposition (resident facets)
    decomp_start = time.time()
    task_decomposition = decompose_task(
        "Test optimization task",
        resident_id="resident_profile",
        identity_id="identity_profile",
    )
    times["task_decomposition"] = time.time() - decomp_start

    # Performance tracker
    perf_start = time.time()
    from performance_tracker import PerformanceTracker
    perf_tracker = PerformanceTracker(workspace)
    times["performance_tracker"] = time.time() - perf_start

    # Knowledge Graph loading
    kg_start = time.time()
    from knowledge_graph import KnowledgeGraph
    kg = KnowledgeGraph()
    kg_file = workspace / "knowledge_graph.json"
    if kg_file.exists():
        kg.load_json(str(kg_file))
    else:
        # This is expensive - populating from codebase
        kg.populate_from_codebase(str(workspace))
    times["knowledge_graph"] = time.time() - kg_start

    # Failure pattern detector
    failure_start = time.time()
    from failure_patterns import FailurePatternDetector
    failure_detector = FailurePatternDetector(workspace=workspace)
    times["failure_detector"] = time.time() - failure_start

    # Safety gateway
    safety_start = time.time()
    from safety_gateway import SafetyGateway
    safety_gateway = SafetyGateway(workspace=workspace)
    times["safety_gateway"] = time.time() - safety_start

    times["total_init"] = time.time() - start

    return times

def profile_prompt_generation():
    """Profile prompt generation performance."""
    from resident_facets import decompose_task
    from context_builder import ContextBuilder
    from failure_patterns import FailurePatternDetector
    from prompt_optimizer import collect_demonstrations, get_relevant_demonstrations

    workspace = Path(__file__).parent
    task = "Test optimization task"

    start = time.time()
    times = {}

    # Task decomposition (resident facets)
    decomp_start = time.time()
    task_decomposition = decompose_task(
        task,
        resident_id="resident_profile",
        identity_id="identity_profile",
    )
    times["decomposition"] = time.time() - decomp_start

    # Context building (expensive)
    context_start = time.time()
    context_builder = ContextBuilder(workspace)
    unified_context = context_builder.add_skills(task, top_k=3) \
                                   .add_lessons(task, top_k=3) \
                                   .add_kg_context(task, depth=2) \
                                   .build(log_injection=True)
    times["context_building"] = time.time() - context_start

    # Failure warnings
    failure_start = time.time()
    failure_detector = FailurePatternDetector(workspace=workspace)
    failure_warning = failure_detector.generate_warning_prompt(task, {
        "complexity": task_decomposition.get("complexity", "unknown"),
        "complexity_score": 0.5
    })
    times["failure_warnings"] = time.time() - failure_start

    # Demonstrations (very expensive)
    demo_start = time.time()
    logs_dir = workspace / "grind_logs"
    all_demonstrations = collect_demonstrations(logs_dir)
    relevant_demos = get_relevant_demonstrations(task, all_demonstrations, top_k=3)
    times["demonstrations"] = time.time() - demo_start

    times["total_prompt"] = time.time() - start

    return times

def profile_safety_checks():
    """Profile safety system startup."""
    from safety_killswitch import get_kill_switch, get_circuit_breaker
    from safety_gateway import SafetyGateway
    from safety_network import scan_for_network_access
    from safety_constitutional import ConstitutionalChecker

    workspace = Path(__file__).parent

    start = time.time()
    times = {}

    # Kill switch
    ks_start = time.time()
    kill_switch = get_kill_switch()
    halt_status = kill_switch.check_halt_flag()
    times["kill_switch"] = time.time() - ks_start

    # Circuit breaker
    cb_start = time.time()
    circuit_breaker = get_circuit_breaker()
    cb_status = circuit_breaker.status()
    times["circuit_breaker"] = time.time() - cb_start

    # Safety gateway
    sg_start = time.time()
    safety_gateway = SafetyGateway(workspace=workspace)
    times["safety_gateway"] = time.time() - sg_start

    # Network scan
    network_start = time.time()
    network_violations = scan_for_network_access("Test task for network scanning")
    times["network_scan"] = time.time() - network_start

    # Constitutional checker
    const_start = time.time()
    constitutional_checker = ConstitutionalChecker(constraints_path=str(workspace / "SAFETY_CONSTRAINTS.json"))
    times["constitutional"] = time.time() - const_start

    times["total_safety"] = time.time() - start

    return times

def main():
    """Run complete startup profiling."""
    print("Profiling grind_spawner startup performance...")

    results = {
        "timestamp": datetime.now().isoformat(),
        "profile_results": {}
    }

    # Profile imports
    print("  1. Profiling imports...")
    results["profile_results"]["imports"] = profile_imports()

    # Profile GrindSession init
    print("  2. Profiling GrindSession initialization...")
    results["profile_results"]["grind_session_init"] = profile_grind_session_init()

    # Profile prompt generation
    print("  3. Profiling prompt generation...")
    results["profile_results"]["prompt_generation"] = profile_prompt_generation()

    # Profile safety systems
    print("  4. Profiling safety systems...")
    results["profile_results"]["safety_checks"] = profile_safety_checks()

    # Calculate totals
    total_startup = (
        results["profile_results"]["imports"]["total_imports"] +
        results["profile_results"]["grind_session_init"]["total_init"] +
        results["profile_results"]["prompt_generation"]["total_prompt"] +
        results["profile_results"]["safety_checks"]["total_safety"]
    )

    results["total_startup_time"] = total_startup

    # Print results
    print("\n" + "="*60)
    print("  STARTUP PERFORMANCE PROFILE")
    print("="*60)
    print(f"  Total Startup Time: {total_startup:.3f}s")
    print("-"*60)

    for category, timings in results["profile_results"].items():
        print(f"  {category.replace('_', ' ').title()}:")
        for component, time_val in timings.items():
            if not component.startswith("total_"):
                print(f"    {component.replace('_', ' ').title():20s}: {time_val:.3f}s")
        if f"total_{category.split('_')[0]}" in timings:
            total_key = f"total_{category.split('_')[0]}"
        elif "total_imports" in timings:
            total_key = "total_imports"
        else:
            total_key = [k for k in timings.keys() if k.startswith("total_")]
            total_key = total_key[0] if total_key else None

        if total_key:
            print(f"    {'SUBTOTAL':20s}: {timings[total_key]:.3f}s")
        print()

    print("="*60)

    # Save to file
    profile_file = Path(__file__).parent / "startup_profile.json"
    with open(profile_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nProfile saved to {profile_file}")

    # Identify optimization opportunities
    slow_components = []
    for category, timings in results["profile_results"].items():
        for component, time_val in timings.items():
            if time_val > 0.1 and not component.startswith("total_"):  # > 100ms
                slow_components.append((category, component, time_val))

    if slow_components:
        print("\nOptimization Opportunities (>100ms):")
        slow_components.sort(key=lambda x: x[2], reverse=True)
        for category, component, time_val in slow_components:
            print(f"  {category}.{component}: {time_val:.3f}s")

if __name__ == "__main__":
    main()