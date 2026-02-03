"""Utils module for Reflexion episodic memory and shared utilities."""

import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime, timezone


def read_json(path: Path) -> Dict[str, Any]:
    """Read and parse a JSON file with error handling."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    """Write data to a JSON file with proper formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_timestamp() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_error(exception: Exception) -> str:
    """Format an exception into a user-friendly error message."""
    exc_type = type(exception).__name__
    exc_msg = str(exception)
    return f"{exc_type}: {exc_msg}" if exc_msg else exc_type
