import json
import glob
import os
from datetime import datetime

PROGRESS_MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PROGRESS.md"))
ACTIVITY_LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "activity_logs"))
LEGACY_GRIND_LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "grind_logs"))
LEARNED_LESSONS_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "learned_lessons.json"))


def collect_metrics():
    # Prefer neutral naming, but keep legacy fallback for older runs.
    log_files = glob.glob(os.path.join(ACTIVITY_LOGS_DIR, "*.json"))
    if not log_files:
        log_files = glob.glob(os.path.join(LEGACY_GRIND_LOGS_DIR, "*.json"))
    total_sessions = len(log_files)
    successes = 0
    failures_by_category = {}
    total_duration = 0.0

    for log_path in log_files:
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # Skip malformed logs
            continue

        returncode = data.get("returncode")
        duration = data.get("duration_seconds")  # assume duration stored in seconds
        if isinstance(duration, (int, float)):
            total_duration += duration

        if returncode == 0:
            successes += 1
        else:
            # categorize failure; fallback to generic if not provided
            category = data.get("failure_category", "unknown")
            failures_by_category[category] = failures_by_category.get(category, 0) + 1

    avg_duration = total_duration / total_sessions if total_sessions else 0
    success_rate = (successes / total_sessions) * 100 if total_sessions else 0

    # Sort failures by frequency descending
    common_failures = sorted(failures_by_category.items(), key=lambda kv: kv[1], reverse=True)

    return {
        "total_sessions": total_sessions,
        "successes": successes,
        "failures_by_category": failures_by_category,
        "avg_duration": avg_duration,
        "success_rate": success_rate,
        "common_failures": common_failures,
    }


def update_progress_md(metrics):
    # Build the health metrics markdown block
    common_failures_md = ", ".join(
        f"`{cat}` ({cnt})" for cat, cnt in metrics["common_failures"][:5]
    ) or "None"

    health_section = (
        "\n## Health Metrics\n"
        f"- Success rate: {metrics['success_rate']:.2f}% ({metrics['successes']}/{metrics['total_sessions']})\n"
        f"- Avg duration: {metrics['avg_duration']:.2f}s\n"
        f"- Common failures: {common_failures_md}\n"
    )

    # Read existing PROGRESS.md
    if not os.path.exists(PROGRESS_MD):
        existing_content = ""
    else:
        with open(PROGRESS_MD, "r", encoding="utf-8") as f:
            existing_content = f.read()

    # Replace existing Health Metrics section if present, otherwise append
    if "## Health Metrics" in existing_content:
        # Split at the start of the section and keep everything before it
        before, _ = existing_content.split("## Health Metrics", 1)
        new_content = before + health_section
    else:
        new_content = existing_content.rstrip() + health_section

    with open(PROGRESS_MD, "w", encoding="utf-8") as f:
        f.write(new_content)


def append_learned_lesson():
    lesson = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "lesson": "Added failure tracking to PROGRESS.md for swarm health visibility.",
        "details": "Metrics include success rate, average session duration, and most common failure categories."
    }

    # Load existing lessons or start a new list
    if os.path.exists(LEARNED_LESSONS_JSON):
        try:
            with open(LEARNED_LESSONS_JSON, "r", encoding="utf-8") as f:
                lessons = json.load(f)
            if not isinstance(lessons, list):
                lessons = []
        except Exception:
            lessons = []
    else:
        lessons = []

    lessons.append(lesson)

    with open(LEARNED_LESSONS_JSON, "w", encoding="utf-8") as f:
        json.dump(lessons, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    metrics = collect_metrics()
    update_progress_md(metrics)
    append_learned_lesson()