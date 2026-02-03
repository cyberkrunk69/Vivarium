# Experiment Sandbox Safety Rules

## Core Protection Rules

### Read-Only Core Files
The following patterns are protected and cannot be modified directly:
- `*.py` (all Python files in workspace root)
- `grind_spawner*.py` (all grind spawner variants)
- `orchestrator.py` (main orchestrator)
- `roles.py` (role system)
- `utils.py` (utility functions)
- `cost_tracker.py` (cost tracking)
- `memory_synthesis.py` (memory systems)

### Safe Write Behavior
When workers attempt to write protected files:
1. Files are automatically redirected to `experiments/auto/` directory
2. A warning is logged about the redirection
3. Workers continue execution with the redirected path

### Experiment Promotion
Protected files can only be modified through the promotion process:
```python
from experiments_sandbox import promote_experiment
promote_experiment("my_experiment", approval_token="OVERRIDE_CORE_PROTECTION")
```

## Implementation Details

### File Interception
- `GroqArtifactExtractor` uses `safe_write_path()` before saving artifacts
- Redirected files maintain original name in `experiments/auto/` subdirectory
- Workers are notified of redirection through log messages

### Approval Tokens
- `OVERRIDE_CORE_PROTECTION`: Allows overwriting protected files during promotion
- Without token: Promotion fails with protection error
- Tokens provide audit trail of intentional core modifications

### Experiment Management
- `experiments_manifest.json` tracks all experiments and promotions
- Each experiment has metadata: author, creation time, file list
- Promoted experiments are archived with promotion timestamp

## Worker Guidelines

### Safe Experimentation
1. Create experiments for new features: `create_experiment("feature_name")`
2. Test changes in sandbox before promotion
3. Use promotion workflow for production deployment

### File Organization
```
experiments/
├── auto/           # Auto-redirected protected files
├── feature_x/      # Named experiments
├── bugfix_y/       # Bug fix experiments
└── research_z/     # Research experiments
```

### Best Practices
- Always test in experiments/ before promotion
- Use descriptive experiment names
- Include documentation in experiment directories
- Clean up failed experiments regularly

## Monitoring and Auditing

### Log Messages
- `[SANDBOX] Redirected {original} -> {safe_path} (protected file)`
- `[PROMOTION] Successfully promoted experiment: {name}`
- `[PROTECTION] Cannot promote: would overwrite protected files`

### Manifest Tracking
- All experiment operations logged to `experiments_manifest.json`
- Promotion history maintained with approval tokens
- File modification timeline preserved

This system ensures worker autonomy while protecting critical system components.