"""
Multi-Path Executor - Parallel Strategy Execution Engine

Explores multiple execution strategies simultaneously and returns the best result.
Uses ThreadPoolExecutor for parallel execution with budget-aware strategy allocation.

Based on:
- LATS (arXiv:2310.04406) - Language Agent Tree Search
- Multi-path exploration for optimal solutions
"""

import json
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Optional, Callable


class StrategyType(Enum):
    """Execution strategy types with different risk/reward profiles."""
    CONSERVATIVE = "conservative"  # Safe, proven approaches (30% budget)
    BALANCED = "balanced"          # Standard best practices (50% budget)
    AGGRESSIVE = "aggressive"      # Experimental, high-risk (20% budget)


@dataclass
class PathResult:
    """Result from a single execution path."""
    output: str
    tokens_used: int
    quality: float  # 0.0-1.0 quality score
    elapsed_time: float  # seconds
    success: bool
    error_message: Optional[str] = None


@dataclass
class ExecutionPath:
    """Represents a single execution path with strategy and results."""
    strategy: StrategyType
    budget: float  # dollars allocated
    result: Optional[PathResult] = None
    quality_score: float = 0.0
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        data = {
            "strategy": self.strategy.value,
            "budget": self.budget,
            "quality_score": self.quality_score,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
        if self.result:
            data["result"] = {
                "output": self.result.output[:500],  # Truncate for storage
                "tokens_used": self.result.tokens_used,
                "quality": self.result.quality,
                "elapsed_time": self.result.elapsed_time,
                "success": self.result.success,
                "error_message": self.result.error_message
            }
        return data


class MultiPathExecutor:
    """
    Parallel execution engine that explores multiple strategies simultaneously.

    Budget allocation:
    - BALANCED: 50% (default approach)
    - CONSERVATIVE: 30% (safe fallback)
    - AGGRESSIVE: 20% (experimental)
    """

    def __init__(self, workspace: Path, total_budget: float):
        """
        Initialize multi-path executor.

        Args:
            workspace: Working directory
            total_budget: Total budget in dollars for all paths
        """
        self.workspace = workspace
        self.total_budget = total_budget
        self.execution_history = []

    def generate_path_variants(self, task: str) -> List[ExecutionPath]:
        """
        Generate execution path variants with different strategies.

        Args:
            task: Task description

        Returns:
            List of ExecutionPath objects with allocated budgets
        """
        # Budget allocation percentages
        budget_allocation = {
            StrategyType.BALANCED: 0.50,
            StrategyType.CONSERVATIVE: 0.30,
            StrategyType.AGGRESSIVE: 0.20
        }

        paths = []
        for strategy, allocation in budget_allocation.items():
            path = ExecutionPath(
                strategy=strategy,
                budget=self.total_budget * allocation
            )
            paths.append(path)

        return paths

    def _execute_single_path(
        self,
        path: ExecutionPath,
        task: str,
        executor_func: Callable[[str, StrategyType, float], PathResult]
    ) -> ExecutionPath:
        """
        Execute a single path with the given strategy.

        Args:
            path: ExecutionPath to execute
            task: Task description
            executor_func: Function that executes the task with a given strategy

        Returns:
            ExecutionPath with populated result
        """
        path.start_time = time.time()

        try:
            print(f"[MultiPath] Starting {path.strategy.value} path (budget: ${path.budget:.3f})")

            # Execute with strategy-specific configuration
            result = executor_func(task, path.strategy, path.budget)

            path.result = result
            path.quality_score = result.quality
            path.end_time = time.time()

            elapsed = path.end_time - path.start_time
            print(f"[MultiPath] {path.strategy.value} completed in {elapsed:.1f}s, quality={result.quality:.2f}")

        except Exception as e:
            path.end_time = time.time()
            elapsed = path.end_time - path.start_time

            # Create error result
            path.result = PathResult(
                output=f"Error: {str(e)}",
                tokens_used=0,
                quality=0.0,
                elapsed_time=elapsed,
                success=False,
                error_message=str(e)
            )
            path.quality_score = 0.0

            print(f"[MultiPath] {path.strategy.value} failed after {elapsed:.1f}s: {e}")

        return path

    def execute_paths_parallel(
        self,
        task: str,
        executor_func: Callable[[str, StrategyType, float], PathResult]
    ) -> Dict[str, any]:
        """
        Execute all paths in parallel and return best result.

        Args:
            task: Task description
            executor_func: Function to execute task with strategy

        Returns:
            Dict with best_path, all_paths, and comparison metadata
        """
        paths = self.generate_path_variants(task)

        print(f"[MultiPath] Executing {len(paths)} parallel strategies...")
        print(f"[MultiPath] Total budget: ${self.total_budget:.3f}")

        completed_paths = []

        # Execute paths in parallel
        with ThreadPoolExecutor(max_workers=len(paths)) as executor:
            futures = {
                executor.submit(self._execute_single_path, path, task, executor_func): path
                for path in paths
            }

            for future in as_completed(futures):
                path = future.result()
                completed_paths.append(path)

        # Select best path based on quality score
        best_path = max(completed_paths, key=lambda p: p.quality_score)

        # Calculate comparison metadata
        comparison = self._generate_comparison_metadata(completed_paths, best_path)

        # Log execution
        self._log_execution(task, completed_paths, best_path, comparison)

        result = {
            "best_path": best_path,
            "all_paths": completed_paths,
            "comparison": comparison,
            "execution_time": sum(p.end_time - p.start_time for p in completed_paths if p.start_time and p.end_time),
            "total_budget_used": sum(p.budget for p in completed_paths if p.result and p.result.success)
        }

        return result

    def _generate_comparison_metadata(
        self,
        all_paths: List[ExecutionPath],
        best_path: ExecutionPath
    ) -> Dict[str, any]:
        """
        Generate comparison metadata for path results.

        Args:
            all_paths: All executed paths
            best_path: Best performing path

        Returns:
            Dictionary with comparison statistics
        """
        successful_paths = [p for p in all_paths if p.result and p.result.success]

        quality_scores = [p.quality_score for p in all_paths]
        elapsed_times = [p.result.elapsed_time for p in all_paths if p.result]

        comparison = {
            "total_paths": len(all_paths),
            "successful_paths": len(successful_paths),
            "best_strategy": best_path.strategy.value,
            "best_quality": best_path.quality_score,
            "quality_range": {
                "min": min(quality_scores) if quality_scores else 0.0,
                "max": max(quality_scores) if quality_scores else 0.0,
                "avg": sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
            },
            "execution_time_range": {
                "min": min(elapsed_times) if elapsed_times else 0.0,
                "max": max(elapsed_times) if elapsed_times else 0.0,
                "avg": sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0.0
            },
            "strategy_rankings": sorted(
                [{"strategy": p.strategy.value, "quality": p.quality_score} for p in all_paths],
                key=lambda x: x["quality"],
                reverse=True
            )
        }

        return comparison

    def _log_execution(
        self,
        task: str,
        paths: List[ExecutionPath],
        best_path: ExecutionPath,
        comparison: Dict[str, any]
    ) -> None:
        """
        Log execution results to file.

        Args:
            task: Task description
            paths: All executed paths
            best_path: Best performing path
            comparison: Comparison metadata
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task[:100],
            "total_budget": self.total_budget,
            "best_strategy": best_path.strategy.value,
            "best_quality": best_path.quality_score,
            "paths": [p.to_dict() for p in paths],
            "comparison": comparison
        }

        self.execution_history.append(log_entry)

        # Save to file
        log_file = self.workspace / "multi_path_execution_log.json"
        try:
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = []

            history.append(log_entry)

            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)

            print(f"[MultiPath] Logged execution to {log_file}")

        except Exception as e:
            print(f"[MultiPath] Warning: Could not log execution: {e}")


def create_strategy_prompt_modifier(strategy: StrategyType) -> str:
    """
    Create prompt modifier based on strategy type.

    Args:
        strategy: Strategy type

    Returns:
        Prompt modification string
    """
    modifiers = {
        StrategyType.CONSERVATIVE: """
STRATEGY: CONSERVATIVE
- Use proven, well-tested approaches
- Prioritize reliability over speed
- Add comprehensive error handling
- Include validation steps
- Document assumptions clearly
""",
        StrategyType.BALANCED: """
STRATEGY: BALANCED
- Use standard best practices
- Balance speed and reliability
- Add essential error handling
- Follow established patterns
- Keep implementation clean
""",
        StrategyType.AGGRESSIVE: """
STRATEGY: AGGRESSIVE
- Explore experimental approaches
- Prioritize speed and innovation
- Take calculated risks
- Try novel solutions
- Focus on optimal performance
"""
    }

    return modifiers.get(strategy, "")


# Integration helper for grind_spawner.py
def execute_task_with_multipath(
    task: str,
    workspace: Path,
    total_budget: float,
    executor_func: Callable[[str, StrategyType, float], PathResult]
) -> Dict[str, any]:
    """
    Execute task with multi-path parallel exploration.

    Args:
        task: Task description
        workspace: Working directory
        total_budget: Total budget for all paths
        executor_func: Function to execute task with given strategy

    Returns:
        Dict with best result and comparison metadata
    """
    executor = MultiPathExecutor(workspace, total_budget)
    return executor.execute_paths_parallel(task, executor_func)
