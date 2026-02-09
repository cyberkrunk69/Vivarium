import csv
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "strategy_performance.csv")

# Ensure header exists
if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "epoch", "strategy", "success_metric", "learning_rate"])

def log_performance(epoch, strategy, success_metric, learning_rate=None):
    """
    Append a single performance record to the CSV log.
    """
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, epoch, strategy, success_metric, learning_rate])
import csv
import os
from datetime import datetime
from typing import List, Tuple

class StrategyPerformanceTracker:
    """
    Simple CSV logger that records per‑iteration performance of each
    strategy.  Used by experiments to generate the comparison plots.
    """

    def __init__(self, log_dir: str = "experiments/meta_learning_comparison"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(self.log_dir, f"performance_{timestamp}.csv")
        self._init_file()

    def _init_file(self) -> None:
        with open(self.log_path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["iteration", "strategy", "success", "learning_rate"]
            )

    def log(
        self,
        iteration: int,
        strategy: str,
        success: bool,
        learning_rate: float,
    ) -> None:
        with open(self.log_path, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([iteration, strategy, int(success), learning_rate])
def apply_strategy(self, strategy_name: str):
        """
        Placeholder hook that can be overridden by the main engine.
        The engine should map `strategy_name` to concrete actions
        (e.g., selecting a different decomposition tool or prompt template).
        """
        # No‑op in the base class – real implementation lives in MetaLearningEngine
        pass
import json
import os
from datetime import datetime

class StrategyPerformanceTracker:
    """
    Persists per‑strategy performance metrics to a JSON file.
    Enables later analysis of which tools/patterns are most effective.
    """

    def __init__(self, output_dir="strategy_logs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.file_path = os.path.join(
            self.output_dir,
            f"performance_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
        )
        self.records = []

    def log(self, strategy_name: str, task_id: str, metric: float):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "strategy": strategy_name,
            "task_id": task_id,
            "metric": metric,
        }
        self.records.append(entry)

    def flush(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)
import csv
import os
from datetime import datetime
from typing import List

LOG_FILE = "strategy_performance_log.csv"

def _ensure_log_file() -> None:
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "strategy",
                "task_id",
                "success_metric",
                "learning_rate",
            ])

def log_performance(
    strategy: str,
    task_id: str,
    success_metric: float,
    learning_rate: float,
) -> None:
    """
    Append a single performance record to the CSV log.
    """
    _ensure_log_file()
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            strategy,
            task_id,
            f"{success_metric:.5f}",
            f"{learning_rate:.6f}",
        ])

def read_logs() -> List[dict]:
    """
    Return the log as a list of dictionaries for downstream analysis.
    """
    if not os.path.isfile(LOG_FILE):
        return []
    with open(LOG_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
from collections import defaultdict
from typing import Optional

class StrategyPerformanceTracker:
    """
    Tracks cumulative reward and count for each strategy to compute
    average performance.
    """

    def __init__(self):
        # strategy -> [cumulative_reward, count]
        self._stats = defaultdict(lambda: [0.0, 0])

    def record(self, strategy: str, reward: float):
        """Add a new reward observation for a strategy."""
        cum, cnt = self._stats[strategy]
        self._stats[strategy] = [cum + reward, cnt + 1]

    def get_average(self, strategy: str) -> Optional[float]:
        """Return the average reward for a strategy, or None if never used."""
        cum, cnt = self._stats.get(strategy, (0.0, 0))
        if cnt == 0:
            return None
        return cum / cnt

    def get_best_strategy(self) -> Optional[str]:
        """Return the strategy with the highest average reward."""
        best, best_score = None, float("-inf")
        for strat, (cum, cnt) in self._stats.items():
            if cnt == 0:
                continue
            avg = cum / cnt
            if avg > best_score:
                best_score = avg
                best = strat
        return best
import json
import os
from datetime import datetime
from typing import Dict, List

class StrategyPerformanceTracker:
    """
    Persists strategy performance data to disk so that meta‑learning
    survives process restarts.
    """

    def __init__(self, storage_path: str = "meta_strategy_log.json"):
        self.storage_path = storage_path
        self._load()

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self.data: Dict[str, List[float]] = json.load(f)
        else:
            self.data = {}

    def _save(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def record(self, strategy: str, reward: float) -> None:
        self.data.setdefault(strategy, []).append(reward)
        self._save()

    def get_history(self, strategy: str) -> List[float]:
        return self.data.get(strategy, [])

    def export_csv(self, csv_path: str) -> None:
        import csv
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "strategy", "reward"])
            for strategy, rewards in self.data.items():
                for r in rewards:
                    writer.writerow([datetime.utcnow().isoformat(), strategy, r])
```
import collections
from typing import Dict, Any, List

class StrategyPerformanceTracker:
    """
    Tracks which tools/strategies succeed on which tasks and maintains a
    sliding window of recent success metrics for meta‑learning decisions.
    """

    def __init__(self):
        # List of dicts: each entry = {task_id, strategy, success, lr}
        self.history: List[Dict[str, Any]] = []
        # Simple counter of LR changes for diagnostics
        self.lr_changes: List[Dict[str, float]] = []

    def record(self, task_id: str, strategy: str, success: float, lr: float):
        self.history.append({
            "task_id": task_id,
            "strategy": strategy,
            "success": success,
            "lr": lr,
        })

    def recent_average_success(self, window: int) -> float:
        if not self.history:
            return 0.0
        recent = self.history[-window:]
        return sum(entry["success"] for entry in recent) / len(recent)

    def log_lr_change(self, old: float, new: float):
        self.lr_changes.append({"old_lr": old, "new_lr": new})

    def most_successful_strategies(self, top_n: int = 3) -> List[str]:
        """
        Return the top‑N strategies by average success across all recorded tasks.
        """
        agg: Dict[str, List[float]] = collections.defaultdict(list)
        for entry in self.history:
            agg[entry["strategy"]].append(entry["success"])
        avg_success = {s: sum(v) / len(v) for s, v in agg.items()}
        return [s for s, _ in sorted(avg_success.items(), key=lambda kv: kv[1], reverse=True)[:top_n]]

    def dump_history(self) -> List[Dict[str, Any]]:
        """Utility for experiment logging."""
        return self.history.copy()
import csv
import os
from datetime import datetime
from typing import Dict, List

class StrategyPerformanceTracker:
    """
    Persists per‑iteration performance data to a CSV file for later analysis.
    Each row contains:
        iteration, strategy_id, reward, learning_rate, timestamp
    """

    def __init__(self, output_dir: str = "experiments/meta_learning_comparison"):
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(output_dir, f"strategy_perf_{timestamp}.csv")
        self._write_header()

    def _write_header(self) -> None:
        with open(self.file_path, "w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["iteration", "strategy_id", "reward", "learning_rate", "timestamp"])

    def log(self, iteration: int, strategy_id: str, reward: float, learning_rate: float) -> None:
        with open(self.file_path, "a", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow([iteration, strategy_id, reward, learning_rate,
                             datetime.now().isoformat()])
```
import math
from collections import deque

class StrategyPerformanceTracker:
    """
    Tracks the performance of different learning strategies (e.g., tool choice,
    decomposition pattern, learning‑rate schedules) and suggests adaptations
    based on recent trends.
    """

    def __init__(self, window_size: int = 10):
        # Recent loss values (deque for O(1) pops)
        self.recent_losses = deque(maxlen=window_size)
        # Mapping strategy name -> cumulative improvement score
        self.strategy_scores = {}
        self.current_strategy = "default"
        self.base_lr = 0.01
        self.min_lr = 1e-5
        self.max_lr = 0.1

    def log_performance(self, iteration: int, loss: float, strategy: str):
        """Record loss for the current iteration and update strategy scores."""
        self.recent_losses.append(loss)
        # Simple improvement metric: negative loss delta
        if len(self.recent_losses) > 1:
            improvement = self.recent_losses[-2] - loss
            self.strategy_scores.setdefault(strategy, 0.0)
            self.strategy_scores[strategy] += improvement

    def suggest_learning_rate(self, current_lr: float) -> float:
        """Adapt learning rate based on loss trend (EMA of recent losses)."""
        if not self.recent_losses:
            return current_lr
        # Exponential moving average of loss
        ema = sum(loss * (0.9 ** i) for i, loss in enumerate(reversed(self.recent_losses)))
        # If loss is decreasing, be more aggressive; otherwise, be conservative
        if self.recent_losses[-1] < self.recent_losses[0]:
            new_lr = min(self.max_lr, current_lr * 1.05)
        else:
            new_lr = max(self.min_lr, current_lr * 0.7)
        return new_lr

    def suggest_strategy(self) -> str:
        """
        Choose the strategy with the highest cumulative improvement.
        Falls back to the current strategy if no clear winner.
        """
        if not self.strategy_scores:
            return self.current_strategy
        best_strategy = max(self.strategy_scores.items(), key=lambda kv: kv[1])[0]
        # Switch only if the best strategy is noticeably better
        if self.strategy_scores[best_strategy] - self.strategy_scores.get(self.current_strategy, 0) > 0.01:
            self.current_strategy = best_strategy
        return self.current_strategy