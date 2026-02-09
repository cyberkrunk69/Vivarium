#!/usr/bin/env python3
"""
Surgical Edit Extractor - Extract and apply targeted code edits from model responses.

Instead of the anti-pattern of "output entire file, hope it's not destructive",
this uses a surgical edit paradigm:
1. Model outputs ONLY the change (search/replace or line-based insert)
2. Extractor intelligently applies the change to existing file
3. Much more token-efficient (less output = less cost)
4. Inherently safe (can't accidentally destroy 500-line files)
5. Self-correcting by design

Supports multiple edit formats:
- SEARCH/REPLACE blocks (edit-tool style)
- Line-based insertions (insert after line N, before function X)
- Append/prepend operations
- Function/class replacement by name
"""

import os
import re
import json
import logging
import difflib
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EditAction(Enum):
    """Types of surgical edits."""
    REPLACE = "replace"       # Search and replace text
    INSERT_AFTER = "insert_after"   # Insert after line/pattern
    INSERT_BEFORE = "insert_before" # Insert before line/pattern
    APPEND = "append"         # Add to end of file
    PREPEND = "prepend"       # Add to start of file
    DELETE = "delete"         # Remove matching text
    REPLACE_FUNCTION = "replace_function"  # Replace entire function by name
    REPLACE_CLASS = "replace_class"        # Replace entire class by name


@dataclass
class SurgicalEdit:
    """Represents a single surgical edit operation."""
    path: str
    action: EditAction
    content: str                    # The new content to insert/replace with
    search: Optional[str] = None    # For REPLACE: text to find
    line_number: Optional[int] = None  # For line-based operations
    pattern: Optional[str] = None   # For pattern-based operations (regex)
    target_name: Optional[str] = None  # For function/class replacement
    confidence: float = 1.0         # How confident we are in this edit


@dataclass
class EditResult:
    """Result of applying an edit."""
    success: bool
    path: str
    action: EditAction
    message: str
    lines_changed: int = 0
    backup_path: Optional[str] = None


class SurgicalEditExtractor:
    """
    Extracts and applies surgical edits from model responses.

    This replaces the old "extract entire file" approach with a safer,
    more efficient edit-based paradigm.
    """

    def __init__(self, workspace_root: str = ".", create_backups: bool = True):
        """
        Initialize the extractor.

        Args:
            workspace_root: Root directory for file operations
            create_backups: Whether to backup files before editing
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.create_backups = create_backups
        self.logger = logging.getLogger(__name__)
        self.backup_dir = self.workspace_root / ".edit_backups"

        if create_backups:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

    # Protected files - these can NEVER be edited by the swarm
    PROTECTED_FILES = {
        'grind_spawner.py',
        'grind_spawner_groq.py',
        'grind_spawner_unified.py',
        'orchestrator.py',
        'roles.py',
        'safety_gateway.py',
        'safety_constitutional.py',
        'safety_network.py',
        'safety_sanitize.py',
        'safety_killswitch.py',
        'safety_sandbox.py',
        'groq_code_extractor.py',
        'surgical_edit_extractor.py',  # This file too
    }

    def extract_edits(self, response_text: str) -> List[SurgicalEdit]:
        """
        Extract surgical edits from model response.

        Supports multiple formats:
        1. <edit> tags with action attribute
        2. SEARCH/REPLACE blocks (edit-tool style)
        3. <<<<<<< MINE / ======= / >>>>>>> THEIRS conflict markers

        Args:
            response_text: Raw model response

        Returns:
            List of SurgicalEdit objects
        """
        edits = []

        # Format 1: <edit> tags
        edits.extend(self._extract_edit_tags(response_text))

        # Format 2: SEARCH/REPLACE blocks
        edits.extend(self._extract_search_replace_blocks(response_text))

        # Format 3: Diff-style conflict markers
        edits.extend(self._extract_diff_markers(response_text))

        # Format 4: Explicit patch blocks
        edits.extend(self._extract_patch_blocks(response_text))

        return edits

    def _extract_edit_tags(self, text: str) -> List[SurgicalEdit]:
        """Extract <edit> XML-style tags."""
        edits = []

        # Pattern: <edit path="file.py" action="replace" search="old">new content</edit>
        pattern = r'<edit\s+([^>]+)>(.*?)</edit>'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        for attrs_str, content in matches:
            try:
                attrs = self._parse_attributes(attrs_str)

                if 'path' not in attrs:
                    self.logger.warning("Edit tag missing 'path' attribute")
                    continue

                action_str = attrs.get('action', 'replace').lower()
                try:
                    action = EditAction(action_str)
                except ValueError:
                    action = EditAction.REPLACE

                edit = SurgicalEdit(
                    path=attrs['path'],
                    action=action,
                    content=content.strip(),
                    search=attrs.get('search'),
                    line_number=int(attrs['line']) if 'line' in attrs else None,
                    pattern=attrs.get('pattern'),
                    target_name=attrs.get('target', attrs.get('function', attrs.get('class')))
                )

                edits.append(edit)

            except Exception as e:
                self.logger.error(f"Failed to parse edit tag: {e}")

        return edits

    def _extract_search_replace_blocks(self, text: str) -> List[SurgicalEdit]:
        """
        Extract SEARCH/REPLACE blocks (edit-tool style).

        Format:
        FILE: path/to/file.py
        <<<<<<< SEARCH
        old code to find
        =======
        new code to replace with
        >>>>>>> REPLACE
        """
        edits = []

        # Pattern for FILE: header followed by search/replace block
        pattern = r'(?:FILE|Path|Edit):\s*([^\n]+)\n<<<<<<+\s*SEARCH\n(.*?)\n=======+\n(.*?)\n>>>>>>>+\s*REPLACE'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        for file_path, search, replace in matches:
            edit = SurgicalEdit(
                path=file_path.strip(),
                action=EditAction.REPLACE,
                content=replace,
                search=search
            )
            edits.append(edit)

        # Also try without FILE: header (just infer from context or use last mentioned file)
        pattern_simple = r'<<<<<<+\s*SEARCH\n(.*?)\n=======+\n(.*?)\n>>>>>>>+\s*REPLACE'
        # This requires file path from context - skip for now

        return edits

    def _extract_diff_markers(self, text: str) -> List[SurgicalEdit]:
        """Extract git-style conflict markers."""
        edits = []

        # Pattern: <<<<<<< MINE ... ======= ... >>>>>>> THEIRS (with optional file path)
        pattern = r'(?:FILE:\s*([^\n]+)\n)?<<<<<<+\s*(?:MINE|HEAD|ORIGINAL)\n(.*?)\n=======+\n(.*?)\n>>>>>>>+\s*(?:THEIRS|BRANCH|NEW)'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        for file_path, original, new in matches:
            if not file_path:
                continue  # Need file path

            edit = SurgicalEdit(
                path=file_path.strip(),
                action=EditAction.REPLACE,
                content=new,
                search=original
            )
            edits.append(edit)

        return edits

    def _extract_patch_blocks(self, text: str) -> List[SurgicalEdit]:
        """
        Extract <patch> blocks for various operations.

        Format:
        <patch path="file.py" action="insert_after" line="42">
        new code to insert
        </patch>

        Or:
        <patch path="file.py" action="replace_function" target="my_function">
        def my_function():
            # new implementation
        </patch>
        """
        edits = []

        pattern = r'<patch\s+([^>]+)>(.*?)</patch>'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        for attrs_str, content in matches:
            try:
                attrs = self._parse_attributes(attrs_str)

                if 'path' not in attrs:
                    continue

                action_str = attrs.get('action', 'replace').lower()
                try:
                    action = EditAction(action_str)
                except ValueError:
                    action = EditAction.REPLACE

                edit = SurgicalEdit(
                    path=attrs['path'],
                    action=action,
                    content=content.strip(),
                    search=attrs.get('search'),
                    line_number=int(attrs['line']) if 'line' in attrs else None,
                    target_name=attrs.get('target')
                )

                edits.append(edit)

            except Exception as e:
                self.logger.error(f"Failed to parse patch block: {e}")

        return edits

    def _parse_attributes(self, attrs_str: str) -> Dict[str, str]:
        """Parse XML-style attributes."""
        attrs = {}
        pattern = r'(\w+)=["\']([^"\']*)["\']|(\w+)=(\S+)'
        matches = re.findall(pattern, attrs_str)

        for match in matches:
            if match[0]:
                attrs[match[0]] = match[1]
            elif match[2]:
                attrs[match[2]] = match[3]

        return attrs

    def apply_edits(self, edits: List[SurgicalEdit]) -> List[EditResult]:
        """
        Apply a list of surgical edits.

        Args:
            edits: List of edits to apply

        Returns:
            List of EditResult objects
        """
        results = []

        for edit in edits:
            result = self._apply_single_edit(edit)
            results.append(result)

        return results

    def _apply_single_edit(self, edit: SurgicalEdit) -> EditResult:
        """Apply a single surgical edit."""

        # Security check
        filename = Path(edit.path).name.lower()
        for protected in self.PROTECTED_FILES:
            if filename == protected.lower():
                return EditResult(
                    success=False,
                    path=edit.path,
                    action=edit.action,
                    message=f"BLOCKED: {edit.path} is a protected file"
                )

        # Validate path
        try:
            file_path = self._resolve_safe_path(edit.path)
        except ValueError as e:
            return EditResult(
                success=False,
                path=edit.path,
                action=edit.action,
                message=str(e)
            )

        # Check if file exists (except for APPEND/PREPEND which can create)
        if not file_path.exists():
            if edit.action in [EditAction.APPEND, EditAction.PREPEND]:
                # Create new file
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(edit.content, encoding='utf-8')
                return EditResult(
                    success=True,
                    path=edit.path,
                    action=edit.action,
                    message=f"Created new file with {len(edit.content)} characters",
                    lines_changed=edit.content.count('\n') + 1
                )
            else:
                return EditResult(
                    success=False,
                    path=edit.path,
                    action=edit.action,
                    message=f"File does not exist: {edit.path}"
                )

        # Read current content
        try:
            original_content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return EditResult(
                success=False,
                path=edit.path,
                action=edit.action,
                message=f"Failed to read file: {e}"
            )

        # Create backup
        backup_path = None
        if self.create_backups:
            backup_path = self._create_backup(file_path, original_content)

        # Apply the edit based on action type
        try:
            new_content, lines_changed = self._perform_edit(
                original_content, edit
            )
        except Exception as e:
            return EditResult(
                success=False,
                path=edit.path,
                action=edit.action,
                message=f"Edit failed: {e}",
                backup_path=str(backup_path) if backup_path else None
            )

        # Safety check: don't reduce file by more than 50%
        if len(new_content) < len(original_content) * 0.5 and len(original_content) > 100:
            return EditResult(
                success=False,
                path=edit.path,
                action=edit.action,
                message=f"BLOCKED: Edit would reduce file from {len(original_content)} to {len(new_content)} chars (>50% reduction)",
                backup_path=str(backup_path) if backup_path else None
            )

        # Write new content
        try:
            file_path.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return EditResult(
                success=False,
                path=edit.path,
                action=edit.action,
                message=f"Failed to write file: {e}",
                backup_path=str(backup_path) if backup_path else None
            )

        return EditResult(
            success=True,
            path=edit.path,
            action=edit.action,
            message=f"Successfully applied {edit.action.value} edit",
            lines_changed=lines_changed,
            backup_path=str(backup_path) if backup_path else None
        )

    def _perform_edit(self, content: str, edit: SurgicalEdit) -> Tuple[str, int]:
        """
        Perform the actual edit operation.

        Returns:
            (new_content, lines_changed)
        """
        lines = content.split('\n')

        if edit.action == EditAction.REPLACE:
            if not edit.search:
                raise ValueError("REPLACE action requires 'search' text")

            if edit.search not in content:
                # Try fuzzy matching
                match = self._fuzzy_find(content, edit.search)
                if match:
                    new_content = content.replace(match, edit.content, 1)
                    return new_content, edit.content.count('\n') + 1
                raise ValueError(f"Search text not found in file (even with fuzzy matching)")

            new_content = content.replace(edit.search, edit.content, 1)
            return new_content, edit.content.count('\n') + 1

        elif edit.action == EditAction.INSERT_AFTER:
            if edit.line_number is not None:
                if edit.line_number > len(lines):
                    raise ValueError(f"Line {edit.line_number} doesn't exist (file has {len(lines)} lines)")
                lines.insert(edit.line_number, edit.content)
                return '\n'.join(lines), edit.content.count('\n') + 1
            elif edit.pattern:
                # Find line matching pattern and insert after
                for i, line in enumerate(lines):
                    if re.search(edit.pattern, line):
                        lines.insert(i + 1, edit.content)
                        return '\n'.join(lines), edit.content.count('\n') + 1
                raise ValueError(f"Pattern '{edit.pattern}' not found")
            else:
                raise ValueError("INSERT_AFTER requires line_number or pattern")

        elif edit.action == EditAction.INSERT_BEFORE:
            if edit.line_number is not None:
                if edit.line_number > len(lines) or edit.line_number < 1:
                    raise ValueError(f"Invalid line number: {edit.line_number}")
                lines.insert(edit.line_number - 1, edit.content)
                return '\n'.join(lines), edit.content.count('\n') + 1
            elif edit.pattern:
                for i, line in enumerate(lines):
                    if re.search(edit.pattern, line):
                        lines.insert(i, edit.content)
                        return '\n'.join(lines), edit.content.count('\n') + 1
                raise ValueError(f"Pattern '{edit.pattern}' not found")
            else:
                raise ValueError("INSERT_BEFORE requires line_number or pattern")

        elif edit.action == EditAction.APPEND:
            if content and not content.endswith('\n'):
                content += '\n'
            new_content = content + edit.content
            return new_content, edit.content.count('\n') + 1

        elif edit.action == EditAction.PREPEND:
            new_content = edit.content + '\n' + content
            return new_content, edit.content.count('\n') + 1

        elif edit.action == EditAction.DELETE:
            if edit.search:
                if edit.search not in content:
                    raise ValueError("Delete target not found")
                new_content = content.replace(edit.search, '', 1)
                return new_content, edit.search.count('\n') + 1
            else:
                raise ValueError("DELETE requires 'search' text to delete")

        elif edit.action == EditAction.REPLACE_FUNCTION:
            if not edit.target_name:
                raise ValueError("REPLACE_FUNCTION requires target_name")
            new_content, changed = self._replace_function(content, edit.target_name, edit.content)
            return new_content, changed

        elif edit.action == EditAction.REPLACE_CLASS:
            if not edit.target_name:
                raise ValueError("REPLACE_CLASS requires target_name")
            new_content, changed = self._replace_class(content, edit.target_name, edit.content)
            return new_content, changed

        else:
            raise ValueError(f"Unknown action: {edit.action}")

    def _fuzzy_find(self, content: str, search: str, threshold: float = 0.8) -> Optional[str]:
        """
        Try to find similar text using fuzzy matching.

        Useful when whitespace or minor differences exist.
        """
        # Normalize whitespace for comparison
        search_normalized = ' '.join(search.split())

        # Try line-by-line matching
        lines = content.split('\n')
        search_lines = search.split('\n')

        if len(search_lines) == 1:
            # Single line search - find most similar line
            best_match = None
            best_ratio = 0

            for line in lines:
                ratio = difflib.SequenceMatcher(None, search_normalized, ' '.join(line.split())).ratio()
                if ratio > best_ratio and ratio >= threshold:
                    best_ratio = ratio
                    best_match = line

            return best_match
        else:
            # Multi-line search - find best matching block
            for i in range(len(lines) - len(search_lines) + 1):
                block = '\n'.join(lines[i:i + len(search_lines)])
                ratio = difflib.SequenceMatcher(None, search, block).ratio()
                if ratio >= threshold:
                    return block

        return None

    def _replace_function(self, content: str, func_name: str, new_content: str) -> Tuple[str, int]:
        """Replace an entire function by name."""
        # Pattern for Python function (handles async, decorators)
        pattern = rf'((?:@\w+.*?\n)*(?:async\s+)?def\s+{re.escape(func_name)}\s*\([^)]*\)[^:]*:.*?)(?=\n(?:@|\w|class\s|def\s|async\s+def\s|$)|\Z)'

        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValueError(f"Function '{func_name}' not found")

        new_content_str = content[:match.start()] + new_content + content[match.end():]
        return new_content_str, new_content.count('\n') + 1

    def _replace_class(self, content: str, class_name: str, new_content: str) -> Tuple[str, int]:
        """Replace an entire class by name."""
        # Pattern for Python class
        pattern = rf'(class\s+{re.escape(class_name)}\s*(?:\([^)]*\))?:.*?)(?=\nclass\s|\n(?![ \t])(?!\n)\S|\Z)'

        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValueError(f"Class '{class_name}' not found")

        new_content_str = content[:match.start()] + new_content + content[match.end():]
        return new_content_str, new_content.count('\n') + 1

    def _resolve_safe_path(self, path: str) -> Path:
        """Resolve path safely within workspace."""
        file_path = Path(path)

        # Check for path traversal
        if '..' in file_path.parts:
            raise ValueError(f"Path traversal not allowed: {path}")

        # Handle absolute paths
        if file_path.is_absolute():
            try:
                file_path = file_path.relative_to(self.workspace_root)
            except ValueError:
                raise ValueError(f"Path outside workspace: {path}")

        return self.workspace_root / file_path

    def _create_backup(self, file_path: Path, content: str) -> Optional[Path]:
        """Create a backup of the file before editing."""
        try:
            import time
            timestamp = int(time.time())
            backup_name = f"{file_path.name}.{timestamp}.bak"
            backup_path = self.backup_dir / backup_name
            backup_path.write_text(content, encoding='utf-8')
            return backup_path
        except Exception as e:
            self.logger.warning(f"Failed to create backup: {e}")
            return None

    def extract_and_apply(self, response_text: str) -> List[EditResult]:
        """
        Complete extraction and application pipeline.

        Args:
            response_text: Raw model response

        Returns:
            List of EditResult objects
        """
        edits = self.extract_edits(response_text)

        if not edits:
            self.logger.info("No surgical edits found in response")
            return []

        self.logger.info(f"Found {len(edits)} surgical edit(s)")
        results = self.apply_edits(edits)

        # Log summary
        successes = sum(1 for r in results if r.success)
        failures = len(results) - successes
        self.logger.info(f"Applied {successes}/{len(results)} edits ({failures} failed)")

        return results


def get_surgical_prompt_instructions() -> str:
    """
    Returns instructions to include in prompts so the model outputs surgical edits.

    Include this in your system prompt to get models to use the surgical format.
    """
    return """
OUTPUT FORMAT FOR CODE CHANGES:
Instead of outputting entire files, output ONLY the specific changes using this format:

For SEARCH/REPLACE (preferred for modifying existing code):
```
FILE: path/to/file.py
<<<<<<< SEARCH
exact code to find (copy from existing file)
=======
new code to replace it with
>>>>>>> REPLACE
```

For inserting new code after a specific line:
```xml
<patch path="path/to/file.py" action="insert_after" line="42">
new code to insert
</patch>
```

For appending to end of file:
```xml
<patch path="path/to/file.py" action="append">
new code to add at end
</patch>
```

For replacing an entire function:
```xml
<patch path="path/to/file.py" action="replace_function" target="function_name">
def function_name():
    # complete new implementation
</patch>
```

RULES:
1. NEVER output entire files - only output the specific changes
2. For SEARCH blocks, copy the EXACT text from the file (including whitespace)
3. Keep changes minimal and focused
4. One change per block - use multiple blocks for multiple changes
"""


if __name__ == "__main__":
    # Test the extractor
    logging.basicConfig(level=logging.INFO)

    extractor = SurgicalEditExtractor()

    # Test response with surgical edit
    test_response = '''
    Here's the fix for the bug:

    FILE: test_file.py
    <<<<<<< SEARCH
    def old_function():
        return "old"
    =======
    def old_function():
        return "fixed"
    >>>>>>> REPLACE

    And we need to add a new utility:

    <patch path="test_file.py" action="append">

    def new_helper():
        """Added by surgical edit."""
        return True
    </patch>
    '''

    edits = extractor.extract_edits(test_response)
    print(f"Found {len(edits)} edits:")
    for edit in edits:
        print(f"  - {edit.action.value} on {edit.path}")
