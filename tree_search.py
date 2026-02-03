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
    Generate child nodes from current state.

    This is a template function - in practice, this would:
    - Apply action generation to the current state
    - Create child nodes for each valid next state
    - Return list of unexplored children

    Args:
        node: TreeNode to expand

    Returns:
        List of newly created child nodes
    """
    # Template implementation - generates synthetic child states
    children = []

    # In a real system, this would call an action generator
    # For demo: create 2-3 children with different action labels
    num_children = 2 if isinstance(node.state, int) and node.state > 5 else 3

    for i in range(num_children):
        # Simulate action: increment state or apply transformation
        next_state = node.state + i + 1 if isinstance(node.state, int) else f"{node.state}_action_{i}"
        action = f"action_{i}"

        child = TreeNode(
            state=next_state,
            action=action,
            parent=node
        )
        children.append(child)
        node.children.append(child)

    return children


def evaluate_node(node: TreeNode) -> float:
    """
    Score a node's state on 0.0-1.0 scale.

    This is a template function - in practice, this would:
    - Call a value estimator (LLM scoring, heuristic eval, etc.)
    - Return confidence score for how good this state is

    Args:
        node: TreeNode to evaluate

    Returns:
        float: Score between 0.0 (bad) and 1.0 (excellent)
    """
    # Template: score based on state properties
    if isinstance(node.state, int):
        # Higher numbers are "better" in demo
        return min(node.state / 10.0, 1.0)

    # String states get random-ish scores based on length
    score = len(str(node.state)) / 20.0
    return min(score, 1.0)


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
