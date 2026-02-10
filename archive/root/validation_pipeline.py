#!/usr/bin/env python3
"""
validation_pipeline.py

A lightweight validation harness used by the swarm to self‑test generated code
before it is merged into the main code‑base.

The pipeline performs, in order:

1. **Syntax check** – attempts to compile all ``.py`` files under the
   experiment directory.  Any `SyntaxError` aborts the pipeline.

2. **Import validation** – imports each module in isolation to ensure that
   all dependencies are resolvable.  Failures are captured and reported.

3. **Pytest execution** – runs the project's existing pytest suite (if any)
   with a short timeout.  The exit code is used to decide success.

4. **Basic smoke tests** – a very small configurable set of sanity checks.
   By default it verifies that the generated ``test_runner.py`` (if present)
   can be executed without raising an exception.

If any step fails, the script exits with a non‑zero status and prints a
JSON‑compatible summary that can be consumed by the swarm controller for
retry or human review.

Usage
-----
    python validation_pipeline.py

The script assumes it is executed from the repository root (``/app``).
"""

import ast
import importlib.util
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import List, Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
EXPERIMENT_ROOT = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 120  # Max time for pytest run
SMOKE_TESTS: List[Dict[str, Any]] = [
    {
        "name": "run_self_test_runner",
        "script": EXPERIMENT_ROOT / "test_runner.py",
        "description": "Execute generated test_runner.py if it exists.",
    }
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def find_python_files(root: Path) -> List[Path]:
    """Recursively collect all ``.py`` files under *root*."""
    return [p for p in root.rglob("*.py") if p.is_file()]

def syntax_check(files: List[Path]) -> List[Dict[str, str]]:
    """Attempt to compile each file; return list of errors."""
    errors = []
    for file_path in files:
        try:
            source = file_path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(file_path))
        except SyntaxError as exc:
            errors.append({
                "file": str(file_path),
                "error": f"SyntaxError: {exc.msg} (line {exc.lineno})"
            })
    return errors

def import_check(files: List[Path]) -> List[Dict[str, str]]:
    """Try to import each module; capture import‑related failures."""
    errors = []
    for file_path in files:
        module_name = file_path.stem
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                raise ImportError("Unable to create import spec")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
        except Exception as exc:
            errors.append({
                "file": str(file_path),
                "error": f"ImportError: {exc.__class__.__name__}: {exc}"
            })
    return errors

def run_pytest() -> Dict[str, Any]:
    """Execute pytest in the repository root with a timeout."""
    result = {
        "passed": False,
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "timeout": False,
    }
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(Path.cwd()),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        result["returncode"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        result["passed"] = proc.returncode == 0
    except subprocess.TimeoutExpired as exc:
        result["timeout"] = True
        result["stderr"] = f"Timeout after {TIMEOUT_SECONDS}s"
    except Exception as exc:
        result["stderr"] = f"Unexpected error while running pytest: {exc}"
    return result

def run_smoke_tests() -> List[Dict[str, Any]]:
    """Execute the configured smoke test commands."""
    outcomes = []
    for test in SMOKE_TESTS:
        script_path: Path = test["script"]
        outcome = {
            "name": test["name"],
            "description": test.get("description", ""),
            "passed": False,
            "error": None,
        }
        if not script_path.is_file():
            # If the script does not exist, we treat it as a skip rather than failure.
            outcome["passed"] = True
            outcome["error"] = "Skipped (file not present)"
            outcomes.append(outcome)
            continue

        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(EXPERIMENT_ROOT),
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            if proc.returncode == 0:
                outcome["passed"] = True
            else:
                outcome["error"] = f"Non‑zero exit ({proc.returncode}). Stderr: {proc.stderr.strip()}"
        except subprocess.TimeoutExpired:
            outcome["error"] = f"Timeout after {TIMEOUT_SECONDS}s"
        except Exception as exc:
            outcome["error"] = f"Exception: {exc}"
        outcomes.append(outcome)
    return outcomes

# --------------------------------------------------------------------------- #
# Main pipeline
# --------------------------------------------------------------------------- #
def main() -> int:
    report: Dict[str, Any] = {
        "syntax_errors": [],
        "import_errors": [],
        "pytest": {},
        "smoke_tests": [],
        "overall_success": False,
    }

    py_files = find_python_files(EXPERIMENT_ROOT)

    # 1. Syntax checking
    report["syntax_errors"] = syntax_check(py_files)
    if report["syntax_errors"]:
        print(json.dumps(report, indent=2))
        return 1

    # 2. Import validation
    report["import_errors"] = import_check(py_files)
    if report["import_errors"]:
        print(json.dumps(report, indent=2))
        return 1

    # 3. Run existing pytest suite
    report["pytest"] = run_pytest()
    if not report["pytest"].get("passed", False):
        print(json.dumps(report, indent=2))
        return 1

    # 4. Basic smoke tests
    report["smoke_tests"] = run_smoke_tests()
    smoke_success = all(t["passed"] for t in report["smoke_tests"])
    if not smoke_success:
        print(json.dumps(report, indent=2))
        return 1

    # All checks passed
    report["overall_success"] = True
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())