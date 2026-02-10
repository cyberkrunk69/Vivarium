"""
Facet-based subscription definitions for the message pool.

Facets are optional focus modes, not identities. These mappings are hints for
which focus modes might want to receive which message types. Nothing here is
mandatory or coercive.
"""

FACET_SUBSCRIPTIONS = {
    "strategy": ["TASK_ASSIGNMENT", "EXECUTION_PLAN", "REVIEW_FEEDBACK"],
    "build": ["TASK_ASSIGNMENT", "CODE_ARTIFACT", "TEST_RESULT"],
    "review": ["CODE_ARTIFACT", "TEST_RESULT", "REVIEW_FEEDBACK"],
    "document": ["COMPLETION_REPORT", "LESSON_CAPTURE"],
}