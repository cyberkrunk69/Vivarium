# Role‑to‑subscription mapping for the MetaGPT communication protocol.
# This file is separate from the protected `roles.py` to avoid modifying protected code.
# Each role lists the message types it is interested in receiving.

ROLE_SUBSCRIPTIONS = {
    "Planner": ["TASK_ASSIGNMENT", "EXECUTION_PLAN", "REVIEW_FEEDBACK"],
    "Coder": ["TASK_ASSIGNMENT", "EXECUTION_PLAN", "CODE_ARTIFACT"],
    "Tester": ["CODE_ARTIFACT", "TEST_RESULT"],
    "Reviewer": ["CODE_ARTIFACT", "TEST_RESULT", "REVIEW_FEEDBACK"],
}
# Subscription mapping for roles in the MetaGPT communication protocol
# Each role lists the roles that should receive its published messages.
ROLE_SUBSCRIPTIONS = {
    "Planner": ["Coder", "Reviewer"],
    "Coder": ["Reviewer"],
    "Reviewer": ["Planner"],
}
# Role subscription mapping for the MetaGPT communication protocol.
# Keys are role names; values are lists of roles that should receive messages
# from the key role.
ROLE_SUBSCRIPTIONS = {
    "Planner": ["Coder"],
    "Coder": ["Tester"],
    "Tester": ["Reviewer"],
    "Reviewer": [],
}
# Role‑to‑subscription mapping for the MetaGPT communication protocol.
# This file is imported by agents that need to know which messages they should listen to.
ROLE_SUBSCRIPTIONS = {
    # Planner creates execution plans for Coder and Tester
    "Planner": ["Coder", "Tester", "Reviewer"],
    # Coder receives execution plans and task assignments, and publishes code artifacts
    "Coder": ["Planner", "Reviewer"],
    # Tester receives code artifacts and publishes test results
    "Tester": ["Coder", "Reviewer"],
    # Reviewer receives test results and execution plans, and publishes review feedback
    "Reviewer": ["Planner", "Coder", "Tester"],
}
"""
Role‑based subscription definitions for the MetaGPT message pool.

Each key is a role name, and the associated list contains the roles whose
messages this role is interested in.  The MessagePool does not enforce the
relationship; it merely provides the ``subscribers`` field when publishing.
Workers can consult this mapping to decide which messages to subscribe to.
"""

ROLE_SUBSCRIPTIONS = {
    # Example mappings – adjust according to your project's workflow
    "Planner": ["Coder", "Tester", "Reviewer"],
    "Coder": ["Planner", "Reviewer"],
    "Tester": ["Coder", "Reviewer"],
    "Reviewer": ["Planner", "Coder", "Tester"],
}