"""
Tree Search Implementation based on LATS (Language Agent Tree Search)
arXiv:2310.04406 - Language Agents as Zero-shot Planners

Implements a tree search system for exploring solution space with:
- UCB (Upper Confidence Bound) selection for balancing exploration/exploitation
- Node value estimation through child aggregation
- Path reconstruction for best solutions found
"""

import math
from typing import Any, List, Tuple, Dict, Optional
from dataclasses import dataclass, field
from critic import CriticAgent


@dataclass
class TreeNode:
    """Node in the solution tree with value and visit tracking."""
    state: Any
    action: Optional[str] = None
    children: List['TreeNode'] = field(default_factory=list)
    value: float = 0.0  # Accumulated value/reward
    visits: int = 0      # Number of times visited
    parent: Optional['TreeNode'] = None

    def ucb_score(self) -> float:
        """
        Calculate UCB (Upper Confidence Bound) score for this node.

        UCB = mean_value + exploration_bonus
        where mean_value = value/visits
        and exploration_bonus = sqrt(2 * ln(parent_visits) / visits)

        Returns:
            float: UCB score for this node
        """
        if self.visits == 0:
            return float('inf')

        mean_value = self.value / self.visits

        if self.parent is None or self.parent.visits == 0:
            exploration_bonus = 0.0
        else:
            exploration_bonus = math.sqrt(2.0 * math.log(self.parent.visits) / self.visits)

        return mean_value + exploration_bonus


def expand_node(node: TreeNode) -> List[TreeNode]:
    """
    Generate child nodes from current state with real strategy variations.

    Generates 2-3 alternative approaches based on task type detection:
    - REFACTOR tasks: incremental, modular, comprehensive strategies
    - IMPLEMENT tasks: minimal, standard, feature-rich strategies
    - FIX tasks: quick-patch, root-cause, test-driven strategies

    Args:
        node: TreeNode to expand

    Returns:
        List of newly created child nodes with different strategy variations
    """
    children = []
    task_state = str(node.state).lower()

    # Detect task type from state description
    is_refactor = any(kw in task_state for kw in ['refactor', 'restructure', 'reorganize', 'clean'])
    is_implement = any(kw in task_state for kw in ['implement', 'add', 'create', 'build', 'feature'])
    is_fix = any(kw in task_state for kw in ['fix', 'bug', 'error', 'issue', 'debug'])

    # Strategy definitions based on task type
    if is_refactor:
        strategies = [
            {
                'action': 'incremental_refactor',
                'description': 'Incremental refactoring: Small, safe changes with tests between each step',
                'prompt_variation': 'Focus on minimal changes. Refactor one component at a time, run tests after each.'
            },
            {
                'action': 'modular_refactor',
                'description': 'Modular refactoring: Extract reusable components and improve separation of concerns',
                'prompt_variation': 'Identify duplicated logic. Extract into modules/functions. Improve interfaces.'
            },
            {
                'action': 'comprehensive_refactor',
                'description': 'Comprehensive refactoring: Redesign architecture with best practices',
                'prompt_variation': 'Apply design patterns. Optimize structure. Improve maintainability and extensibility.'
            }
        ]
    elif is_implement:
        strategies = [
            {
                'action': 'minimal_implementation',
                'description': 'Minimal implementation: Core functionality only, fastest path to working',
                'prompt_variation': 'Implement only required features. Skip extras. Get to working prototype fast.'
            },
            {
                'action': 'standard_implementation',
                'description': 'Standard implementation: Core features + error handling + basic validation',
                'prompt_variation': 'Implement features with proper error handling, input validation, and logging.'
            },
            {
                'action': 'robust_implementation',
                'description': 'Robust implementation: Full features + edge cases + tests + documentation',
                'prompt_variation': 'Comprehensive solution with tests, docs, edge case handling, and extensibility.'
            }
        ]
    elif is_fix:
        strategies = [
            {
                'action': 'quick_patch',
                'description': 'Quick patch: Immediate fix for symptoms, minimal changes',
                'prompt_variation': 'Find the failing point. Apply minimal fix. Verify it works.'
            },
            {
                'action': 'root_cause_fix',
                'description': 'Root cause fix: Investigate deeply, fix underlying issue',
                'prompt_variation': 'Trace the bug to its source. Fix the root cause, not symptoms. Prevent recurrence.'
            },
            {
                'action': 'test_driven_fix',
                'description': 'Test-driven fix: Write failing test first, then fix to pass',
                'prompt_variation': 'Create test that reproduces bug. Fix code until test passes. Add regression tests.'
            }
        ]
    else:
        # Generic exploration strategies for unknown task types
        strategies = [
            {
                'action': 'conservative_approach',
                'description': 'Conservative: Minimal changes, low risk',
                'prompt_variation': 'Make smallest possible changes. Preserve existing behavior. Low risk approach.'
            },
            {
                'action': 'balanced_approach',
                'description': 'Balanced: Moderate changes with good tradeoffs',
                'prompt_variation': 'Balance speed vs quality. Make reasonable improvements without over-engineering.'
            },
            {
                'action': 'aggressive_approach',
                'description': 'Aggressive: Comprehensive changes, higher complexity',
                'prompt_variation': 'Go deep. Make significant improvements. Accept higher initial complexity.'
            }
        ]

    # Generate child nodes for each strategy
    for strategy in strategies:
        next_state = {
            'original_state': node.state,
            'strategy': strategy['action'],
            'description': strategy['description'],
            'prompt': strategy['prompt_variation']
        }

        child = TreeNode(
            state=next_state,
            action=strategy['action'],
            parent=node
        )
        children.append(child)
        node.children.append(child)

    return children


_evaluation_cache: Dict[str, float] = {}
_critic: Optional[CriticAgent] = None


def evaluate_node(node: TreeNode) -> float:
    """
    Score a node's state on 0.0-1.0 scale using CriticAgent.

    Uses critic.review() to evaluate code quality when node state is a string (code).
    Results are cached to avoid redundant evaluations.

    Args:
        node: TreeNode to evaluate

    Returns:
        float: Score between 0.0 (bad) and 1.0 (excellent)
    """
    global _critic, _evaluation_cache

    # Handle nodes without output
    if node.state is None or (isinstance(node.state, str) and not node.state.strip()):
        return 0.0

    # Check cache
    state_key = str(node.state)
    if state_key in _evaluation_cache:
        return _evaluation_cache[state_key]

    # Initialize critic if needed
    if _critic is None:
        _critic = CriticAgent()

    # Evaluate based on state type
    if isinstance(node.state, str) and len(node.state) > 10:
        # Treat as code - use critic
        review_result = _critic.review(node.state)
        score = review_result["score"]
    elif isinstance(node.state, int):
        # Numeric state - normalize to 0-1
        score = min(node.state / 10.0, 1.0)
    else:
        # Default heuristic
        score = len(str(node.state)) / 20.0
        score = min(score, 1.0)

    # Cache result
    _evaluation_cache[state_key] = score

    return score


def select_best_child(node: TreeNode) -> Optional[TreeNode]:
    """
    Select child with highest UCB score.

    Args:
        node: TreeNode to select from

    Returns:
        TreeNode with best UCB score, or None if no children
    """
    if not node.children:
        return None

    best_child = max(node.children, key=lambda child: child.ucb_score())
    return best_child


def select_best_path(root: TreeNode) -> Tuple[List[str], float]:
    """
    Reconstruct best path from root to best leaf.

    Uses greedy selection based on value/visits ratio (mean reward).

    Args:
        root: Root node of search tree

    Returns:
        Tuple of:
        - List of action strings from root to best leaf
        - Final accumulated value
    """
    path = []
    current = root

    while current.children:
        # Select child with best mean value (value/visits)
        if current.visits == 0:
            best_child = current.children[0]
        else:
            best_child = max(
                current.children,
                key=lambda c: c.value / c.visits if c.visits > 0 else 0.0
            )

        if best_child.action:
            path.append(best_child.action)
        current = best_child

    return path, current.value


def run_tree_search(
    initial_state: Any,
    max_expansions: int = 10,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Execute tree search starting from initial state.

    Algorithm:
    1. Create root node from initial state
    2. Iteratively:
       a. Select most promising node via UCB
       b. Expand it with new children
       c. Evaluate children
       d. Backpropagate values up tree
    3. Return best path found

    Args:
        initial_state: Starting state for search
        max_expansions: Maximum number of node expansions
        verbose: Print search progress

    Returns:
        Dict with keys:
        - best_path: List of actions to reach best state
        - best_value: Value of best state found
        - nodes_expanded: Number of expansions performed
        - total_nodes: Total nodes in tree
    """
    root = TreeNode(state=initial_state)
    nodes_expanded = 0

    for expansion_round in range(max_expansions):
        if verbose:
            print(f"Expansion {expansion_round + 1}/{max_expansions}")

        # Select most promising node using UCB
        current = root
        while current.children and current.visits > 0:
            current = select_best_child(current)
            if current is None:
                current = root
                break

        # Expand selected node
        if nodes_expanded < max_expansions:
            children = expand_node(current)
            nodes_expanded += 1

            # Evaluate and update each child
            for child in children:
                # Evaluate the child state
                reward = evaluate_node(child)

                # Backpropagate value up the tree
                node = child
                while node is not None:
                    node.value += reward
                    node.visits += 1
                    node = node.parent

                if verbose:
                    print(f"  Evaluated {child.action}: reward={reward:.3f}")

    # Count total nodes in tree
    def count_nodes(node: TreeNode) -> int:
        return 1 + sum(count_nodes(child) for child in node.children)

    total_nodes = count_nodes(root)

    # Extract best path
    best_path, best_value = select_best_path(root)

    result = {
        'best_path': best_path,
        'best_value': best_value,
        'nodes_expanded': nodes_expanded,
        'total_nodes': total_nodes
    }

    return result


if __name__ == "__main__":
    # Example usage
    print("=== Tree Search Example (LATS) ===")
    print()

    result = run_tree_search(
        initial_state=0,
        max_expansions=5,
        verbose=True
    )

    print()
    print("=== Results ===")
    print(f"Best path: {' -> '.join(result['best_path'])}")
    print(f"Best value: {result['best_value']:.3f}")
    print(f"Nodes expanded: {result['nodes_expanded']}")
    print(f"Total nodes: {result['total_nodes']}")
