#!/usr/bin/env python3
"""
Lightweight repository security scan.

Goal: catch "unsafe-by-default" patterns before they reach main/master.

This is intentionally conservative and focuses on high-risk execution paths:
- Docker build instructions
- Shell scripts
- Python entrypoints / servers

It is NOT a substitute for a full SAST/secret scanner.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".checkpoints",
    ".grind_cache",
}

SCAN_SUFFIXES = {".sh", ".yml", ".yaml"}
# Focus on high-risk execution entrypoints (not docs/tests).
SCAN_FILENAMES = {
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}

BANNED = [
    (
        re.compile(r"curl\s+[^|]*\|\s*(bash|sh)\b", re.IGNORECASE),
        "piping curl output to a shell (`curl | bash`)",
    ),
    (
        re.compile(r"wget\s+[^|]*\|\s*(bash|sh)\b", re.IGNORECASE),
        "piping wget output to a shell (`wget | sh`)",
    ),
    (
        re.compile(r"deb\.nodesource\.com/setup_\d+\.x", re.IGNORECASE),
        "NodeSource `setup_*.x` installer (remote script execution)",
    ),
    (
        re.compile(r"npm\s+install\s+-g\s+@anthropic-ai/claude-code", re.IGNORECASE),
        "auto-installing `@anthropic-ai/claude-code` during builds",
    ),
]


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        # Skip directories by name anywhere in the path
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        # Skip tests and this scanner itself (tests may intentionally contain patterns)
        if "tests" in path.parts:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.name in SCAN_FILENAMES or path.suffix in SCAN_SUFFIXES:
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def main() -> int:
    findings: list[str] = []

    # Guardrail: remote execution modules should not exist at repo root
    for bad in ("remote_execution.py", "remote_execution_client.py", "remote_execution_relay.py", "remote_execution_protocol.py"):
        if (ROOT / bad).exists():
            findings.append(f"{bad}: remote execution module present at repo root")

    for file in iter_files(ROOT):
        text = read_text(file)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            # Ignore comment-only lines in common formats (Dockerfile, shell, yaml)
            if stripped.startswith("#"):
                continue
            for regex, desc in BANNED:
                if regex.search(line):
                    findings.append(f"{file.relative_to(ROOT)}:{i}: {desc}")

    if findings:
        sys.stderr.write("SECURITY SCAN FAILED:\n")
        for item in findings:
            sys.stderr.write(f" - {item}\n")
        return 1

    print("Security scan OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

