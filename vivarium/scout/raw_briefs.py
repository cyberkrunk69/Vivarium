"""
Raw brief capture for calibration data (TICKET-8).

Stores unparsed 70B outputs to ~/.scout/raw_briefs/{timestamp}.md.
Sanitizes absolute paths to prevent PII leakage.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# Absolute path patterns that may leak PII (user home, system paths)
_ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"/Users/[^\s\]\)\"']+", re.IGNORECASE),
    re.compile(r"/home/[^\s\]\)\"']+", re.IGNORECASE),
    re.compile(r"~/[^\s\]\)\"']+"),
    re.compile(r"[A-Za-z]:\\[^\s\]\)\"']+"),  # Windows C:\...
    re.compile(r"/tmp/[^\s\]\)\"']+", re.IGNORECASE),
    re.compile(r"/var/[^\s\]\)\"']+", re.IGNORECASE),
]

RAW_BRIEFS_DIR = Path("~/.scout/raw_briefs").expanduser()
REDACTED_PLACEHOLDER = "[PATH_REDACTED]"


def sanitize_for_pii(raw: str) -> Tuple[str, bool]:
    """
    Redact absolute paths to prevent PII leakage.
    Returns (sanitized_content, had_absolute_paths).
    """
    had_absolute = False
    result = raw
    for pattern in _ABSOLUTE_PATH_PATTERNS:
        matches = pattern.findall(result)
        if matches:
            had_absolute = True
        result = pattern.sub(REDACTED_PLACEHOLDER, result)
    return result, had_absolute


def store_raw_brief(raw: str) -> Optional[Path]:
    """
    Store raw 70B output to ~/.scout/raw_briefs/{timestamp}.md.
    Sanitizes for PII. Returns path if stored, None on error.
    """
    if not raw or not raw.strip():
        return None

    sanitized, _ = sanitize_for_pii(raw)
    RAW_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    # Ensure uniqueness with microseconds if needed
    path = RAW_BRIEFS_DIR / f"{ts}.md"
    if path.exists():
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S.%f")[:-3]
        path = RAW_BRIEFS_DIR / f"{ts}.md"

    try:
        path.write_text(sanitized, encoding="utf-8")
        return path
    except OSError:
        return None


def list_raw_briefs(limit: int = 100) -> list[Path]:
    """List raw brief files for analysis. Returns paths sorted by mtime (newest first)."""
    if not RAW_BRIEFS_DIR.exists():
        return []
    paths = sorted(
        RAW_BRIEFS_DIR.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return paths[:limit]
