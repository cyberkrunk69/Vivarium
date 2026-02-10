import random
import time
from strategy_performance_tracker import StrategyPerformanceTracker
import math
from collections import defaultdict

class MetaLearningEngine:
    """
    Core engine that tracks strategy performance, adapts learning rates,
    and selects high‑value learning opportunities.
    """

    def __init__(self):
        # Statistics for each strategy: {'count': int, 'cumulative_success': float}
        self.strategy_stats = defaultdict(lambda: {"count": 0, "cumulative_success": 0.0})
        # Base learning rate – can be tuned by meta‑optimization
        self.base_lr = 0.01
        # Minimum and maximum learning rates for safety
        self.min_lr = 1e-5
        self.max_lr = 0.1
        # Exploration factor for strategy selection
        self.epsilon = 0.2

    # ------------------------------------------------------------------
    # Strategy selection (ε‑greedy)
    # ------------------------------------------------------------------
    def select_strategy(self, task):
        """
        Choose a learning strategy for the given task.
        Currently supports a simple set of named strategies; can be expanded.
        """
        available_strategies = ["default", "gradient_accumulation", "curriculum", "meta_rl"]
        # Exploration
        if random.random() < self.epsilon:
            return random.choice(available_strategies)

        # Exploitation: pick the strategy with highest average success
        best_strategy = "default"
        best_score = -math.inf
        for strat in available_strategies:
            stats = self.strategy_stats[strat]
            if stats["count"] == 0:
# Initialize performance tracker for meta‑learning of strategies
        self.tracker = StrategyPerformanceTracker()
                avg = 0.0
            else:
                avg = stats["cumulative_success"] / stats["count"]
            if avg > best_score:
                best_score = avg
def _adjust_learning_rate(self, recent_success: float):
        """
        Simple meta‑learning rule:
        - If recent success (average reward/accuracy) > 0.8 → increase LR
        - If recent success < 0.5 → decrease LR
        - Clamp between min_lr and max_lr
        """
        if recent_success > 0.8:
            new_lr = min(self.max_lr, self.learning_rate * self.lr_step)
        elif recent_success < 0.5:
            new_lr = max(self.min_lr, self.learning_rate / self.lr_step)
        else:
            new_lr = self.learning_rate  # keep unchanged

        if new_lr != self.learning_rate:
            self.base_learner.set_learning_rate(new_lr)
# Adaptive learning rate: ask the tracker for the next LR based on recent performance
self.learning_rate = self.tracker.suggest_learning_rate(self.learning_rate)
            self.tracker.log_lr_change(old=self.learning_rate, new=new_lr)
                best_strategy = strat
        return best_strategy

    # ------------------------------------------------------------------
    # Record outcome of a strategy execution
    # ------------------------------------------------------------------
    def record_strategy(self, strategy, success_metric):
        """
        Update internal statistics for a strategy.
        `success_metric` should be a positive float where larger means better.
        """
        stats = self.strategy_stats[strategy]
        stats["count"] += 1
        stats["cumulative_success"] += success_metric

    # ------------------------------------------------------------------
    # Adapt learning rate based on recent success
    # ------------------------------------------------------------------
    def adapt_learning_rate(self, recent_success):
        """
        Simple adaptive rule: increase LR if success is high, decrease otherwise.
        Uses a moving‑average style update.
        """
        target = 0.8  # desired success level (can be tuned)
        error = target - recent_success
        # Proportional adjustment
        lr_change = 0.1 * error * self.base_lr
        self.base_lr = max(self.min_lr, min(self.max_lr, self.base_lr + lr_change))

    # ------------------------------------------------------------------
    # Expose current learning rate for downstream learners
    # ------------------------------------------------------------------
    def get_learning_rate(self):
        return self.base_lr

    # ------------------------------------------------------------------
    # Meta‑optimization hook (placeholder for future extensions)
    # ------------------------------------------------------------------
    def meta_optimize(self):
        """
        Placeholder for higher‑order optimization of the meta‑learning loop
        (e.g., evolving the epsilon, target success, or strategy set).
        """
        pass
import random
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

class MetaLearningEngine:
    """
    Core engine for meta‑learning the learning process itself.
    It tracks which strategies (e.g., tool choices, decomposition patterns)
    succeed, adapts the learning rate, and suggests high‑value learning
    opportunities.
    """

    def __init__(self, state_path: str = "meta_engine_state.json"):
        # Statistics: {strategy_name: {"success": int, "attempts": int}}
        self.strategy_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "attempts": 0}
        )
        self.base_lr: float = 0.01          # starting learning rate
        self.min_lr: float = 1e-5
        self.max_lr: float = 0.1
        self.lr: float = self.base_lr
        self.state_path = state_path
        self._load_state()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def update(self, strategy: str, success: bool) -> None:
        """
        Record the outcome of a single learning iteration.
        """
        stats = self.strategy_stats[strategy]
        stats["attempts"] += 1
        if success:
            stats["success"] += 1
        self._adapt_learning_rate()
# After the iteration, record performance and possibly adapt strategy
        loss = self.run_iteration(iteration)
        self.tracker.log_performance(iteration, loss, self.current_strategy)
        # Optionally switch strategy if the tracker recommends a better one
        new_strategy = self.tracker.suggest_strategy()
        if new_strategy != self.current_strategy:
            self.current_strategy = new_strategy
            self.apply_strategy(new_strategy)  # user‑defined hook to reconfigure the engine
        self._save_state()

    def select_strategy(self, candidates: List[str]) -> str:
        """
        Choose a strategy from *candidates*.
        Uses a simple epsilon‑greedy approach favouring historically
        successful strategies.
        """
        epsilon = 0.1
        if random.random() < epsilon:
            return random.choice(candidates)

        # Choose the candidate with highest success rate
        best = None
        best_rate = -1.0
        for cand in candidates:
            stats = self.strategy_stats.get(cand, {"success": 0, "attempts": 0})
            attempts = stats["attempts"]
            success = stats["success"]
            rate = success / attempts if attempts > 0 else 0.0
            if rate > best_rate:
                best_rate = rate
                best = cand
        return best if best is not None else random.choice(candidates)

    def get_learning_rate(self) -> float:
        """Return the current learning rate."""
        return self.lr

    def identify_high_value_opportunities(self) -> List[Tuple[str, float]]:
        """
        Simple heuristic: return strategies whose success rate is above
        the median but still have low attempt counts (i.e., promising but
        under‑explored).
        """
        if not self.strategy_stats:
            return []

        # Compute median success rate
        rates = [
            (s, stats["success"] / stats["attempts"] if stats["attempts"] > 0 else 0.0)
            for s, stats in self.strategy_stats.items()
        ]
        sorted_rates = sorted(rates, key=lambda x: x[1])
        median_idx = len(sorted_rates) // 2
        median_rate = sorted_rates[median_idx][1]

        # Return promising under‑explored strategies
        opportunities = [
            (s, r) for s, r in rates
            if r > median_rate and self.strategy_stats[s]["attempts"] < 5
        ]
        return opportunities

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _adapt_learning_rate(self) -> None:
        """
        Adjust the learning rate based on recent aggregate success.
        If overall success rate > 0.7 → increase lr (up to max_lr).
        If < 0.3 → decrease lr (down to min_lr).
        """
        total_attempts = sum(v["attempts"] for v in self.strategy_stats.values())
        total_success = sum(v["success"] for v in self.strategy_stats.values())
        if total_attempts == 0:
            return

        success_rate = total_success / total_attempts
        if success_rate > 0.7:
            self.lr = min(self.lr * 1.2, self.max_lr)
        elif success_rate < 0.3:
            self.lr = max(self.lr * 0.8, self.min_lr)

    def _save_state(self) -> None:
        """Persist strategy statistics and learning rate."""
        state = {
            "strategy_stats": dict(self.strategy_stats),
            "lr": self.lr,
        }
        try:
            with open(self.state_path, "w") as f:
                json.dump(state, f, indent=2)
        except IOError:
            pass  # Silently ignore persistence errors

    def _load_state(self) -> None:
        """Load persisted state if it exists."""
        if not os.path.isfile(self.state_path):
            return
        try:
            with open(self.state_path, "r") as f:
                state = json.load(f)
                self.strategy_stats = defaultdict(
                    lambda: {"success": 0, "attempts": 0},
                    {k: v for k, v in state.get("strategy_stats", {}).items()}
                )
                self.lr = state.get("lr", self.base_lr)
        except (IOError, json.JSONDecodeError):
            pass
import random
import logging
from lesson_recorder import LessonRecorder
from collections import defaultdict

logger = logging.getLogger(__name__)

class MetaLearningEngine:
    """
    Core engine that meta‑learns which learning strategies (e.g., tool choice,
    task decomposition, curriculum ordering) work best and adapts the learning
    rate accordingly.
    """

    def __init__(self, base_lr: float = 1e-3, min_lr: float = 1e-5, max_lr: float = 1e-2):
        self.base_lr = base_lr
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.strategy_success = defaultdict(lambda: {"wins": 0, "tries": 0})
        self.recent_performance = []          # store last N task scores
        self.window_size = 20                  # number of recent tasks to consider
        self.lr_adjust_factor = 0.9            # factor to shrink/expand LR

    # ------------------------------------------------------------------ #
    # Strategy tracking
    # ------------------------------------------------------------------ #
    def record_outcome(self, strategy_name: str, success_metric: float):
        """
        Record the outcome of a single learning episode.
        success_metric should be a scalar where higher is better (e.g., validation accuracy).
        """
        stats = self.strategy_success[strategy_name]
        stats["wins"] += success_metric
        stats["tries"] += 1

        # keep a rolling window of recent performance for LR adaptation
        self.recent_performance.append(success_metric)
        if len(self.recent_performance) > self.window_size:
            self.recent_performance.pop(0)

        logger.debug(
            f"Strategy '{strategy_name}' updated: {stats['wins']}/{stats['tries']} (cumulative score)."
        )

    # ------------------------------------------------------------------ #
    # Strategy selection
    # ------------------------------------------------------------------ #
    def select_strategy(self, candidate_strategies):
        """
        Choose a strategy based on historic performance.
        Uses a simple epsilon‑greedy approach to keep exploration.
        """
        epsilon = 0.2  # 20 % chance to explore
        if random.random() < epsilon or not self.strategy_success:
            chosen = random.choice(candidate_strategies)
            logger.debug(f"Exploring strategy: {chosen}")
            return chosen

        # exploit: pick the strategy with highest average score
        avg_scores = {
            s: self.strategy_success[s]["wins"] / max(1, self.strategy_success[s]["tries"])
            for s in candidate_strategies
            if s in self.strategy_success
        }
        if not avg_scores:
            chosen = random.choice(candidate_strategies)
            logger.debug(f"No historic data, random pick: {chosen}")
            return chosen

        best = max(avg_scores, key=avg_scores.get)
        logger.debug(f"Exploiting best strategy: {best} (avg score {avg_scores[best]:.4f})")
        return best

    # ------------------------------------------------------------------ #
    # Learning‑rate adaptation
    # ------------------------------------------------------------------ #
    def adapt_learning_rate(self):
        """
        Adjust the base learning rate based on recent performance trends.
        If performance is improving, gently increase LR; if deteriorating,
        decrease it. Returns the new learning rate.
        """
        if len(self.recent_performance) < self.window_size:
            # not enough data yet – keep base LR
            return self.base_lr

        # simple trend: compare mean of first half vs second half
        half = self.window_size // 2
        first_half = sum(self.recent_performance[:half]) / half
        second_half = sum(self.recent_performance[half:]) / (self.window_size - half)

        if second_half > first_half:
            # improve → increase LR (but cap)
            new_lr = min(self.base_lr * (1 / self.lr_adjust_factor), self.max_lr)
        else:
            # degrade → decrease LR (but floor)
            new_lr = max(self.base_lr * self.lr_adjust_factor, self.min_lr)

        if new_lr != self.base_lr:
            logger.info(f"Learning rate adapted from {self.base_lr:.6f} to {new_lr:.6f}")
            self.base_lr = new_lr
        return self.base_lr
import random
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

class MetaLearningEngine:
    """
    Core engine that tracks the performance of different learning strategies,
    adapts the learning rate, and selects high‑value opportunities for future
    learning tasks.
    """

    def __init__(self, storage_path: str = "meta_learning_state.json"):
        self.storage_path = Path(storage_path)
        self.strategy_stats: Dict[str, Dict[str, Any]] = {}
        self.base_lr: float = 0.01  # default learning rate
        self._load_state()

    # --------------------------------------------------------------------- #
    # Persistence
    # --------------------------------------------------------------------- #
    def _load_state(self) -> None:
        if self.storage_path.is_file():
            try:
                data = json.loads(self.storage_path.read_text())
                self.strategy_stats = data.get("strategy_stats", {})
                self.base_lr = data.get("base_lr", self.base_lr)
            except Exception:
                # Corrupt file – start fresh
                self.strategy_stats = {}
                self.base_lr = 0.01

    def _save_state(self) -> None:
        data = {
            "strategy_stats": self.strategy_stats,
            "base_lr": self.base_lr,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))

    # --------------------------------------------------------------------- #
    # Strategy tracking
    # --------------------------------------------------------------------- #
    def update_strategy_performance(
        self,
        strategy_name: str,
        task_id: str,
        success_metric: float,
    ) -> None:
        """
        Record the outcome of a strategy on a particular task.
        `success_metric` should be a normalized value where higher is better.
        """
        stats = self.strategy_stats.setdefault(strategy_name, {
            "count": 0,
            "cumulative_success": 0.0,
            "tasks": [],
        })
        stats["count"] += 1
        stats["cumulative_success"] += success_metric
        stats["tasks"].append({"task_id": task_id, "metric": success_metric})
        self._save_state()

    def get_strategy_score(self, strategy_name: str) -> float:
        """Return the average success metric for a strategy (0 if never used)."""
        stats = self.strategy_stats.get(strategy_name)
        if not stats or stats["count"] == 0:
            return 0.0
        return stats["cumulative_success"] / stats["count"]

    # --------------------------------------------------------------------- #
    # Strategy selection
    # --------------------------------------------------------------------- #
    def select_strategy(self, candidate_strategies: List[str]) -> str:
        """
        Choose the best‑performing strategy from the candidate list.
        If none have prior data, pick one at random.
        """
        if not candidate_strategies:
            raise ValueError("No candidate strategies provided")

        # Compute scores for each candidate
        scored = [
            (self.get_strategy_score(name), name) for name in candidate_strategies
        ]
        # Sort descending by score
        scored.sort(reverse=True)
        best_score, best_name = scored[0]

        # If the best score is zero (no history), fall back to random choice
        if best_score == 0.0:
            return random.choice(candidate_strategies)
        return best_name

    # --------------------------------------------------------------------- #
    # Learning‑rate adaptation
    # --------------------------------------------------------------------- #
    def adapt_learning_rate(self, recent_success: float, target: float = 0.8) -> float:
        """
        Simple proportional controller:
        - If recent_success > target → increase LR (capped at 0.1)
        - If recent_success < target → decrease LR (floored at 0.0001)
        Returns the new learning rate.
        """
        if recent_success > target:
            self.base_lr = min(self.base_lr * 1.2, 0.1)
        else:
            self.base_lr = max(self.base_lr * 0.8, 0.0001)
        self._save_state()
        return self.base_lr

    # --------------------------------------------------------------------- #
    # High‑value opportunity identification
    # --------------------------------------------------------------------- #
    def identify_high_value_tasks(
        self,
        pending_tasks: List[Tuple[str, Dict]],
        top_k: int = 5,
    ) -> List[Tuple[str, Dict]]:
        """
        Rank pending tasks by estimated value. For this prototype we use a
        heuristic: tasks whose feature vector (in `task_meta`) has the greatest
        Euclidean distance from previously solved tasks are considered novel
        and thus high‑value.
        """
        # Collect feature vectors of already‑solved tasks
        solved_vectors = [
            t["features"]
            for stats in self.strategy_stats.values()
            for t in stats["tasks"]
            if "features" in t
        ]
        if not solved_vectors:
            # No history – just return the first `top_k` tasks
            return pending_tasks[:top_k]

        def novelty_score(task_meta: Dict) -> float:
            from math import sqrt
            vec = task_meta.get("features", [])
            if not vec:
                return 0.0
            # Minimum distance to any solved vector
            min_dist = min(
                sqrt(sum((a - b) ** 2 for a, b in zip(vec, sv))) for sv in solved_vectors
            )
            return min_dist

        scored_tasks = [
            (novelty_score(meta), (task_id, meta))
            for task_id, meta in pending_tasks
        ]
        scored_tasks.sort(reverse=True, key=lambda x: x[0])
        return [t for _, t in scored_tasks[:top_k]]
import random
from collections import defaultdict
from strategy_performance_tracker import StrategyPerformanceTracker

class MetaLearningEngine:
    """
    Core engine that meta‑learns which learning strategies (e.g., tool choice,
    problem decomposition) work best for a given task and adapts the learning
    rate accordingly.
    """

    def __init__(self, initial_lr: float = 0.01, epsilon: float = 0.2):
        # Exploration vs exploitation parameter
        self.epsilon = epsilon
        # Base learning rate that will be adapted over time
        self.learning_rate = initial_lr
        # Performance tracker for each strategy
        self.tracker = StrategyPerformanceTracker()
        # Historical rewards to drive learning‑rate adaptation
        self.recent_rewards = []

    # ------------------------------------------------------------------
    # Strategy selection
    # ------------------------------------------------------------------
    def select_strategy(self, task_id: str, candidate_strategies: list) -> str:
        """
        Choose a strategy for the given task.

        Uses epsilon‑greedy: with probability epsilon pick a random strategy
        (exploration), otherwise pick the strategy with the highest average
        reward so far (exploitation).
        """
        if not candidate_strategies:
            raise ValueError("No candidate strategies provided.")

        # Exploration
        if random.random() < self.epsilon:
            chosen = random.choice(candidate_strategies)
            return chosen

        # Exploitation: pick best known strategy for this task
        best_strategy = None
        best_score = float("-inf")
        for strat in candidate_strategies:
            avg = self.tracker.get_average(strat)
            # If a strategy has never been tried, treat its avg as 0
            avg = avg if avg is not None else 0.0
            if avg > best_score:
                best_score = avg
                best_strategy = strat

        # Fallback to random if all scores are equal (e.g., all None)
        return best_strategy or random.choice(candidate_strategies)

    # ------------------------------------------------------------------
    # Performance update
    # ------------------------------------------------------------------
    def update_performance(self, strategy: str, reward: float):
        """
        Record the reward obtained after using a strategy and keep a short
        history for learning‑rate adaptation.
        """
        self.tracker.record(strategy, reward)
        self.recent_rewards.append(reward)
        # Keep only the last 20 rewards to smooth adaptation
        if len(self.recent_rewards) > 20:
            self.recent_rewards.pop(0)

        # After each update, possibly adapt the learning rate
        self._adapt_learning_rate()

    # ------------------------------------------------------------------
    # Learning‑rate adaptation
    # ------------------------------------------------------------------
    def _adapt_learning_rate(self):
        """
        Simple adaptation: if the average reward over the recent window
        improves, increase LR modestly; otherwise decay it.
        """
        if len(self.recent_rewards) < 5:
            return  # Not enough data yet

        recent_avg = sum(self.recent_rewards[-5:]) / 5.0
        past_avg = sum(self.recent_rewards[-10:-5]) / 5.0 if len(self.recent_rewards) >= 10 else recent_avg

        # If improvement > 2%, boost LR up to 2× initial
        if recent_avg > past_avg * 1.02:
            self.learning_rate = min(self.learning_rate * 1.05, 0.1)
        # If degradation > 2%, decay LR down to 0.001
        elif recent_avg < past_avg * 0.98:
            self.learning_rate = max(self.learning_rate * 0.95, 0.001)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def get_current_lr(self) -> float:
        """Expose the current learning rate for external modules."""
        return self.learning_rate
import random
import math
from collections import defaultdict, deque
from typing import Any, Dict, List, Tuple

class MetaLearningEngine:
    """
    Core engine that meta‑learns *how* to learn.
    It tracks strategy performance, adapts learning rates,
    and suggests high‑value learning opportunities.
    """

    def __init__(self, base_lr: float = 0.01, window: int = 20):
        # Base learning rate used when no data is available
        self.base_lr = base_lr
        # Sliding window of recent performances for each strategy
        self.window = window
        # performance history: {strategy_name: deque([reward, ...])}
        self._history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=self.window))
        # recent overall rewards for adaptive LR computation
        self._recent_rewards: deque = deque(maxlen=self.window)

    # ------------------------------------------------------------------
    # Strategy tracking
    # ------------------------------------------------------------------
    def record_strategy_performance(self, strategy: str, reward: float) -> None:
        """
        Record the reward obtained when using a particular strategy.
        """
        self._history[strategy].append(reward)
        self._recent_rewards.append(reward)

    def best_strategy(self) -> str:
        """
        Return the strategy with the highest average reward over the window.
        If no history exists, fall back to a random choice from known strategies.
        """
        if not self._history:
            raise ValueError("No strategy performance data available.")
        avg_rewards = {
            s: sum(rewards) / len(rewards) for s, rewards in self._history.items()
        }
        best = max(avg_rewards, key=avg_rewards.get)
        return best

    def suggest_strategy(self, candidate_strategies: List[str]) -> str:
        """
        Given a list of candidate strategies, choose the one expected to perform best.
        If none have history, pick uniformly at random.
        """
        known = [s for s in candidate_strategies if s in self._history]
        if known:
            # Choose the known strategy with highest avg reward
            avg = {s: sum(self._history[s]) / len(self._history[s]) for s in known}
            return max(avg, key=avg.get)
        # No data → explore
        return random.choice(candidate_strategies)

    # ------------------------------------------------------------------
    # Adaptive learning‑rate logic
    # ------------------------------------------------------------------
    def adaptive_lr(self) -> float:
        """
        Compute an adaptive learning rate based on recent reward trends.
        If recent rewards are improving, increase LR modestly;
        if they are degrading, decrease LR.
        """
        if len(self._recent_rewards) < 2:
            return self.base_lr

        # Simple trend: compare last reward to mean of previous window
        recent = list(self._recent_rewards)
        last = recent[-1]
        prev_mean = sum(recent[:-1]) / (len(recent) - 1)

        # Ratio determines scaling; clamp to reasonable bounds
        ratio = last / (prev_mean + 1e-8)
        scaling = 1.0 + 0.2 * (ratio - 1.0)  # up to ±20% change
        new_lr = self.base_lr * scaling
        # Clamp between 0.1× and 5× the base LR
        return max(self.base_lr * 0.1, min(new_lr, self.base_lr * 5))

    # ------------------------------------------------------------------
    # High‑value opportunity identification
    # ------------------------------------------------------------------
    def identify_opportunity(self, task_difficulty: float, reward: float) -> bool:
        """
        Heuristic: if reward is far below expected given difficulty,
        flag the task as a high‑value learning opportunity.
        """
        expected = math.exp(-task_difficulty)  # simple decreasing expectation
        return reward < 0.5 * expected

    # ------------------------------------------------------------------
    # Meta‑optimization of the learning loop
    # ------------------------------------------------------------------
    def meta_optimize(self, learner: Any, task: Any, strategy: str) -> None:
        """
        Hook that can be called after each learning step.
        Allows the learner to be re‑configured based on meta‑insights.
        """
        # Example: adjust learner's internal LR if the engine suggests it
        if hasattr(learner, "set_learning_rate"):
            learner.set_learning_rate(self.adaptive_lr())
```
import random
import json
import os
from collections import defaultdict, deque
from typing import Any, Dict, List, Tuple

class MetaLearningEngine:
    """
    Core engine that tracks the performance of different learning strategies
    (tool choice, decomposition pattern, learning‑rate schedule) and adapts
    future decisions based on observed success.

    The engine maintains:
      • a rolling performance window per strategy
      • an adaptive learning‑rate that is increased for successful strategies
        and decayed for failures
      • a simple bandit‑style selector that prefers high‑value strategies
    """

    def __init__(self,
                 performance_window: int = 10,
                 lr_base: float = 0.01,
                 lr_min: float = 1e-5,
                 lr_max: float = 0.1,
                 decay_factor: float = 0.9,
                 boost_factor: float = 1.1,
                 state_path: str = "meta_engine_state.json"):
        self.performance_window = performance_window
        self.lr = lr_base
        self.lr_min = lr_min
        self.lr_max = lr_max
        self.decay_factor = decay_factor
        self.boost_factor = boost_factor
        self.state_path = state_path

        # strategy -> deque of recent scores
        self.strategy_history: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=self.performance_window)
        )
        # strategy -> estimated value (mean of history)
        self.strategy_values: Dict[str, float] = defaultdict(float)

        self._load_state()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def register_outcome(self, strategy_id: str, reward: float) -> None:
        """
        Record the reward (e.g., improvement in loss or quality metric) for a
        particular strategy.
        """
        self.strategy_history[strategy_id].append(reward)
        self.strategy_values[strategy_id] = (
            sum(self.strategy_history[strategy_id]) /
            len(self.strategy_history[strategy_id])
        )
        self._adjust_learning_rate(reward)

    def select_strategy(self, candidate_strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Choose a strategy from the candidate pool. Uses an ε‑greedy bandit:
          • 10 % random exploration
          • 90 % exploitation of the highest‑valued known strategy
        """
        epsilon = 0.1
        if random.random() < epsilon or not self.strategy_values:
            # pure exploration – pick a random candidate
            return random.choice(candidate_strategies)

        # exploitation – pick the candidate with the best estimated value
        best_id = max(
            self.strategy_values,
            key=lambda sid: self.strategy_values.get(sid, 0.0)
        )
        # Find the candidate dict that matches the best_id
        for cand in candidate_strategies:
            if cand.get("id") == best_id:
                return cand
        # Fallback (should not happen)
        return random.choice(candidate_strategies)

    def get_current_lr(self) -> float:
        """Return the learning‑rate currently being used by the engine."""
        return self.lr

    def save_state(self) -> None:
        """Persist internal state to disk so learning persists across runs."""
        state = {
            "lr": self.lr,
            "strategy_history": {
                sid: list(hist) for sid, hist in self.strategy_history.items()
            }
        }
        with open(self.state_path, "w", encoding="utf-8") as fp:
            json.dump(state, fp, indent=2)

    # --------------------------------------------------------------------- #
    # Internals
    # --------------------------------------------------------------------- #
    def _adjust_learning_rate(self, reward: float) -> None:
        """
        Simple adaptive rule:
          • reward > 0 → increase learning‑rate (up to lr_max)
          • reward ≤ 0 → decay learning‑rate (down to lr_min)
        """
        if reward > 0:
            self.lr = min(self.lr * self.boost_factor, self.lr_max)
        else:
            self.lr = max(self.lr * self.decay_factor, self.lr_min)

    def _load_state(self) -> None:
        """Load persisted state if it exists."""
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, "r", encoding="utf-8") as fp:
                    state = json.load(fp)
                self.lr = state.get("lr", self.lr)
                for sid, hist in state.get("strategy_history", {}).items():
                    self.strategy_history[sid] = deque(hist, maxlen=self.performance_window)
                    self.strategy_values[sid] = (
                        sum(self.strategy_history[sid]) / len(self.strategy_history[sid])
                        if self.strategy_history[sid] else 0.0
                    )
            except Exception as e:
                print(f"[MetaLearningEngine] Failed to load state: {e}")
```