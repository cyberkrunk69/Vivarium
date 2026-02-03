"""
Shared utilities module for Black Swarm codebase.

Provides reusable functions for:
- JSON file operations (read/write)
- Timestamp handling
- Directory management
- Error formatting
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Import sandbox for file operation validation
try:
    from safety_sandbox import get_sandbox
    get_global_sandbox = get_sandbox
except ImportError:
    # Sandbox not available, continue without validation
    get_global_sandbox = lambda: None


def read_json(path: Path) -> Dict[str, Any]:
    """
    Read and parse a JSON file with error handling.

    Args:
        path: Path to the JSON file to read.

    Returns:
        dict: Parsed JSON content, or empty dict if file doesn't exist.

    Raises:
        json.JSONDecodeError: If file exists but contains invalid JSON.

    Example:
        data = read_json(Path("queue.json"))
        tasks = data.get("tasks", [])
    """
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def write_json(path: Path, data: Dict[str, Any]) -> None:
    """
    Write data to a JSON file with proper formatting.

    Creates parent directories if they don't exist. Writes with 2-space
    indentation for readability.

    Args:
        path: Path where JSON file should be written.
        data: Dictionary to serialize as JSON.

    Raises:
        PermissionError: If sandbox validation fails (path outside workspace or sensitive location).

    Example:
        write_json(Path("queue.json"), {"tasks": [], "completed": []})
    """
    # Validate write operation through sandbox if available
    sandbox = get_global_sandbox()
    if sandbox is not None:
        if not sandbox.is_path_allowed(str(path)):
            sandbox.log_operation("write", str(path), False, "blocked_by_sandbox")
            raise PermissionError(f"Sandbox blocked write to: {path}")
        sandbox.log_operation("write", str(path), True, "write_json")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_timestamp() -> str:
    """
    Get current UTC timestamp in ISO format.

    Returns:
        str: ISO 8601 formatted timestamp (e.g., '2024-01-15T10:30:00+00:00')

    Example:
        timestamp = get_timestamp()
        print(f"Task started at {timestamp}")
    """
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> Path:
    """
    Create directory if it doesn't exist.

    Creates all parent directories as needed. Safe to call multiple times.

    Args:
        path: Directory path to ensure exists.

    Returns:
        Path: The path that was created or already exists.

    Example:
        locks_dir = ensure_dir(Path("task_locks"))
        lock_file = locks_dir / "task_001.lock"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_error(exception: Exception) -> str:
    """
    Format an exception into a user-friendly error message.

    Extracts the exception type and message without internal Python details.

    Args:
        exception: The exception to format.

    Returns:
        str: Human-readable error message (e.g., "ConnectError: Cannot reach host")

    Example:
        try:
            make_api_call()
        except Exception as e:
            error_msg = format_error(e)
            log_entry["errors"] = error_msg
    """
    exc_type = type(exception).__name__
    exc_msg = str(exception)
    return f"{exc_type}: {exc_msg}" if exc_msg else exc_type
