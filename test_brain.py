from brain import Brain

def test_brain():
    brain = Brain()
    brain.think("Hello world")
    print(brain.recall())  # Should print: ["Hello world"]

    try:
        brain.think(123)
    except TypeError as e:
        print(e)  # Should print: Thought must be a string

    try:
        brain = Brain()
        brain.recall()
    except ValueError as e:
        print(e)  # Should print: No thoughts to recall

test_brain()