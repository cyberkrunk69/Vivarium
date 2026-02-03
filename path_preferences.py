"""
Path Preference Learning System
Learns which role chain paths work best for different task types over time.
Tracks success rates and quality metrics to adaptively recommend optimal paths.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class PathPreferenceLearner:
    """Learns and tracks which role chain paths perform best for different task categories."""

    def __init__(self, preferences_file: str = "path_preferences.json"):
        self.preferences_file = Path(preferences_file)
        self.preferences = self._load_preferences()

    def _load_preferences(self) -> Dict:
        """Load existing preferences from disk."""
        if self.preferences_file.exists():
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        return {
            "outcomes": {},  # (task_category, path_type) -> [outcomes]
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_outcomes": 0
            }
        }

    def _save_preferences(self):
        """Persist preferences to disk."""
        self.preferences["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)

    def record_outcome(self, task_type: str, path_type: str, success: bool, quality: float):
        """
        Record an outcome for a specific task type and path combination.

        Args:
            task_type: Category of task (e.g., "knowledge_infrastructure", "feedback_loops")
            path_type: Role chain path used (e.g., "PLANNER->CODER->REVIEWER", "CODER->REVIEWER")
            success: Whether the task completed successfully
            quality: Quality score (0.0-1.0)
        """
        key = f"{task_type}|{path_type}"

        if key not in self.preferences["outcomes"]:
            self.preferences["outcomes"][key] = []

        outcome = {
            "success": success,
            "quality": quality,
            "timestamp": datetime.now().isoformat()
        }

        self.preferences["outcomes"][key].append(outcome)
        self.preferences["metadata"]["total_outcomes"] += 1
        self._save_preferences()

    def get_success_rate(self, task_type: str, path_type: str) -> float:
        """
        Calculate success rate for a specific task type and path combination.

        Args:
            task_type: Category of task
            path_type: Role chain path

        Returns:
            Success rate as float (0.0-1.0), or 0.5 if no data
        """
        key = f"{task_type}|{path_type}"
        outcomes = self.preferences["outcomes"].get(key, [])

        if not outcomes:
            return 0.5  # Neutral default when no data

        successes = sum(1 for o in outcomes if o["success"])
        return successes / len(outcomes)

    def get_average_quality(self, task_type: str, path_type: str) -> float:
        """
        Calculate average quality for a specific task type and path combination.

        Args:
            task_type: Category of task
            path_type: Role chain path

        Returns:
            Average quality as float (0.0-1.0), or 0.5 if no data
        """
        key = f"{task_type}|{path_type}"
        outcomes = self.preferences["outcomes"].get(key, [])

        if not outcomes:
            return 0.5  # Neutral default when no data

        total_quality = sum(o["quality"] for o in outcomes)
        return total_quality / len(outcomes)

    def get_recommended_path(self, task_type: str) -> str:
        """
        Get the recommended role chain path for a given task type.

        Args:
            task_type: Category of task

        Returns:
            Recommended path_type string (e.g., "PLANNER->CODER->REVIEWER->DOCUMENTER")
        """
        # Find all paths used for this task type
        relevant_keys = [k for k in self.preferences["outcomes"].keys()
                        if k.startswith(f"{task_type}|")]

        if not relevant_keys:
            # No data for this task type, use full chain by default
            return "PLANNER->CODER->REVIEWER->DOCUMENTER"

        # Score each path by combining success rate and quality
        path_scores = {}
        for key in relevant_keys:
            _, path_type = key.split("|", 1)
            success_rate = self.get_success_rate(task_type, path_type)
            avg_quality = self.get_average_quality(task_type, path_type)

            # Combined score: 60% success rate, 40% quality
            score = (0.6 * success_rate) + (0.4 * avg_quality)
            path_scores[path_type] = score

        # Return path with highest score
        best_path = max(path_scores.items(), key=lambda x: x[1])
        return best_path[0]

    def generate_decision_rules(self) -> Dict:
        """
        Generate decision rules based on learned preferences.

        Returns:
            Dict mapping task types to recommended paths with confidence scores
        """
        rules = {}

        # Group outcomes by task type
        task_types = set()
        for key in self.preferences["outcomes"].keys():
            task_type, _ = key.split("|", 1)
            task_types.add(task_type)

        # Generate rules for each task type
        for task_type in task_types:
            relevant_keys = [k for k in self.preferences["outcomes"].keys()
                            if k.startswith(f"{task_type}|")]

            # Calculate scores for all paths
            path_analysis = {}
            for key in relevant_keys:
                _, path_type = key.split("|", 1)
                outcomes = self.preferences["outcomes"][key]

                success_rate = self.get_success_rate(task_type, path_type)
                avg_quality = self.get_average_quality(task_type, path_type)
                sample_size = len(outcomes)

                # Confidence based on sample size (caps at 20 samples)
                confidence = min(sample_size / 20.0, 1.0)

                path_analysis[path_type] = {
                    "success_rate": success_rate,
                    "avg_quality": avg_quality,
                    "sample_size": sample_size,
                    "confidence": confidence,
                    "combined_score": (0.6 * success_rate) + (0.4 * avg_quality)
                }

            # Find best path
            if path_analysis:
                best_path = max(path_analysis.items(), key=lambda x: x[1]["combined_score"])
                rules[task_type] = {
                    "recommended_path": best_path[0],
                    "confidence": best_path[1]["confidence"],
                    "success_rate": best_path[1]["success_rate"],
                    "avg_quality": best_path[1]["avg_quality"],
                    "sample_size": best_path[1]["sample_size"],
                    "all_paths": path_analysis
                }

        return rules

    def get_task_type_from_description(self, task_description: str) -> str:
        """
        Infer task type from description for preference lookup.
        Uses keyword matching against known categories.

        Args:
            task_description: The task description string

        Returns:
            Inferred task type category
        """
        description_lower = task_description.lower()

        # Known task categories with keywords
        categories = {
            "knowledge_infrastructure": ["knowledge", "graph", "ontology", "schema"],
            "feedback_loops": ["feedback", "loop", "monitor", "track"],
            "testing": ["test", "pytest", "coverage", "verify"],
            "refactoring": ["refactor", "cleanup", "improve", "optimize"],
            "bug_fix": ["fix", "bug", "error", "issue"],
            "feature": ["add", "create", "implement", "new"],
            "documentation": ["document", "readme", "doc", "comment"]
        }

        # Score each category
        scores = defaultdict(int)
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in description_lower:
                    scores[category] += 1

        # Return category with highest score, or "general" if no match
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        return "general"


def get_learner() -> PathPreferenceLearner:
    """Factory function to get a PathPreferenceLearner instance."""
    return PathPreferenceLearner()


if __name__ == "__main__":
    # Example usage and testing
    learner = PathPreferenceLearner()

    # Record some example outcomes
    learner.record_outcome("knowledge_infrastructure", "PLANNER->CODER->REVIEWER->DOCUMENTER", True, 1.0)
    learner.record_outcome("knowledge_infrastructure", "PLANNER->CODER->REVIEWER", True, 0.9)
    learner.record_outcome("bug_fix", "CODER->REVIEWER", True, 0.95)

    # Get recommendations
    print("Recommended path for knowledge_infrastructure:",
          learner.get_recommended_path("knowledge_infrastructure"))
    print("Recommended path for bug_fix:",
          learner.get_recommended_path("bug_fix"))

    # Generate decision rules
    rules = learner.generate_decision_rules()
    print("\nDecision Rules:")
    print(json.dumps(rules, indent=2))
