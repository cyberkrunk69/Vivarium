class QualityGateSubject:
    """Subject in the Observer pattern that notifies registered observers
    about a diff before it is merged."""
    def __init__(self):
        self._observers = []

    def register(self, observer):
        """Register an observer that implements an ``update(diff)`` method."""
        self._observers.append(observer)

    def notify(self, diff):
        """Notify all observers. If any observer returns ``False`` the
        notification short‑circuits and the diff is considered rejected."""
        for observer in self._observers:
            try:
                result = observer.update(diff)
                if not result:
                    return False
            except Exception as exc:
                # An unexpected error in an observer should also reject the diff
                print(f"[QualityGate] Observer {observer} raised an exception: {exc}")
                return False
        return True


class QualityGateObserver:
    """Concrete observer that performs the secondary validation."""
    def update(self, diff):
        """
        Perform a secondary check on the supplied ``diff``.
        Return ``True`` if the diff passes all quality checks,
        otherwise return ``False`` to reject the change.
        """
        # -----------------------------------------------------------------
        # INSERT YOUR REAL VALIDATION LOGIC HERE.
        # For the purpose of this scaffold we simply approve every diff.
        # -----------------------------------------------------------------
        return True


# Create a module‑level singleton subject and register the default observer.
quality_gate_subject = QualityGateSubject()
quality_gate_subject.register(QualityGateObserver())