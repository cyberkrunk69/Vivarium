"""
Structured artifact schemas for CAMEL multi-agent system.

Provides typed outputs for each role to prevent hallucination cascading
and ensure consistency in artifact generation across the role chain.

Reference: MetaGPT (arXiv:2308.00352) - "Structured outputs prevent cascading hallucinations"
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class RoleEnum(str, Enum):
    """Available roles in the CAMEL system."""
    PLANNER = "PLANNER"
    CODER = "CODER"
    REVIEWER = "REVIEWER"
    DOCUMENTER = "DOCUMENTER"


class Step(BaseModel):
    """Single execution step in a plan."""
    step_number: int = Field(..., description="Sequential step number")
    description: str = Field(..., description="What needs to be done in this step")
    expected_output: str = Field(..., description="Expected result/artifact from this step")


class TaskAssignment(BaseModel):
    """Assignment of a task to a specific role."""
    task_id: str = Field(..., description="Unique identifier for this task")
    description: str = Field(..., description="Clear description of what needs to be done")
    assigned_to: RoleEnum = Field(..., description="Which role is assigned this task")
    acceptance_criteria: List[str] = Field(
        ...,
        description="List of criteria that must be met for task completion"
    )
    complexity: Optional[str] = Field(
        None,
        description="Task complexity level: simple or complex"
    )


class ExecutionPlan(BaseModel):
    """Complete execution plan for a task."""
    task_id: str = Field(..., description="Unique identifier for this task")
    complexity: str = Field(..., description="Complexity level: simple or complex")
    steps: List[Step] = Field(..., description="Ordered list of execution steps")
    estimated_complexity: int = Field(
        ...,
        description="Numeric complexity score (1-10) for resource estimation"
    )
    role_chain: List[RoleEnum] = Field(
        ...,
        description="Sequence of roles that will handle this task"
    )


class CodeArtifact(BaseModel):
    """Output artifact from CODER role."""
    task_id: str = Field(..., description="Unique identifier for this task")
    files_modified: List[str] = Field(
        ...,
        description="List of file paths that were modified"
    )
    changes_summary: str = Field(
        ...,
        description="Summary of changes made and why"
    )
    tests_status: str = Field(
        ...,
        description="Status of tests: passed, failed, or not_applicable"
    )
    blockers: List[str] = Field(
        default_factory=list,
        description="Any blockers encountered during implementation"
    )


class ReviewIssue(BaseModel):
    """Single issue found during code review."""
    severity: str = Field(..., description="Severity level: critical, warning, or info")
    file_path: str = Field(..., description="File where issue was found")
    line_number: Optional[int] = Field(None, description="Line number if applicable")
    description: str = Field(..., description="Description of the issue")
    suggested_fix: Optional[str] = Field(None, description="Suggested fix if available")


class ReviewFeedback(BaseModel):
    """Output artifact from REVIEWER role."""
    task_id: str = Field(..., description="Unique identifier for this task")
    approved: bool = Field(..., description="Whether changes are approved for merge")
    issues: List[ReviewIssue] = Field(
        default_factory=list,
        description="List of issues found during review"
    )
    test_results: str = Field(
        ...,
        description="Status of test execution: passed, failed, or not_applicable"
    )
    review_summary: str = Field(
        ...,
        description="Summary of review findings"
    )
    next_action: str = Field(
        ...,
        description="What should happen next: proceed_to_documenter, return_to_coder, or escalate"
    )


class LessonRecord(BaseModel):
    """Record of lessons learned from task execution."""
    task_id: str = Field(..., description="Unique identifier for this task")
    role: RoleEnum = Field(..., description="Which role generated this lesson")
    pattern: str = Field(..., description="Pattern or observation discovered")
    insight: str = Field(..., description="Key insight or takeaway from this pattern")


class TaskCompletionRecord(BaseModel):
    """Final documentation record for a completed task."""
    task_id: str = Field(..., description="Unique identifier for this task")
    role_patterns: List[LessonRecord] = Field(
        ...,
        description="Patterns and insights from each role in the chain"
    )
    completed: bool = Field(..., description="Whether task is fully completed")
    timestamp: Optional[str] = Field(None, description="When task was completed (ISO format)")
