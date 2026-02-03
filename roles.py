"""
CAMEL Role-Based Task Decomposition (arXiv:2303.17760)

Implements role-playing for autonomous cooperation through inception prompting.
Each role has specific responsibilities, allowed tools, and handoff conditions.

Structured outputs prevent hallucination cascading (MetaGPT, arXiv:2308.00352).
Each role now specifies an output_schema to ensure artifact consistency.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Type, Optional
from enum import Enum
from pydantic import BaseModel, ValidationError

# Import artifact schemas
try:
    from artifacts.schemas import (
        TaskAssignment,
        ExecutionPlan,
        CodeArtifact,
        ReviewFeedback,
        TaskCompletionRecord
    )
except ImportError:
    # Schemas not yet available - they will be imported when needed
    TaskAssignment = None
    ExecutionPlan = None
    CodeArtifact = None
    ReviewFeedback = None
    TaskCompletionRecord = None


class RoleType(Enum):
    """Available roles in the CAMEL system."""
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"
    DOCUMENTER = "documenter"


@dataclass
class Role:
    """Represents a role with capabilities and responsibilities."""

    type: RoleType
    description: str
    system_prompt: str
    allowed_tools: List[str]
    handoff_conditions: Dict[str, Any]
    output_schema: Optional[Type[BaseModel]] = None

    def get_inception_prompt(self, subtask: str, next_role: str = None) -> str:
        """Generate inception prompt for role-playing."""
        prompt = f"You are the {self.type.value.upper()}. Your job is to {self.description}.\n\n"
        prompt += f"The PLANNER has assigned you: {subtask}\n\n"
        if next_role:
            prompt += f"When done, hand off to {next_role} with:\n"
            prompt += f"- Summary of what you completed\n"
            prompt += f"- Any blockers or issues encountered\n"
            prompt += f"- Ready-to-review artifacts\n"
        return prompt

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate role output against schema.

        Args:
            output: Raw output from role execution

        Returns:
            True if output validates, False otherwise

        Raises:
            ValidationError if schema validation fails
        """
        if self.output_schema is None:
            return True

        try:
            self.output_schema(**output)
            return True
        except ValidationError as e:
            raise ValidationError(f"Output validation failed for {self.type.value}: {e}")

    def get_output_schema_instructions(self) -> str:
        """Return instructions for output schema as string."""
        if self.output_schema is None:
            return ""

        schema = self.output_schema.model_json_schema()
        return f"\nExpected output format:\n{schema}"


# Role Definitions
ROLES = {
    RoleType.PLANNER: Role(
        type=RoleType.PLANNER,
        description="break complex tasks into atomic subtasks and assign to specialists",
        system_prompt="""You are the PLANNER role in a cooperative multi-agent system.
Your responsibility is to:
1. Analyze incoming tasks for complexity
2. Break complex tasks into subtasks (3-5 items max)
3. Assign each subtask to the appropriate specialist (CODER, REVIEWER, DOCUMENTER)
4. Provide clear handoff instructions with acceptance criteria

When a task is simple (can be done in <30 min), pass directly to CODER.
When complex, decompose and create a task plan JSON.

Output format:
{
  "complexity": "simple|complex",
  "subtasks": [
    {"id": 1, "assigned_to": "CODER", "description": "...", "acceptance_criteria": "..."},
    ...
  ],
  "next_role": "CODER"
}""",
        allowed_tools=["task_analysis", "decomposition", "json_output"],
        handoff_conditions={
            "simple_task": {"destination": "CODER", "criteria": "task_complexity < 2"},
            "complex_task": {"destination": "queue", "criteria": "task_complexity >= 2"}
        },
        output_schema=ExecutionPlan if ExecutionPlan else None
    ),

    RoleType.CODER: Role(
        type=RoleType.CODER,
        description="implement code changes according to specifications",
        system_prompt="""You are the CODER role in a cooperative multi-agent system.
Your responsibility is to:
1. Understand the subtask requirements from PLANNER
2. Write clean, focused code (no over-engineering)
3. Test locally if possible
4. Document what you changed with references

Rules:
- Follow existing code patterns in the repository
- Edit existing files, don't create new ones unless required
- Keep changes minimal and focused on the task
- Include file:line references for changes

When complete, hand off to REVIEWER with:
- Files modified
- Changes summary
- Test status (if applicable)""",
        allowed_tools=["file_read", "file_edit", "file_write", "bash_execute", "test_run"],
        handoff_conditions={
            "ready_for_review": {"destination": "REVIEWER", "criteria": "code_complete and tested"},
            "blocker": {"destination": "PLANNER", "criteria": "cannot proceed without clarification"}
        },
        output_schema=CodeArtifact if CodeArtifact else None
    ),

    RoleType.REVIEWER: Role(
        type=RoleType.REVIEWER,
        description="validate code against requirements and quality standards",
        system_prompt="""You are the REVIEWER role in a cooperative multi-agent system.
Your responsibility is to:
1. Validate code changes match the original requirements
2. Check for security issues, obvious bugs, style violations
3. Verify tests pass (if applicable)
4. Accept or reject with specific feedback

When rejecting, pass back to CODER with:
- Specific issues found
- Lines/files affected
- Requested changes

When accepting, hand off to DOCUMENTER with:
- Validation summary
- Files approved
- Test results""",
        allowed_tools=["code_review", "test_validate", "quality_check"],
        handoff_conditions={
            "approved": {"destination": "DOCUMENTER", "criteria": "all_checks_pass"},
            "needs_changes": {"destination": "CODER", "criteria": "issues_found"}
        },
        output_schema=ReviewFeedback if ReviewFeedback else None
    ),

    RoleType.DOCUMENTER: Role(
        type=RoleType.DOCUMENTER,
        description="update project documentation and record lessons learned",
        system_prompt="""You are the DOCUMENTER role in a cooperative multi-agent system.
Your responsibility is to:
1. Update learned_lessons.json with insights from this task
2. Record patterns discovered
3. Note any architectural decisions
4. Log what went well and what could improve

Append to learned_lessons.json:
{
  "task_id": "...",
  "role_patterns": [
    {"role": "PLANNER", "pattern": "...", "insight": "..."},
    {"role": "CODER", "pattern": "...", "insight": "..."},
    {"role": "REVIEWER", "pattern": "...", "insight": "..."}
  ],
  "completed": true
}""",
        allowed_tools=["json_read", "json_write", "documentation_update"],
        handoff_conditions={
            "task_complete": {"destination": "queue", "criteria": "documentation_recorded"}
        },
        output_schema=TaskCompletionRecord if TaskCompletionRecord else None
    )
}


def get_role(role_type: RoleType) -> Role:
    """Get a role by type."""
    return ROLES.get(role_type)


def decompose_task(task: str) -> Dict[str, Any]:
    """
    Analyze task complexity with adaptive signals and return decomposition plan with float score.

    Signals analyzed:
    - Word count of task description
    - Presence of high-complexity keywords ('create', 'implement', 'design')
    - Presence of low-complexity keywords ('fix', 'update', 'add')
    - Number of files mentioned
    - References to papers or architectures

    Returns complexity_score as float 0.0-1.0 for fine-grained adaptation.
    """
    task_lower = task.lower()
    words = task.split()
    word_count = len(words)

    # Base score from word count (longer tasks tend to be more complex)
    # Normalize: 0-50 words = 0.1, 50+ words = 0.3
    word_count_score = min(word_count / 50.0 * 0.3, 0.3)

    # High-complexity keywords (indicate significant implementation)
    high_complexity_keywords = ["create", "implement", "design", "architecture", "build", "refactor"]
    high_complexity_score = len([kw for kw in high_complexity_keywords if kw in task_lower]) * 0.15

    # Low-complexity keywords (indicate minor fixes)
    low_complexity_keywords = ["fix", "update", "add", "change", "modify"]
    low_complexity_penalty = len([kw for kw in low_complexity_keywords if kw in task_lower]) * 0.08

    # Multi-word complexity phrases
    complexity_phrases = ["multiple", "several", "various", "integrate", "coordinate", "complex"]
    phrase_score = len([phrase for phrase in complexity_phrases if phrase in task_lower]) * 0.12

    # File references (count file paths, extensions, or mentions like "file X", "files")
    file_indicators = task_lower.count("file") + task_lower.count(".py") + task_lower.count(".js") + \
                      task_lower.count(".ts") + task_lower.count(".jsx") + task_lower.count(".tsx")
    file_score = min(file_indicators * 0.05, 0.2)

    # Paper/architecture references (indicates research or significant design)
    paper_keywords = ["arxiv", "paper", "algorithm", "framework", "architecture", "pattern", "design pattern"]
    paper_score = len([kw for kw in paper_keywords if kw in task_lower]) * 0.1

    # Calculate final complexity score
    complexity_score = min(
        word_count_score + high_complexity_score - low_complexity_penalty + phrase_score + file_score + paper_score,
        1.0
    )
    # Floor at 0.0
    complexity_score = max(complexity_score, 0.0)

    # Determine simple vs complex using threshold
    # Use 0.35 as threshold for classification
    is_complex = complexity_score >= 0.35

    return {
        "complexity": "complex" if is_complex else "simple",
        "assigned_to": "PLANNER" if is_complex else "CODER",
        "complexity_score": round(complexity_score, 3),  # 3 decimal places
        "analysis": {
            "word_count": word_count,
            "word_count_signal": round(word_count_score, 3),
            "high_complexity_signals": round(high_complexity_score, 3),
            "low_complexity_signals": round(low_complexity_penalty, 3),
            "phrase_signals": round(phrase_score, 3),
            "file_reference_signals": round(file_score, 3),
            "paper_reference_signals": round(paper_score, 3)
        }
    }


def get_role_chain(complexity: str) -> List[RoleType]:
    """Return the role chain based on task complexity."""
    if complexity == "simple":
        return [RoleType.CODER, RoleType.REVIEWER, RoleType.DOCUMENTER]
    else:
        return [RoleType.PLANNER, RoleType.CODER, RoleType.REVIEWER, RoleType.DOCUMENTER]


def format_handoff(current_role: RoleType, next_role: RoleType, context: Dict[str, Any]) -> str:
    """Format a handoff message from one role to the next."""
    handoff = f"\n{'='*60}\n"
    handoff += f"HANDOFF: {current_role.value.upper()} -> {next_role.value.upper()}\n"
    handoff += f"{'='*60}\n"

    if "completion_summary" in context:
        handoff += f"COMPLETION SUMMARY:\n{context['completion_summary']}\n\n"

    if "artifacts" in context:
        handoff += f"ARTIFACTS READY FOR REVIEW:\n"
        for artifact in context["artifacts"]:
            handoff += f"  - {artifact}\n"
        handoff += "\n"

    if "blockers" in context and context["blockers"]:
        handoff += f"BLOCKERS/ISSUES:\n"
        for blocker in context["blockers"]:
            handoff += f"  - {blocker}\n"
        handoff += "\n"

    handoff += f"Next role: {next_role.value.upper()}\n"
    handoff += f"{'='*60}\n"

    return handoff


class RoleExecutor:
    """Manages role-based task execution with handoff logic."""

    def __init__(self, initial_role: RoleType, task: str):
        self.current_role = initial_role
        self.task = task
        self.execution_log = []
        self.context = {"task": task}

    def should_pass_to_reviewer(self) -> bool:
        """Check if current execution should pass through REVIEWER role."""
        return self.current_role in [RoleType.CODER, RoleType.PLANNER]

    def get_current_role_prompt(self) -> str:
        """Get system prompt for current role with inception prompting."""
        role = get_role(self.current_role)
        subtask = self.context.get("assigned_subtask", self.task)
        next_role = self.get_next_role_in_chain()
        return role.get_inception_prompt(subtask, next_role.value.upper() if next_role else None)

    def get_next_role_in_chain(self) -> RoleType:
        """Determine next role in execution chain."""
        role_chain = get_role_chain(self.context.get("complexity", "simple"))
        try:
            current_index = role_chain.index(self.current_role)
            if current_index < len(role_chain) - 1:
                return role_chain[current_index + 1]
        except (ValueError, IndexError):
            pass
        return None

    def execute_role(self) -> Dict[str, Any]:
        """Execute current role and return results."""
        role = get_role(self.current_role)
        return {
            "role": self.current_role.value,
            "system_prompt": role.system_prompt,
            "allowed_tools": role.allowed_tools,
            "inception_prompt": self.get_current_role_prompt()
        }

    def transition_to_next_role(self) -> bool:
        """Move to next role in chain. Returns False if no next role."""
        next_role = self.get_next_role_in_chain()
        if next_role:
            self.execution_log.append({
                "from_role": self.current_role.value,
                "to_role": next_role.value,
                "context": self.context.copy()
            })
            self.current_role = next_role
            return True
        return False


# MetaGPT-style Role Subscriptions (arXiv:2308.00352)
# Defines which message types each role subscribes to for structured communication
ROLE_SUBSCRIPTIONS = {
    "Orchestrator": ["TASK_REQUEST", "COMPLETION_REPORT"],
    "Planner": ["TASK_ASSIGNMENT", "REVIEW_FEEDBACK"],
    "Coder": ["EXECUTION_PLAN", "TEST_RESULT", "REVIEW_FEEDBACK"],
    "Tester": ["CODE_ARTIFACT"],
    "Reviewer": ["CODE_ARTIFACT", "TEST_RESULT"],
    "Documenter": ["COMPLETION_REPORT"],
}

# Available message types for publish-subscribe communication
MESSAGE_TYPES = {
    "TASK_ASSIGNMENT": "Orchestrator → Planner/Coder: Initial task distribution",
    "DESIGN_SPEC": "Architect → Planner/Coder/Reviewer: System design and API specs",
    "EXECUTION_PLAN": "Planner → Coder: Detailed task decomposition",
    "CODE_ARTIFACT": "Coder → Tester/Reviewer: Implementation outputs",
    "TEST_RESULT": "Tester → Coder/Reviewer: Test execution results",
    "REVIEW_FEEDBACK": "Reviewer → Coder/Integrator: Code review comments",
    "REFLECTION": "Any → All (on failure): Learning and improvement insights",
}
