import json
import glob
import os
import datetime

def update_health_metrics():
    # Gather all grind log JSON files
    log_files = glob.glob(os.path.join('grind_logs', '*.json'))
    total_sessions = len(log_files)

    successful = 0
    durations = []
    failure_counts = {}

    for log_path in log_files:
        try:
            with open(log_path, 'r') as f:
                data = json.load(f)
        except Exception:
            # Skip unreadable or malformed logs
            continue

        returncode = data.get('returncode')
        if returncode == 0:
            successful += 1
        else:
            # Categorise failures; default to 'unknown' if not provided
            category = data.get('failure_category', 'unknown')
            failure_counts[category] = failure_counts.get(category, 0) + 1

        # Record duration if present
        duration = data.get('duration_seconds')
        if isinstance(duration, (int, float)):
            durations.append(duration)

    # Compute health metrics
    success_rate = (successful / total_sessions * 100) if total_sessions else 0.0
    avg_duration = (sum(durations) / len(durations)) if durations else 0.0

    # Determine most common failure categories (top 3)
    common_failures = sorted(failure_counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
    common_failure_list = [cat for cat, _ in common_failures]

    # Append health metrics section to PROGRESS.md
    progress_path = 'PROGRESS.md'
    with open(progress_path, 'a') as md:
        md.write('\n## Health Metrics\n')
        md.write(f'- Success rate: {success_rate:.1f}%\n')
        md.write(f'- Avg duration: {avg_duration:.1f}s\n')
        md.write(f'- Common failures: {", ".join(common_failure_list) if common_failure_list else "None"}\n')

    # Record the metrics as a learned lesson
    lessons_path = 'learned_lessons.json'
    lesson_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "health_metrics": {
            "total_sessions": total_sessions,
            "successful_sessions": successful,
            "success_rate_percent": round(success_rate, 1),
            "average_duration_seconds": round(avg_duration, 1),
            "common_failures": common_failure_list
        }
    }

    try:
        with open(lessons_path, 'r') as lf:
            lessons = json.load(lf)
    except Exception:
        lessons = []

    lessons.append(lesson_entry)

    with open(lessons_path, 'w') as lf:
        json.dump(lessons, lf, indent=2)