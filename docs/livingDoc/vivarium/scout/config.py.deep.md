<!-- FACT_CHECKSUM: bd6e196bb66529e3f4a08d5235731b69c34f12dbe1219adb3b9fa547b341169d -->

## Constants

### DEFAULT_CONFIG
Value: {'triggers': {'default': 'on-commit', 'patterns': [{'pattern': 'vivarium/runtime/**/*.py', 'trigger': 'on-save', 'max_cost': 0.02}, {'pattern': 'tests/**/*', 'trigger': 'manual'}, {'pattern': 'docs/**/*.md', 'trigger': 'disabled'}]}, 'limits': {'max_cost_per_event': 0.05, 'hourly_budget': 1.0, 'hard_safety_cap': 10.0}, 'models': {'scout_nav': 'llama-3.1-8b', 'max_for_auto': 'llama-3.1-8b', 'tldr': 'llama-3.1-8b-instant', 'deep': 'llama-3.3-70b-versatile', 'eliv': 'llama-3.1-8b-instant', 'pr_synthesis': 'llama-3.3-70b-versatile'}, 'notifications': {'on_validation_failure': 'alert'}, 'drafts': {'enable_commit_drafts': True, 'enable_pr_snippets': True, 'enable_impact_analysis': False, 'enable_module_briefs': True}, 'roast': {'enable_roast': True}, 'doc_generation': {'generate_eliv': True}, 'ui': {'whimsy': False}}
Used at lines: 254, 341

### ENV_TO_CONFIG
Value: {'SCOUT_MAX_COST_PER_EVENT': ('limits', 'max_cost_per_event', float), 'SCOUT_HOURLY_BUDGET': ('limits', 'hourly_budget', float), 'SCOUT_DEFAULT_TRIGGER': ('triggers', 'default', str), 'SCOUT_ON_VALIDATION_FAILURE': ('notifications', 'on_validation_failure', str)}
Used at lines: 275

### HARD_MAX_AUTO_ESCALATIONS
Value: 3
Used at lines: 379

### HARD_MAX_COST_PER_EVENT
Value: 1.0
Used at lines: 313, 334, 339, 342, 358, 377

### HARD_MAX_HOURLY_BUDGET
Value: 10.0
Used at lines: 295, 363, 378

### _SEMAPHORE
Value: None
Type: Optional[asyncio.Semaphore]
Used at lines: 166, 168

### logger
Value: logging.getLogger(__name__)
Used at lines: 202, 216, 290

## Methods

### EnvLoader.load
Used at lines: (none)

### ScoutConfig.__init__
Used at lines: (none)

### ScoutConfig._default_search_paths
Used at lines: (none)

### ScoutConfig._apply_env_overrides
Used at lines: (none)

### ScoutConfig._ensure_hard_cap_in_limits
Used at lines: (none)

### ScoutConfig.resolve_trigger
Used at lines: (none)

### ScoutConfig.effective_max_cost
Used at lines: (none)

### ScoutConfig.should_process
Used at lines: (none)

### ScoutConfig.to_dict
Used at lines: (none)

### ScoutConfig.get_user_config_path
Used at lines: (none)

### ScoutConfig.get_project_config_path
Used at lines: (none)

### ScoutConfig.whimsy_mode
Used at lines: (none)

### ScoutConfig.get
Used at lines: (none)

### ScoutConfig.set
Used at lines: (none)

### ScoutConfig.validate_yaml
Used at lines: (none)

### TriggerConfig
Used at lines: 298, 316, 321

### _deep_merge
Used at lines: 185, 263

### _get_nested
Used at lines: 335, 401

### _glob_to_regex
Used at lines: 83

### _load_yaml
Used at lines: 261

### _max_concurrent_calls
Used at lines: 167

### _path_matches
Used at lines: 309, 331

### _save_yaml
Used at lines: 411, 414

### _set_nested
Used at lines: 408

### get_global_semaphore
Used at lines: (none)

## Control Flow

### _set_nested
Sets a nested value in a dictionary.

### _get_nested
Gets a nested value from a dictionary.

### _deep_merge
Merges two dictionaries recursively.

### _load_yaml
Loads a YAML file.

### _save_yaml
Saves a YAML file.

### _max_concurrent_calls
Gets the maximum number of concurrent calls.

### _path_matches
Checks if a path matches a pattern.

### _glob_to_regex
Converts a glob pattern to a regular expression.

### get_global_semaphore
Gets a global semaphore.

### EnvLoader.load
Loads an environment.

### ScoutConfig.__init__
Initializes a ScoutConfig object.

### ScoutConfig._default_search_paths
Gets the default search paths.

### ScoutConfig._apply_env_overrides
Applies environment overrides.

### ScoutConfig._ensure_hard_cap_in_limits
Ensures the hard cap in limits.

### ScoutConfig.resolve_trigger
Resolves a trigger.

### ScoutConfig.effective_max_cost
Gets the effective maximum cost.

### ScoutConfig.should_process
Checks if a file should be processed.

### ScoutConfig.to_dict
Converts the config to a dictionary.

### ScoutConfig.get_user_config_path
Gets the user config path.

### ScoutConfig.get_project_config_path
Gets the project config path.

### ScoutConfig.whimsy_mode
Checks if whimsy mode is enabled.

### ScoutConfig.get
Gets a value from the config.

### ScoutConfig.set
Sets a value in the config.

### ScoutConfig.validate_yaml
Validates a YAML file.

### TriggerConfig
Represents a trigger configuration.