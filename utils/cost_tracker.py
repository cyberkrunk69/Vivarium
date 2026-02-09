import threading

class BudgetExceededError(RuntimeError):
    """Raised when a requested operation would exceed the allocated budget."""
    pass

class CostTracker:
    """
    Thread‑safe singleton that records USD spend for LLM API calls
    and enforces a configurable budget.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # Ensure singleton semantics
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(CostTracker, cls).__new__(cls)
        return cls._instance

    def __init__(self, budget_usd: float = 2.0):
        # `__init__` may be called multiple times; guard against re‑initialisation
        if not hasattr(self, "_initialized"):
            self.budget_usd = budget_usd
            self.spent_usd = 0.0
            self._initialized = True

    def add_cost(self, amount_usd: float):
        """Add cost and raise if budget would be exceeded."""
        if amount_usd < 0:
            raise ValueError("Cost amount must be non‑negative")
        if self.spent_usd + amount_usd > self.budget_usd:
            raise BudgetExceededError(
                f"Attempted to spend ${self.spent_usd + amount_usd:.2f} "
                f"which exceeds the budget of ${self.budget_usd:.2f}"
            )
        self.spent_usd += amount_usd
        print(f"[COST] Spent: ${self.spent_usd:.4f} / Budget: ${self.budget_usd:.2f}")

    def get_remaining_budget(self) -> float:
        """Return how much budget is left."""
        return max(self.budget_usd - self.spent_usd, 0.0)

    def reset(self, new_budget: float = None):
        """Reset spent amount; optionally set a new budget."""
        self.spent_usd = 0.0
        if new_budget is not None:
            self.budget_usd = new_budget

# Export a module‑level singleton for easy import
cost_tracker = CostTracker()