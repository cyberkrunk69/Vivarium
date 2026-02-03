#!/usr/bin/env python3
"""
Groq Artifact Extractor - Enhanced file extraction from Groq model responses.

Based on groq_artifact_design.md specification.
Extracts files from XML-style artifact tags and saves them safely to workspace.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError


@dataclass
class FileArtifact:
    """Represents a file artifact extracted from model response."""
    type: str
    path: str
    content: str
    encoding: str = "utf-8"
    is_binary: bool = False


class GroqArtifactExtractor:
    """
    Extracts and saves file artifacts from Groq model responses.

    Supports:
    - XML-style artifact tag parsing
    - Fallback code block extraction
    - Security validation and path safety
    - Multiple file encodings
    """

    def __init__(self, workspace_root: str = ".", max_file_size: int = 1024 * 1024):
        """
        Initialize the extractor.

        Args:
            workspace_root: Root directory for file operations
            max_file_size: Maximum allowed file size in bytes (default 1MB)
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.max_file_size = max_file_size
        self.logger = logging.getLogger(__name__)

        # Ensure workspace exists
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def extract_artifacts(self, response_text: str) -> List[FileArtifact]:
        """
        Extract file artifacts from response text.

        Args:
            response_text: Raw model response text

        Returns:
            List of FileArtifact objects
        """
        artifacts = []

        # Primary: Extract XML-style artifacts
        xml_artifacts = self._extract_xml_artifacts(response_text)
        artifacts.extend(xml_artifacts)

        # Fallback: Extract markdown code blocks if no artifacts found
        if not artifacts:
            code_artifacts = self._extract_code_blocks(response_text)
            artifacts.extend(code_artifacts)

        return artifacts

    def _extract_xml_artifacts(self, text: str) -> List[FileArtifact]:
        """Extract artifacts from XML-style <artifact> tags."""
        artifacts = []

        # Find all artifact tags with regex
        artifact_pattern = r'<artifact\s+([^>]*?)>(.*?)</artifact>'
        matches = re.findall(artifact_pattern, text, re.DOTALL | re.IGNORECASE)

        for attrs_str, content in matches:
            try:
                # Parse attributes
                attrs = self._parse_attributes(attrs_str)

                # Validate required attributes
                if 'path' not in attrs:
                    self.logger.warning("Artifact missing required 'path' attribute")
                    continue

                artifact = FileArtifact(
                    type=attrs.get('type', 'file'),
                    path=attrs['path'],
                    content=content.strip(),
                    encoding=attrs.get('encoding', 'utf-8')
                )

                artifacts.append(artifact)

            except Exception as e:
                self.logger.error(f"Failed to parse artifact: {e}")
                continue

        return artifacts

    def _extract_code_blocks(self, text: str) -> List[FileArtifact]:
        """Extract code blocks as fallback when no artifacts found."""
        artifacts = []

        # Pattern for markdown code blocks with language
        code_pattern = r'```(\w+)?\s*\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)

        for i, (language, content) in enumerate(matches):
            # Auto-generate filename based on language
            if language:
                ext = self._language_to_extension(language)
                filename = f"extracted_code_{i+1}.{ext}"
            else:
                filename = f"extracted_code_{i+1}.txt"

            artifact = FileArtifact(
                type='file',
                path=filename,
                content=content.strip(),
                encoding='utf-8'
            )

            artifacts.append(artifact)

        return artifacts

    def _parse_attributes(self, attrs_str: str) -> Dict[str, str]:
        """Parse XML-style attributes from string."""
        attrs = {}

        # Simple attribute parsing - handles quoted and unquoted values
        attr_pattern = r'(\w+)=(["\'])(.*?)\2|(\w+)=(\S+)'
        matches = re.findall(attr_pattern, attrs_str)

        for match in matches:
            if match[0]:  # Quoted value
                attrs[match[0]] = match[2]
            elif match[3]:  # Unquoted value
                attrs[match[3]] = match[4]

        return attrs

    def _language_to_extension(self, language: str) -> str:
        """Map programming language to file extension."""
        lang_map = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'yaml': 'yml',
            'yml': 'yml',
            'xml': 'xml',
            'sql': 'sql',
            'shell': 'sh',
            'bash': 'sh',
            'c': 'c',
            'cpp': 'cpp',
            'java': 'java',
            'go': 'go',
            'rust': 'rs',
            'php': 'php',
            'ruby': 'rb',
            'markdown': 'md',
            'md': 'md'
        }
        return lang_map.get(language.lower(), 'txt')

    def save_artifacts(self, artifacts: List[FileArtifact]) -> List[str]:
        """
        Save artifacts to filesystem.

        Args:
            artifacts: List of artifacts to save

        Returns:
            List of saved file paths
        """
        saved_files = []

        for artifact in artifacts:
            try:
                saved_path = self._save_artifact(artifact)
                if saved_path:
                    saved_files.append(saved_path)
            except Exception as e:
                self.logger.error(f"Failed to save artifact {artifact.path}: {e}")

        return saved_files

    def _save_artifact(self, artifact: FileArtifact) -> Optional[str]:
        """Save a single artifact to filesystem."""
        # Validate and sanitize path
        safe_path = self._validate_path(artifact.path)
        if not safe_path:
            return None

        # Validate content size
        content_size = len(artifact.content.encode(artifact.encoding))
        if content_size > self.max_file_size:
            self.logger.error(f"File {artifact.path} exceeds size limit ({content_size} > {self.max_file_size})")
            return None

        # Validate content safety
        if not self._validate_content_safety(artifact.content):
            self.logger.error(f"Content validation failed for {artifact.path}")
            return None

        full_path = self.workspace_root / safe_path

        try:
            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(full_path, 'w', encoding=artifact.encoding) as f:
                f.write(artifact.content)

            self.logger.info(f"Saved artifact: {full_path}")
            return str(safe_path)

        except Exception as e:
            self.logger.error(f"Failed to write file {full_path}: {e}")
            return None

    # HARD-CODED protected files that CANNOT be overwritten under any circumstances
    PROTECTED_FILES = {
        'grind_spawner.py',
        'grind_spawner_groq.py',
        'orchestrator.py',
        'roles.py',
        'safety_gateway.py',
        'safety_constitutional.py',
        'safety_network.py',
        'safety_sanitize.py',
        'safety_killswitch.py',
        'safety_sandbox.py',
        'cost_tracker.py',
        'knowledge_graph.py',
        'lesson_recorder.py',
        'memory_synthesis.py',
        'groq_client.py',
        'groq_code_extractor.py',
        'experiments_sandbox.py',
    }

    def _validate_path(self, path: str) -> Optional[Path]:
        """Validate and sanitize file path."""
        try:
            # Convert to Path and resolve
            file_path = Path(path)

            # HARD PROTECTION: Never allow writing to core system files
            filename = file_path.name.lower()
            for protected in self.PROTECTED_FILES:
                if filename == protected.lower() or filename.endswith(protected.lower()):
                    self.logger.error(f"BLOCKED: Attempt to write to protected file: {path}")
                    print(f"[SAFETY] BLOCKED write to protected file: {path}")
                    return None

            # Block any Python file in the root that matches protected patterns
            if file_path.suffix == '.py' and len(file_path.parts) == 1:
                # Check if it's an existing core file
                full_check = self.workspace_root / file_path
                if full_check.exists():
                    file_size = full_check.stat().st_size
                    # If existing file is large (>5KB), it's probably important - don't overwrite
                    if file_size > 5000:
                        self.logger.error(f"BLOCKED: Won't overwrite large existing Python file: {path} ({file_size} bytes)")
                        print(f"[SAFETY] BLOCKED overwrite of existing file: {path} ({file_size} bytes)")
                        return None

            # Check for path traversal attempts
            if '..' in file_path.parts:
                self.logger.error(f"Path traversal attempt detected: {path}")
                return None

            # Ensure path is relative
            if file_path.is_absolute():
                self.logger.error(f"Absolute path not allowed: {path}")
                return None

            # Check for dangerous characters
            dangerous_chars = ['<', '>', ':', '|', '?', '*']
            if any(char in str(file_path) for char in dangerous_chars):
                self.logger.error(f"Dangerous characters in path: {path}")
                return None

            return file_path

        except Exception as e:
            self.logger.error(f"Path validation failed for {path}: {e}")
            return None

    def _validate_content_safety(self, content: str) -> bool:
        """Basic content safety validation."""
        # Check for extremely suspicious patterns
        suspicious_patterns = [
            r'rm\s+-rf\s+/',  # Dangerous shell commands
            r'del\s+/[sq]',   # Windows delete commands
            r'format\s+c:',   # Format commands
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return False

        return True

    def extract_and_save(self, response_text: str) -> List[str]:
        """
        Complete extraction and save pipeline.

        Args:
            response_text: Raw model response

        Returns:
            List of saved file paths
        """
        artifacts = self.extract_artifacts(response_text)
        saved_files = self.save_artifacts(artifacts)

        self.logger.info(f"Extracted and saved {len(saved_files)} files from response")
        return saved_files

    def get_extraction_stats(self, response_text: str) -> Dict[str, Any]:
        """Get statistics about extraction process."""
        artifacts = self.extract_artifacts(response_text)

        stats = {
            'total_artifacts': len(artifacts),
            'file_types': {},
            'total_size': 0,
            'paths': []
        }

        for artifact in artifacts:
            # Count file types
            ext = Path(artifact.path).suffix.lower()
            stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1

            # Sum content sizes
            stats['total_size'] += len(artifact.content.encode(artifact.encoding))

            # Collect paths
            stats['paths'].append(artifact.path)

        return stats


def test_extractor():
    """Simple test function for the extractor."""
    extractor = GroqArtifactExtractor()

    # Test XML artifact extraction
    test_response = '''
    Here's a simple Python script:

    <artifact type="file" path="test_script.py" encoding="utf-8">
#!/usr/bin/env python3

def hello():
    print("Hello from extracted artifact!")

if __name__ == "__main__":
    hello()
    </artifact>

    And here's a config file:

    <artifact type="file" path="config/settings.json">
{
    "app_name": "Test App",
    "version": "1.0.0",
    "debug": true
}
    </artifact>
    '''

    saved_files = extractor.extract_and_save(test_response)
    print(f"Test completed. Saved files: {saved_files}")

    # Test code block extraction (fallback)
    test_code_block = '''
    Here's some JavaScript code:

    ```javascript
    function greet(name) {
        console.log(`Hello, ${name}!`);
    }

    greet("World");
    ```
    '''

    saved_files = extractor.extract_and_save(test_code_block)
    print(f"Code block test completed. Saved files: {saved_files}")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    test_extractor()