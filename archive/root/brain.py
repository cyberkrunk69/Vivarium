class Brain:
    def __init__(self):
        self.thoughts = []

    def think(self, thought):
        if not isinstance(thought, str):
            raise TypeError("Thought must be a string")
        self.thoughts.append(thought)

    def recall(self):
        if not self.thoughts:
            raise ValueError("No thoughts to recall")
        return self.thoughts