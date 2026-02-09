#!/usr/bin/env python3
"""
Performance Tracker - Track and analyze self-improvement metrics over sessions.

Implements metrics collection from grind sessions:
- Session completion time
- Success/failure rates
- Quality scores from critic
- Lessons learned per session

Enables empirical measurement of system improvement over time.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque
import statistics


class PerformanceTracker:
    """Tracks performance metrics across grind sessions."""

    def __init__(self, workspace: Path = None, history_file: str = "performance_history.json"):
        """Initialize tracker with workspace context."""
        self.workspace = workspace or Path(__file__).parent
        self.history_file = self.workspace / history_file
        self.metrics = self._load_history()

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load historical metrics from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self):
        """Persist metrics to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)

    def track_session(self, session_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record metrics from a completed grind session.

        Args:
            session_result: Dict with keys:
                - session_id: int
                - duration_seconds: float
                - success: bool
                - quality_score: float (0.0-1.0)
                - task_description: str
                - files_modified: List[str]
                - lessons_learned: List[str]

        Returns:
            Stored metric record with timestamp.
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_result.get("session_id"),
            "duration_seconds": session_result.get("duration_seconds", 0.0),
            "success": session_result.get("success", False),
            "quality_score": session_result.get("quality_score", 0.0),
            "task_description": session_result.get("task_description", ""),
            "files_modified": session_result.get("files_modified", []),
            "lessons_learned": session_result.get("lessons_learned", []),
        }

        self.metrics.append(record)
        self._save_history()
        return record

    def get_rolling_average(self, metric: str, window: int = 10) -> Optional[float]:
        """
        Calculate rolling average for a metric over recent sessions.

        Args:
            metric: Name of metric (duration_seconds, quality_score, etc.)
            window: Number of recent sessions to average

        Returns:
            Floating point average or None if insufficient data.
        """
        if not self.metrics or metric not in ["duration_seconds", "quality_score"]:
            return None

        # Get last `window` sessions
        recent = self.metrics[-window:]
        values = [m.get(metric, 0.0) for m in recent if metric in m]

        if not values:
            return None

        return statistics.mean(values)

    def get_success_rate(self, window: int = 10) -> Optional[float]:
        """
        Calculate success rate over recent sessions.

        Args:
            window: Number of recent sessions to consider

        Returns:
            Success rate as percentage (0.0-100.0) or None if insufficient data.
        """
        if not self.metrics:
            return None

        recent = self.metrics[-window:]
        if not recent:
            return None

        successes = sum(1 for m in recent if m.get("success", False))
        return (successes / len(recent)) * 100.0

    def compute_improvement_rate(self, metric: str = "quality_score", window: int = 10) -> Optional[float]:
        """
        Calculate percentage change in a metric over recent sessions.

        Positive values indicate improvement.

        Args:
            metric: Metric to analyze (quality_score, duration_seconds)
            window: Number of recent sessions to use for trend

        Returns:
            Percentage change ((current - baseline) / baseline * 100) or None if insufficient data.
        """
        if not self.metrics or len(self.metrics) < 2:
            return None

        recent = self.metrics[-window:]
        if len(recent) < 2:
            return None

        values = [m.get(metric, 0.0) for m in recent if metric in m]
        if len(values) < 2:
            return None

        baseline = values[0]
        current = values[-1]

        if baseline == 0:
            return None

        # For duration_seconds, lower is better (negative % improvement)
        # For quality_score, higher is better (positive % improvement)
        improvement = ((current - baseline) / abs(baseline)) * 100.0

        if metric == "duration_seconds":
            # Invert so negative duration improvement is positive
            improvement = -improvement

        return improvement

    def get_metrics_summary(self, window: int = 10) -> Dict[str, Any]:
        """
        Generate comprehensive metrics summary for recent sessions.

        Args:
            window: Number of recent sessions to include

        Returns:
            Dictionary with all key metrics and trends.
        """
        if not self.metrics:
            return {
                "total_sessions": 0,
                "recent_sessions": 0,
                "avg_duration_seconds": None,
                "avg_quality_score": None,
                "success_rate_percent": None,
                "quality_improvement_percent": None,
                "duration_improvement_percent": None,
                "total_lessons_learned": 0,
            }

        recent = self.metrics[-window:]
        total_lessons = sum(
            len(m.get("lessons_learned", []))
            for m in self.metrics
        )

        return {
            "total_sessions": len(self.metrics),
            "recent_sessions": len(recent),
            "avg_duration_seconds": self.get_rolling_average("duration_seconds", window),
            "avg_quality_score": self.get_rolling_average("quality_score", window),
            "success_rate_percent": self.get_success_rate(window),
            "quality_improvement_percent": self.compute_improvement_rate("quality_score", window),
            "duration_improvement_percent": self.compute_improvement_rate("duration_seconds", window),
            "total_lessons_learned": total_lessons,
        }

    def get_lesson_frequency(self, top_n: int = 10) -> Dict[str, int]:
        """
        Get most frequently learned lessons across all sessions.

        Args:
            top_n: Number of top lessons to return

        Returns:
            Dict mapping lesson text to frequency count.
        """
        lesson_counts = {}

        for record in self.metrics:
            for lesson in record.get("lessons_learned", []):
                lesson_counts[lesson] = lesson_counts.get(lesson, 0) + 1

        # Sort by frequency and return top N
        sorted_lessons = sorted(lesson_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_lessons[:top_n])

    def export_trends(self) -> Dict[str, Any]:
        """
        Export all metrics for trend analysis and visualization.

        Returns:
            Dictionary with timeseries data suitable for plotting.
        """
        return {
            "sessions": [
                {
                    "id": m.get("session_id"),
                    "timestamp": m.get("timestamp"),
                    "duration_seconds": m.get("duration_seconds"),
                    "quality_score": m.get("quality_score"),
                    "success": m.get("success"),
                }
                for m in self.metrics
            ],
            "summary": self.get_metrics_summary(),
            "top_lessons": self.get_lesson_frequency(),
        }
