<!-- FACT_CHECKSUM: 94098d66ea9df0466a683fffa46f0ecc365bccac71215f4942f48c51759b40f1 -->

# ELIV
This module provides work coordination, resource limits, activity logging.

## Constants

### Configuration Constants

* `BRIEF_COST_PER_FILE`: 0.005
  * Used at lines: 723
* `COST_PER_MILLION_70B`: 0.9
  * Used at lines: (none)
* `COST_PER_MILLION_8B`: 0.2
  * Used at lines: 157
* `DRAFT_COST_PER_FILE`: 0.0004
  * Used at lines: 270, 281
* `TASK_NAV_ESTIMATED_COST`: 0.002
  * Used at lines: 342
* `TOKENS_PER_SMALL_FILE`: 500
  * Used at lines: 144, 149
* `logger`: logging.getLogger(__name__)
  * Used at lines: 322, 774, 785, 820, 846, 848

### Implementation Constants

* `BudgetExhaustedError`: Raised when hourly budget is exhausted before an LLM operation.
* `NavResult`: Result of scout-nav LLM call.
* `SymbolDoc`: Generated symbol documentation.
* `TriggerRouter`: Orchestrates triggers, respects limits, prevents infinite loops, and cascades doc updates safely.

## Methods

### Functions

* `_notify_user`: Notify user (stub — override for testing or real UI).
* `check_budget_with_message`: Check if operation can proceed within hourly budget.
* `on_git_commit`: Proactive echo: invalidate dependency graph for changed files.

### Class Methods

* `TriggerRouter`:
  * `__init__`: Initializes the TriggerRouter instance.
  * `should_trigger`: Checks if a trigger should be executed.
  * `_quick_token_estimate`: Estimates the number of tokens in a file.
  * `estimate_cascade_cost`: Estimates the cost of a cascade operation.
  * `on_file_save`: Handles file save events.
  * `on_git_commit`: Handles git commit events.
  * `prepare_commit_msg`: Prepares a commit message.
  * `estimate_task_nav_cost`: Estimates the cost of a task navigation operation.
  * `_list_python_files`: Lists Python files in a repository.
  * `_parse_nav_json`: Parses navigation JSON data.
  * `navigate_task`: Navigates a task.
  * `on_manual_trigger`: Handles manual trigger events.
  * `_quick_parse`: Performs a quick parse operation.
  * `_scout_nav`: Performs a scout navigation operation.
  * `_affects_module_boundary`: Checks if a file affects a module boundary.
  * `_is_public_api`: Checks if a file is part of the public API.
  * `_detect_module`: Detects a module.
  * `_critical_path_files`: Lists critical path files.
  * `_generate_symbol_doc`: Generates symbol documentation.
  * `_write_draft`: Writes a draft.
  * `_update_module_brief`: Updates a module brief.
  * `_create_human_ticket`: Creates a human ticket.
  * `_create_pr_draft`: Creates a PR draft.
  * `_load_symbol_docs`: Loads symbol documentation.
  * `_generate_commit_draft`: Generates a commit draft.
  * `_generate_pr_snippet`: Generates a PR snippet.
  * `_generate_impact_summary`: Generates an impact summary.
  * `_process_file`: Processes a file.

## Control Flow

* `check_budget_with_message`: Checks if an operation can proceed within the hourly budget.
* `on_git_commit`: Handles git commit events and invalidates the dependency graph for changed files.