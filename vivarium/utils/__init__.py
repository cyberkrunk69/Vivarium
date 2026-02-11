"""Utils module for Reflexion episodic memory and shared utilities."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timezone


def read_json(path: Path, *, default: Any = None) -> Any:
    """Read and parse a JSON file. Raises if missing unless default provided."""
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(f"JSON file does not exist: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    """Write data to a JSON file with proper formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_jsonl(path: Path, *, default: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    """Read a JSONL file into a list. Raises on parse errors unless default provided."""
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(f"JSONL file does not exist: {path}")
    records: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSONL at {path}:{line_num}: {e}") from e
    return records


def append_jsonl(path: Path, record: Dict[str, Any]) -> None:
    """Append a record to a JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


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
