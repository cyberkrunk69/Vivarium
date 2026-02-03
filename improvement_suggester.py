"""
Self-modification suggestion system.
Analyzes learned lessons and suggests improvements for the AI agent.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Any
from datetime import datetime
from performance_tracker import PerformanceTracker


class ImprovementSuggester:
    """Analyzes patterns in learned lessons and generates improvement suggestions."""

    def __init__(self, lessons_path: str = "learned_lessons.json"):
        """Initialize suggester with lessons file path."""
        self.lessons_path = Path(lessons_path)
        self.lessons = self._load_lessons()

    def _load_lessons(self) -> List[Dict[str, Any]]:
        """Load lessons from JSON file."""
        if not self.lessons_path.exists():
            return []
        try:
            with open(self.lessons_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def analyze_performance_trends(self, tracker: PerformanceTracker = None) -> Dict[str, Any]:
        """
        Analyze performance trends from tracker and identify declining metrics.

        Args:
            tracker: PerformanceTracker instance. If None, creates default.

        Returns:
            Dictionary with performance analysis including:
            - rolling_averages: Current metric averages
            - improvement_rates: Trend direction for quality and duration
            - declining_metrics: List of metrics showing negative trends
            - performance_health: Overall performance status
        """
        if tracker is None:
            tracker = PerformanceTracker()

        metrics_summary = tracker.get_metrics_summary()

        analysis = {
            "rolling_averages": {
                "quality_score": metrics_summary.get("avg_quality_score"),
                "duration_seconds": metrics_summary.get("avg_duration_seconds"),
            },
            "improvement_rates": {
                "quality_percent": metrics_summary.get("quality_improvement_percent"),
                "duration_percent": metrics_summary.get("duration_improvement_percent"),
            },
            "success_rate_percent": metrics_summary.get("success_rate_percent"),
            "declining_metrics": [],
            "performance_health": "stable",
        }

        # Identify declining metrics
        quality_improvement = analysis["improvement_rates"]["quality_percent"]
        duration_improvement = analysis["improvement_rates"]["duration_percent"]

        if quality_improvement is not None and quality_improvement < 0:
            analysis["declining_metrics"].append({
                "metric": "quality_score",
                "trend_percent": quality_improvement,
                "suggestion": "Quality score is declining - review recent session failures and implement quality checks",
            })

        if duration_improvement is not None and duration_improvement < -5:
            analysis["declining_metrics"].append({
                "metric": "duration_seconds",
                "trend_percent": duration_improvement,
                "suggestion": "Session duration is increasing - optimize workflow and reduce unnecessary operations",
            })

        # Determine health status
        if analysis["declining_metrics"]:
            analysis["performance_health"] = "declining"
        elif quality_improvement is not None and quality_improvement > 10:
            analysis["performance_health"] = "improving"

        return analysis

    def analyze_patterns(self, lessons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify recurring issues and patterns in lessons.

        Returns:
            Dictionary with:
            - error_categories: Counter of task categories with most lessons
            - common_issues: Most frequently repeated lesson themes
            - importance_distribution: High-importance lesson density
            - skill_gaps: Task categories with most failures
        """
        if not lessons:
            return {}

        patterns = {
            "error_categories": Counter(),
            "common_themes": Counter(),
            "importance_distribution": {"high": 0, "medium": 0, "low": 0},
            "skill_gaps": [],
            "total_lessons": len(lessons),
        }

        # Analyze error categories
        for lesson in lessons:
            category = lesson.get("task_category", "unknown")
            patterns["error_categories"][category] += 1

            # Track importance
            importance = lesson.get("importance", 3)
            if importance >= 4:
                patterns["importance_distribution"]["high"] += 1
            elif importance >= 3:
                patterns["importance_distribution"]["medium"] += 1
            else:
                patterns["importance_distribution"]["low"] += 1

            # Extract common themes from lesson text
            lesson_text = lesson.get("lesson", "").lower()
            if "read" in lesson_text:
                patterns["common_themes"]["file_reading"] += 1
            if "parallel" in lesson_text or "concurrency" in lesson_text:
                patterns["common_themes"]["parallelization"] += 1
            if "error" in lesson_text or "validation" in lesson_text:
                patterns["common_themes"]["error_handling"] += 1
            if "todo" in lesson_text or "task" in lesson_text:
                patterns["common_themes"]["task_management"] += 1
            if "codebase" in lesson_text or "exploration" in lesson_text:
                patterns["common_themes"]["codebase_navigation"] += 1

        # Identify skill gaps (categories with most lessons = most problems)
        patterns["skill_gaps"] = patterns["error_categories"].most_common(3)

        return patterns

    def suggest_improvements(self, patterns: Dict[str, Any], tracker: PerformanceTracker = None) -> List[Dict[str, Any]]:
        """
        Generate actionable improvement suggestions based on analyzed patterns and performance trends.

        Args:
            patterns: Pattern analysis from analyze_patterns()
            tracker: Optional PerformanceTracker instance for performance-based suggestions

        Returns:
            List of suggestion dictionaries with priority and rationale.
        """
        suggestions = []

        if not patterns:
            return suggestions

        # Analyze performance trends if tracker available
        performance_analysis = None
        if tracker is not None:
            performance_analysis = self.analyze_performance_trends(tracker)

            # Add performance-based suggestions for declining metrics
            if performance_analysis.get("declining_metrics"):
                for declining in performance_analysis["declining_metrics"]:
                    suggestions.append({
                        "suggestion": declining["suggestion"],
                        "category": "performance_optimization",
                        "rationale": f"{declining['metric']} trend: {declining['trend_percent']:.1f}%",
                        "estimated_effort": "medium",
                    })

        # Suggestion 1: Address high-importance categories
        high_impact_categories = patterns.get("importance_distribution", {}).get("high", 0)
        if high_impact_categories > 5:
            suggestions.append({
                "suggestion": "Implement proactive validation hooks for high-risk operations",
                "category": "error_prevention",
                "rationale": f"There are {high_impact_categories} high-importance lessons indicating systemic issues in error handling",
                "estimated_effort": "medium",
            })

        # Suggestion 2: Improve task management if it's a common theme
        common_themes = patterns.get("common_themes", {})
        if common_themes.get("task_management", 0) >= 2:
            suggestions.append({
                "suggestion": "Add automatic task validation before marking completion",
                "category": "task_management",
                "rationale": "Task management is a recurring issue - add validation to prevent incomplete task marking",
                "estimated_effort": "low",
            })

        # Suggestion 3: Improve codebase exploration efficiency
        if common_themes.get("codebase_navigation", 0) >= 2:
            suggestions.append({
                "suggestion": "Create codebase indexing system for faster pattern discovery",
                "category": "efficiency",
                "rationale": "Codebase navigation is frequently mentioned - indexing can reduce exploration time",
                "estimated_effort": "high",
            })

        # Suggestion 4: Enhance parallel execution
        if common_themes.get("parallelization", 0) >= 1:
            suggestions.append({
                "suggestion": "Audit all multi-tool operations for parallelization opportunities",
                "category": "efficiency",
                "rationale": "Parallelization is mentioned - systematically identify bottlenecks in sequential operations",
                "estimated_effort": "medium",
            })

        # Suggestion 5: Strengthen error handling
        if common_themes.get("error_handling", 0) >= 2:
            suggestions.append({
                "suggestion": "Implement comprehensive error recovery patterns",
                "category": "robustness",
                "rationale": "Error handling is a recurring lesson - implement defensive strategies early",
                "estimated_effort": "medium",
            })

        # Suggestion 6: Skill gap mitigation
        skill_gaps = patterns.get("skill_gaps", [])
        if skill_gaps:
            top_gap = skill_gaps[0]
            suggestions.append({
                "suggestion": f"Create specialized handler for '{top_gap[0]}' tasks",
                "category": "capability_enhancement",
                "rationale": f"'{top_gap[0]}' has the most lessons ({top_gap[1]} issues) - dedicated handling can reduce errors",
                "estimated_effort": "high",
            })

        return suggestions

    def prioritize_suggestions(
        self, suggestions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Rank suggestions by impact and effort.

        Returns:
            Sorted list with priority scores.
        """
        # Effort scoring
        effort_score = {"low": 3, "medium": 2, "high": 1}

        for suggestion in suggestions:
            effort = suggestion.get("estimated_effort", "medium")
            suggestion["priority_score"] = effort_score.get(effort, 2)

        # Sort by priority (higher score = higher priority)
        return sorted(
            suggestions, key=lambda x: x.get("priority_score", 0), reverse=True
        )

    def generate_full_report(self, tracker: PerformanceTracker = None) -> Dict[str, Any]:
        """Generate complete improvement analysis report including performance trends."""
        patterns = self.analyze_patterns(self.lessons)

        # Use provided tracker or create default
        if tracker is None:
            tracker = PerformanceTracker()

        performance_analysis = self.analyze_performance_trends(tracker)
        suggestions = self.suggest_improvements(patterns, tracker)
        prioritized = self.prioritize_suggestions(suggestions)

        return {
            "generated_at": datetime.now().isoformat(),
            "total_lessons_analyzed": len(self.lessons),
            "performance_analysis": performance_analysis,
            "patterns": patterns,
            "suggestions": prioritized,
            "next_steps": [s["suggestion"] for s in prioritized[:3]],
        }


def main():
    """Run the improvement suggester and output results."""
    suggester = ImprovementSuggester("learned_lessons.json")
    tracker = PerformanceTracker()

    # Generate analysis
    report = suggester.generate_full_report(tracker)

    # Save to improvement_queue.json
    output_path = Path("improvement_queue.json")
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[OK] Generated improvement suggestions: {len(report['suggestions'])} suggestions")
    print(f"[OK] Saved to: {output_path}")

    # Display top 3 suggestions
    print("\nTop 3 Priorities:")
    for i, suggestion in enumerate(report["suggestions"][:3], 1):
        print(f"{i}. {suggestion['suggestion']}")
        print(f"   Priority: {suggestion['priority_score']}/3")
        print(f"   Effort: {suggestion['estimated_effort']}\n")


if __name__ == "__main__":
    main()
