"""
PATH ANALYZER: Comparative Analysis System

Analyzes parallel execution results to determine which paths work best for which task types.
Builds decision rules for optimal path selection.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class PathComparison:
    """Stores comparison data between parallel execution paths."""
    task_id: str
    task_type: str
    task_description: str
    timestamp: str
    paths: List[Dict[str, Any]]  # List of path results
    quality_variance: float
    cost_efficiency_leader: str
    best_path: str
    insights: List[str]


class PathComparativeAnalyzer:
    """Analyzes parallel execution results and builds decision rules for path selection."""

    def __init__(self, log_file: str = "path_analysis_log.json"):
        self.log_file = Path(log_file)
        self.comparisons: List[PathComparison] = []
        self.decision_tree: Dict[str, str] = {}
        self._load_existing_data()

    def _load_existing_data(self):
        """Load existing comparisons and decision tree from disk."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.comparisons = [
                        PathComparison(**comp) for comp in data.get('comparisons', [])
                    ]
                    self.decision_tree = data.get('decision_tree', {})
            except Exception:
                pass

    def analyze_quality_variance(self, results: List[Dict[str, Any]]) -> float:
        """
        Calculate quality differential across parallel paths.

        Args:
            results: List of path execution results with 'quality' field

        Returns:
            Quality variance (standard deviation)
        """
        if not results or len(results) < 2:
            return 0.0

        qualities = [r.get('quality', 0.0) for r in results]
        mean_quality = sum(qualities) / len(qualities)
        variance = sum((q - mean_quality) ** 2 for q in qualities) / len(qualities)
        return variance ** 0.5

    def analyze_cost_efficiency(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate quality/cost ratio for each path.

        Args:
            results: List of path execution results with 'quality' and 'cost' fields

        Returns:
            Dict mapping path_id to efficiency ratio
        """
        efficiency = {}
        for result in results:
            path_id = result.get('path_id', 'unknown')
            quality = result.get('quality', 0.0)
            cost = result.get('cost', 1.0)

            # Avoid division by zero
            if cost > 0:
                efficiency[path_id] = quality / cost
            else:
                efficiency[path_id] = quality

        return efficiency

    def extract_strategy_patterns(self, comparisons: List[PathComparison]) -> List[Dict[str, Any]]:
        """
        Extract decision rules from historical comparisons.

        Args:
            comparisons: List of PathComparison objects

        Returns:
            List of strategy patterns (rules)
        """
        patterns = []

        # Group by task type
        task_type_wins: Dict[str, Dict[str, int]] = {}

        for comp in comparisons:
            task_type = comp.task_type
            best_path = comp.best_path

            if task_type not in task_type_wins:
                task_type_wins[task_type] = {}

            if best_path not in task_type_wins[task_type]:
                task_type_wins[task_type][best_path] = 0

            task_type_wins[task_type][best_path] += 1

        # Extract patterns
        for task_type, wins in task_type_wins.items():
            total = sum(wins.values())
            sorted_paths = sorted(wins.items(), key=lambda x: x[1], reverse=True)

            if sorted_paths:
                winner = sorted_paths[0][0]
                win_rate = sorted_paths[0][1] / total

                patterns.append({
                    'task_type': task_type,
                    'recommended_path': winner,
                    'win_rate': win_rate,
                    'sample_size': total,
                    'confidence': 'high' if total >= 5 and win_rate >= 0.6 else 'medium' if total >= 3 else 'low'
                })

        return patterns

    def recommend_path_by_task_type(self, task: Dict[str, Any]) -> str:
        """
        Recommend best path for a given task based on historical data.

        Args:
            task: Task dictionary with 'task_type' field

        Returns:
            Recommended path_id
        """
        task_type = task.get('task_type', 'unknown')

        # Check decision tree first
        if task_type in self.decision_tree:
            return self.decision_tree[task_type]

        # Fallback: Extract patterns and use highest confidence
        patterns = self.extract_strategy_patterns(self.comparisons)

        for pattern in patterns:
            if pattern['task_type'] == task_type:
                return pattern['recommended_path']

        # Default fallback
        return 'standard'

    def add_comparison(self, task_id: str, task_type: str, task_description: str,
                       results: List[Dict[str, Any]]) -> PathComparison:
        """
        Add a new comparison and update decision tree.

        Args:
            task_id: Unique task identifier
            task_type: Type/category of task
            task_description: Description of task
            results: List of parallel execution results

        Returns:
            PathComparison object
        """
        # Analyze results
        quality_var = self.analyze_quality_variance(results)
        efficiency = self.analyze_cost_efficiency(results)

        # Determine best path (highest efficiency)
        best_path = max(efficiency.items(), key=lambda x: x[1])[0] if efficiency else 'unknown'
        cost_leader = best_path

        # Generate insights
        insights = []
        if quality_var < 0.1:
            insights.append("Low quality variance - paths perform similarly")
        elif quality_var > 0.3:
            insights.append("High quality variance - path selection is critical")

        if efficiency:
            avg_efficiency = sum(efficiency.values()) / len(efficiency)
            if efficiency[best_path] > avg_efficiency * 1.5:
                insights.append(f"Path {best_path} significantly outperforms others")

        # Create comparison
        comparison = PathComparison(
            task_id=task_id,
            task_type=task_type,
            task_description=task_description,
            timestamp=datetime.now().isoformat(),
            paths=results,
            quality_variance=quality_var,
            cost_efficiency_leader=cost_leader,
            best_path=best_path,
            insights=insights
        )

        self.comparisons.append(comparison)

        # Update decision tree
        self._update_decision_tree()

        # Save to disk
        self._save()

        return comparison

    def _update_decision_tree(self):
        """Update decision tree based on all comparisons."""
        patterns = self.extract_strategy_patterns(self.comparisons)

        # Only update with high or medium confidence patterns
        for pattern in patterns:
            if pattern['confidence'] in ['high', 'medium']:
                self.decision_tree[pattern['task_type']] = pattern['recommended_path']

    def _save(self):
        """Save comparisons and decision tree to JSON file."""
        data = {
            'comparisons': [asdict(comp) for comp in self.comparisons],
            'decision_tree': self.decision_tree,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of analysis state."""
        return {
            'total_comparisons': len(self.comparisons),
            'task_types_analyzed': len(set(c.task_type for c in self.comparisons)),
            'decision_tree_size': len(self.decision_tree),
            'decision_tree': self.decision_tree,
            'patterns': self.extract_strategy_patterns(self.comparisons)
        }


if __name__ == '__main__':
    # Example usage
    analyzer = PathComparativeAnalyzer()

    # Simulate adding a comparison
    example_results = [
        {'path_id': 'standard', 'quality': 0.85, 'cost': 10.0},
        {'path_id': 'optimized', 'quality': 0.92, 'cost': 8.5},
        {'path_id': 'experimental', 'quality': 0.88, 'cost': 12.0}
    ]

    comparison = analyzer.add_comparison(
        task_id='example_001',
        task_type='code_generation',
        task_description='Generate utility function',
        results=example_results
    )

    print("Comparison added:", comparison)
    print("\nSummary:", json.dumps(analyzer.get_summary(), indent=2))
