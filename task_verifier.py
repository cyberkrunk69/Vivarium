"""
Task Verifier - Validates task outputs before marking complete.

Integrates the Critic pattern from OBSERVER_PATTERN_DESIGN.md.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from safety_validator import SyntaxValidator


class Verdict(Enum):
    """Verification verdict."""
    APPROVE = "APPROVE"
    MINOR_ISSUES = "MINOR_ISSUES"
    REJECT = "REJECT"


@dataclass
class VerificationResult:
    """Result of verifying a task output."""
    verdict: Verdict
    confidence: float  # 0.0 to 1.0
    issues: List[str]
    suggestions: List[str]
    cost_usd: float = 0.0

    def should_accept(self) -> bool:
        """Whether to accept this output."""
        return self.verdict in [Verdict.APPROVE, Verdict.MINOR_ISSUES]

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict.value,
            "confidence": self.confidence,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "cost_usd": self.cost_usd
        }


class TaskVerifier:
    """
    Verifies task outputs before accepting them.

    This is the "Critic" node from the architecture.
    Currently uses deterministic checks; can be upgraded to LLM-based verification.
    """

    def __init__(self):
        self.syntax_validator = SyntaxValidator()

    def verify_task_output(
        self,
        task: Dict,
        output: Dict,
        files_created: List[str] = None
    ) -> VerificationResult:
        """
        Verify a task's output.

        Args:
            task: The original task dict
            output: The task output
            files_created: List of files that were created/modified

        Returns:
            VerificationResult with verdict
        """
        issues = []
        suggestions = []
        files_created = files_created or []

        # 1. Check if files were actually created
        if files_created:
            for filepath in files_created:
                path = Path(filepath)
                if not path.exists():
                    issues.append(f"Claimed to create {filepath} but file doesn't exist")

        # 2. Validate Python syntax for any created Python files
        python_files = [f for f in files_created if f.endswith('.py')]
        for filepath in python_files:
            validation = self.syntax_validator.validate_file(Path(filepath))
            if not validation.valid:
                issues.extend(validation.errors)

        # 3. Check for placeholder content
        for filepath in files_created:
            if self._contains_placeholders(Path(filepath)):
                issues.append(f"{filepath} contains placeholder code (TODO, FIXME, ...)")

        # 4. Check if error field is set
        if output.get("error"):
            issues.append(f"Task reported error: {output['error']}")

        # 5. Check if success field is False
        if not output.get("success", True):
            issues.append("Task marked as unsuccessful")

        # Determine verdict
        if len(issues) == 0:
            verdict = Verdict.APPROVE
            confidence = 0.95
        elif len(issues) <= 2 and all("placeholder" in i.lower() for i in issues):
            verdict = Verdict.MINOR_ISSUES
            confidence = 0.75
            suggestions.append("Clean up placeholder code in a follow-up task")
        else:
            verdict = Verdict.REJECT
            confidence = 0.90
            suggestions.append("Fix the issues and retry the task")

        return VerificationResult(
            verdict=verdict,
            confidence=confidence,
            issues=issues,
            suggestions=suggestions,
            cost_usd=0.0  # Deterministic verification is free
        )

    def verify_with_llm(
        self,
        task: Dict,
        output: Dict,
        files_created: List[str] = None,
        use_cheap_model: bool = True
    ) -> VerificationResult:
        """
        Verify using an LLM (Critic pattern).

        Args:
            task: Original task
            output: Task output
            files_created: Files created
            use_cheap_model: Use GPT-OSS 20B (cheap) vs larger model

        Returns:
            VerificationResult
        """
        # TODO: Implement LLM-based verification
        # For now, fall back to deterministic verification
        return self.verify_task_output(task, output, files_created)

    def _contains_placeholders(self, filepath: Path) -> bool:
        """Check if a file contains placeholder code."""
        if not filepath.exists() or filepath.suffix != '.py':
            return False

        try:
            content = filepath.read_text(encoding='utf-8')
            placeholders = ['TODO', 'FIXME', 'XXX', '...', 'pass  # placeholder']
            return any(ph in content for ph in placeholders)
        except:
            return False


class VerificationTracker:
    """Tracks verification statistics over time."""

    def __init__(self, log_file: Path = None):
        self.log_file = log_file or Path("verification_log.json")
        self.stats = self._load_stats()

    def record_verification(self, result: VerificationResult, task_id: str):
        """Record a verification result."""
        self.stats["total"] = self.stats.get("total", 0) + 1
        self.stats[result.verdict.value] = self.stats.get(result.verdict.value, 0) + 1

        # Record in log
        entry = {
            "task_id": task_id,
            "verdict": result.verdict.value,
            "confidence": result.confidence,
            "issues_count": len(result.issues),
            "timestamp": str(Path().absolute())
        }

        log = self._load_log()
        log.append(entry)

        # Keep last 1000 entries
        log = log[-1000:]
        self._save_log(log)

        # Update stats
        self._save_stats()

    def get_approval_rate(self) -> float:
        """Get the percentage of tasks that were approved."""
        total = self.stats.get("total", 0)
        if total == 0:
            return 0.0

        approved = self.stats.get("APPROVE", 0) + self.stats.get("MINOR_ISSUES", 0)
        return approved / total

    def get_stats(self) -> Dict:
        """Get verification statistics."""
        return {
            "total_verifications": self.stats.get("total", 0),
            "approved": self.stats.get("APPROVE", 0),
            "minor_issues": self.stats.get("MINOR_ISSUES", 0),
            "rejected": self.stats.get("REJECT", 0),
            "approval_rate": self.get_approval_rate()
        }

    def _load_stats(self) -> Dict:
        """Load statistics from disk."""
        stats_file = self.log_file.with_suffix('.stats.json')
        if not stats_file.exists():
            return {}

        try:
            return json.loads(stats_file.read_text())
        except:
            return {}

    def _save_stats(self):
        """Save statistics to disk."""
        stats_file = self.log_file.with_suffix('.stats.json')
        stats_file.write_text(json.dumps(self.stats, indent=2))

    def _load_log(self) -> List[Dict]:
        """Load verification log."""
        if not self.log_file.exists():
            return []

        try:
            return json.loads(self.log_file.read_text())
        except:
            return []

    def _save_log(self, log: List[Dict]):
        """Save verification log."""
        self.log_file.write_text(json.dumps(log, indent=2))


if __name__ == "__main__":
    # Test the verifier
    print("Testing Task Verifier...")

    verifier = TaskVerifier()

    # Test case 1: Successful task with valid file
    Path("test_output.py").write_text("def hello():\n    print('world')\n")

    result = verifier.verify_task_output(
        task={"task": "Create hello function"},
        output={"success": True, "error": None},
        files_created=["test_output.py"]
    )

    assert result.verdict == Verdict.APPROVE, "Should approve valid output"
    print("✓ Test 1 passed: Valid output approved")

    # Test case 2: Task with syntax error
    Path("test_bad.py").write_text("def hello(\n    print('world'\n")

    result = verifier.verify_task_output(
        task={"task": "Create hello function"},
        output={"success": True, "error": None},
        files_created=["test_bad.py"]
    )

    assert result.verdict == Verdict.REJECT, "Should reject syntax errors"
    print("✓ Test 2 passed: Syntax errors rejected")

    # Cleanup
    Path("test_output.py").unlink()
    Path("test_bad.py").unlink()

    print("\n✓ All verifier tests passed")
