"""
Skill Extraction Module
Automatically extracts skills from successful high-quality sessions
"""
import json
from pathlib import Path


def extract_skill_from_session(session_log):
    """Extract reusable skill from successful session log

    Args:
        session_log: Dict containing session results with keys:
            - quality_score: float (0.0-1.0)
            - task: str (task description)
            - log_file: str (path to log file)
            - returncode: int
            - self_verified: bool

    Returns:
        Skill name if extracted and registered, None otherwise
    """
    # Import here to avoid circular dependency
    from skills.skill_registry import register_skill, get_skill

    # Only extract from high-quality successful sessions
    if session_log.get('quality_score', 0) < 0.9:
        return None
    if session_log.get('returncode', 1) != 0:
        return None
    if not session_log.get('self_verified', False):
        return None

    task_desc = session_log.get('task', '')
    log_file_path = session_log.get('log_file', '')

    # Read log file to extract output
    try:
        log_path = Path(log_file_path)
        if not log_path.exists():
            return None

        log_data = json.loads(log_path.read_text())
        output = log_data.get('result', log_data.get('output', ''))

        # Extract code patterns (look for function definitions, classes, imports)
        code_patterns = []
        lines = output.split('\n') if output else []

        in_code_block = False
        current_block = []

        for line in lines:
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    code_patterns.append('\n'.join(current_block))
                    current_block = []
                in_code_block = not in_code_block
            elif in_code_block:
                current_block.append(line)

        # If no code blocks found, try extracting functions/classes
        if not code_patterns:
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') or line.strip().startswith('class '):
                    # Extract this function/class
                    func_lines = [line]
                    indent_level = len(line) - len(line.lstrip())
                    for j in range(i + 1, len(lines)):
                        next_line = lines[j]
                        if next_line.strip() and (len(next_line) - len(next_line.lstrip())) <= indent_level:
                            break
                        func_lines.append(next_line)
                    code_patterns.append('\n'.join(func_lines))

        if not code_patterns:
            return None

        # Generate skill name from task
        skill_name = task_desc.lower()[:50].replace(' ', '_').replace(':', '').replace('.', '')
        skill_name = ''.join(c for c in skill_name if c.isalnum() or c == '_')
        skill_name = f"learned_{skill_name}"

        # Check if skill already exists
        if get_skill(skill_name):
            return None

        # Create skill code
        skill_code = f"# Learned from session: {log_file_path}\n"
        skill_code += f"# Task: {task_desc}\n"
        skill_code += f"# Quality score: {session_log.get('quality_score', 0):.2f}\n\n"
        skill_code += '\n\n'.join(code_patterns)

        # Register the skill
        register_skill(
            name=skill_name,
            code=skill_code,
            description=f"Auto-extracted pattern from: {task_desc[:100]}",
            preconditions=["High-quality session (>= 0.9)", "Self-verified success"],
            postconditions=["Reusable code pattern extracted"]
        )

        return skill_name

    except Exception as e:
        print(f"Warning: Could not extract skill from session: {e}")
        return None
