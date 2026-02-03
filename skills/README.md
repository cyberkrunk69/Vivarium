# Voyager Skill Library

An ever-growing library of executable skills implementing the Voyager architecture from **arXiv:2305.16291**.

## Architecture

Skills are **temporally extended, interpretable, and compositional**:

- **Temporally Extended**: Each skill encapsulates multi-step learned patterns
- **Interpretable**: Clear preconditions, postconditions, and documented code
- **Compositional**: Skills combine to solve larger problems, compounding agent capabilities

## Core Components

### `skill_registry.py`

Central registry for skill management:

```python
from skills.skill_registry import (
    register_skill,           # Add new skill
    retrieve_skill,           # Find matching skill by task description
    compose_skills,           # Combine 2+ skills into executable sequence
    list_skills,              # Enumerate all registered skills
    get_skill                 # Retrieve specific skill by name
)
```

**API:**

- `register_skill(name, code, description, preconditions, postconditions)` - Register new skill
- `retrieve_skill(task_description)` - Keyword-based retrieval matching task
- `compose_skills(skill_names)` - Combine multiple skills into Python code
- `list_skills()` - Get all skill names
- `get_skill(name)` - Get specific skill metadata

## Base Skills

### 1. `import_config_constants`

**Purpose**: Centralize configuration and constants imports

**Category**: Configuration

**Preconditions:**
- `config` module exists
- Constants defined

**Postconditions:**
- Constants imported from centralized location
- No magic strings in code

**Use Case**: Remove scattered configuration values, enable rapid config changes

```python
from skills.skill_registry import retrieve_skill

skill = retrieve_skill("import configuration")
# Returns skill data with executable code
```

### 2. `migrate_to_utils`

**Purpose**: Extract repeated patterns to utility modules

**Category**: Code Deduplication

**Preconditions:**
- Identified repeated patterns
- Utils module ready

**Postconditions:**
- No code duplication
- Utilities centralized
- Imports from utils

**Use Case**: Consolidate utility functions, eliminate 40+ lines of duplication

### 3. `add_test_coverage`

**Purpose**: Implement systematic test patterns

**Category**: Testing

**Preconditions:**
- Function/class to test exists
- Tests directory exists
- pytest available

**Postconditions:**
- Test file created
- Happy path and error paths tested
- Mocking and isolation patterns applied
- All tests passing

**Use Case**: Enable safe refactoring, document expected behavior, catch regressions

## Usage Examples

### Single Skill Application

```python
from skills.skill_registry import get_skill

skill = get_skill('import_config_constants')
print(skill['description'])
print(skill['preconditions'])
print(skill['code'])
```

### Skill Composition

Combine multiple skills for complex workflows:

```python
from skills.skill_registry import compose_skills

# Configuration-first refactoring workflow
composed = compose_skills(['import_config_constants', 'migrate_to_utils'])

# Output: Combined executable code with skill headers and documentation
print(composed)
```

### Task-Based Skill Retrieval

```python
from skills.skill_registry import retrieve_skill

# Automatic skill suggestion based on task description
skill = retrieve_skill('add test coverage to new module')
# Returns: add_test_coverage skill

skill = retrieve_skill('centralize configuration values')
# Returns: import_config_constants skill
```

## Skill Registration

New skills are loaded at module initialization:

```python
# skills/skill_registry.py registers all base skills
# Custom skills can be added:

from skills.skill_registry import register_skill

register_skill(
    'my_skill',
    '# Skill code here\nmy_pattern()',
    'Description of what skill does',
    preconditions=['condition1', 'condition2'],
    postconditions=['outcome1', 'outcome2']
)
```

## Composition Patterns

### Pattern 1: Configuration-First Refactoring
```
import_config_constants → migrate_to_utils
Clean config enables consistent utility implementations
```

### Pattern 2: Safe Code Migration
```
migrate_to_utils → add_test_coverage
Testing prevents regressions when refactoring
```

### Pattern 3: Complete Module Refactoring
```
import_config_constants → migrate_to_utils → add_test_coverage
Organize config, consolidate utilities, add test coverage
```

## Design Insights

### Capability Compounding
- 3 base skills enable ~9 two-skill combinations
- Each new skill multiplies problem-solving capability
- Skills build on each other (e.g., test coverage applies to migrated utils)

### Retrieval Strategy
- Keyword-based matching for base skills
- Task description → automatic skill suggestion
- Scales to fuzzy matching if library grows beyond ~50 skills

### Execution Flow
1. **Retrieve**: Match task description to skill
2. **Validate**: Check preconditions before applying
3. **Execute**: Run skill code (or compose with other skills)
4. **Verify**: Ensure postconditions are satisfied

## Files

- `skill_registry.py` - Core registry implementation
- `registered_skills.json` - Metadata catalog of all skills
- `import_config_constants.py` - Configuration pattern skill
- `migrate_to_utils.py` - Code deduplication pattern skill
- `add_test_coverage.py` - Testing pattern skill
- `README.md` - This documentation

## Integration Points

- **Agent Planning**: Task planner queries registry for relevant skills
- **Learning Loop**: New patterns extracted from completed SOPs added as skills
- **Composition Engine**: Skill composer chains skills into complex workflows
- **Session Persistence**: Registry serialized to JSON for cross-session skill retention

## References

- **Voyager**: An Open-Ended Embodied Agent with Large Language Models (arXiv:2305.16291)
- **Learned from**: SOP execution patterns, refactoring workflows, testing best practices

## Next Steps

As the system evolves:
1. Extract new skills from completed high-impact SOPs
2. Measure skill reusability and composition frequency
3. Add skill versioning as patterns improve
4. Implement fuzzy matching for skill retrieval at scale
5. Build UI for skill discovery and composition
