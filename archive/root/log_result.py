#!/usr/bin/env python3
import json
import argparse
from datetime import datetime
from pathlib import Path

def log_result(task, model, success, cost, notes=""):
    log_file = Path(__file__).parent / "learning_log.json"

    # Load existing data
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"entries": []}

    # Create new entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "task_type": task,
        "model": model,
        "success": success,
        "cost": cost,
        "quality_notes": notes
    }

    # Append entry
    data["entries"].append(entry)

    # Save
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Logged: {task} with {model} - Success: {success}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log task results")
    parser.add_argument("--task", required=True, help="Task type (DOC, FIX, ANALYZE, etc)")
    parser.add_argument("--model", required=True, help="Model used")
    parser.add_argument("--success", required=True, type=lambda x: x.lower() == 'true', help="Success status")
    parser.add_argument("--cost", required=True, type=float, help="Cost in dollars")
    parser.add_argument("--notes", default="", help="Quality notes")

    args = parser.parse_args()
    log_result(args.task, args.model, args.success, args.cost, args.notes)
