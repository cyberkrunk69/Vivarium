"""
Safety Sandbox: Workspace isolation and file operation validation
Implements defense-in-depth for agent file operations.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class WorkspaceSandbox:
    """
    Validates file operations to prevent unauthorized access.
    Logs all operations for audit trail.
    """

    # Sensitive patterns to block
    SENSITIVE_PATTERNS = [
        '.env',
        'credentials',
        'secrets',
        'private_key',
        'id_rsa',
        'config.json',
        'password',
        'token',
        'api_key'
    ]

    # System directories to block (Windows + Unix)
    SYSTEM_DIRS = [
        'C:\\Windows',
        'C:\\Program Files',
        'C:\\Program Files (x86)',
        '/etc',
        '/bin',
        '/sbin',
        '/usr/bin',
        '/usr/sbin',
        '/sys',
        '/proc',
        '/root',
        '/boot'
    ]

    def __init__(self, workspace_root: str):
        """
        Initialize sandbox with workspace root.

        Args:
            workspace_root: Absolute path to workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.audit_log: List[Dict] = []

        # Ensure workspace exists
        if not self.workspace_root.exists():
            raise ValueError(f"Workspace root does not exist: {self.workspace_root}")

    def is_path_allowed(self, path: str) -> bool:
        """
        Check if a file path is allowed for operations.

        Args:
            path: File path to validate

        Returns:
            True if path is allowed, False otherwise
        """
        try:
            # Resolve to absolute path
            abs_path = Path(path).resolve()

            # Check 1: Must be within workspace
            try:
                abs_path.relative_to(self.workspace_root)
            except ValueError:
                self._log_blocked(path, "outside_workspace")
                return False

            # Check 2: Not a sensitive file
            path_lower = str(abs_path).lower()
            for pattern in self.SENSITIVE_PATTERNS:
                if pattern in path_lower:
                    self._log_blocked(path, f"sensitive_pattern:{pattern}")
                    return False

            # Check 3: Not in system directory
            for sys_dir in self.SYSTEM_DIRS:
                sys_dir_path = Path(sys_dir)
                try:
                    abs_path.relative_to(sys_dir_path)
                    self._log_blocked(path, f"system_directory:{sys_dir}")
                    return False
                except (ValueError, OSError):
                    # Not under this system dir, continue checking
                    pass

            # Path is allowed
            return True

        except Exception as e:
            # If we can't resolve or validate, block it
            self._log_blocked(path, f"validation_error:{str(e)}")
            return False

    def log_operation(self, operation: str, path: str, success: bool, details: Optional[str] = None):
        """
        Log a file operation for audit trail.

        Args:
            operation: Type of operation (read, write, delete, etc.)
            path: File path
            success: Whether operation succeeded
            details: Optional additional details
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "path": path,
            "success": success,
            "details": details
        }
        self.audit_log.append(entry)

    def _log_blocked(self, path: str, reason: str):
        """Log a blocked operation."""
        self.log_operation("BLOCKED", path, False, reason)

    def get_audit_log(self) -> List[Dict]:
        """
        Get the complete audit log.

        Returns:
            List of audit log entries
        """
        return self.audit_log.copy()

    def save_audit_log(self, output_path: Optional[str] = None):
        """
        Save audit log to file.

        Args:
            output_path: Where to save log (defaults to workspace_root/safety_audit.log)
        """
        if output_path is None:
            output_path = self.workspace_root / "safety_audit.log"
        else:
            output_path = Path(output_path)

        with open(output_path, 'w') as f:
            json.dump(self.audit_log, f, indent=2)

    def validate_write(self, path: str) -> bool:
        """
        Validate a write operation before executing.

        Args:
            path: Path to write to

        Returns:
            True if write is allowed, False otherwise
        """
        if not self.is_path_allowed(path):
            return False

        self.log_operation("write_validated", path, True)
        return True

    def validate_read(self, path: str) -> bool:
        """
        Validate a read operation before executing.

        Args:
            path: Path to read from

        Returns:
            True if read is allowed, False otherwise
        """
        if not self.is_path_allowed(path):
            return False

        self.log_operation("read_validated", path, True)
        return True

    def validate_delete(self, path: str) -> bool:
        """
        Validate a delete operation before executing.

        Args:
            path: Path to delete

        Returns:
            True if delete is allowed, False otherwise
        """
        if not self.is_path_allowed(path):
            return False

        # Extra caution for deletes
        abs_path = Path(path).resolve()
        if abs_path == self.workspace_root:
            self._log_blocked(path, "cannot_delete_workspace_root")
            return False

        self.log_operation("delete_validated", path, True)
        return True


# Global sandbox instance (initialized by orchestrator)
_global_sandbox: Optional[WorkspaceSandbox] = None

def initialize_sandbox(workspace_root: str):
    """Initialize the global sandbox instance."""
    global _global_sandbox
    _global_sandbox = WorkspaceSandbox(workspace_root)


# Backwards-compatible alias
def init_sandbox(workspace_root: str):
    """Alias for initialize_sandbox."""
    initialize_sandbox(workspace_root)

def get_sandbox() -> Optional[WorkspaceSandbox]:
    """Get the global sandbox instance."""
    return _global_sandbox

def safe_write(path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    Safe file write with sandbox validation.

    Args:
        path: File path to write
        content: Content to write
        encoding: File encoding

    Returns:
        True if write succeeded, False if blocked
    """
    sandbox = get_sandbox()
    if sandbox is None:
        raise RuntimeError("Sandbox not initialized; refusing unsafe write")

    if not sandbox.validate_write(path):
        print(f"BLOCKED: Write to {path} blocked by sandbox")
        return False

    try:
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        sandbox.log_operation("write", path, True)
        return True
    except Exception as e:
        sandbox.log_operation("write", path, False, str(e))
        raise

def safe_read(path: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Safe file read with sandbox validation.

    Args:
        path: File path to read
        encoding: File encoding

    Returns:
        File contents if allowed, None if blocked
    """
    sandbox = get_sandbox()
    if sandbox is None:
        raise RuntimeError("Sandbox not initialized; refusing unsafe read")

    if not sandbox.validate_read(path):
        print(f"BLOCKED: Read from {path} blocked by sandbox")
        return None

    try:
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        sandbox.log_operation("read", path, True)
        return content
    except Exception as e:
        sandbox.log_operation("read", path, False, str(e))
        raise
