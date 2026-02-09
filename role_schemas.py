# This module assigns output schemas to role classes to enforce structured outputs.
# It should be imported early in the application initialization.

from artifacts.schemas import TaskAssignment, ExecutionPlan, CodeArtifact, ReviewFeedback
import roles  # Assuming roles module defines the role classes

# Mapping of role class names to their respective output schemas
_role_output_schema_map = {
    "TaskAssigner": TaskAssignment,
    "Planner": ExecutionPlan,
    "Coder": CodeArtifact,
    "Reviewer": ReviewFeedback,
}

# Dynamically set the output_schema attribute on each role class if it exists
for _role_name, _schema in _role_output_schema_map.items():
    _role_cls = getattr(roles, _role_name, None)
    if _role_cls is not None:
        setattr(_role_cls, "output_schema", _schema)