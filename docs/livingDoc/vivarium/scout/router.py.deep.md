<!-- FACT_CHECKSUM: 94098d66ea9df0466a683fffa46f0ecc365bccac71215f4942f48c51759b40f1 -->

# ELIV
This module provides work coordination, resource limits, activity logging.

## Constants

### Configuration Constants

* `BRIEF_COST_PER_FILE`: 0.005, used at lines 723
* `COST_PER_MILLION_70B`: 0.9, used at no lines
* `COST_PER_MILLION_8B`: 0.2, used at line 157
* `DRAFT_COST_PER_FILE`: 0.0004, used at lines 270, 281
* `TASK_NAV_ESTIMATED_COST`: 0.002, used at line 342
* `TOKENS_PER_SMALL_FILE`: 500, used at lines 144, 149
* `logger`: logging.getLogger(__name__), used at lines 322, 774, 785, 820, 846, 848

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
  - `__init__`: 
  - `should_trigger`: 
  - `_quick_token_estimate`: 
  - `estimate_cascade_cost`: 
  - `on_file_save`: 
  - `on_git_commit`: 
  - `prepare_commit_msg`: 
  - `estimate_task_nav_cost`: 
  - `_list_python_files`: 
  - `_parse_nav_json`: 
  - `navigate_task`: 
  - `on_manual_trigger`: 
  - `_quick_parse`: 
  - `_scout_nav`: 
  - `_affects_module_boundary`: 
  - `_is_public_api`: 
  - `_detect_module`: 
  - `_critical_path_files`: 
  - `_generate_symbol_doc`: 
  - `_write_draft`: 
  - `_update_module_brief`: 
  - `_create_human_ticket`: 
  - `_create_pr_draft`: 
  - `_load_symbol_docs`: 
  - `_generate_commit_draft`: 
  - `_generate_pr_snippet`: 
  - `_generate_impact_summary`: 
  - `_process_file`: 

## Control Flow

* `check_budget_with_message`: Check if operation can proceed within hourly budget.
  - Returns True if OK, False if blocked (and prints actionable error to stderr).