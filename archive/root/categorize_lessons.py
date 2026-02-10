import os
from lesson import Lesson  # Added missing import statement

def categorize(lesson):
    # Categorize the lessons
    return [lesson.category for lesson in lessons]
# Export the primary public function for `from categorize_lessons import *`
__all__ = ["categorize"]