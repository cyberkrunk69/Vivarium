#!/usr/bin/env python3
"""
SOP Executor - Executes standardized operating procedures step-by-step
Based on MetaGPT principles for structured agent workflows
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class SOPExecutor:
    """Execute SOP procedures with intermediate verification and context tracking."""

    def __init__(self, sop_file: str):
        """Initialize executor with an SOP definition file."""
        self.sop_path = Path(sop_file)
        self.sop = self._load_sop()
        self.context: Dict[str, Any] = {}
        self.results: List[Dict[str, Any]] = []
        self.lessons_file = Path("learned_lessons.json")

    def _load_sop(self) -> Dict[str, Any]:
        """Load SOP definition from JSON file."""
        with open(self.sop_path, 'r') as f:
            return json.load(f)

    def execute(self) -> bool:
        """Execute all steps in the SOP and verify quality gates."""
        print(f"\n{'='*60}")
        print(f"Executing SOP: {self.sop['name']}")
        print(f"{'='*60}\n")

        for i, step in enumerate(self.sop['steps'], 1):
            print(f"Step {i}/{len(self.sop['steps'])}: {step['action']}")

            # Get input from context if specified
            step_input = None
            if 'input' in step:
                step_input = self._resolve_input(step['input'])

            # Execute the step
            result = self._execute_step(step, step_input)

            # Store output in context if specified
            if 'output' in step:
                self.context[step['output']] = result

            # Store step result
            self.results.append({
                'step': i,
                'action': step['action'],
                'status': 'completed',
                'output_key': step.get('output', None)
            })

            print(f"  [OK] Completed\n")

        # Verify quality gates
        return self._verify_quality_gates()

    def _resolve_input(self, input_spec: Any) -> Any:
        """Resolve input from context or return as-is."""
        if isinstance(input_spec, str):
            return self.context.get(input_spec, input_spec)
        elif isinstance(input_spec, list):
            return [self.context.get(item, item) if isinstance(item, str) else item
                    for item in input_spec]
        return input_spec

    def _execute_step(self, step: Dict[str, Any], input_data: Any) -> Any:
        """Execute a single step - placeholder for actual action handling."""
        action = step['action']

        # Mock execution - in real implementation, dispatch to actual handlers
        print(f"    Action: {action}")
        if input_data:
            print(f"    Input: {input_data if not isinstance(input_data, str) else f'<{input_data}>'}")

        return f"{action}_result"

    def _verify_quality_gates(self) -> bool:
        """Verify all quality gates pass."""
        print(f"\n{'='*60}")
        print("Quality Gate Verification")
        print(f"{'='*60}\n")

        gates = self.sop.get('quality_gates', [])
        all_pass = True

        for gate in gates:
            status = "[PASS]" if self._check_gate(gate) else "[FAIL]"
            print(f"{status}: {gate}")
            if status.startswith("[FAIL]"):
                all_pass = False

        print()
        return all_pass

    def _check_gate(self, gate: str) -> bool:
        """Check if a quality gate passes."""
        # Placeholder - in real implementation, verify actual conditions
        return True

    def save_lessons(self, lesson: str) -> None:
        """Append a lesson learned to the lessons file."""
        lessons = {}
        if self.lessons_file.exists():
            with open(self.lessons_file, 'r') as f:
                lessons = json.load(f)

        sop_name = self.sop['name']
        if sop_name not in lessons:
            lessons[sop_name] = []

        lessons[sop_name].append({
            'lesson': lesson,
            'timestamp': str(Path.cwd())
        })

        with open(self.lessons_file, 'w') as f:
            json.dump(lessons, f, indent=2)

    def print_summary(self) -> None:
        """Print execution summary."""
        print(f"\n{'='*60}")
        print("Execution Summary")
        print(f"{'='*60}")
        print(f"SOP: {self.sop['name']}")
        print(f"Steps completed: {len(self.results)}/{len(self.sop['steps'])}")
        print(f"Status: {'SUCCESS' if all(r['status'] == 'completed' for r in self.results) else 'FAILURE'}")
        print()


def main():
    """Main entry point for SOP executor."""
    if len(sys.argv) < 2:
        print("Usage: python sop_executor.py <path_to_sop.json>")
        sys.exit(1)

    sop_file = sys.argv[1]
    executor = SOPExecutor(sop_file)

    success = executor.execute()
    executor.print_summary()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
