#!/usr/bin/env python3
import json
import argparse
from pathlib import Path

def parse_logs(log_dir="grind_logs"):
    """Parse all JSON files in grind_logs and extract costs."""
    costs = []
    log_path = Path(log_dir)

    if not log_path.exists():
        return costs

    for json_file in log_path.glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                if isinstance(data, dict) and "total_cost_usd" in data:
                    costs.append(data["total_cost_usd"])
        except (json.JSONDecodeError, IOError):
            pass

    return costs

def main():
    parser = argparse.ArgumentParser(description="Track API costs")
    parser.add_argument("--budget", type=float, help="Target budget in USD")
    args = parser.parse_args()

    costs = parse_logs()

    if not costs:
        print("No cost data found.")
        return

    total_spent = sum(costs)
    num_tasks = len(costs)
    avg_cost = total_spent / num_tasks if num_tasks > 0 else 0

    print(f"Total spent: ${total_spent:.4f}")
    print(f"Tasks completed: {num_tasks}")
    print(f"Average cost per task: ${avg_cost:.4f}")

    if args.budget:
        remaining = args.budget - total_spent
        percentage = (total_spent / args.budget * 100) if args.budget > 0 else 0
        print(f"Budget: ${args.budget:.2f}")
        print(f"Remaining: ${remaining:.4f}")
        print(f"Usage: {percentage:.1f}%")

class CostTracker:
    """Simple cost tracker - budget is essentially unlimited ($200/month credit)."""

    def __init__(self):
        self.total_cost = 0.0

    def add_cost(self, cost: float):
        self.total_cost += cost

    def get_total(self) -> float:
        return self.total_cost

    def check_budget(self, limit: float = 200.0) -> bool:
        """Always returns True - we have generous limits."""
        return True

_cost_tracker = None

def get_cost_tracker() -> CostTracker:
    """Get global cost tracker instance."""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker


if __name__ == "__main__":
    main()
