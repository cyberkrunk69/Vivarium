class NarrativeIdentityTracker:
    """
    Tracks the evolution of a persona's core traits over time.
    Stores a chronological history of trait dictionaries with timestamps.
    """
    def __init__(self):
        self.history = []  # List of records

    def record(self, change_record: dict):
        """
        Append a new change record to the history.
        The record should contain at least a timestamp and the new traits.
        """
        self.history.append(change_record)

    def get_history(self):
        """Return the full history of trait changes."""
        return self.history