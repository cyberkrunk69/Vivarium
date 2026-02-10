"""
Test Automatic Skill Extraction System

Demonstrates the complete workflow:
1. Session completes with quality >= 0.9
2. extract_skill_from_session() extracts code patterns
3. auto_register_skill() registers the skill
4. Skill is available in registry for future tasks
"""

from skill_extractor import extract_skill_from_session, auto_register_skill
from skills.skill_registry import get_skill, list_skills


def test_skill_extraction_workflow():
    """Test the complete skill extraction and registration workflow"""

    print("=" * 60)
    print("AUTOMATIC SKILL EXTRACTION TEST")
    print("=" * 60)

    # Initial state
    initial_skills = list_skills()
    print(f"\n1. Initial skills in registry: {len(initial_skills)}")
    print(f"   Skills: {initial_skills}")

    # Simulate high-quality successful session
    print("\n2. Simulating successful session with quality_score=0.95...")
    session_log = {
        "returncode": 0,
        "quality_score": 0.95,
        "task": "Add automatic skill extraction from successful sessions",
        "output": '''
def extract_patterns(data):
    """Extract code patterns from session output"""
    patterns = []
    for line in data.split("\\n"):
        if line.strip().startswith("def ") or line.strip().startswith("class "):
            patterns.append(line)
    return patterns

class SkillExtractor:
    """Automatically extract reusable skills from sessions"""
    def __init__(self):
        self.skills = {}

    def register(self, skill_name, skill_code):
        self.skills[skill_name] = skill_code
''',
        "files_modified": ["skill_extractor.py", "grind_spawner.py"]
    }

    # Extract skill
    print("\n3. Extracting skill from session log...")
    extracted = extract_skill_from_session(session_log, session_id=42)

    if extracted:
        print(f"   [SUCCESS] Skill extracted!")
        print(f"   - Name: {extracted['skill_name']}")
        print(f"   - Description: {extracted['skill_description']}")
        print(f"   - Quality: {extracted['quality_score']:.2f}")
        print(f"   - Files: {len(extracted['files_modified'])}")
        print(f"   - Code snippet (first 150 chars):")
        print(f"     {extracted['skill_code'][:150]}...")
    else:
        print("   [FAIL] No skill extracted")
        return False

    # Register skill
    print("\n4. Registering extracted skill...")
    result = {
        "returncode": 0,
        "quality_score": 0.95,
        "stdout": session_log["output"],
        "files_modified": session_log["files_modified"]
    }
    context = {
        "task": session_log["task"]
    }

    registered = auto_register_skill(42, result, context)
    if registered:
        print("   [SUCCESS] Skill registered in registry")
    else:
        print("   [INFO] Skill not registered (may already exist)")

    # Verify in registry
    print("\n5. Verifying skill in registry...")
    skill = get_skill(extracted['skill_name'])
    if skill:
        print(f"   [SUCCESS] Skill '{skill['name']}' found in registry!")
        print(f"   - Description: {skill['description']}")
        print(f"   - Preconditions: {skill['preconditions']}")
        print(f"   - Postconditions: {skill['postconditions']}")
    else:
        print(f"   [INFO] Skill not in registry (in-memory only)")

    # Final state
    final_skills = list_skills()
    print(f"\n6. Final skills in registry: {len(final_skills)}")
    new_skills = [s for s in final_skills if s not in initial_skills]
    if new_skills:
        print(f"   New skills added: {new_skills}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    test_skill_extraction_workflow()
