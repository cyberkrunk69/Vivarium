import threading

class BudgetExceededError(RuntimeError):
    """Raised when an operation would exceed the allowed budget."""
    pass

class BudgetTracker:
    """
    Thread‑safe singleton that tracks remaining monetary budget.
    The default budget is $2.00 as required by the project constraints.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, initial_budget: float = 2.0):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._budget = initial_budget
                cls._instance._budget_lock = threading.Lock()
            return cls._instance

    @property
    def remaining(self) -> float:
        """Current remaining budget."""
        with self._budget_lock:
            return self._budget

    def deduct(self, amount: float):
        """
        Deduct `amount` from the budget.
        Raises BudgetExceededError if insufficient funds.
        """
        if amount < 0:
            raise ValueError("Deduction amount must be non‑negative")
        with self._budget_lock:
            if self._budget - amount < -1e-9:  # allow tiny floating‑point tolerance
                raise BudgetExceededError(
                    f"Budget of ${self._budget:.2f} insufficient for deduction of ${amount:.2f}"
                )
            self._budget -= amount

    def reset(self, amount: float = 2.0):
        """Reset the budget to a new amount (useful for tests)."""
        with self._budget_lock:
            self._budget = amount