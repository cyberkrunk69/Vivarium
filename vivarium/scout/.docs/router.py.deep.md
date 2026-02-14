<!-- FACT_CHECKSUM: 64a879eac9f89bc01abbc0e4a63b337a3be508015ecbf237e55abe76eb1e19f4 -->

## Constants

### BRIEF_COST_PER_FILE
Value: 0.005
Used at lines: 723

### COST_PER_MILLION_70B
Value: 0.9
Used at lines: (none)

### COST_PER_MILLION_8B
Value: 0.2
Used at lines: 157

### DRAFT_COST_PER_FILE
Value: 0.0004
Used at lines: 270, 281

### TASK_NAV_ESTIMATED_COST
Value: 0.002
Used at lines: 342

### TOKENS_PER_SMALL_FILE
Value: 500
Used at lines: 144, 149

### logger
Value: logging.getLogger(__name__)
Used at lines: 322, 774, 785, 820, 846, 848

## Classes

### BudgetExhaustedError
Used at lines: 275

### NavResult
Used at lines: 656, 664, 672, 704, 734

### SymbolDoc
Used at lines: 704, 707, 709

### TriggerRouter
Used at lines: (none)
Methods:
- __init__
- should_trigger
- _quick_token_estimate
- estimate_cascade_cost
- on_file_save
- on_git_commit
- prepare_commit_msg
- estimate_task_nav_cost
- _list_python_files
- _parse_nav_json
- on_manual_trigger
- _quick_parse
- _scout_nav
- _affects_module_boundary
- _is_public_api
- _detect_module
- _critical_path_files
- _generate_symbol_doc
- _write_draft
- _update_module_brief
- _create_human_ticket
- _create_pr_draft
- _load_symbol_docs
- _process_file

## Functions

### _notify_user
Used at lines: 133

### check_budget_with_message
Used at lines: 272

### on_git_commit
Used at lines: (none)