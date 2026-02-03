"""
Prompt Injection Defense System
Sanitizes task inputs to prevent malicious prompt injection attacks.
"""

import re
import json
from typing import Dict, Any, List, Tuple


class PromptSanitizer:
    """Detects and strips prompt injection patterns from task inputs."""

    # Dangerous injection patterns
    INJECTION_PATTERNS = [
        # Role manipulation attempts
        r'\[SYSTEM\]',
        r'\[ASSISTANT\]',
        r'\[USER\]',
        r'<\|im_start\|>',
        r'<\|im_end\|>',
        r'You are now',
        r'Ignore previous instructions',
        r'Disregard all',
        r'Forget everything',

        # Command injection
        r'\[SANITIZED\]',
        r'\[APPROVED\]',
        r'\[BYPASS\]',
        r'\[OVERRIDE\]',
        r'sudo ',
        r'rm -rf',
        r'--no-sandbox',

        # Format manipulation
        r'```json\s*{[^}]*"role"\s*:',
        r'OUTPUT FORMAT:',
        r'RESPOND ONLY WITH:',

        # Meta-instructions
        r'print\s+your\s+instructions',
        r'reveal\s+your\s+prompt',
        r'show\s+system\s+prompt',
        r'what\s+are\s+your\s+rules',

        # Execution hijacking
        r'exec\(',
        r'eval\(',
        r'__import__\(',
        r'compile\(',

        # Path traversal in task text
        r'\.\./\.\.',
        r'%2e%2e%2f',
    ]

    # High-risk keywords (case-insensitive)
    HIGH_RISK_KEYWORDS = [
        'ignore', 'disregard', 'forget', 'bypass', 'override',
        'jailbreak', 'prompt', 'instructions', 'system', 'sudo',
        'elevated', 'admin', 'root', 'privilege'
    ]

    def __init__(self):
        """Initialize the prompt sanitizer."""
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.INJECTION_PATTERNS]

    def detect_injection_attempt(self, text: str) -> bool:
        """
        Detect if text contains prompt injection patterns.

        Args:
            text: Input text to analyze

        Returns:
            True if injection attempt detected, False otherwise
        """
        if not isinstance(text, str):
            return False

        # Check compiled regex patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True

        # Check high-risk keyword density
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in self.HIGH_RISK_KEYWORDS if keyword in text_lower)

        # If 3+ high-risk keywords in short text, flag as suspicious
        if keyword_count >= 3 and len(text) < 500:
            return True

        # Check for excessive special characters (obfuscation)
        special_char_ratio = sum(1 for c in text if not c.isalnum() and not c.isspace()) / max(len(text), 1)
        if special_char_ratio > 0.3:
            return True

        return False

    def sanitize_task(self, task: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Sanitize task input by removing dangerous patterns.

        Args:
            task: Task dictionary to sanitize

        Returns:
            Tuple of (cleaned_task, was_modified)
        """
        if not isinstance(task, dict):
            raise ValueError("Task must be a dictionary")

        # Validate required fields - accept either 'task' or 'description'
        if "description" not in task and "task" not in task:
            raise ValueError("Task must contain 'task' or 'description' field")

        # Normalize: if 'task' exists but not 'description', use 'task'
        if "task" in task and "description" not in task:
            task = task.copy()
            task["description"] = task["task"]

        cleaned_task = task.copy()
        was_modified = False

        # Sanitize description field
        original_desc = str(task.get("description", ""))
        cleaned_desc = self._sanitize_text(original_desc)

        if cleaned_desc != original_desc:
            cleaned_task["description"] = cleaned_desc
            was_modified = True

        # Sanitize other text fields
        for field in ["context", "instructions", "notes"]:
            if field in task:
                original = str(task[field])
                cleaned = self._sanitize_text(original)
                if cleaned != original:
                    cleaned_task[field] = cleaned
                    was_modified = True

        # Validate task structure (prevent malformed JSON attacks)
        self._validate_structure(cleaned_task)

        return cleaned_task, was_modified

    def _sanitize_text(self, text: str) -> str:
        """
        Remove dangerous patterns from text.

        Args:
            text: Text to sanitize

        Returns:
            Sanitized text with dangerous patterns removed
        """
        if not isinstance(text, str):
            return str(text)

        sanitized = text

        # Remove injection patterns
        for pattern in self.compiled_patterns:
            sanitized = pattern.sub('[REMOVED]', sanitized)

        # Limit consecutive special characters (anti-obfuscation)
        sanitized = re.sub(r'([^a-zA-Z0-9\s])\1{3,}', r'\1\1', sanitized)

        # Remove zero-width characters (hidden text attacks)
        sanitized = re.sub(r'[\u200b-\u200f\ufeff]', '', sanitized)

        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()

        return sanitized

    def _validate_structure(self, task: Dict[str, Any]) -> None:
        """
        Validate task structure to prevent malformed data attacks.

        Args:
            task: Task dictionary to validate

        Raises:
            ValueError: If task structure is invalid
        """
        # Check for excessive nesting (JSON bomb prevention)
        try:
            json_str = json.dumps(task)
            if json_str.count('{') > 50 or json_str.count('[') > 50:
                raise ValueError("Task structure too deeply nested")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid task structure: {e}")

        # Check total size (prevent memory attacks)
        if len(json_str) > 100_000:  # 100KB limit
            raise ValueError("Task size exceeds maximum allowed")

        # Validate field types
        if "description" in task and not isinstance(task["description"], str):
            raise ValueError("Task description must be a string")

        if "priority" in task:
            try:
                priority = int(task["priority"])
                if priority < 0 or priority > 10:
                    raise ValueError("Priority must be between 0 and 10")
            except (ValueError, TypeError):
                raise ValueError("Priority must be an integer")


def sanitize_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to sanitize a task.

    Args:
        task: Task dictionary to sanitize

    Returns:
        Sanitized task dictionary

    Raises:
        ValueError: If task is invalid or injection detected
    """
    sanitizer = PromptSanitizer()

    # Detect injection attempts
    text_to_check = task.get("description") or task.get("task")
    if text_to_check:
        if sanitizer.detect_injection_attempt(str(text_to_check)):
            raise ValueError("Potential prompt injection detected in task")

    # Sanitize and return
    cleaned_task, was_modified = sanitizer.sanitize_task(task)

    if was_modified:
        print(f"WARNING: Task was sanitized (dangerous patterns removed)")

    return cleaned_task


def detect_injection_attempt(text: str) -> bool:
    """
    Convenience function to detect injection attempts.

    Args:
        text: Text to analyze

    Returns:
        True if injection attempt detected, False otherwise
    """
    sanitizer = PromptSanitizer()
    return sanitizer.detect_injection_attempt(text)
