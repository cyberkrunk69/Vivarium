#!/usr/bin/env python3
"""
Failure Pattern Detection - Learn from failures to prevent repeats.

Tracks failed tasks with error details, characteristics, and attempted solutions.
Provides warnings for tasks similar to past failures.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import difflib


class FailurePatternDetector:
    """Detects and learns from task failure patterns."""

    def __init__(self, workspace: Path = None, failures_file: str = "failure_patterns.json"):
        """Initialize detector with workspace context."""
        self.workspace = workspace or Path(__file__).parent
        self.failures_file = self.workspace / failures_file
        self.failures = self._load_failures()

    def _load_failures(self) -> List[Dict[str, Any]]:
        """Load historical failures from file."""
        if self.failures_file.exists():
            try:
                with open(self.failures_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_failures(self):
        """Persist failures to file."""
        with open(self.failures_file, 'w') as f:
            json.dump(self.failures, f, indent=2, default=str)

    def track_failure(
        self,
        task_description: str,
        error_type: str,
        error_message: str,
        task_characteristics: Dict[str, Any],
        attempted_approaches: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record a task failure with complete context.

        Args:
            task_description: Description of the failed task
            error_type: Type/category of error (e.g., "ImportError", "TimeoutError", "LogicError")
            error_message: Full error message or failure reason
            task_characteristics: Dict with task metadata (e.g., complexity, domain, file types)
            attempted_approaches: List of strategies that were tried
            context: Optional additional context (model used, duration, etc.)

        Returns:
            Stored failure record with timestamp and ID.
        """
        failure_id = len(self.failures) + 1

        record = {
            "id": failure_id,
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "error_type": error_type,
            "error_message": error_message,
            "task_characteristics": task_characteristics,
            "attempted_approaches": attempted_approaches,
            "context": context or {},
        }

        self.failures.append(record)
        self._save_failures()
        return record

    def _compute_task_similarity(self, task1: str, task2: str) -> float:
        """
        Compute similarity between two task descriptions.

        Uses sequence matching to find similar tasks.

        Args:
            task1: First task description
            task2: Second task description

        Returns:
            Similarity score between 0.0 and 1.0
        """
        return difflib.SequenceMatcher(None, task1.lower(), task2.lower()).ratio()

    def _check_characteristic_overlap(
        self,
        chars1: Dict[str, Any],
        chars2: Dict[str, Any]
    ) -> int:
        """
        Count overlapping characteristics between two tasks.

        Args:
            chars1: First task's characteristics
            chars2: Second task's characteristics

        Returns:
            Number of matching characteristics
        """
        overlap = 0
        for key in chars1:
            if key in chars2 and chars1[key] == chars2[key]:
                overlap += 1
        return overlap

    def check_failure_patterns(
        self,
        task_description: str,
        task_characteristics: Optional[Dict[str, Any]] = None,
        similarity_threshold: float = 0.6,
        top_n: int = 3
    ) -> Dict[str, Any]:
        """
        Check if a task is similar to past failures.

        Args:
            task_description: Description of the task to check
            task_characteristics: Optional task metadata for matching
            similarity_threshold: Minimum similarity score (0.0-1.0) to flag
            top_n: Number of similar failures to return

        Returns:
            Dictionary containing:
                - similar_failures: List of similar past failures
                - warning_level: "high", "medium", "low", or "none"
                - suggested_strategies: List of avoidance strategies
        """
        if not self.failures:
            return {
                "similar_failures": [],
                "warning_level": "none",
                "suggested_strategies": []
            }

        task_characteristics = task_characteristics or {}

        # Score each past failure for similarity
        scored_failures = []
        for failure in self.failures:
            # Text similarity
            text_sim = self._compute_task_similarity(
                task_description,
                failure["task_description"]
            )

            # Characteristic overlap
            char_overlap = 0
            if task_characteristics:
                char_overlap = self._check_characteristic_overlap(
                    task_characteristics,
                    failure["task_characteristics"]
                )

            # Combined score (weighted average)
            combined_score = (text_sim * 0.7) + (min(char_overlap / 3, 1.0) * 0.3)

            if combined_score >= similarity_threshold:
                scored_failures.append((combined_score, failure))

        # Sort by similarity score
        scored_failures.sort(key=lambda x: x[0], reverse=True)
        similar_failures = [f[1] for f in scored_failures[:top_n]]

        # Determine warning level
        if not similar_failures:
            warning_level = "none"
        elif scored_failures[0][0] >= 0.85:
            warning_level = "high"
        elif scored_failures[0][0] >= 0.75:
            warning_level = "medium"
        else:
            warning_level = "low"

        # Generate avoidance strategies
        strategies = self._generate_avoidance_strategies(similar_failures)

        return {
            "similar_failures": [
                {
                    "id": f["id"],
                    "task": f["task_description"],
                    "error_type": f["error_type"],
                    "error_message": f["error_message"],
                    "attempted_approaches": f["attempted_approaches"],
                    "timestamp": f["timestamp"]
                }
                for f in similar_failures
            ],
            "warning_level": warning_level,
            "suggested_strategies": strategies
        }

    def _generate_avoidance_strategies(
        self,
        similar_failures: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate suggested strategies based on past failures.

        Args:
            similar_failures: List of similar failed tasks

        Returns:
            List of strategy suggestions
        """
        strategies = []

        if not similar_failures:
            return strategies

        # Collect all error types
        error_types = [f["error_type"] for f in similar_failures]
        error_type_counts = defaultdict(int)
        for et in error_types:
            error_type_counts[et] += 1

        # Strategy: Avoid previously failed approaches
        all_attempted = []
        for f in similar_failures:
            all_attempted.extend(f["attempted_approaches"])

        if all_attempted:
            unique_attempted = list(set(all_attempted))
            strategies.append(
                f"Avoid these previously failed approaches: {', '.join(unique_attempted[:3])}"
            )

        # Strategy: Common error type warnings
        most_common_error = max(error_type_counts.items(), key=lambda x: x[1])[0]
        strategies.append(
            f"Watch for {most_common_error} - occurred in {error_type_counts[most_common_error]} similar task(s)"
        )

        # Strategy: Review error messages
        strategies.append(
            "Review similar failure error messages before implementing"
        )

        # Strategy: Consider alternative approach
        if len(all_attempted) >= 2:
            strategies.append(
                "Multiple approaches failed previously - consider a fundamentally different strategy"
            )

        return strategies[:4]  # Limit to top 4 strategies

    def get_error_type_stats(self) -> Dict[str, int]:
        """
        Get frequency of each error type across all failures.

        Returns:
            Dictionary mapping error type to count.
        """
        error_counts = defaultdict(int)
        for failure in self.failures:
            error_counts[failure["error_type"]] += 1
        return dict(error_counts)

    def get_most_problematic_tasks(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get tasks that have failed most frequently.

        Args:
            top_n: Number of top problematic tasks to return

        Returns:
            List of task patterns with failure counts.
        """
        # Group similar tasks
        task_groups = defaultdict(list)
        for failure in self.failures:
            # Use first 50 chars as grouping key
            key = failure["task_description"][:50].lower()
            task_groups[key].append(failure)

        # Sort by group size
        sorted_groups = sorted(
            task_groups.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )

        return [
            {
                "task_pattern": group[0],
                "failure_count": len(group[1]),
                "examples": [f["task_description"] for f in group[1][:3]]
            }
            for group in sorted_groups[:top_n]
        ]

    def generate_warning_prompt(
        self,
        task_description: str,
        task_characteristics: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a warning prompt section for risky tasks.

        Args:
            task_description: Task to check
            task_characteristics: Optional task metadata

        Returns:
            Formatted warning text to inject into prompts (empty string if no warnings).
        """
        check_result = self.check_failure_patterns(
            task_description,
            task_characteristics
        )

        if check_result["warning_level"] == "none":
            return ""

        warning_lines = [
            "WARNING  FAILURE PATTERN WARNING WARNING",
            f"Warning Level: {check_result['warning_level'].upper()}",
            "",
            "Similar tasks have failed previously:",
        ]

        for failure in check_result["similar_failures"]:
            warning_lines.append(f"  - {failure['error_type']}: {failure['task'][:80]}...")

        warning_lines.append("")
        warning_lines.append("Suggested Avoidance Strategies:")
        for strategy in check_result["suggested_strategies"]:
            warning_lines.append(f"  * {strategy}")

        warning_lines.append("")

        return "\n".join(warning_lines)
