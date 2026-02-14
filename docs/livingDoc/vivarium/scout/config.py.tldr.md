<!-- FACT_CHECKSUM: bd6e196bb66529e3f4a08d5235731b69c34f12dbe1219adb3b9fa547b341169d -->

# Module Summary

- `DEFAULT_CONFIG`: constant (used at lines 254, 341)
  Value: {'triggers': {'default': 'on-commit', 'patterns': [{'pattern': 'vivarium/runtime/**/*.py', 'trigger': 'on-save', 'max_cost': 0.02}, {'pattern': 'tests/**/*', 'trigger': 'manual'}, {'pattern': 'docs/**/*.md', 'trigger': 'disabled'}]}, 'limits': {'max_cost_per_event': 0.05, 'hourly_budget': 1.0, 'hard_safety_cap': 10.0}, 'models': {'scout_nav': 'llama-3.1-8b', 'max_for_auto': 'llama-3.1-8b', 'tldr': 'llama-3.1-8b-instant', 'deep': 'llama-3.3-70b-versatile', 'eliv': 'llama-3.1-8b-instant', 'pr_synthesis': 'llama-3.3-70b-versatile'}, 'notifications': {'on_validation_failure': 'alert'}, 'drafts': {'enable_commit_drafts': True, 'enable_pr_snippets': True, 'enable_impact_analysis': False, 'enable_module_briefs': True}, 'roast': {'enable_roast': True}, 'doc_generation': {'generate_eliv': True}, 'ui': {'whimsy': False}}
- `ENV_TO_CONFIG`: constant (used at lines 275)
  Value: {'SCOUT_MAX_COST_PER_EVENT': ('limits', 'max_cost_per_event', float), 'SCOUT_HOURLY_BUDGET': ('limits', 'hourly_budget', float), 'SCOUT_DEFAULT_TRIGGER': ('triggers', 'default', str), 'SCOUT_ON_VALIDATION_FAILURE': ('notifications', 'on_validation_failure', str)}
- `EnvLoader`: class with methods load
- `HARD_MAX_AUTO_ESCALATIONS`: constant (used at lines 379)
  Value: 3
- `HARD_MAX_COST_PER_EVENT`: constant (used at lines 313, 334, 339, 342, 358, 377)
  Value: 1.0
- `HARD_MAX_HOURLY_BUDGET`: constant (used at lines 295, 363, 378)
  Value: 10.0
- `ScoutConfig`: class with methods __init__, _default_search_paths, _apply_env_overrides, _ensure_hard_cap_in_limits, resolve_trigger, effective_max_cost, should_process, to_dict, get_user_config_path, get_project_config_path, whimsy_mode, get, set, validate_yaml
- `TriggerConfig`: class with methods 
- `_semaphore`: constant (used at lines 166, 168)
  Value: None
- `logger`: constant (used at lines 202, 216, 290)
  Value: logging.getLogger(__name__)