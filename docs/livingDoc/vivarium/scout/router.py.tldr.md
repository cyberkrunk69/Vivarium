<!-- FACT_CHECKSUM: 94098d66ea9df0466a683fffa46f0ecc365bccac71215f4942f48c51759b40f1 -->

# ELIV
This module provides work coordination, resource limits, activity logging.

## Module Constants
- `BRIEF_COST_PER_FILE`: 0.005 (used at line 723)
- `COST_PER_MILLION_70B`: 0.9 (used at lines none)
- `COST_PER_MILLION_8B`: 0.2 (used at line 157)
- `DRAFT_COST_PER_FILE`: 0.0004 (used at lines 270, 281)
- `logger`: (used at lines 322, 774, 785, 820, 846, 848)
- `TASK_NAV_ESTIMATED_COST`: 0.002 (used at line 342)
- `TOKENS_PER_SMALL_FILE`: 500 (used at lines 144, 149)

# BudgetExhaustedError
Raised when hourly budget is exhausted before an LLM operation.

## Constants
- None

## Methods
- None

# NavResult
Result of scout-nav LLM call.

## Constants
- None

## Methods
- None

# SymbolDoc
Generated symbol documentation.

## Constants
- None

## Methods
- None

# TriggerRouter
Orchestrates triggers, respects limits, prevents infinite loops, and cascades doc updates safely.

## Constants
- None

## Methods
- `__init__(self, config: ScoutConfig=None, audit: AuditLog=None, validator: Validator=None, repo_root: Path=None, notify: Callable[[str], None]=None)`: 
- `should_trigger(self)`: 
- `_quick_token_estimate(self)`: 
- `estimate_cascade_cost(self)`: 
- `on_file_save(self)`: 
- `on_git_commit(self)`: 
- `prepare_commit_msg(self)`: 
- `estimate_task_nav_cost(self)`: 
- `_list_python_files(self)`: 
- `_parse_nav_json(self)`: 
- `navigate_task(self)`: 
- `on_manual_trigger(self)`: 
- `_quick_parse(self)`: 
- `_scout_nav(self)`: 
- `_affects_module_boundary(self)`: 
- `_is_public_api(self)`: 
- `_detect_module(self)`: 
- `_critical_path_files(self)`: 
- `_generate_symbol_doc(self)`: 
- `_write_draft(self)`: 
- `_update_module_brief(self)`: 
- `_create_human_ticket(self)`: 
- `_create_pr_draft(self)`: 
- `_load_symbol_docs(self)`: 
- `_generate_commit_draft(self)`: 
- `_generate_pr_snippet(self)`: 
- `_generate_impact_summary(self)`: 
- `_process_file(self)`: 

# _notify_user
Notify user (stub — override for testing or real UI).

## Constants
- None

## Methods
- `def _notify_user(message: str) -> None`: 

# check_budget_with_message
Check if operation can proceed within hourly budget.

    Returns True if OK, False if blocked (and prints actionable error to stderr).

## Constants
- None

## Methods
- `def check_budget_with_message(config: ScoutConfig, estimated_cost: float=0.01, audit: Optional[AuditLog]=None) -> bool`: