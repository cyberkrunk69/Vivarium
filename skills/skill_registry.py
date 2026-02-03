"""
Voyager Skill Library Registry
Manages registration, retrieval, and composition of learned skills

Implements the Voyager architecture from arXiv:2305.16291:
- Skills are temporally extended, interpretable, and compositional
- Ever-growing skill library enables rapid capability compounding
- Retrieval by task description matches skills to new problems
- Embedding-based semantic retrieval enables precise skill matching
"""

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


class SkillRegistry:
    def __init__(self):
        self.skills = {}
        self.embeddings = None
        self.vectorizer = None
        self._embedding_mode = None
        self._initialize_builtin_skills()
        self._build_embeddings()

    def _initialize_builtin_skills(self):
        """Load built-in learned skills from the skill library"""
        # Skill 1: import_config_constants
        self.register_skill(
            'import_config_constants',
            """# Import config and constants from centralized location
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Centralized imports
from config import (
    DEFAULT_TIMEOUT,
    API_ENDPOINTS,
    LOGGING_CONFIG,
    DATABASE_URL
)

# Use constants instead of magic strings
timeout = DEFAULT_TIMEOUT
endpoints = API_ENDPOINTS
logging_config = LOGGING_CONFIG
""",
            "Centralizes configuration and constants imports to reduce duplication and enable easy maintenance",
            ["config module exists", "constants defined"],
            ["constants imported", "no magic strings in code"]
        )

        # Skill 2: migrate_to_utils
        self.register_skill(
            'migrate_to_utils',
            """# Migrate repeated patterns to utils module
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import utilities instead of duplicating code
from utils import (
    validate_input,
    format_response,
    handle_errors,
    parse_config
)

def process_data(data):
    # Use utility functions instead of inline code
    validated = validate_input(data)
    processed = handle_errors(validated)
    return format_response(processed)

# Reduce duplication across modules by centralizing common patterns
""",
            "Extracts repeated patterns and migrates them to utility modules for code reuse and maintainability",
            ["identified repeated patterns", "utils module ready"],
            ["no code duplication", "utilities centralized", "imports from utils"]
        )

        # Skill 3: add_test_coverage
        self.register_skill(
            'add_test_coverage',
            """import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from mymodule import my_function

class TestMyFunction:
    \"\"\"Test suite for my_function.\"\"\"

    def test_happy_path(self):
        \"\"\"Test normal operation with valid inputs.\"\"\"
        result = my_function(valid_input)
        assert result == expected_output

    def test_with_default_args(self):
        \"\"\"Test function with default arguments.\"\"\"
        result = my_function(required_arg)
        assert result is not None

    def test_error_on_invalid_input(self):
        \"\"\"Test exception handling for invalid input.\"\"\"
        with pytest.raises(ValueError):
            my_function(invalid_input)

    def test_error_on_missing_required_arg(self):
        \"\"\"Test exception for missing required argument.\"\"\"
        with pytest.raises(TypeError):
            my_function()

    def test_file_operation_isolated(self):
        \"\"\"Test file I/O with isolated temporary directory.\"\"\"
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test.json"
            write_json(test_path, {"key": "value"})
            data = read_json(test_path)
            assert data["key"] == "value"

    def test_with_mocked_external_call(self):
        \"\"\"Test with mocked external dependency.\"\"\"
        with patch('module.external_function') as mock_func:
            mock_func.return_value = expected_value
            result = function_under_test()
            mock_func.assert_called_once()
            assert result == expected_value

    def test_error_recovery(self):
        \"\"\"Test graceful error handling and recovery.\"\"\"
        with patch('module.api_call') as mock_api:
            mock_api.side_effect = ConnectionError("Network failed")
            result = function_under_test()
            assert result is None or result == default_value
""",
            "Comprehensive test coverage with happy path and error scenarios",
            ["Function/class to test exists", "tests/ directory exists", "pytest available"],
            ["Test file created", "Happy path tests verify correct output", "Error path tests implemented", "All tests passing"]
        )

    def _build_embeddings(self):
        """Generate TF-IDF embeddings for all skill descriptions"""
        if not EMBEDDING_AVAILABLE or not self.skills:
            self._embedding_mode = 'keyword' if self.skills else None
            return

        try:
            descriptions = [skill['description'] for skill in self.skills.values()]
            self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
            self.embeddings = self.vectorizer.fit_transform(descriptions)
            self._embedding_mode = 'tfidf'
        except Exception:
            self._embedding_mode = 'keyword'
            self.vectorizer = None
            self.embeddings = None

    def register_skill(self, name, code, description, preconditions=None, postconditions=None):
        """Register a new skill in the library"""
        self.skills[name] = {
            'name': name,
            'code': code,
            'description': description,
            'preconditions': preconditions or [],
            'postconditions': postconditions or []
        }
        # Rebuild embeddings when new skill is registered
        if EMBEDDING_AVAILABLE:
            self._build_embeddings()

    def retrieve_skill(self, task_description):
        """Retrieve matching skill code for a task description

        Strategy: embedding -> keyword matching -> composition -> None
        """
        # Try embedding-based retrieval first
        if self._embedding_mode == 'tfidf':
            result = self._retrieve_by_embedding(task_description)
            if result:
                return result

        # Try keyword matching
        result = self._retrieve_by_keywords(task_description)
        if result:
            return result

        # Try composition if no exact match
        sub_skills = self.decompose_task(task_description)
        if len(sub_skills) >= 2:
            return self.compose_skills(sub_skills)

        return None

    def _retrieve_by_embedding(self, task_description):
        """Retrieve skill using TF-IDF cosine similarity"""
        if not self.vectorizer or self.embeddings is None or len(self.skills) == 0:
            return None

        try:
            task_embedding = self.vectorizer.transform([task_description])
            similarities = cosine_similarity(task_embedding, self.embeddings)[0]

            # Return skill with highest similarity
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]

            # Only return if there's meaningful similarity (>= 0.3 threshold)
            if best_score >= 0.3:
                skill_name = list(self.skills.keys())[best_idx]
                return self.skills[skill_name]
        except Exception:
            pass

        return None

    def _retrieve_by_keywords(self, task_description):
        """Retrieve skill using keyword matching (fallback)"""
        task_lower = task_description.lower()

        # First try exact keyword matching in skill names
        for skill_name, skill_data in self.skills.items():
            keywords = skill_name.lower().split('_')
            if any(keyword in task_lower for keyword in keywords):
                return skill_data

        # Try matching description and metadata keywords
        keyword_map = {
            'duplicate': 'migrate_to_utils',
            'duplication': 'migrate_to_utils',
            'dedup': 'migrate_to_utils',
            'centrali': 'import_config_constants',
            'config': 'import_config_constants',
            'constant': 'import_config_constants',
            'magic string': 'import_config_constants',
            'test': 'add_test_coverage',
            'coverage': 'add_test_coverage',
        }

        for keyword, skill_name in keyword_map.items():
            if keyword in task_lower and skill_name in self.skills:
                return self.skills[skill_name]

        return None

    def decompose_task(self, task_description):
        """Analyze task and identify sub-skills needed

        Returns list of atomic skill names that can be composed to solve task.
        Uses embedding and keyword matching to find relevant skills.
        """
        task_lower = task_description.lower()
        matching_skills = []

        # Find all skills with relevant keywords
        for skill_name, skill_data in self.skills.items():
            skill_keywords = skill_name.lower().split('_')
            description_lower = skill_data['description'].lower()

            # Check if any skill keywords match task
            if any(keyword in task_lower for keyword in skill_keywords):
                matching_skills.append(skill_name)
                continue

            # Check if skill description matches task themes
            skill_desc_words = description_lower.split()
            task_words = set(task_lower.split())

            # Count overlapping words
            overlap = sum(1 for word in skill_desc_words if word in task_words)
            if overlap >= 2:  # At least 2 matching words
                matching_skills.append(skill_name)

        return matching_skills if matching_skills else []

    def compose_skills(self, skill_list):
        """Combine multiple skills into executable sequence

        Merges code, descriptions, and keywords from multiple skills.
        Returns composite skill with merged metadata.
        """
        if not skill_list:
            return None

        combined_code = "# Composed skill sequence\n\n"
        merged_keywords = set()
        descriptions = []

        for skill_name in skill_list:
            if skill_name in self.skills:
                skill = self.skills[skill_name]
                combined_code += f"# Skill: {skill['name']}\n"
                combined_code += f"# {skill['description']}\n"
                combined_code += skill['code'] + "\n\n"
                descriptions.append(skill['description'])

                # Extract keywords from skill name
                keywords = skill['name'].lower().split('_')
                merged_keywords.update(keywords)

        if not descriptions:
            return None

        # Create composite skill metadata
        composite_skill = {
            'name': f"composed_{len(skill_list)}_skills",
            'code': combined_code,
            'description': ' + '.join(descriptions),
            'component_skills': skill_list,
            'merged_keywords': list(merged_keywords),
            'preconditions': [],
            'postconditions': []
        }

        # Merge preconditions and postconditions
        for skill_name in skill_list:
            if skill_name in self.skills:
                skill = self.skills[skill_name]
                composite_skill['preconditions'].extend(skill.get('preconditions', []))
                composite_skill['postconditions'].extend(skill.get('postconditions', []))

        return composite_skill

    def list_skills(self):
        """List all registered skills"""
        return list(self.skills.keys())

    def get_skill(self, name):
        """Get a specific skill by name"""
        return self.skills.get(name)

    def save_registry(self, filepath):
        """Save skill registry to JSON file"""
        import json
        registry_data = {
            'metadata': {
                'description': 'Voyager Skill Library Registry',
                'total_skills': len(self.skills),
                'timestamp': __import__('datetime').datetime.now().isoformat()
            },
            'skills': {}
        }
        for name, skill in self.skills.items():
            registry_data['skills'][name] = {
                'name': skill['name'],
                'description': skill['description'],
                'preconditions': skill['preconditions'],
                'postconditions': skill['postconditions']
            }
        with open(filepath, 'w') as f:
            json.dump(registry_data, f, indent=2)


# Global registry instance
_registry = SkillRegistry()

def register_skill(name, code, description, preconditions=None, postconditions=None):
    """Register a skill in the global registry"""
    _registry.register_skill(name, code, description, preconditions, postconditions)

def retrieve_skill(task_description):
    """Retrieve a skill matching the task description"""
    return _registry.retrieve_skill(task_description)

def compose_skills(skill_list):
    """Compose multiple skills into executable code"""
    return _registry.compose_skills(skill_list)

def decompose_task(task_description):
    """Analyze task and return list of sub-skills needed"""
    return _registry.decompose_task(task_description)

def list_skills():
    """List all registered skills"""
    return _registry.list_skills()

def get_skill(name):
    """Get a specific skill by name"""
    return _registry.get_skill(name)
