#!/usr/bin/env python3
"""
CriticAgent - Code Review System based on LATS/TextGrad patterns

Implements automated code quality assessment and feedback generation
to support iterative code improvement in the grind spawner system.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
from logger import get_logger

logger = get_logger()


class CriticAgent:
    """
    Automated code reviewer implementing LATS/TextGrad critic patterns.

    Evaluates code quality across multiple dimensions:
    - Error handling robustness
    - Pattern consistency with codebase
    - Logic correctness
    - Import and dependency integrity
    """

    def __init__(self, workspace: Path = None):
        """Initialize critic with optional codebase context."""
        self.workspace = workspace or Path(__file__).parent
        self.issues = []
        self.quality_score = 0.0

    def review(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive code review.

        Args:
            code: Source code to review
            context: Optional context dict with keys:
                - filename: Name of the file being reviewed
                - task: Description of what the code should do
                - related_files: List of related files in codebase

        Returns:
            Review result dict with:
                - score: 0.0-1.0 quality score
                - issues: List of identified issues
                - feedback: List of improvement suggestions
                - passed: Boolean indicating if code meets minimum quality threshold
        """
        self.issues = []
        context = context or {}

        # Run quality checks
        self._check_error_handling(code)
        self._check_imports(code)
        self._check_syntax_basic(code)
        self._check_patterns(code, context)
        self._check_logic(code)

        # Calculate quality score
        self.quality_score = self.score_quality(code)

        # Generate feedback
        feedback = self.generate_feedback(code, self.issues)

        return {
            "score": self.quality_score,
            "issues": self.issues,
            "feedback": feedback,
            "passed": self.quality_score >= 0.65,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }

    def score_quality(self, code: str) -> float:
        """
        Calculate quality score from 0.0 to 1.0.

        Scoring factors:
        - No critical issues: 0.2 points
        - Proper error handling: 0.2 points
        - Clean imports: 0.2 points
        - Pattern consistency: 0.2 points
        - Logic validity: 0.2 points

        Returns:
            Float between 0.0 and 1.0
        """
        if not code or not code.strip():
            return 0.0

        score = 1.0

        # Deduct points for each issue severity
        critical_count = len([i for i in self.issues if i.get("severity") == "critical"])
        warning_count = len([i for i in self.issues if i.get("severity") == "warning"])
        info_count = len([i for i in self.issues if i.get("severity") == "info"])

        score -= critical_count * 0.15
        score -= warning_count * 0.05
        score -= info_count * 0.02

        return max(0.0, min(1.0, score))

    def generate_feedback(self, code: str, issues: List[Dict]) -> List[str]:
        """
        Generate actionable improvement suggestions.

        Args:
            code: Source code
            issues: List of identified issues from review

        Returns:
            List of prioritized feedback strings
        """
        feedback = []

        # Critical issues first
        critical = [i for i in issues if i.get("severity") == "critical"]
        if critical:
            feedback.append(f"[CRITICAL] ({len(critical)} issues): " +
                          ", ".join([i["message"] for i in critical[:2]]))

        # Warnings
        warnings = [i for i in issues if i.get("severity") == "warning"]
        if warnings:
            feedback.append(f"[WARNINGS] ({len(warnings)} issues): " +
                          ", ".join([i["message"] for i in warnings[:2]]))

        # Suggestions for improvement
        if not critical and not warnings:
            feedback.append("[OK] Code quality looks good!")

        # Add specific recommendations
        if any(i["type"] == "missing_error_handling" for i in issues):
            feedback.append("Consider adding try-except blocks around external calls")

        if any(i["type"] == "unused_import" for i in issues):
            feedback.append("Remove unused imports to reduce dependencies")

        if any(i["type"] == "inconsistent_style" for i in issues):
            feedback.append("Review code style for consistency with project conventions")

        return feedback

    def _check_error_handling(self, code: str) -> None:
        """Check for adequate error handling patterns."""
        # Count try-except blocks
        try_blocks = len(re.findall(r'\btry\s*:', code))
        except_blocks = len(re.findall(r'\bexcept\s+', code))

        # Check for external API calls without error handling
        api_patterns = [
            r'requests\.',
            r'json\.load',
            r'json\.dump',
            r'open\(',
            r'subprocess\.',
            r'os\.path\.'
        ]

        api_calls = sum(len(re.findall(p, code)) for p in api_patterns)

        # If there are external calls but few exception handlers, flag it
        if api_calls > 0 and try_blocks < max(1, api_calls // 2):
            self.issues.append({
                "type": "missing_error_handling",
                "severity": "warning",
                "line": None,
                "message": f"Found {api_calls} external API calls but only {try_blocks} try-except blocks"
            })

    def _check_imports(self, code: str) -> None:
        """Check import validity and usage."""
        # Extract all imports
        import_lines = re.findall(r'^(?:from|import)\s+([^\s]+)', code, re.MULTILINE)

        for imp in import_lines:
            # Remove 'as' aliases
            module = imp.split(' as ')[0].strip()

            # Check if it's used in code
            # Simple heuristic: module name appears in code after import
            if module and module not in '__future__':
                # Very basic - just check if module is mentioned
                pattern = re.escape(module.split('.')[0])
                if not re.search(pattern, code[code.find('\n', code.find(imp)):]):
                    self.issues.append({
                        "type": "unused_import",
                        "severity": "info",
                        "line": None,
                        "message": f"Possible unused import: {imp}"
                    })

    def _check_syntax_basic(self, code: str) -> None:
        """Check for basic syntax issues."""
        # Check for mismatched brackets
        open_parens = code.count('(')
        close_parens = code.count(')')
        open_brackets = code.count('[')
        close_brackets = code.count(']')
        open_braces = code.count('{')
        close_braces = code.count('}')

        if open_parens != close_parens:
            self.issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": None,
                "message": "Mismatched parentheses"
            })

        if open_brackets != close_brackets:
            self.issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": None,
                "message": "Mismatched brackets"
            })

        if open_braces != close_braces:
            self.issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": None,
                "message": "Mismatched braces"
            })

    def _check_patterns(self, code: str, context: Dict) -> None:
        """Check for consistency with codebase patterns."""
        # Check for common codebase patterns

        # Pattern 1: Logger usage
        if 'logger' in code and 'from logger import' not in code and 'import logger' not in code:
            self.issues.append({
                "type": "missing_import",
                "severity": "warning",
                "line": None,
                "message": "Uses logger but doesn't import from logger module"
            })

        # Pattern 2: Path handling - should use pathlib.Path
        if 'os.path' in code and 'from pathlib import Path' not in code:
            self.issues.append({
                "type": "inconsistent_style",
                "severity": "info",
                "line": None,
                "message": "Uses os.path instead of pathlib.Path (codebase standard)"
            })

        # Pattern 3: JSON handling - check for safe patterns
        if 'json.load' in code and 'json.JSONDecodeError' not in code:
            self.issues.append({
                "type": "missing_error_handling",
                "severity": "warning",
                "line": None,
                "message": "json.load() used without JSONDecodeError handling"
            })

    def _check_logic(self, code: str) -> None:
        """Check for obvious logical issues."""
        # Check for empty functions
        func_pattern = r'def\s+\w+\([^)]*\):\s*(?:"""[^"]*"""|\'\'\'[^\']*\'\'\')?(?:\n\s+)?(?:pass|\.\.\.)?$'
        empty_funcs = re.findall(func_pattern, code, re.MULTILINE)

        if empty_funcs:
            self.issues.append({
                "type": "incomplete_implementation",
                "severity": "warning",
                "line": None,
                "message": f"Found {len(empty_funcs)} function(s) with no implementation"
            })

        # Check for hardcoded values that should be config
        if re.search(r'(127\.0\.0\.1|localhost|"http://"|"https://")', code):
            self.issues.append({
                "type": "hardcoded_config",
                "severity": "info",
                "line": None,
                "message": "Contains hardcoded URLs/IPs - consider using config/environment variables"
            })
