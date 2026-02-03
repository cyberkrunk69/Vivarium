#!/usr/bin/env python3
"""
Fixed startup profiler - times actual grind spawner startup operations.
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

    workspace = Path(__file__).parent.parent.parent
    spawner_path = workspace / "grind_spawner_groq.py"

    print(f"Testing: {spawner_path}")
    print(f"Exists: {spawner_path.exists()}")

    if not spawner_path.exists():
        print(f"ERROR: {spawner_path} not found")
        return 0

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
        else:
            print("Help output length:", len(result.stdout))

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

    workspace = Path(__file__).parent.parent.parent
    spawner_path = workspace / "grind_spawner_groq.py"

    if not spawner_path.exists():
        print(f"ERROR: {spawner_path} not found")
        return [], [], []

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

def time_actual_session_creation():
    """Time creating a single session (the expensive part)."""
    print("\n" + "=" * 60)
    print("  SESSION CREATION TIMING")
    print("=" * 60)

    workspace = Path(__file__).parent.parent.parent

    # Write a minimal test script
    test_script = f"""
import sys
sys.path.append('{workspace}')
import time
from pathlib import Path

start = time.perf_counter()

# Test safety imports
try:
    from safety_sandbox import initialize_sandbox
    print(f"safety_sandbox: {{time.perf_counter() - start:.3f}}s")
except ImportError as e:
    print(f"safety_sandbox: MISSING - {{e}}")

safety_time = time.perf_counter()
try:
    from safety_gateway import SafetyGateway
    from safety_sanitize import sanitize_task
    from safety_killswitch import get_kill_switch
    from safety_network import scan_for_network_access
    print(f"safety modules: {{time.perf_counter() - safety_time:.3f}}s")
except ImportError as e:
    print(f"safety modules: MISSING - {{e}}")

kg_time = time.perf_counter()
try:
    from knowledge_graph import KnowledgeGraph
    kg = KnowledgeGraph()
    kg_file = Path('{workspace}') / 'knowledge_graph.json'
    if kg_file.exists():
        kg.load_json(str(kg_file))
    print(f"knowledge graph: {{time.perf_counter() - kg_time:.3f}}s")
except Exception as e:
    print(f"knowledge graph: FAILED - {{e}}")

total = time.perf_counter() - start
print(f"Total simulation: {{total:.3f}}s")
"""

    test_file = workspace / "experiments" / "exp_20260203_101127_unified_session_1" / "test_session_timing.py"
    with open(test_file, 'w') as f:
        f.write(test_script)

    try:
        result = subprocess.run([
            sys.executable, str(test_file)
        ], capture_output=True, text=True, cwd=workspace, timeout=30)

        print("Session creation simulation:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)

    except Exception as e:
        print(f"Session timing failed: {e}")

def main():
    # Time current startup
    startup_time = time_startup_sequence()

    # Analyze import structure
    safety_imports, core_imports, std_imports = analyze_imports_in_spawner()

    # Time session creation
    time_actual_session_creation()

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"Script startup time: {startup_time:.3f}s")
    print(f"Safety imports: {len(safety_imports)}")
    print(f"Core imports: {len(core_imports)}")

if __name__ == "__main__":
    main()