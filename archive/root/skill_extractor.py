"""
Automatic Skill Extraction Module

Extracts reusable skills from successful high-quality sessions (>= 0.9 quality score).
Integrates with skill_registry.py to populate skill library automatically.
"""

from skills.skill_registry import register_skill, get_skill


def extract_skill_from_session(session_log: dict, session_id: int) -> dict:
    """
    Extract reusable skill from successful session log.

    Args:
        session_log: Dict containing session output, quality score, task, etc.
        session_id: Session identifier

    Returns:
        Dict with extracted skill metadata, or None if no skill extracted
    """
    try:
        # Only extract from high-quality successful sessions
        if session_log.get("returncode") != 0 or session_log.get("quality_score", 0) < 0.9:
            return None

        task = session_log.get("task", "")
        output = session_log.get("output", "")
        files_modified = session_log.get("files_modified", [])

        # Detect code patterns from output
        code_patterns = []
        if "def " in output or "class " in output:
            # Extract function/class definitions
            lines = output.split("\n")
            for i, line in enumerate(lines):
                if line.strip().startswith("def ") or line.strip().startswith("class "):
                    # Extract function/class and a few lines of context
                    pattern = "\n".join(lines[i:min(i+10, len(lines))])
                    code_patterns.append(pattern)

        if not code_patterns:
            return None

        # Identify reusable approach from task description
        task_lower = task.lower()
        skill_name = None
        skill_desc = None

        # Pattern-based skill naming
        if "extract" in task_lower or "parse" in task_lower:
            skill_name = f"extract_pattern_{session_id}"
            skill_desc = f"Extract and parse data pattern learned from: {task[:50]}"
        elif "auto" in task_lower and "skill" in task_lower:
            skill_name = f"auto_skill_extraction_{session_id}"
            skill_desc = "Automatically extract skills from successful sessions"
        elif "register" in task_lower or "create" in task_lower:
            skill_name = f"registration_pattern_{session_id}"
            skill_desc = f"Registration/creation pattern from: {task[:50]}"
        else:
            # Generic skill naming
            task_words = [w for w in task_lower.split() if len(w) > 4][:3]
            skill_name = "_".join(task_words) if task_words else f"learned_skill_{session_id}"
            skill_desc = f"Learned pattern from successful task: {task[:60]}"

        # Build skill code from extracted patterns
        skill_code = f"""# Auto-extracted skill: {skill_name}
# Source session: {session_id}
# Original task: {task}
# Quality score: {session_log.get('quality_score', 0):.2f}

{chr(10).join(code_patterns[:3])}  # Top 3 patterns extracted
"""

        return {
            "skill_name": skill_name,
            "skill_code": skill_code,
            "skill_description": skill_desc,
            "source_session": session_id,
            "quality_score": session_log.get("quality_score", 0),
            "files_modified": files_modified,
            "preconditions": [f"Task similar to: {task[:50]}"],
            "postconditions": ["High quality completion", "Quality score >= 0.9"]
        }
    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not extract skill: {e}")
        return None


def auto_register_skill(session_id: int, result: dict, context: dict) -> bool:
    """
    Automatically extract and register skill from session if quality >= 0.9.

    Args:
        session_id: Session identifier
        result: Session result dict with returncode, quality_score, etc.
        context: Session context dict with task, role, etc.

    Returns:
        True if skill was extracted and registered, False otherwise
    """
    try:
        # Only process successful high-quality runs
        if result.get("returncode") != 0 or result.get("quality_score", 0) < 0.9:
            return False

        session_log = {
            "returncode": result.get("returncode"),
            "quality_score": result.get("quality_score", 0),
            "task": context.get("task", ""),
            "output": result.get("stdout", ""),
            "files_modified": result.get("files_modified", [])
        }

        extracted_skill = extract_skill_from_session(session_log, session_id)
        if not extracted_skill:
            return False

        skill_name = extracted_skill["skill_name"]

        # Only register if skill doesn't already exist
        if get_skill(skill_name):
            print(f"[Session {session_id}] Skill '{skill_name}' already exists, skipping")
            return False

        # Register the skill
        register_skill(
            name=skill_name,
            code=extracted_skill["skill_code"],
            description=extracted_skill["skill_description"],
            preconditions=extracted_skill["preconditions"],
            postconditions=extracted_skill["postconditions"]
        )

        print(f"[Session {session_id}] Auto-extracted and registered skill: {skill_name}")
        print(f"[Session {session_id}]   Quality: {extracted_skill['quality_score']:.2f}")
        print(f"[Session {session_id}]   Files: {len(extracted_skill['files_modified'])}")
        return True

    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not auto-register skill: {e}")
        return False
