#!/usr/bin/env python3
"""
Integration module: Wire PerformanceTracker to ImprovementSuggester.

This connects performance tracking with the improvement suggestion system,
automatically generating improvement reports after each wave of grind sessions.
"""

import json
from pathlib import Path
from datetime import datetime
from performance_tracker import PerformanceTracker
from improvement_suggester import ImprovementSuggester


def connect_tracker_to_suggester(
    tracker: PerformanceTracker = None,
    suggester: ImprovementSuggester = None,
    workspace: Path = None
) -> dict:
    """
    Wire performance tracker to improvement suggester for post-wave analysis.

    Args:
        tracker: PerformanceTracker instance. If None, creates default.
        suggester: ImprovementSuggester instance. If None, creates default.
        workspace: Workspace path for saving reports.

    Returns:
        Dictionary with report data and file path.
    """
    # Initialize components if not provided
    if workspace is None:
        workspace = Path(__file__).parent

    if tracker is None:
        tracker = PerformanceTracker(workspace)

    if suggester is None:
        suggester = ImprovementSuggester(str(workspace / "learned_lessons.json"))

    # Generate improvement report with performance trends
    report = suggester.generate_full_report(tracker)

    # Save report to improvement_reports/ directory
    reports_dir = workspace / "improvement_reports"
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"improvement_report_{timestamp}.json"

    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[OK] Generated improvement report: {report_file}")
    print(f"[OK] Total suggestions: {len(report.get('suggestions', []))}")

    # Extract top suggestion for next wave planning
    top_suggestions = report.get("suggestions", [])[:3]
    if top_suggestions:
        print(f"[OK] Top priority suggestion: {top_suggestions[0]['suggestion']}")

    return {
        "report": report,
        "report_file": str(report_file),
        "top_suggestions": top_suggestions,
        "generated_at": report.get("generated_at"),
    }


def post_wave_analysis(wave_number: int, workspace: Path = None) -> dict:
    """
    Run post-wave analysis after grind sessions complete.

    This is the main entry point called after each wave finishes.

    Args:
        wave_number: Current wave number for tracking
        workspace: Workspace path

    Returns:
        Analysis results with suggestions for next wave
    """
    if workspace is None:
        workspace = Path(__file__).parent

    print(f"\n{'='*60}")
    print(f"  POST-WAVE ANALYSIS - Wave {wave_number}")
    print(f"{'='*60}")

    # Wire tracker to suggester
    result = connect_tracker_to_suggester(workspace=workspace)

    # Display performance trends
    report = result["report"]
    perf_analysis = report.get("performance_analysis", {})

    print(f"\nPerformance Health: {perf_analysis.get('performance_health', 'unknown').upper()}")

    rolling_avgs = perf_analysis.get("rolling_averages", {})
    print(f"  Avg Quality: {rolling_avgs.get('quality_score', 0.0):.2f}")
    print(f"  Avg Duration: {rolling_avgs.get('duration_seconds', 0.0):.1f}s")

    improvement_rates = perf_analysis.get("improvement_rates", {})
    quality_trend = improvement_rates.get("quality_percent")
    duration_trend = improvement_rates.get("duration_percent")

    if quality_trend is not None:
        print(f"  Quality Trend: {quality_trend:+.1f}%")
    if duration_trend is not None:
        print(f"  Duration Trend: {duration_trend:+.1f}%")

    # Display top suggestions
    print(f"\nTop 3 Suggestions for Next Wave:")
    for i, suggestion in enumerate(result["top_suggestions"], 1):
        print(f"  {i}. {suggestion['suggestion']}")
        print(f"     Category: {suggestion['category']}, Effort: {suggestion['estimated_effort']}")

    print(f"\n{'='*60}\n")

    return result


if __name__ == "__main__":
    # Test integration
    result = connect_tracker_to_suggester()
    print(f"Integration test complete. Report saved to: {result['report_file']}")
