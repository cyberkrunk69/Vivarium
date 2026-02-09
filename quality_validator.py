import os
import re
import ast

class ValidationError(Exception):
    """Raised when code fails any quality validation rule."""
    pass

def strip_markdown(text: str) -> str:
    """
    Remove common markdown formatting from a string.
    This includes back‑ticks, headings, lists, bold/italic markers, and
    code fences.
    """
    # Remove fenced code blocks (```...``` or ~~~...~~~)
    text = re.sub(r'(?s)```.*?```', '', text)
    text = re.sub(r'(?s)~~~.*?~~~', '', text)

    # Remove inline back‑ticks
    text = re.sub(r'`([^`]*)`', r'\1', text)

    # Remove markdown headings, lists, bold/italic markers
    lines = []
    for line in text.splitlines():
        line = re.sub(r'^\s{0,3}(#{1,6})\s+', '', line)   # headings
        line = re.sub(r'^\s*[-*+]\s+', '', line)         # unordered list
        line = re.sub(r'^\s*\d+\.\s+', '', line)        # ordered list
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)    # bold
        line = re.sub(r'\*(.*?)\*', r'\1', line)        # italic
        line = re.sub(r'__(.*?)__', r'\1', line)        # bold alternative
        line = re.sub(r'_(.*?)_', r'\1', line)          # italic alternative
        lines.append(line)
    return "\n".join(lines)

def contains_markdown_fence(text: str) -> bool:
    """Return True if the text contains any markdown code fence."""
    return bool(re.search(r'```', text))

def contains_placeholder_logic(text: str) -> bool:
    """
    Detect placeholder constructs such as `random()`, `TODO()`,
    or obvious stub returns like `pass`/`...` without real implementation.
    """
    placeholders = [
        r'\brandom\s*\(',
        r'\bTODO\s*\(',
        r'\bpass\b',
        r'\.\.\.',
    ]
    pattern = re.compile("|".join(placeholders))
    return bool(pattern.search(text))

def contains_todo_comments(text: str) -> bool:
    """Detect unresolved TODO comments."""
    return bool(re.search(r'#\s*TODO\b', text, re.IGNORECASE))

def is_syntax_valid_python(code: str) -> bool:
    """Check if Python code can be parsed without SyntaxError."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def safe_overwrite_check(path: str, new_content: str) -> bool:
    """
    Ensure that overwriting a file is safe:
    - If the file does not exist, it's safe.
    - If it exists, only allow overwrite when the new content is larger.
    """
    if not os.path.exists(path):
        return True
    try:
        existing_size = os.path.getsize(path)
        new_size = len(new_content.encode('utf-8'))
        return new_size >= existing_size
    except OSError:
        # If we cannot read the existing file size, be conservative and deny.
        return False

def validate_code(text: str) -> str:
    """
    Run the full validation pipeline on the supplied code.
    Returns the cleaned (markdown‑stripped) code if all checks pass.
    Raises ValidationError with a clear message on failure.
    """
    cleaned = strip_markdown(text)

    if contains_markdown_fence(cleaned):
        raise ValidationError("Markdown code fences detected in code.")

    if contains_placeholder_logic(cleaned):
        raise ValidationError("Placeholder logic (e.g., random(), TODO(), pass, ...) found.")

    if contains_todo_comments(cleaned):
        raise ValidationError("Unresolved TODO comment found in code.")

    if not is_syntax_valid_python(cleaned):
        raise ValidationError("Python syntax validation failed.")

    return cleaned

def write_validated_file(path: str, content: str, *, force: bool = False) -> None:
    """
    Validate the content and write it to `path` safely.
    Parameters
    ----------
    path: str
        Destination file path.
    content: str
        Raw code to be written (may contain markdown that will be stripped).
    force: bool
        If True, bypass the size‑check when overwriting.
    Raises
    ------
    ValidationError
        If any quality rule is violated.
    OSError
        If the file cannot be written.
    """
    cleaned = validate_code(content)

    if not force and not safe_overwrite_check(path, cleaned):
        raise ValidationError(
            f"Refusing to overwrite '{path}' because the new content is smaller "
            "than the existing file."
        )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)

# Example usage (not executed during import):
# try:
#     write_validated_file("my_module.py", generated_code)
# except ValidationError as e:
#     print(f"Validation failed: {e}")
"""
quality_validator.py

A tiny utility that enforces the project's quality rules before any file is
written to disk.  Import and use `validate_and_write(path, content, mode='w')`
instead of direct `open(...).write(...)`.

The validator performs:
1. Stripping of markdown formatting.
2. Detection of markdown code fences.
3. Detection of placeholder logic (`random(`, `pass`, `TODO` comments).
4. Syntactic validation for Python files.
5. Safe‑overwrite checks (existing file must be larger than new content).
6. Guarantees the final content is written only if all checks pass.
"""

import ast
import os
import re
from typing import Optional


_MARKDOWN_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*$", re.MULTILINE)
_TODO_RE = re.compile(r"#\s*TODO[:]?|TODO[:]?")
_PLACEHOLDER_RE = re.compile(r"\brandom\s*\(|\bpass\b")
_MARKDOWN_FORMAT_RE = re.compile(r"(?m)^[#>*-]\s?.*$")  # headings, lists, blockquotes


def _strip_markdown_formatting(text: str) -> str:
    """Remove common markdown formatting while leaving code untouched."""
    # Remove headings, blockquotes, bullet lists that are on their own lines
    return _MARKDOWN_FORMAT_RE.sub("", text)


def _detect_markdown_fences(text: str) -> bool:
    """Return True if any markdown code fence is present."""
    return bool(_MARKDOWN_FENCE_RE.search(text))


def _detect_todo_comments(text: str) -> bool:
    """Return True if a TODO comment is found."""
    return bool(_TODO_RE.search(text))


def _detect_placeholder_logic(text: str) -> bool:
    """Return True if placeholder constructs like random() or bare pass are found."""
    return bool(_PLACEHOLDER_RE.search(text))


def _validate_syntax_python(text: str) -> bool:
    """Parse Python code to ensure syntactic correctness."""
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


def _is_safe_to_overwrite(path: str, new_content: str) -> bool:
    """Check that an existing file is larger (by line count) than the new content."""
    if not os.path.exists(path):
        return True  # No existing file, safe to create
    try:
        with open(path, "r", encoding="utf-8") as f:
            old_lines = f.readlines()
        new_lines = new_content.splitlines()
        return len(old_lines) >= len(new_lines)
    except Exception:
        # If we cannot read the old file, be conservative and refuse to overwrite
        return False


def validate_content(path: str, content: str) -> str:
    """
    Run all quality checks on ``content`` destined for ``path``.
    Returns the cleaned content (markdown stripped) if all checks pass,
    otherwise raises a ``ValueError`` describing the failure.
    """
    # 1. Strip markdown formatting
    cleaned = _strip_markdown_formatting(content)

    # 2. Prohibit markdown fences
    if _detect_markdown_fences(cleaned):
        raise ValueError("Markdown code fences are not allowed in source files.")

    # 3. Prohibit TODO comments
    if _detect_todo_comments(cleaned):
        raise ValueError("TODO comments must be resolved before saving.")

    # 4. Prohibit placeholder logic
    if _detect_placeholder_logic(cleaned):
        raise ValueError("Placeholder logic (e.g., random(), pass) is forbidden.")

    # 5. Syntax validation for Python files
    if path.lower().endswith(".py"):
        if not _validate_syntax_python(cleaned):
            raise ValueError("Generated Python code is syntactically invalid.")

    # 6. Safe overwrite check
    if not _is_safe_to_overwrite(path, cleaned):
        raise ValueError(
            f"Refusing to overwrite '{path}' with a smaller or unreadable file."
        )

    return cleaned


def validate_and_write(path: str, content: str, mode: str = "w", encoding: str = "utf-8"):
    """
    Validate ``content`` according to the quality rules and write it to ``path``.
    ``mode`` defaults to ``'w'`` (text write).  For binary writes, pass ``'wb'``.
    """
    cleaned = validate_content(path, content)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    with open(path, mode, encoding=encoding if "b" not in mode else None) as f:
        f.write(cleaned)


__all__ = [
    "validate_and_write",
    "validate_content",
]
\"\"\"quality_validator.py
Utility module that enforces the Quality Rules defined in QUALITY_RULES.md.

All code‑generation components should import and use the
`validate_and_save(content: str, path: str)` function instead of writing
files directly.
\"\"\"

import os
import re
import ast
from typing import Optional


# ----------------------------------------------------------------------
# Helper regexes
# ----------------------------------------------------------------------
_MARKDOWN_FENCE_RE = re.compile(r\"```(?:[a-zA-Z]*\\n)?(.*?)```\", re.DOTALL)
_TODO_COMMENT_RE = re.compile(r\"#\\s*TODO|#\\s*FIXME\", re.IGNORECASE)
_PLACEHOLDER_RE = re.compile(
    r\"\\brandom\\s*\\(\\s*\\)\\b|\\bpass\\b|\\.\\.\\.\", re.IGNORECASE
)


def strip_markdown_fences(code: str) -> str:
    \"\"\"Remove any markdown code fences from *code*.

    If the whole string is wrapped in a fence, only the inner content is
    returned.  Stand‑alone fences are also stripped.
    \"\"\"
    # Remove triple‑backtick fences, preserving inner code
    def _replacer(match: re.Match) -> str:
        return match.group(1)

    return _MARKDOWN_FENCE_RE.sub(_replacer, code)


def contains_markdown_fence(code: str) -> bool:
    \"\"\"Return ``True`` if any markdown fence (````` ````) is present.\"\"\"
    return bool(_MARKDOWN_FENCE_RE.search(code))


def contains_todo_comments(code: str) -> bool:
    \"\"\"Return ``True`` if a TODO/FIXME comment is found.\"\"\"
    return bool(_TODO_COMMENT_RE.search(code))


def contains_placeholder_logic(code: str) -> bool:
    \"\"\"Return ``True`` if placeholder constructs such as ``random()`` or ``pass`` are found.\"\"\"
    return bool(_PLACEHOLDER_RE.search(code))


def is_python_syntax_valid(code: str, filename: Optional[str] = None) -> bool:
    \"\"\"Validate Python syntax using ``ast.parse``.

    ``filename`` is used only for error messages; it does not affect parsing.
    \"\"\"
    try:
        ast.parse(code, filename=filename or \"<string>\")
        return True
    except SyntaxError:
        return False


def can_overwrite(new_content: str, path: str) -> bool:
    \"\"\"Determine whether *new_content* is allowed to overwrite *path*.

    The rule is: overwrite only if the new content is **>=** the existing
    file size (in bytes).  If the file does not exist, overwriting is allowed.
    \"\"\"
    if not os.path.exists(path):
        return True
    existing_size = os.path.getsize(path)
    return len(new_content.encode(\"utf-8\")) >= existing_size


def validate_code(content: str, path: str) -> None:
    \"\"\"Run all quality checks on *content* intended for *path*.

    Raises:
        ValueError: If any rule is violated.  The exception message
        identifies the offending rule.
    \"\"\"
    # 1. Strip markdown fences before any other check
    stripped = strip_markdown_fences(content)

    # 2. No markdown fences should remain
    if contains_markdown_fence(stripped):
        raise ValueError(\"Rule violation: markdown code fences must be removed before saving.\")

    # 3. No TODO/FIXME comments
    if contains_todo_comments(stripped):
        raise ValueError(\"Rule violation: TODO/FIXME comments must be resolved before saving.\")

    # 4. No placeholder logic
    if contains_placeholder_logic(stripped):
        raise ValueError(\"Rule violation: placeholder logic (e.g., random(), pass, ...) detected.\")
    
    # 5. Syntax validation for Python files
    if path.lower().endswith(\".py\") and not is_python_syntax_valid(stripped, filename=path):
        raise ValueError(f\"Rule violation: Python syntax error in generated code for {path}.\")

    # 6. Overwrite size check
    if not can_overwrite(stripped, path):
        raise ValueError(
            f\"Rule violation: refusing to overwrite {path} with a smaller file (size check failed).\")

    # If we reach here, all checks passed
    return stripped  # return the cleaned content for saving


def validate_and_save(content: str, path: str, mode: str = \"w\", encoding: str = \"utf-8\") -> None:
    \"\"\"Validate *content* according to the quality rules and write it to *path*.

    Parameters
    ----------
    content: str
        The raw code output (may contain markdown).
    path: str
        Destination file path.
    mode: str, optional
        File opening mode (default ``\"w\"``).  Only text modes are supported.
    encoding: str, optional
        Text encoding (default ``\"utf-8\"``).

    Raises
    ------
    ValueError
        If any quality rule is broken.
    IOError
        Propagated from the underlying file operation.
    \"\"\"
    cleaned = validate_code(content, path)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path) or \".\", exist_ok=True)
    with open(path, mode, encoding=encoding) as f:
        f.write(cleaned)


__all__ = [
    \"strip_markdown_fences\",
    \"contains_markdown_fence\",
    \"contains_todo_comments\",
    \"contains_placeholder_logic\",
    \"is_python_syntax_valid\",
    \"can_overwrite\",
    \"validate_code\",
    \"validate_and_save\",\n]
"""
quality_validator.py

Utility functions that enforce the QUALITY_RULES.md specifications.
All file writes in the project should go through `safe_write` to guarantee
that no markdown, placeholder logic, TODOs, or syntax errors are introduced,
and that overwrites are safe.
"""

import ast
import os
import re
from typing import Optional


_MARKDOWN_FENCE_RE = re.compile(r"```(?:[a-zA-Z]*\n)?(.*?)```", re.DOTALL)
_TODO_RE = re.compile(r"\bTODO\b", re.IGNORECASE)
_PLACEHOLDER_RE = re.compile(
    r"\b(random\s*\(\s*\)|pass\s*#\s*placeholder|#\s*placeholder)\b"
)


def strip_markdown_fences(text: str) -> str:
    """
    Remove any markdown code fences from the supplied text.
    """
    def _replacer(match: re.Match) -> str:
        # Return the inner code without the fences.
        return match.group(1)

    return _MARKDOWN_FENCE_RE.sub(_replacer, text)


def contains_todo(text: str) -> bool:
    """Return True if a TODO comment is found."""
    return bool(_TODO_RE.search(text))


def contains_placeholder_logic(text: str) -> bool:
    """Return True if obvious placeholder logic (e.g., random()) is found."""
    return bool(_PLACEHOLDER_RE.search(text))


def is_valid_python_syntax(text: str) -> bool:
    """
    Validate that the supplied Python source code can be parsed.
    Returns True if parsing succeeds, False otherwise.
    """
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


def _read_existing_file(path: str) -> Optional[str]:
    """Read the existing file if it exists; otherwise return None."""
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def safe_write(path: str, content: str) -> None:
    """
    Write `content` to `path` after performing all quality checks.

    Steps:
    1. Strip markdown fences.
    2. Ensure no TODO comments.
    3. Ensure no placeholder logic.
    4. Validate Python syntax.
    5. If the file exists, only overwrite when the new content is at least as
       large as the existing one (preventing accidental downgrade).
    6. Write the file.
    """
    # 1. Strip markdown.
    cleaned = strip_markdown_fences(content)

    # 2. TODO check.
    if contains_todo(cleaned):
        raise ValueError(f"TODO comment found in {path}. Resolve before saving.")

    # 3. Placeholder logic check.
    if contains_placeholder_logic(cleaned):
        raise ValueError(
            f"Placeholder logic detected in {path}. Implement real logic before saving."
        )

    # 4. Syntax validation.
    if not is_valid_python_syntax(cleaned):
        raise SyntaxError(f"Generated code for {path} is not syntactically valid Python.")

    # 5. Safe overwrite check.
    existing = _read_existing_file(path)
    if existing is not None:
        if len(cleaned) < len(existing):
            raise IOError(
                f"Refusing to overwrite {path}: new content is smaller than existing file."
            )

    # 6. Write the file.
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)


def validate_file(path: str) -> None:
    """
    Convenience wrapper that reads a file and runs all validation checks.
    Raises an exception if any rule is violated.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File {path} does not exist for validation.")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Run the same pipeline as safe_write (without the overwrite size check).
    cleaned = strip_markdown_fences(content)
    if contains_todo(cleaned):
        raise ValueError(f"TODO comment found in {path}.")
    if contains_placeholder_logic(cleaned):
        raise ValueError(f"Placeholder logic found in {path}.")
    if not is_valid_python_syntax(cleaned):
        raise SyntaxError(f"File {path} contains invalid Python syntax.")