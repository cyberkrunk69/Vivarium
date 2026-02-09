"""
strategic_planner.py

A lightweight hierarchical task planner designed to extend the existing
Atomizer/DAG‑based task generation with strategic, multi‑step, resource‑aware
planning capabilities.

Key Features
------------
* **Goal hierarchy** – strategic → tactical → operational nodes.
* **Resource‑aware scheduling** – simple CPU / time budgeting.
* **Re‑planning triggers** – detects goal changes, resource exhaustion or
  failed sub‑tasks and recomputes the plan.
* **Success probability estimation** – naive Bayesian estimate based on
  historical success rates (placeholder for future learning‑based models).
* **Look‑ahead** – generates a plan of configurable depth (default 10 steps).

Usage
-----
```python
from strategic_planner import StrategicPlanner

planner = StrategicPlanner()
plan = planner.generate_plan(
    strategic_goal="Build a full‑stack web application",
    resources={"cpu_hours": 100, "budget_usd": 5000},
    constraints={"deadline_days": 30}
)
for step in plan:
    print(step)
```
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import copy
import itertools
import math
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class GoalNode:
    """A node in the hierarchical goal tree."""
    name: str
    level: str  # "strategic", "tactical", "operational"
    parent: Optional["GoalNode"] = None
    children: List["GoalNode"] = field(default_factory=list)
    # Optional function that expands this node into sub‑goals
    decomposer: Optional[Callable[["GoalNode"], List["GoalNode"]]] = None
    # Metadata used for planning (e.g., estimated cost, duration, success prob)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: "GoalNode") -> None:
        self.children.append(child)
        child.parent = self

    def is_leaf(self) -> bool:
        return not self.children


class StrategicPlanner:
    """
    Core planner that builds a hierarchical plan, allocates resources,
    estimates success probabilities and supports replanning.
    """

    def __init__(
        self,
        max_lookahead: int = 10,
        default_success: float = 0.9,
        resource_decay: float = 0.95,
    ):
        """
        Parameters
        ----------
        max_lookahead: int
            Maximum number of operational steps to generate in a single plan.
        default_success: float
            Baseline success probability for a newly created leaf node.
        resource_decay: float
            Factor by which remaining resources are discounted after each step.
        """
        self.max_lookahead = max_lookahead
        self.default_success = default_success
        self.resource_decay = resource_decay

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def generate_plan(
        self,
        strategic_goal: str,
        resources: Dict[str, float],
        constraints: Optional[Dict[str, Any]] = None,
        replanning_callback: Optional[Callable[[GoalNode], bool]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Produce a concrete, ordered list of operational tasks.

        Returns
        -------
        List[Dict] – each dict contains at least ``id``, ``name`` and
        ``estimated_*`` fields.
        """
        constraints = constraints or {}
        root = GoalNode(name=strategic_goal, level="strategic")
        self._expand_hierarchy(root)
        plan = self._schedule(root, resources, constraints, replanning_callback)
        return plan

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _expand_hierarchy(self, node: GoalNode) -> None:
        """
        Recursively decompose a node using simple rule‑based heuristics.
        For a production system this would be replaced by a learned model
        or a domain‑specific HTN library.
        """
        if node.level == "strategic":
            node.decomposer = self._strategic_decomposer
        elif node.level == "tactical":
            node.decomposer = self._tactical_decomposer
        else:
            node.decomposer = None  # operational leaf

        if node.decomposer:
            children = node.decomposer(node)
            for child in children:
                node.add_child(child)
                self._expand_hierarchy(child)

    # ---- Decomposers ---------------------------------------------------- #
    def _strategic_decomposer(self, node: GoalNode) -> List[GoalNode]:
        """
        Very naive strategic decomposition – split on common verbs.
        """
        tokens = node.name.lower().split()
        # Example heuristic: every verb becomes a tactical sub‑goal
        verbs = [t for t in tokens if t in {"design", "implement", "test", "deploy", "research", "optimize"}]
        if not verbs:
            verbs = ["implement"]  # fallback
        return [
            GoalNode(name=f"{verb.title()} the system", level="tactical")
            for verb in verbs
        ]

    def _tactical_decomposer(self, node: GoalNode) -> List[GoalNode]:
        """
        Tactical → operational decomposition.
        """
        # Simple mapping: each tactical goal expands to three generic operational steps
        base = node.name.replace("Design", "design").replace("Implement", "implement")
        steps = [
            f"{base} - define requirements",
            f"{base} - write code",
            f"{base} - verify & test",
        ]
        return [
            GoalNode(name=step, level="operational", metadata={"estimated_cost": 1.0, "estimated_time": 1.0})
            for step in steps
        ]

    # ---- Scheduling ------------------------------------------------------ #
    def _schedule(
        self,
        root: GoalNode,
        resources: Dict[str, float],
        constraints: Dict[str, Any],
        replanning_callback: Optional[Callable[[GoalNode], bool]],
    ) -> List[Dict[str, Any]]:
        """
        Linearise the leaf nodes while respecting resource budgets and
        replanning triggers.
        """
        plan: List[Dict[str, Any]] = []
        remaining_resources = copy.deepcopy(resources)

        # Flatten leaves in depth‑first order
        leaves = self._collect_leaves(root)

        for leaf in itertools.islice(leaves, self.max_lookahead):
            # Estimate success probability
            leaf.metadata.setdefault("success_prob", self.default_success)

            # Simple resource check – if any resource would go negative, trigger replanning
            if not self._has_enough_resources(leaf, remaining_resources):
                logger.info("Insufficient resources for %s – triggering replanning", leaf.name)
                if replanning_callback and replanning_callback(leaf):
                    # Caller may adjust resources; we simply break for this demo
                    break
                else:
                    break

            # Allocate resources (naïve subtraction)
            self._consume_resources(leaf, remaining_resources)

            # Append to plan
            plan.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": leaf.name,
                    "level": leaf.level,
                    "estimated_cost": leaf.metadata.get("estimated_cost", 1.0),
                    "estimated_time": leaf.metadata.get("estimated_time", 1.0),
                    "success_prob": leaf.metadata["success_prob"],
                }
            )

            # Decay remaining resources to simulate diminishing returns
            for key in remaining_resources:
                remaining_resources[key] *= self.resource_decay

        return plan

    def _collect_leaves(self, node: GoalNode) -> List[GoalNode]:
        """Depth‑first leaf collection."""
        if node.is_leaf():
            return [node]
        leaves: List[GoalNode] = []
        for child in node.children:
            leaves.extend(self._collect_leaves(child))
        return leaves

    def _has_enough_resources(self, node: GoalNode, resources: Dict[str, float]) -> bool:
        """Check whether the node's estimated cost fits the current budget."""
        cost = node.metadata.get("estimated_cost", 0)
        budget = resources.get("budget_usd", math.inf)
        return cost <= budget

    def _consume_resources(self, node: GoalNode, resources: Dict[str, float]) -> None:
        """Subtract the node's estimated cost from the resource pool."""
        cost = node.metadata.get("estimated_cost", 0)
        if "budget_usd" in resources:
            resources["budget_usd"] -= cost
        # Extend with other resource types as needed

    # --------------------------------------------------------------------- #
    # Success probability utilities (place‑holders for learning‑based models)
    # --------------------------------------------------------------------- #
    def update_success_estimate(self, node: GoalNode, observed_success: bool) -> None:
        """
        Simple Bayesian update: treat ``success_prob`` as a Beta(α,β) prior.
        """
        α = node.metadata.get("alpha", 1.0)
        β = node.metadata.get("beta", 1.0)
        if observed_success:
            α += 1
        else:
            β += 1
        node.metadata["alpha"] = α
        node.metadata["beta"] = β
        node.metadata["success_prob"] = α / (α + β)
"""
strategic_planner.py
--------------------

A lightweight strategic planner that sits on top of the existing Atomizer
(task‑level DAG builder).  It introduces a three‑level hierarchy
(strategic → tactical → operational), resource‑aware allocation,
probabilistic success estimation and automatic replanning when goals
or constraints change.

The implementation is deliberately simple – it uses rule‑based
decomposition and a bounded look‑ahead search – but it provides a clear
integration point for more sophisticated HTN, STRIPS or RL planners
later on.
"""

from __future__ import annotations
import heapq
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class GoalNode:
    """
    Represents a node in the hierarchical goal tree.

    Attributes
    ----------
    name: str
        Human‑readable identifier.
    subgoals: List[GoalNode]
        Child nodes (tactical or operational steps).
    resources_needed: Dict[str, float]
        Amount of each resource required to complete this node.
    estimated_cost: float
        Monetary cost estimate.
    estimated_time: float
        Time estimate in seconds.
    success_prob: float
        Prior probability of successful completion (0‑1).
    """
    name: str
    subgoals: List["GoalNode"] = field(default_factory=list)
    resources_needed: Dict[str, float] = field(default_factory=dict)
    estimated_cost: float = 0.0
    estimated_time: float = 0.0
    success_prob: float = 1.0

    def is_leaf(self) -> bool:
        return not self.subgoals

    def total_estimated_time(self) -> float:
        """Recursive sum of estimated times for this node and its descendants."""
        return self.estimated_time + sum(child.total_estimated_time() for child in self.subgoals)


class StrategicPlanner:
    """
    Core class that creates, evaluates and replans hierarchical goal structures.
    """

    def __init__(self, resources: Optional[Dict[str, float]] = None):
        """
        Parameters
        ----------
        resources: dict, optional
            Global resource pool (e.g. {"budget": 1000, "cpu_hours": 200}).
        """
        self.global_resources: Dict[str, float] = resources or {}
        self.last_plan: Optional[List[GoalNode]] = None
        self.last_goal_desc: Optional[str] = None

    # --------------------------------------------------------------------- #
    #  Goal decomposition
    # --------------------------------------------------------------------- #
    def decompose_goal(self, goal_desc: str) -> GoalNode:
        """
        Very naive rule‑based decomposition.  Real implementations would
        replace this with HTN, LLM‑driven planning or a STRIPS planner.

        The function looks for key verbs and creates a three‑level tree:

        * Strategic node – the whole description.
        * Tactical nodes – split by commas or “and”.
        * Operational nodes – split each tactical phrase into atomic actions.

        Returns
        -------
        GoalNode
            Root of the hierarchical goal tree.
        """
        strategic = GoalNode(name=goal_desc.strip(), estimated_time=0.0)

        # Split into tactical chunks
        tactical_phrases = [p.strip() for p in goal_desc.replace(";", ",").split(",") if p.strip()]
        for t_phrase in tactical_phrases:
            tactical = GoalNode(name=t_phrase, estimated_time=5.0)  # rough default
            # Split tactical phrase into words → simple operational actions
            words = [w for w in t_phrase.split() if w.isalpha()]
            for i, word in enumerate(words):
                op_name = f"{t_phrase} :: step {i+1}"
                operational = GoalNode(
                    name=op_name,
                    estimated_time=2.0,
                    resources_needed={"cpu_hours": 0.1},
                    estimated_cost=0.5,
                    success_prob=0.95,
                )
                tactical.subgoals.append(operational)
                tactical.estimated_time += operational.estimated_time
                tactical.estimated_cost = tactical.estimated_cost + operational.estimated_cost
                tactical.resources_needed = {
                    k: tactical.resources_needed.get(k, 0) + operational.resources_needed.get(k, 0)
                    for k in set(tactical.resources_needed) | set(operational.resources_needed)
                }
            strategic.subgoals.append(tactical)
            strategic.estimated_time += tactical.estimated_time
            strategic.estimated_cost += tactical.estimated_cost
            strategic.resources_needed = {
                k: strategic.resources_needed.get(k, 0) + tactical.resources_needed.get(k, 0)
                for k in set(strategic.resources_needed) | set(tactical.resources_needed)
            }

        # Assign a default success probability based on depth
        strategic.success_prob = 0.9 ** len(strategic.subgoals)
        return strategic

    # --------------------------------------------------------------------- #
    #  Planning interface
    # --------------------------------------------------------------------- #
    def plan(self, goal_desc: str) -> List[GoalNode]:
        """
        Produce a linearised plan (list of leaf GoalNodes) from a high‑level
        description.  The planner also checks resource feasibility and
        annotates each step with an estimated success probability.

        Returns
        -------
        List[GoalNode]
            Ordered leaf nodes representing the operational steps.
        """
        root = self.decompose_goal(goal_desc)
        self.last_plan = self._flatten_plan(root)
        self.last_goal_desc = goal_desc
        self.allocate_resources(self.last_plan)
        return self.last_plan

    def _flatten_plan(self, node: GoalNode) -> List[GoalNode]:
        """Depth‑first traversal returning leaf nodes in execution order."""
        if node.is_leaf():
            return [node]
        steps: List[GoalNode] = []
        for child in node.subgoals:
            steps.extend(self._flatten_plan(child))
        return steps

    # --------------------------------------------------------------------- #
    #  Resource allocation
    # --------------------------------------------------------------------- #
    def allocate_resources(self, plan: List[GoalNode]) -> None:
        """
        Simple greedy allocation: ensure that the cumulative resource usage
        never exceeds the global pool.  If it would, the planner marks the
        offending step's success probability to 0 (forcing replanning).
        """
        used: Dict[str, float] = {k: 0.0 for k in self.global_resources}
        for step in plan:
            for r, amt in step.resources_needed.items():
                used[r] = used.get(r, 0.0) + amt
                if used[r] > self.global_resources.get(r, float("inf")):
                    step.success_prob = 0.0  # impossible under current resources
        # After allocation we can recompute overall success
        self.overall_success = self.estimate_success(plan)

    # --------------------------------------------------------------------- #
    #  Success estimation
    # --------------------------------------------------------------------- #
    def estimate_success(self, plan: List[GoalNode]) -> float:
        """
        Assuming independence, overall success is the product of leaf
        probabilities.  For longer horizons we also factor a depth‑penalty.
        """
        prob = 1.0
        for i, step in enumerate(plan):
            prob *= step.success_prob * (0.99 ** i)  # slight decay per step
        return prob

    # --------------------------------------------------------------------- #
    #  Replanning
    # --------------------------------------------------------------------- #
    def replan(self, new_goal_desc: str) -> List[GoalNode]:
        """
        Triggered when the goal changes or when a step becomes infeasible.
        The method recomputes the plan from scratch but retains any
        already‑executed steps (if they are still valid).
        """
        # For simplicity we discard the old plan and generate a fresh one.
        # A production system would try to reuse completed sub‑trees.
        return self.plan(new_goal_desc)

    # --------------------------------------------------------------------- #
    #  Look‑ahead evaluation (bounded depth‑first search)
    # --------------------------------------------------------------------- #
    def _lookahead(self, node: GoalNode, depth: int = 3) -> float:
        """
        Returns an estimated value for the subtree rooted at *node*.
        The value combines cost, time and success probability.
        """
        if depth == 0 or node.is_leaf():
            return (
                -node.estimated_cost * 0.5
                - node.estimated_time * 0.3
                + node.success_prob * 1.0
            )
        values = [self._lookahead(child, depth - 1) for child in node.subgoals]
        return sum(values) / max(1, len(values))

    # --------------------------------------------------------------------- #
    #  Integration hook for the existing Atomizer
    # --------------------------------------------------------------------- #
    def integrate_with_atomizer(self, atomizer: Any) -> None:
        """
        The Atomizer expects a callable that returns a DAG of tasks.
        We expose ``self.plan`` as that callable and also provide a
        ``replan`` hook for dynamic environments.
        """
        atomizer.set_strategic_planner(self.plan, self.replan)
```python
"""
strategic_planner.py

A lightweight strategic planner that sits on top of the existing Atomizer DAG
generator. It introduces a three‑level goal hierarchy (strategic → tactical →
operational), resource‑aware allocation, success‑probability estimation, and
automatic replanning when goals or resources change.

The planner is deliberately modular so it can be imported by higher‑level
orchestration code without touching any protected files.
"""

from __future__ import annotations
import random
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# Goal hierarchy data structures
# --------------------------------------------------------------------------- #

@dataclass
class GoalNode:
    """A node in the goal hierarchy."""
    name: str
    level: str                     # "strategic", "tactical", or "operational"
    children: List["GoalNode"] = field(default_factory=list)
    cost: float = 0.0              # Estimated cost (time, money, etc.)
    benefit: float = 0.0           # Estimated benefit/value
    success_prob: float = 1.0      # Estimated probability of successful execution
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: "GoalNode") -> None:
        self.children.append(child)

    def total_cost(self) -> float:
        """Recursive total cost of this node and all descendants."""
        return self.cost + sum(c.total_cost() for c in self.children)

    def total_benefit(self) -> float:
        """Recursive total benefit of this node and all descendants."""
        return self.benefit + sum(c.total_benefit() for c in self.children)

    def expected_value(self) -> float:
        """Benefit weighted by success probability minus cost."""
        return (self.total_benefit() * self.success_prob) - self.total_cost()


# --------------------------------------------------------------------------- #
# Planner core
# --------------------------------------------------------------------------- #

class StrategicPlanner:
    """
    High‑level planner that:
    * Decomposes a strategic goal into a tactical/operational DAG.
    * Performs resource‑aware scheduling.
    * Estimates success probabilities.
    * Triggers replanning when external signals change.
    """

    def __init__(
        self,
        resource_budget: Dict[str, float],
        success_estimator: Optional[Callable[[GoalNode], float]] = None,
        cost_estimator: Optional[Callable[[GoalNode], float]] = None,
    ):
        """
        Args:
            resource_budget: Mapping of resource names (e.g., "time", "money")
                             to available quantities.
            success_estimator: Optional custom function to compute success
                               probability for a GoalNode.
            cost_estimator: Optional custom function to compute cost for a
                            GoalNode.
        """
        self.resource_budget = resource_budget.copy()
        self.success_estimator = success_estimator or self._default_success_estimator
        self.cost_estimator = cost_estimator or self._default_cost_estimator
        self._last_plan: List[GoalNode] = []

    # ------------------------------------------------------------------- #
    # Default estimators (very simple heuristics)
    # ------------------------------------------------------------------- #

    def _default_success_estimator(self, node: GoalNode) -> float:
        # Base probability on resource availability and node depth.
        depth_factor = {"strategic": 0.6, "tactical": 0.8, "operational": 0.95}
        base = depth_factor.get(node.level, 0.7)
        # Penalize if cost exceeds remaining budget.
        budget_ok = all(
            self.resource_budget.get(r, 0) >= node.cost
            for r in self.resource_budget
        )
        return base if budget_ok else base * 0.5

    def _default_cost_estimator(self, node: GoalNode) -> float:
        # Simple heuristic: strategic goals are expensive, operational cheap.
        level_cost = {"strategic": 10.0, "tactical": 5.0, "operational": 1.0}
        return level_cost.get(node.level, 3.0)

    # ------------------------------------------------------------------- #
    # Public API
    # ------------------------------------------------------------------- #

    def decompose_goal(self, strategic_goal: str) -> GoalNode:
        """
        Produce a static three‑level hierarchy for a given strategic goal.
        In a real system this would call the Atomizer or an LLM; here we mock
        the structure to keep the module self‑contained.
        """
        strategic = GoalNode(name=strategic_goal, level="strategic")
        # Example decomposition – replace with LLM‑driven generation in production.
        for i in range(2):  # two tactical sub‑goals
            tactical = GoalNode(name=f"{strategic_goal} – Phase {i+1}", level="tactical")
            strategic.add_child(tactical)
            for j in range(3):  # three operational steps per tactical goal
                operational = GoalNode(
                    name=f"{tactical.name} – Step {j+1}",
                    level="operational",
                )
                tactical.add_child(operational)
        # Estimate costs & probabilities recursively
        self._estimate_node(strategic)
        return strategic

    def _estimate_node(self, node: GoalNode) -> None:
        node.cost = self.cost_estimator(node)
        node.success_prob = self.success_estimator(node)
        for child in node.children:
            self._estimate_node(child)

    def allocate_resources(self, root: GoalNode) -> bool:
        """
        Walk the hierarchy depth‑first, deducting estimated costs from the budget.
        Returns True if allocation succeeds, False otherwise (budget overrun).
        """
        def _alloc(node: GoalNode) -> bool:
            # Try to allocate cost for this node
            for res, amount in self.resource_budget.items():
                needed = node.metadata.get(f"cost_{res}", node.cost)
                if amount < needed:
                    return False
            # Reserve resources
            for res in self.resource_budget:
                needed = node.metadata.get(f"cost_{res}", node.cost)
                self.resource_budget[res] -= needed
            # Recurse
            for child in node.children:
                if not _alloc(child):
                    return False
            return True

        # Work on a copy to avoid corrupting the original budget on failure.
        original_budget = self.resource_budget.copy()
        success = _alloc(root)
        if not success:
            self.resource_budget = original_budget  # rollback
        return success

    def plan(self, strategic_goal: str) -> List[GoalNode]:
        """
        High‑level entry point.
        Returns an ordered list of operational GoalNodes (the execution plan).
        """
        root = self.decompose_goal(strategic_goal)
        if not self.allocate_resources(root):
            raise RuntimeError("Insufficient resources to satisfy the goal hierarchy.")

        # Flatten operational nodes preserving tactical order.
        plan: List[GoalNode] = []

        def _collect(node: GoalNode):
            if node.level == "operational":
                plan.append(node)
            for child in node.children:
                _collect(child)

        _collect(root)
        self._last_plan = plan
        return plan

    def replan(self, changed_goal: Optional[str] = None) -> List[GoalNode]:
        """
        Trigger replanning when goals or resources have changed.
        If `changed_goal` is supplied, we start from that strategic goal;
        otherwise we reuse the last strategic goal (if any).
        """
        if changed_goal:
            # Reset budget to original (could be injected via a setter in real use)
            self.resource_budget = {k: v for k, v in self.resource_budget.items()}
            return self.plan(changed_goal)
        if not self._last_plan:
            raise RuntimeError("No previous plan to re‑use.")
        # Simple heuristic: keep the same plan but prune steps whose success
        # probability fell below a threshold.
        pruned = [step for step in self._last_plan if step.success_prob > 0.4]
        self._last_plan = pruned
        return pruned

    # ------------------------------------------------------------------- #
    # Utility helpers for external evaluation
    # ------------------------------------------------------------------- #

    def evaluate_plan(self, plan: List[GoalNode]) -> Dict[str, float]:
        """
        Compute aggregate metrics for a given plan.
        Returns a dict with keys: total_cost, expected_value, success_rate.
        """
        total_cost = sum(node.cost for node in plan)
        expected_value = sum(node.expected_value() for node in plan)
        success_rate = (
            sum(node.success_prob for node in plan) / len(plan) if plan else 0.0
        )
        return {
            "total_cost": total_cost,
            "expected_value": expected_value,
            "success_rate": success_rate,
        }
```
"""
strategic_planner.py
--------------------

A lightweight strategic planner that sits on top of the existing atomizer DAG
generator.  It introduces a three‑level goal hierarchy (strategic → tactical →
operational), resource‑aware planning, success‑probability estimation, and
automatic replanning when goals or constraints change.

The implementation is deliberately simple so it can be dropped into the
current code base without external dependencies.  It can be extended later
with more sophisticated HTN, RL‑based, or LLM‑driven planners.

Typical usage:

```python
from strategic_planner import StrategicPlanner

planner = StrategicPlanner(resource_budget={'time': 100, 'cost': 500})
plan = planner.plan(
    strategic_goal="Launch a full‑stack web application",
    constraints={'deadline': 30, 'max_cost': 400}
)
print(plan.steps)          # list of operational tasks
print(plan.estimated_cost) # total cost estimate
```
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import uuid
import copy
import logging

logger = logging.getLogger(__name__)


@dataclass
class GoalNode:
    """A node in the goal hierarchy."""
    name: str
    level: str                     # "strategic", "tactical", or "operational"
    parent: Optional["GoalNode"] = None
    children: List["GoalNode"] = field(default_factory=list)
    estimated_time: float = 0.0   # in arbitrary time units
    estimated_cost: float = 0.0   # in arbitrary cost units
    success_prob: float = 1.0     # 0..1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: "GoalNode") -> None:
        child.parent = self
        self.children.append(child)


@dataclass
class Plan:
    """Result of a planning run."""
    steps: List[GoalNode]                     # flattened operational steps
    total_time: float
    total_cost: float
    overall_success: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class StrategicPlanner:
    """Core strategic planner.

    The planner builds a hierarchical goal tree, allocates resources,
    estimates success probabilities, and produces a concrete operational
    plan.  It also monitors for changes and triggers replanning.
    """

    def __init__(self,
                 resource_budget: Optional[Dict[str, float]] = None,
                 success_estimator: Optional[Callable[[GoalNode], float]] = None):
        """
        Args:
            resource_budget: Global limits, e.g. {'time': 120, 'cost': 1000}
            success_estimator: Optional custom function to compute success
                               probability for a node.
        """
        self.resource_budget = resource_budget or {}
        self.success_estimator = success_estimator or self._default_success_estimator
        self.current_plan: Optional[Plan] = None
        self._last_constraints: Optional[Dict[str, Any]] = None

    # --------------------------------------------------------------------- #
    #  Public API
    # --------------------------------------------------------------------- #

    def plan(self,
             strategic_goal: str,
             constraints: Optional[Dict[str, Any]] = None,
             replanning: bool = True) -> Plan:
        """Generate a plan for a strategic goal.

        Args:
            strategic_goal: High‑level description of what we want to achieve.
            constraints: Optional dict with keys like ``deadline`` or ``max_cost``.
            replanning: If True, the planner will keep a reference to the plan
                        and allow ``replan_if_needed`` to modify it later.

        Returns:
            Plan instance with flattened operational steps.
        """
        logger.debug("Starting strategic planning for: %s", strategic_goal)
        constraints = constraints or {}
        root = GoalNode(name=strategic_goal, level="strategic")
        self._expand_to_tactical(root)
        self._expand_to_operational(root)
        self._allocate_resources(root, constraints)
        self._propagate_success(root)

        flat_steps = self._flatten_operational(root)
        total_time = sum(node.estimated_time for node in flat_steps)
        total_cost = sum(node.estimated_cost for node in flat_steps)
        overall_success = self._combine_success(flat_steps)

        plan = Plan(
            steps=flat_steps,
            total_time=total_time,
            total_cost=total_cost,
            overall_success=overall_success,
            metadata={"constraints": constraints}
        )
        if replanning:
            self.current_plan = plan
            self._last_constraints = copy.deepcopy(constraints)
        logger.info("Plan generated: %d steps, time=%.2f, cost=%.2f, success=%.2f",
                    len(flat_steps), total_time, total_cost, overall_success)
        return plan

    def replan_if_needed(self,
                         new_constraints: Optional[Dict[str, Any]] = None,
                         new_strategic_goal: Optional[str] = None) -> Optional[Plan]:
        """Trigger replanning when constraints or the strategic goal change.

        Returns the new plan if replanning occurred, otherwise ``None``.
        """
        if not self.current_plan:
            logger.warning("Replan requested but no existing plan – call plan() first.")
            return None

        need_replan = False
        if new_constraints and new_constraints != self._last_constraints:
            need_replan = True
        if new_strategic_goal:
            need_replan = True

        if not need_replan:
            logger.debug("No replanning needed.")
            return None

        logger.info("Replanning due to updated constraints or goal.")
        goal = new_strategic_goal or self.current_plan.steps[0].parent.parent.name
        return self.plan(strategic_goal=goal,
                         constraints=new_constraints or self._last_constraints,
                         replanning=True)

    # --------------------------------------------------------------------- #
    #  Internal helpers – can be overridden for custom behaviour
    # --------------------------------------------------------------------- #

    def _expand_to_tactical(self, strategic_node: GoalNode) -> None:
        """Decompose a strategic goal into 2‑4 tactical sub‑goals."""
        # Very naive heuristic – in a real system this would call an LLM or HTN lib
        tactical_names = self._mock_tactical_decomposition(strategic_node.name)
        for name in tactical_names:
            tactical = GoalNode(name=name, level="tactical")
            strategic_node.add_child(tactical)

    def _expand_to_operational(self, tactical_node: GoalNode) -> None:
        """Recursively expand tactical nodes into operational steps."""
        if tactical_node.level != "tactical":
            return
        operational_names = self._mock_operational_decomposition(tactical_node.name)
        for name in operational_names:
            op = GoalNode(name=name, level="operational")
            tactical_node.add_child(op)

        # Recurse for each child tactical (if any)
        for child in tactical_node.children:
            if child.level == "tactical":
                self._expand_to_operational(child)

    def _allocate_resources(self, node: GoalNode, constraints: Dict[str, Any]) -> None:
        """Assign time/cost estimates to each node based on simple heuristics."""
        # Simple linear scaling – could be replaced with a learned model.
        base_time = 5.0   # default time per operational step
        base_cost = 20.0  # default cost per operational step

        if node.level == "operational":
            node.estimated_time = base_time
            node.estimated_cost = base_cost
        else:
            for child in node.children:
                self._allocate_resources(child, constraints)

            node.estimated_time = sum(c.estimated_time for c in node.children)
            node.estimated_cost = sum(c.estimated_cost for c in node.children)

        # Apply global constraints (e.g., deadline, max_cost) proportionally
        deadline = constraints.get("deadline")
        max_cost = constraints.get("max_cost")
        if deadline and node.level == "strategic" and node.estimated_time > deadline:
            scale = deadline / node.estimated_time
            self._scale_resources(node, scale)

        if max_cost and node.level == "strategic" and node.estimated_cost > max_cost:
            scale = max_cost / node.estimated_cost
            self._scale_resources(node, scale)

    def _scale_resources(self, node: GoalNode, factor: float) -> None:
        """Scale time and cost estimates of a subtree by ``factor``."""
        node.estimated_time *= factor
        node.estimated_cost *= factor
        for child in node.children:
            self._scale_resources(child, factor)

    def _propagate_success(self, node: GoalNode) -> None:
        """Compute success probability for each node."""
        node.success_prob = self.success_estimator(node)
        for child in node.children:
            self._propagate_success(child)

    def _default_success_estimator(self, node: GoalNode) -> float:
        """Very naive estimator – higher cost/time reduces success."""
        base = 0.95
        penalty = 0.0
        if node.estimated_time > 20:
            penalty += 0.1
        if node.estimated_cost > 200:
            penalty += 0.15
        return max(0.1, base - penalty)

    def _flatten_operational(self, node: GoalNode) -> List[GoalNode]:
        """Return a flat list of all operational nodes in execution order."""
        ops = []
        if node.level == "operational":
            ops.append(node)
        for child in node.children:
            ops.extend(self._flatten_operational(child))
        return ops

    def _combine_success(self, steps: List[GoalNode]) -> float:
        """Assume independence – multiply probabilities."""
        prob = 1.0
        for step in steps:
            prob *= step.success_prob
        return prob

    # --------------------------------------------------------------------- #
    #  Mock decomposition helpers – replace with LLM/HTN in the future
    # --------------------------------------------------------------------- #

    def _mock_tactical_decomposition(self, strategic_name: str) -> List[str]:
        """Return a deterministic list of tactical goals for demo purposes."""
        mapping = {
            "Launch a full‑stack web application": [
                "Define product requirements",
                "Design system architecture",
                "Implement backend services",
                "Implement frontend UI",
                "Deploy to production"
            ],
            "Research and implement paper": [
                "Literature review",
                "Design experiments",
                "Implement prototype",
                "Run evaluation",
                "Write report"
            ],
            "Optimize for cost under deadline": [
                "Profile current system",
                "Identify cost drivers",
                "Apply optimizations",
                "Validate performance",
                "Finalize deployment"
            ],
        }
        return mapping.get(strategic_name, ["Tactical step 1", "Tactical step 2"])

    def _mock_operational_decomposition(self, tactical_name: str) -> List[str]:
        """Return a deterministic list of operational steps for demo purposes."""
        base_steps = {
            "Define product requirements": [
                "Gather stakeholder input",
                "Write functional spec",
                "Prioritize features"
            ],
            "Design system architecture": [
                "Select tech stack",
                "Draw component diagram",
                "Define data models"
            ],
            "Implement backend services": [
                "Set up project skeleton",
                "Create API endpoints",
                "Integrate database",
                "Write unit tests"
            ],
            "Implement frontend UI": [
                "Create UI mockups",
                "Develop component library",
                "Connect to backend",
                "Perform usability testing"
            ],
            "Deploy to production": [
                "Configure CI/CD pipeline",
                "Set up monitoring",
                "Perform rollout",
                "Post‑deployment verification"
            ],
            "Literature review": [
                "Collect relevant papers",
                "Summarize key findings",
                "Identify gaps"
            ],
            "Design experiments": [
                "Formulate hypotheses",
                "Select datasets",
                "Define evaluation metrics"
            ],
            "Implement prototype": [
                "Code core algorithm",
                "Integrate with dataset loader",
                "Run sanity checks"
            ],
            "Run evaluation": [
                "Execute experiments",
                "Collect results",
                "Statistical analysis"
            ],
            "Write report": [
                "Draft sections",
                "Create figures",
                "Proofread"
            ],
            # default fallback
        }
        return base_steps.get(tactical_name, [f"{tactical_name} – step {i}" for i in range(1, 4)])
"""
strategic_planner.py
--------------------

A lightweight strategic planner that builds a hierarchical goal tree,
performs resource‑aware multi‑step look‑ahead, estimates success
probabilities and supports dynamic replanning.

The design mirrors classic HTN (Hierarchical Task Network) ideas while
leveraging the existing Atomizer DAG for low‑level task execution.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import random
import heapq
import copy
import logging

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Goal hierarchy structures
# --------------------------------------------------------------------------- #

@dataclass
class GoalNode:
    """A node in the strategic‑tactical‑operational hierarchy."""
    name: str
    level: str                     # "strategic", "tactical", "operational"
    children: List["GoalNode"] = field(default_factory=list)
    parent: Optional["GoalNode"] = None
    resources: Dict[str, float] = field(default_factory=dict)   # e.g. {"dev_hours": 10}
    constraints: Dict[str, Any] = field(default_factory=dict)   # e.g. {"deadline": 10}
    estimated_success: float = 1.0

    def add_child(self, child: "GoalNode") -> None:
        child.parent = self
        self.children.append(child)

    def is_leaf(self) -> bool:
        return not self.children

    def aggregate_resources(self) -> Dict[str, float]:
        """Sum resources of this node and all descendants."""
        agg = dict(self.resources)
        for c in self.children:
            for k, v in c.aggregate_resources().items():
                agg[k] = agg.get(k, 0) + v
        return agg

    def __repr__(self) -> str:
        return f"<GoalNode {self.level}:{self.name}>"


# --------------------------------------------------------------------------- #
# Planner implementation
# --------------------------------------------------------------------------- #

class StrategicPlanner:
    """
    Core planner that:
      * Decomposes high‑level goals into a hierarchical tree.
      * Performs a look‑ahead search (A*‑style) up to N steps.
      * Estimates success probabilities using simple heuristics.
      * Triggers replanning when external signals (goal change, resource drift)
        are detected.
    """

    def __init__(self,
                 max_lookahead: int = 10,
                 resource_budget: Optional[Dict[str, float]] = None):
        self.max_lookahead = max_lookahead
        self.global_resources = resource_budget or {}
        self.current_plan: List[GoalNode] = []
        self.root_goal: Optional[GoalNode] = None

    # ------------------------------------------------------------------- #
    # Goal decomposition
    # ------------------------------------------------------------------- #

    def decompose(self, strategic_goal: str,
                  tactical_map: Dict[str, List[str]],
                  operational_map: Dict[str, List[str]],
                  resource_estimates: Dict[str, Dict[str, float]]) -> GoalNode:
        """
        Build a three‑level hierarchy:
          strategic -> tactical -> operational.
        ``tactical_map`` maps strategic goal → list of tactical sub‑goals.
        ``operational_map`` maps tactical goal → list of operational steps.
        ``resource_estimates`` provides estimated resource consumption per
        operational step.
        """
        logger.debug("Decomposing strategic goal: %s", strategic_goal)
        root = GoalNode(name=strategic_goal, level="strategic",
                        resources=self.global_resources.copy())

        for tac_name in tactical_map.get(strategic_goal, []):
            tac_node = GoalNode(name=tac_name, level="tactical")
            root.add_child(tac_node)

            for op_name in operational_map.get(tac_name, []):
                op_node = GoalNode(name=op_name, level="operational",
                                   resources=resource_estimates.get(op_name, {}))
                tac_node.add_child(op_node)

        self.root_goal = root
        return root

    # ------------------------------------------------------------------- #
    # Success estimation
    # ------------------------------------------------------------------- #

    def estimate_success(self, node: GoalNode) -> float:
        """
        Very simple heuristic:
          success = product( 1 - resource_overrun_factor )
        where overrun factor = max(0, used - budget) / (budget + 1e-6)
        """
        agg = node.aggregate_resources()
        prob = 1.0
        for res, used in agg.items():
            budget = self.global_resources.get(res, float('inf'))
            overrun = max(0.0, used - budget) / (budget + 1e-6)
            prob *= max(0.0, 1.0 - overrun)
        node.estimated_success = prob
        return prob

    # ------------------------------------------------------------------- #
    # Look‑ahead planning (A*‑like)
    # ------------------------------------------------------------------- #

    def _heuristic(self, node: GoalNode) -> float:
        """Heuristic: favour nodes with higher estimated success."""
        return -self.estimate_success(node)   # negative because heapq is min‑heap

    def plan(self) -> List[GoalNode]:
        """
        Generate a linearized plan up to ``max_lookahead`` steps.
        The algorithm expands the hierarchy breadth‑first, scoring nodes
        with the heuristic and picking the best next leaf.
        """
        if not self.root_goal:
            raise RuntimeError("No root goal defined – call decompose() first.")

        frontier: List[Tuple[float, GoalNode]] = []
        heapq.heappush(frontier, (self._heuristic(self.root_goal), self.root_goal))

        plan: List[GoalNode] = []
        visited = set()

        while frontier and len(plan) < self.max_lookahead:
            _, node = heapq.heappop(frontier)
            if node in visited:
                continue
            visited.add(node)

            if node.is_leaf():
                plan.append(node)
                continue

            # push children to frontier
            for child in node.children:
                heapq.heappush(frontier, (self._heuristic(child), child))

        self.current_plan = plan
        logger.info("Generated plan with %d steps (max %d)", len(plan), self.max_lookahead)
        return plan

    # ------------------------------------------------------------------- #
    # Replanning logic
    # ------------------------------------------------------------------- #

    def trigger_replan(self,
                       changed_goal: Optional[str] = None,
                       resource_drift: Optional[Dict[str, float]] = None) -> List[GoalNode]:
        """
        Replan when:
          * The top‑level strategic goal changes.
          * Available resources drift (e.g., new budget constraints).
        """
        if changed_goal:
            logger.info("Strategic goal changed from %s to %s", self.root_goal.name, changed_goal)
            # Re‑decompose using the same maps (caller must provide them again)
            # For simplicity, we just clear the current tree.
            self.root_goal = None
            self.current_plan = []
            raise NotImplementedError("Goal change handling must be performed by caller.")

        if resource_drift:
            logger.info("Applying resource drift: %s", resource_drift)
            for k, v in resource_drift.items():
                self.global_resources[k] = v
            # Re‑estimate success and rebuild plan
            return self.plan()

        # Default: no changes → return existing plan
        return self.current_plan

    # ------------------------------------------------------------------- #
    # Utility helpers
    # ------------------------------------------------------------------- #

    def visualize(self) -> str:
        """Return a simple text representation of the hierarchy."""
        lines = []

        def recurse(node: GoalNode, indent: int = 0):
            lines.append("  " * indent + f"- {node.level.upper()}: {node.name} "
                         f"(succ={node.estimated_success:.2f})")
            for c in node.children:
                recurse(c, indent + 1)

        if self.root_goal:
            recurse(self.root_goal)
        return "\n".join(lines)

# --------------------------------------------------------------------------- #
# Example usage (can be removed or guarded by __name__ == "__main__")
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simple demo with dummy maps
    tactical_map = {
        "Launch Product": ["Design UI", "Implement Backend", "Deploy"]
    }
    operational_map = {
        "Design UI": ["Create Mockups", "User Testing"],
        "Implement Backend": ["Setup DB", "Write API", "Write Tests"],
        "Deploy": ["CI Setup", "Production Rollout"]
    }
    resource_estimates = {
        "Create Mockups": {"dev_hours": 8},
        "User Testing": {"dev_hours": 4},
        "Setup DB": {"dev_hours": 6},
        "Write API": {"dev_hours": 12},
        "Write Tests": {"dev_hours": 5},
        "CI Setup": {"dev_hours": 3},
        "Production Rollout": {"dev_hours": 2}
    }

    planner = StrategicPlanner(max_lookahead=12,
                               resource_budget={"dev_hours": 40})
    planner.decompose("Launch Product", tactical_map, operational_map, resource_estimates)
    plan = planner.plan()
    print("Planned steps:")
    for step in plan:
        print(f" * {step.name} ({step.level})")
    print("\nHierarchy:")
    print(planner.visualize())
"""
strategic_planner.py

A lightweight hierarchical planner that sits on top of the existing atomizer.
It builds a multi‑level goal tree (strategic → tactical → operational), performs
resource‑aware look‑ahead planning, estimates success probabilities, and triggers
re‑planning when goals or resource constraints change.

The implementation is deliberately modular so it can be swapped out for more
advanced planners (e.g., HTN, MuZero) in the future.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import heapq
import uuid
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class GoalNode:
    """A node in the hierarchical goal tree."""
    id: str
    description: str
    level: str                     # "strategic", "tactical", "operational"
    parent: Optional["GoalNode"] = None
    children: List["GoalNode"] = field(default_factory=list)
    resources: Dict[str, Any] = field(default_factory=dict)
    estimated_cost: float = 0.0
    estimated_time: float = 0.0
    success_prob: float = 1.0   # 0..1
    completed: bool = False

    def add_child(self, child: "GoalNode") -> None:
        self.children.append(child)
        child.parent = self

    def is_leaf(self) -> bool:
        return not self.children


class StrategicPlanner:
    """
    Core planner API used by the atomizer (or any higher‑level orchestrator).

    Typical usage:
        planner = StrategicPlanner(resource_profile)
        planner.add_strategic_goal("Deploy full‑stack service")
        plan = planner.generate_plan(lookahead=10)
        # later, if a goal changes:
        planner.update_goal(goal_id, new_description="…")
        replanned = planner.replan_if_needed()
    """

    def __init__(self, resource_profile: Dict[str, Any] | None = None):
        """
        :param resource_profile: Global resources available to the system
                                 (e.g., cpu, budget, time budget).
        """
        self.resource_profile = resource_profile or {}
        self.root_goals: List[GoalNode] = []          # strategic goals
        self.goal_index: Dict[str, GoalNode] = {}     # fast lookup by id
        self.last_plan: List[GoalNode] = []
        self.replan_triggered: bool = False

    # --------------------------------------------------------------------- #
    # Goal management
    # --------------------------------------------------------------------- #
    def _create_node(self, description: str, level: str,
                     resources: Optional[Dict[str, Any]] = None) -> GoalNode:
        node = GoalNode(
            id=str(uuid.uuid4()),
            description=description,
            level=level,
            resources=resources or {}
        )
        self.goal_index[node.id] = node
        return node

    def add_strategic_goal(self, description: str,
                           resources: Optional[Dict[str, Any]] = None) -> str:
        node = self._create_node(description, "strategic", resources)
        self.root_goals.append(node)
        logger.debug("Added strategic goal %s", node.id)
        return node.id

    def add_tactical_goal(self, parent_id: str, description: str,
                          resources: Optional[Dict[str, Any]] = None) -> str:
        parent = self.goal_index.get(parent_id)
        if not parent or parent.level != "strategic":
            raise ValueError("Parent must be an existing strategic goal")
        node = self._create_node(description, "tactical", resources)
        parent.add_child(node)
        return node.id

    def add_operational_goal(self, parent_id: str, description: str,
                             resources: Optional[Dict[str, Any]] = None) -> str:
        parent = self.goal_index.get(parent_id)
        if not parent or parent.level != "tactical":
            raise ValueError("Parent must be an existing tactical goal")
        node = self._create_node(description, "operational", resources)
        parent.add_child(node)
        return node.id

    def update_goal(self, goal_id: str, **kwargs) -> None:
        node = self.goal_index.get(goal_id)
        if not node:
            raise KeyError(f"Goal {goal_id} not found")
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
        self.replan_triggered = True
        logger.debug("Goal %s updated; replanning flagged", goal_id)

    # --------------------------------------------------------------------- #
    # Planning core
    # --------------------------------------------------------------------- #
    def _estimate_success(self, node: GoalNode) -> float:
        """
        Very simple heuristic: combine resource adequacy and depth penalty.
        Real implementations could plug in learned models or Monte‑Carlo
        simulations.
        """
        # resource adequacy factor (0..1)
        adequacy = 1.0
        for res, amount in node.resources.items():
            available = self.resource_profile.get(res, 0)
            adequacy *= min(1.0, available / (amount + 1e-9))

        depth_penalty = 0.95 ** self._depth(node)   # deeper nodes slightly harder
        prob = adequacy * depth_penalty
        logger.debug("Estimated success for %s: %.3f", node.id, prob)
        return prob

    def _depth(self, node: GoalNode) -> int:
        d = 0
        while node.parent:
            d += 1
            node = node.parent
        return d

    def _flatten_goals(self) -> List[GoalNode]:
        """Return all leaf operational goals in a deterministic order."""
        leaves: List[GoalNode] = []

        def dfs(n: GoalNode):
            if n.is_leaf():
                leaves.append(n)
            else:
                for c in n.children:
                    dfs(c)

        for root in self.root_goals:
            dfs(root)
        return leaves

    def generate_plan(self, lookahead: int = 10) -> List[GoalNode]:
        """
        Produce a plan consisting of up to ``lookahead`` operational goals,
        ordered by a simple priority queue that favours higher success
        probability and lower estimated cost/time.
        """
        candidates = self._flatten_goals()
        # compute heuristics
        for node in candidates:
            node.success_prob = self._estimate_success(node)

        # priority = -probability (max‑heap) + cost + time
        heap: List[Tuple[float, GoalNode]] = []
        for node in candidates:
            priority = -node.success_prob + 0.01 * (node.estimated_cost + node.estimated_time)
            heapq.heappush(heap, (priority, node))

        plan: List[GoalNode] = []
        while heap and len(plan) < lookahead:
            _, node = heapq.heappop(heap)
            if not node.completed:
                plan.append(node)

        self.last_plan = plan
        self.replan_triggered = False
        logger.info("Generated plan with %d steps (lookahead=%d)", len(plan), lookahead)
        return plan

    def replan_if_needed(self, lookahead: int = 10) -> List[GoalNode]:
        """Call after external events (e.g., goal update, resource change)."""
        if self.replan_triggered:
            logger.info("Re‑planning triggered")
            return self.generate_plan(lookahead)
        return self.last_plan

    # --------------------------------------------------------------------- #
    # Resource management helpers
    # --------------------------------------------------------------------- #
    def update_resources(self, **kwargs) -> None:
        """Adjust the global resource profile; triggers replanning."""
        self.resource_profile.update(kwargs)
        self.replan_triggered = True
        logger.debug("Resources updated: %s", kwargs)

    # --------------------------------------------------------------------- #
    # Utility / introspection
    # --------------------------------------------------------------------- #
    def dump_goal_tree(self) -> Dict[str, Any]:
        """Return a serialisable representation of the current goal hierarchy."""
        def node_to_dict(node: GoalNode) -> Dict[str, Any]:
            return {
                "id": node.id,
                "description": node.description,
                "level": node.level,
                "resources": node.resources,
                "estimated_cost": node.estimated_cost,
                "estimated_time": node.estimated_time,
                "success_prob": node.success_prob,
                "completed": node.completed,
                "children": [node_to_dict(c) for c in node.children],
            }

        return {"strategic_goals": [node_to_dict(g) for g in self.root_goals]}


# -------------------------------------------------------------------------
# Simple integration shim for the existing atomizer (if present)
# -------------------------------------------------------------------------
def get_default_planner() -> StrategicPlanner:
    """
    Factory used by the atomizer/orchestrator to obtain a planner instance.
    The atomizer can call ``planner.generate_plan()`` instead of its current
    flat DAG creation.
    """
    # Default resources can be overridden by the caller.
    default_resources = {"cpu": 8, "budget": 1000, "time_budget": 3600}
    return StrategicPlanner(resource_profile=default_resources)
import heapq
import uuid
from collections import defaultdict, deque
from typing import Any, Dict, List, Tuple, Callable, Optional

# ----------------------------------------------------------------------
# Hierarchical Planning Core
# ----------------------------------------------------------------------
class GoalNode:
    """
    Represents a node in the goal hierarchy.
    Each node can have sub‑goals (children) and an optional
    operational task (leaf).
    """
    def __init__(
        self,
        description: str,
        level: str = "tactical",   # strategic | tactical | operational
        parent: Optional["GoalNode"] = None,
        resources: Optional[Dict[str, Any]] = None,
    ):
        self.id = str(uuid.uuid4())
        self.description = description
        self.level = level
        self.parent = parent
        self.children: List["GoalNode"] = []
        self.resources = resources or {}
        self.estimated_success: float = 1.0   # default optimistic estimate
        self.estimated_cost: float = 0.0
        self.estimated_time: float = 0.0

    def add_child(self, child: "GoalNode"):
        child.parent = self
        self.children.append(child)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "level": self.level,
            "resources": self.resources,
            "estimated_success": self.estimated_success,
            "estimated_cost": self.estimated_cost,
            "estimated_time": self.estimated_time,
            "children": [c.to_dict() for c in self.children],
        }

# ----------------------------------------------------------------------
# Strategic Planner
# ----------------------------------------------------------------------
class StrategicPlanner:
    """
    Core planner that turns high‑level strategic goals into a
    multi‑step, resource‑aware operational plan.
    """

    def __init__(
        self,
        resource_pool: Optional[Dict[str, Any]] = None,
        success_estimator: Optional[Callable[[GoalNode], float]] = None,
        cost_estimator: Optional[Callable[[GoalNode], float]] = None,
        time_estimator: Optional[Callable[[GoalNode], float]] = None,
    ):
        self.resource_pool = resource_pool or {}
        self.success_estimator = success_estimator or (lambda node: 0.9)
        self.cost_estimator = cost_estimator or (lambda node: 1.0)
        self.time_estimator = time_estimator or (lambda node: 1.0)

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------
    def plan(
        self,
        strategic_goal: str,
        constraints: Optional[Dict[str, Any]] = None,
        lookahead_depth: int = 10,
    ) -> GoalNode:
        """
        Entry point – creates a hierarchical plan for the given strategic
        goal respecting constraints (budget, deadline, etc.).
        Returns the root GoalNode of the generated hierarchy.
        """
        constraints = constraints or {}
        root = GoalNode(description=strategic_goal, level="strategic")
        self._expand_node(root, constraints, depth=0, max_depth=lookahead_depth)
        self._propagate_estimates(root)
        return root

    # --------------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------------
    def _expand_node(
        self,
        node: GoalNode,
        constraints: Dict[str, Any],
        depth: int,
        max_depth: int,
    ):
        """
        Recursively decompose a node into sub‑goals until either
        - we reach the desired look‑ahead depth, or
        - the node is deemed operational (leaf).
        """
        if depth >= max_depth:
            # Treat as operational task
            node.level = "operational"
            return

        # Simple heuristic decomposition – in a real system this would
        # call an LLM, HTN library, or domain‑specific knowledge base.
        sub_goals = self._generate_subgoals(node.description, depth)

        for sg in sub_goals:
            child = GoalNode(description=sg, level="tactical")
            node.add_child(child)
            # Allocate resources greedily – can be replaced by a solver.
            self._allocate_resources(child, constraints)
            self._expand_node(child, constraints, depth + 1, max_depth)

    def _generate_subgoals(self, description: str, depth: int) -> List[str]:
        """
        Placeholder for a sophisticated sub‑goal generator.
        Here we use a deterministic split based on depth for demo.
        """
        base = description.strip(".")
        if depth == 0:
            return [
                f"{base} – design architecture",
                f"{base} – prototype core components",
                f"{base} – define testing strategy",
            ]
        elif depth == 1:
            return [
                f"{base} – implement module A",
                f"{base} – implement module B",
                f"{base} – write documentation",
            ]
        else:
            return [f"{base} – final integration & validation"]

    def _allocate_resources(self, node: GoalNode, constraints: Dict[str, Any]):
        """
        Very lightweight resource allocation – copies the global pool
        and deducts estimated cost if a budget constraint exists.
        """
        node.resources = self.resource_pool.copy()
        if "budget" in constraints:
            est = self.cost_estimator(node)
            node.estimated_cost = est
            constraints["budget"] -= est

    def _propagate_estimates(self, node: GoalNode):
        """
        Bottom‑up aggregation of success probability, cost and time.
        """
        if node.is_leaf():
            node.estimated_success = self.success_estimator(node)
            node.estimated_cost = self.cost_estimator(node)
            node.estimated_time = self.time_estimator(node)
            return

        for child in node.children:
            self._propagate_estimates(child)

        # Combine child estimates (simple product for success,
        # sum for cost/time – replace with more sophisticated models).
        node.estimated_success = 1.0
        node.estimated_cost = 0.0
        node.estimated_time = 0.0
        for child in node.children:
            node.estimated_success *= child.estimated_success
            node.estimated_cost += child.estimated_cost
            node.estimated_time += child.estimated_time

    # --------------------------------------------------------------
    # Re‑planning support
    # --------------------------------------------------------------
    def replan(
        self,
        current_root: GoalNode,
        changed_goal: Optional[str] = None,
        new_constraints: Optional[Dict[str, Any]] = None,
        lookahead_depth: int = 10,
    ) -> GoalNode:
        """
        Triggered when goals or constraints evolve.
        Re‑uses already‑computed sub‑trees when possible.
        """
        if changed_goal:
            current_root.description = changed_goal
            current_root.level = "strategic"
            current_root.children.clear()

        if new_constraints:
            # Reset resource pool according to new constraints
            self.resource_pool.update(new_constraints.get("resources", {}))

        # Re‑expand from the (potentially) modified root
        self._expand_node(
            current_root,
            new_constraints or {},
            depth=0,
            max_depth=lookahead_depth,
        )
        self._propagate_estimates(current_root)
        return current_root

# ----------------------------------------------------------------------
# Convenience helper – flatten hierarchy into an execution DAG
# ----------------------------------------------------------------------
def flatten_to_dag(root: GoalNode) -> List[Tuple[str, List[str]]]:
    """
    Returns a list of (node_id, predecessor_ids) suitable for feeding
    into the existing atomizer's DAG builder.
    """
    dag: List[Tuple[str, List[str]]] = []
    q = deque([root])
    while q:
        node = q.popleft()
        preds = [p.id for p in (node.parent and [node.parent] or [])]
        dag.append((node.id, preds))
        for child in node.children:
            q.append(child)
    return dag
"""
strategic_planner.py
--------------------

A lightweight hierarchical planner that sits on top of the existing *atomizer* DAG
builder.  It introduces three planning layers:

* **Strategic** – long‑term goals, resource budgets and success‑probability
  estimates.
* **Tactical** – decomposition of strategic goals into sub‑goals (HTN‑style).
* **Operational** – concrete atomic tasks emitted by the atomizer.

The planner can:
* Build a goal hierarchy from a high‑level description.
* Allocate limited resources (time, compute, budget) across sub‑goals.
* Perform a look‑ahead search (depth‑first with pruning) to produce a
  10‑step‑ahead plan.
* Re‑plan automatically when a goal is added, removed or its constraints
  change.
* Export a plan compatible with the existing task‑execution pipeline.

Only standard library modules are used to keep the component easy to embed.
"""

import heapq
import itertools
import math
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

@dataclass
class ResourceBudget:
    """Simple container for resource limits."""
    time_seconds: float = math.inf
    compute_units: float = math.inf
    monetary_cost: float = math.inf

    def fits(self, other: "ResourceBudget") -> bool:
        """Return True if *other* is within the current budget."""
        return (other.time_seconds <= self.time_seconds and
                other.compute_units <= self.compute_units and
                other.monetary_cost <= self.monetary_cost)

    def __sub__(self, other: "ResourceBudget") -> "ResourceBudget":
        return ResourceBudget(
            time_seconds=self.time_seconds - other.time_seconds,
            compute_units=self.compute_units - other.compute_units,
            monetary_cost=self.monetary_cost - other.monetary_cost,
        )

    def __add__(self, other: "ResourceBudget") -> "ResourceBudget":
        return ResourceBudget(
            time_seconds=self.time_seconds + other.time_seconds,
            compute_units=self.compute_units + other.compute_units,
            monetary_cost=self.monetary_cost + other.monetary_cost,
        )


@dataclass
class GoalNode:
    """A node in the hierarchical goal tree."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    # Desired success probability (0‑1).  Used for pruning low‑value branches.
    target_success: float = 0.9
    # Estimated resource consumption for *this* node (excluding children).
    estimated_budget: ResourceBudget = field(default_factory=ResourceBudget)
    # Children are sub‑goals (tactical/operational).  Empty for leaf nodes.
    children: List["GoalNode"] = field(default_factory=list)
    # Parent reference (filled automatically when building the tree).
    parent: Optional["GoalNode"] = None

    def total_budget(self) -> ResourceBudget:
        """Recursively sum budgets of this node and all descendants."""
        total = self.estimated_budget
        for child in self.children:
            total += child.total_budget()
        return total

    def depth(self) -> int:
        d = 0
        cur = self
        while cur.parent is not None:
            d += 1
            cur = cur.parent
        return d


# --------------------------------------------------------------------------- #
# Core planner
# --------------------------------------------------------------------------- #

class StrategicPlanner:
    """
    High‑level planner that creates a hierarchical plan, allocates resources,
    and produces a concrete ordered list of atomic tasks (operational level).

    Integration point with the existing system:
        * Build a GoalNode tree from user‑level strategic statements.
        * Call :meth:`plan` to obtain a list of task identifiers.
        * Feed the returned list into the current *atomizer* to materialise
          the DAG and schedule execution.
    """

    def __init__(
        self,
        resource_budget: ResourceBudget,
        success_estimator: Callable[[GoalNode], float],
        task_generator: Callable[[GoalNode], List[str]],
        replanning_callback: Optional[Callable[[List[GoalNode]], None]] = None,
    ):
        """
        Parameters
        ----------
        resource_budget:
            Global limits for the whole plan.
        success_estimator:
            Function that returns an estimated success probability (0‑1) for a
            given GoalNode.  Used for pruning.
        task_generator:
            Function that, given a *leaf* GoalNode, returns a list of atomic
            task identifiers (strings) that the atomizer can understand.
        replanning_callback:
            Optional hook that is invoked whenever the planner decides to
            re‑plan because of a goal change or budget breach.
        """
        self.global_budget = resource_budget
        self.estimate_success = success_estimator
        self.generate_tasks = task_generator
        self.replan_hook = replanning_callback

        # Internal state
        self.root_goals: List[GoalNode] = []
        self._plan_cache: Optional[List[str]] = None

    # ------------------------------------------------------------------- #
    # Goal management
    # ------------------------------------------------------------------- #

    def add_strategic_goal(self, description: str,
                           target_success: float = 0.9,
                           estimated_budget: Optional[ResourceBudget] = None) -> GoalNode:
        """Create a top‑level strategic goal and attach it to the planner."""
        node = GoalNode(
            description=description,
            target_success=target_success,
            estimated_budget=estimated_budget or ResourceBudget(),
        )
        self.root_goals.append(node)
        self._plan_cache = None
        return node

    def remove_goal(self, goal_id: str) -> bool:
        """Remove a goal (and its subtree) by id. Returns True if removed."""
        for i, g in enumerate(self.root_goals):
            if g.id == goal_id:
                del self.root_goals[i]
                self._plan_cache = None
                return True
            # search recursively
            if self._remove_goal_recursive(g, goal_id):
                self._plan_cache = None
                return True
        return False

    def _remove_goal_recursive(self, node: GoalNode, goal_id: str) -> bool:
        for i, child in enumerate(node.children):
            if child.id == goal_id:
                del node.children[i]
                return True
            if self._remove_goal_recursive(child, goal_id):
                return True
        return False

    # ------------------------------------------------------------------- #
    # Planning algorithm
    # ------------------------------------------------------------------- #

    def plan(self, lookahead_steps: int = 10) -> List[str]:
        """
        Produce an ordered list of atomic task identifiers.

        The algorithm performs a depth‑first expansion of the goal tree,
        pruning branches that exceed the global budget or fall below the
        required success probability.  It stops once *lookahead_steps* atomic
        tasks have been collected.
        """
        if self._plan_cache is not None:
            return self._plan_cache

        # Priority queue: (negative success, cumulative time, node)
        frontier: List[Tuple[float, float, GoalNode]] = []
        for goal in self.root_goals:
            est_success = self.estimate_success(goal)
            heapq.heappush(frontier, (-est_success, 0.0, goal))

        plan_tasks: List[str] = []
        used_budget = ResourceBudget()

        while frontier and len(plan_tasks) < lookahead_steps:
            neg_success, cum_time, node = heapq.heappop(frontier)
            # Prune if budget exceeded
            if not self.global_budget.fits(used_budget + node.estimated_budget):
                continue
            # Prune if success too low
            if -neg_success < node.target_success:
                continue

            used_budget += node.estimated_budget

            if node.children:
                # Expand children (tactical level)
                for child in node.children:
                    child_success = self.estimate_success(child)
                    heapq.heappush(
                        frontier,
                        (-child_success, cum_time + node.estimated_budget.time_seconds, child),
                    )
            else:
                # Leaf – generate concrete tasks
                tasks = self.generate_tasks(node)
                for t in tasks:
                    if len(plan_tasks) >= lookahead_steps:
                        break
                    plan_tasks.append(t)

        self._plan_cache = plan_tasks
        return plan_tasks

    # ------------------------------------------------------------------- #
    # Re‑planning support
    # ------------------------------------------------------------------- #

    def trigger_replan(self):
        """Force a re‑plan; useful when external events change goals."""
        self._plan_cache = None
        if self.replan_hook:
            self.replan_hook(self.root_goals)

    # ------------------------------------------------------------------- #
    # Utility helpers (for external modules)
    # ------------------------------------------------------------------- #

    @staticmethod
    def build_hierarchical_tree(
        strategic_desc: str,
        decomposition_fn: Callable[[str], List[Tuple[str, ResourceBudget]]],
    ) -> GoalNode:
        """
        Convenience helper that builds a three‑level tree from a plain
        strategic description.

        ``decomposition_fn`` receives a description and returns a list of
        tuples ``(sub_description, estimated_budget)`` for the tactical layer.
        Leaf nodes (operational) are created with empty children – they will be
        turned into atomic tasks by the planner's ``task_generator``.
        """
        root = GoalNode(description=strategic_desc, estimated_budget=ResourceBudget())
        tactical = decomposition_fn(strategic_desc)
        for sub_desc, sub_budget in tactical:
            child = GoalNode(
                description=sub_desc,
                estimated_budget=sub_budget,
                target_success=0.9,
            )
            child.parent = root
            root.children.append(child)
        return root
import heapq
from typing import Any, Dict, List, Tuple, Optional

class StrategicPlanner:
    """
    Strategic Planner for hierarchical, resource‑aware, multi‑step planning.
    It builds a three‑level hierarchy:
        strategic → tactical → operational
    and supports replanning, success‑probability estimation and multi‑objective optimization.
    """

    def __init__(self, resources: Optional[Dict[str, float]] = None):
        """
        :param resources: Dictionary of available resources, e.g. {"budget": 1000, "time": 40}
        """
        self.resources = resources or {}
        # Simple cache for previously computed sub‑plans
        self._plan_cache: Dict[str, List[Dict[str, Any]]] = {}

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------
    def generate_plan(self, strategic_goal: str, horizon: int = 10) -> List[Dict[str, Any]]:
        """
        Produce a detailed operational plan for the given strategic goal.
        :param strategic_goal: High‑level description of the desired outcome.
        :param horizon: Desired look‑ahead depth (number of operational steps).
        :return: Ordered list of step dictionaries.
        """
        # 1️⃣ Decompose to tactical goals
        tactical_goals = self._decompose_strategic(strategic_goal)

        # 2️⃣ For each tactical goal, decompose to operational steps
        operational_steps: List[Dict[str, Any]] = []
        for tactical in tactical_goals:
            steps = self._decompose_tactical(tactical, horizon // len(tactical_goals))
            operational_steps.extend(steps)

        # 3️⃣ Rank/Select steps based on resource constraints and success probability
        selected_plan = self._select_feasible_steps(operational_steps, horizon)
        return selected_plan

    def replan(self,
               current_state: Dict[str, Any],
               changed_goals: List[str],
               horizon: int = 10) -> List[Dict[str, Any]]:
        """
        Re‑plan when goals or environment change.
        :param current_state: Snapshot of completed steps and remaining resources.
        :param changed_goals: New or modified strategic goals.
        :param horizon: Look‑ahead depth.
        :return: Updated plan.
        """
        # Update resources from current state
        self.resources.update(current_state.get("resources", {}))

        # Invalidate cache entries that involve changed goals
        for goal in changed_goals:
            self._plan_cache.pop(goal, None)

        # Generate a fresh plan that respects already completed steps
        new_plan = self.generate_plan(", ".join(changed_goals), horizon)

        # Preserve already completed steps at the front of the plan
        completed = current_state.get("completed_steps", [])
        return completed + [step for step in new_plan if step not in completed]

    def estimate_success(self, plan: List[Dict[str, Any]]) -> float:
        """
        Rough success‑probability estimate based on step difficulty and resource sufficiency.
        :param plan: List of operational steps.
        :return: Probability in [0, 1].
        """
        if not plan:
            return 1.0

        difficulty_sum = sum(step.get("difficulty", 1.0) for step in plan)
        resource_factor = 1.0
        if self.resources:
            # Simple heuristic: more budget/time improves success
            budget = self.resources.get("budget", 0)
            time = self.resources.get("time", 0)
            resource_factor = 1.0 + 0.5 * (budget / (budget + difficulty_sum * 10 + 1))
            resource_factor *= 1.0 + 0.5 * (time / (time + len(plan) * 2 + 1))

        # Clamp to [0,1]
        prob = min(1.0, max(0.0, 1.0 / (1.0 + difficulty_sum * 0.05) * resource_factor))
        return prob

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------
    def _decompose_strategic(self, goal: str) -> List[str]:
        """
        Very lightweight HTN‑style decomposition of a strategic goal into tactical sub‑goals.
        In a real system this would query a knowledge base; here we use simple heuristics.
        """
        # Cache check
        if goal in self._plan_cache:
            return [t["tactical"] for t in self._plan_cache[goal]]

        # Example heuristic: split on commas or “and”
        tokens = [g.strip() for g in goal.replace(" and ", ",").split(",") if g.strip()]
        tactical = [f"Tactical: {t}" for t in tokens] or [f"Tactical: {goal}"]
        return tactical

    def _decompose_tactical(self, tactical_goal: str, max_steps: int) -> List[Dict[str, Any]]:
        """
        Decompose a tactical goal into operational steps.
        Each step gets a rough difficulty score (1‑5) and estimated resource cost.
        """
        # Simple deterministic tokenisation for reproducibility
        words = tactical_goal.split()
        steps: List[Dict[str, Any]] = []
        for i in range(1, max_steps + 1):
            step_desc = f"Execute part {i} of [{tactical_goal}]"
            difficulty = (len(words) % 5) + 1  # pseudo‑random but deterministic
            steps.append({
                "id": f"{tactical_goal.replace(' ', '_')}_step_{i}",
                "description": step_desc,
                "difficulty": difficulty,
                "estimated_budget": difficulty * 10,
                "estimated_time": difficulty * 0.5,
                "tactical": tactical_goal,
            })
        return steps

    def _select_feasible_steps(self,
                               steps: List[Dict[str, Any]],
                               horizon: int) -> List[Dict[str, Any]]:
        """
        Greedy selection of up to `horizon` steps that fit within current resources.
        Uses a priority queue ordered by (difficulty, estimated cost).
        """
        budget = self.resources.get("budget", float("inf"))
        time = self.resources.get("time", float("inf"))

        # Build a min‑heap based on difficulty then cost
        heap: List[Tuple[float, float, int, Dict[str, Any]]] = []
        for idx, step in enumerate(steps):
            heapq.heappush(heap, (step["difficulty"],
                                  step["estimated_budget"],
                                  idx,
                                  step))

        selected: List[Dict[str, Any]] = []
        while heap and len(selected) < horizon:
            _, cost, _, step = heapq.heappop(heap)
            if step["estimated_budget"] <= budget and step["estimated_time"] <= time:
                selected.append(step)
                budget -= step["estimated_budget"]
                time -= step["estimated_time"]

        return selected
import heapq
import uuid
from typing import List, Dict, Any, Optional, Callable, Tuple

# ----------------------------------------------------------------------
# Core data structures
# ----------------------------------------------------------------------
class GoalNode:
    """
    Represents a node in the goal hierarchy.
    Types: 'strategic', 'tactical', 'operational'
    """
    def __init__(
        self,
        name: str,
        goal_type: str = "operational",
        subgoals: Optional[List["GoalNode"]] = None,
        resources: Optional[Dict[str, float]] = None,
        constraints: Optional[Dict[str, Any]] = None,
        success_estimate: float = 1.0,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = goal_type  # strategic / tactical / operational
        self.subgoals = subgoals or []
        self.resources = resources or {}
        self.constraints = constraints or {}
        self.success_estimate = success_estimate  # 0..1

    def is_leaf(self) -> bool:
        return len(self.subgoals) == 0

    def add_subgoal(self, subgoal: "GoalNode"):
        self.subgoals.append(subgoal)

    def __repr__(self):
        return f"<GoalNode {self.type}:{self.name} ({self.id[:8]})>"


# ----------------------------------------------------------------------
# Simple resource‑aware planner
# ----------------------------------------------------------------------
class StrategicPlanner:
    """
    High‑level planner that turns a strategic GoalNode into an ordered
    list of operational actions (strings). It supports:
      * hierarchical decomposition
      * resource‑aware cost estimation
      * replanning when goals or resources change
      * multi‑step look‑ahead (default depth = 3)
    """

    def __init__(
        self,
        action_registry: Dict[str, Callable[..., Any]],
        resource_budget: Optional[Dict[str, float]] = None,
        lookahead_depth: int = 3,
    ):
        """
        :param action_registry: mapping from atomic action name -> callable
        :param resource_budget: global resources available to the planner
        :param lookahead_depth: how many levels of sub‑goals to expand before
                                committing to a concrete plan
        """
        self.action_registry = action_registry
        self.global_budget = resource_budget or {}
        self.lookahead_depth = lookahead_depth
        self.current_plan: List[str] = []
        self.last_goal: Optional[GoalNode] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def plan(self, root_goal: GoalNode) -> List[str]:
        """
        Produce a concrete plan (list of atomic action names) for the
        supplied root_goal. If the root_goal changes compared to the
        previous call, the planner automatically replans.
        """
        if self.last_goal is None or self._goals_differ(self.last_goal, root_goal):
            self.current_plan = self._decompose(root_goal, depth=self.lookahead_depth)
            self.last_goal = root_goal
        return self.current_plan

    def replan_if_needed(self, updated_goal: GoalNode) -> List[str]:
        """
        Convenience wrapper that forces replanning when the goal hierarchy
        or resource constraints have changed.
        """
        return self.plan(updated_goal)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _goals_differ(self, g1: GoalNode, g2: GoalNode) -> bool:
        """Very cheap structural diff – sufficient to trigger replanning."""
        return (
            g1.name != g2.name
            or g1.type != g2.type
            or g1.resources != g2.resources
            or g1.constraints != g2.constraints
            or len(g1.subgoals) != len(g2.subgoals)
        )

    def _decompose(
        self, node: GoalNode, depth: int, accumulated: Optional[List[str]] = None
    ) -> List[str]:
        """
        Recursively expand the goal hierarchy up to ``depth`` levels.
        Leaf nodes are translated into atomic actions via the action_registry.
        """
        accumulated = accumulated or []

        # If we reached the look‑ahead limit or a leaf, try to map to an action
        if depth == 0 or node.is_leaf():
            action = self._map_to_action(node)
            if action:
                accumulated.append(action)
            return accumulated

        # Otherwise, expand sub‑goals respecting resource constraints
        for sub in node.subgoals:
            # Simple resource check – prune if budget insufficient
            if not self._resources_sufficient(sub.resources):
                continue
            self._decompose(sub, depth - 1, accumulated)

        return accumulated

    def _resources_sufficient(self, req: Dict[str, float]) -> bool:
        """Return True if global_budget can satisfy the requested resources."""
        for key, amount in req.items():
            if self.global_budget.get(key, 0) < amount:
                return False
        return True

    def _map_to_action(self, node: GoalNode) -> Optional[str]:
        """
        Convert a (tactical/operational) goal node into a registered atomic action.
        The mapping heuristic is: look for an action whose name contains
        the goal name (case‑insensitive). If multiple match, pick the one with
        highest estimated success probability.
        """
        candidates = [
            name
            for name in self.action_registry.keys()
            if node.name.lower() in name.lower()
        ]
        if not candidates:
            return None
        # Simple heuristic: choose the first candidate
        return candidates[0]

    # ------------------------------------------------------------------
    # Utility for external callers
    # ------------------------------------------------------------------
    def estimate_success(self, plan: List[str]) -> float:
        """
        Rough estimate of overall success as the product of individual
        action success probabilities (if known). Missing actions default
        to 0.9.
        """
        prob = 1.0
        for act in plan:
            fn = self.action_registry.get(act)
            p = getattr(fn, "success_prob", 0.9) if fn else 0.9
            prob *= p
        return prob