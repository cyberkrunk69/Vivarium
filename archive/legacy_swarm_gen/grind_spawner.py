"""
Compatibility shim for legacy imports.

Historical code and a few test/utility scripts import `grind_spawner`.
The current UI launches `grind_spawner_unified.py`; this module keeps the
old import path working by:
- Re-exporting `verify_grind_completion`
- Delegating `main()` to `grind_spawner_unified.main()`
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from legacy_swarm_gen import grind_spawner_unified
except ImportError:  # pragma: no cover - direct script execution fallback
    import grind_spawner_unified  # type: ignore[no-redef]


_FILE_CLAIM_PATTERNS = [
    # "dashboard.html:1-544"
    re.compile(r"(?P<file>[A-Za-z0-9_./-]+\.[A-Za-z0-9]+):\d+(?:-\d+)?"),
    # "- dashboard.html"
    re.compile(r"[-*]\s+(?P<file>[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)\b"),
]


def _extract_claimed_files(output: str) -> List[str]:
    claimed: List[str] = []

    # Primary: JSON output with files_modified
    try:
        data = json.loads(output or "{}")
        if isinstance(data, dict):
            files = data.get("files_modified")
            if isinstance(files, list):
                for f in files:
                    if isinstance(f, str) and f.strip():
                        claimed.append(f.strip())
    except Exception:
        pass

    # Secondary: pattern extraction from text claims
    if not claimed:
        text = output or ""
        for pat in _FILE_CLAIM_PATTERNS:
            for m in pat.finditer(text):
                f = m.group("file")
                if f and f not in claimed:
                    claimed.append(f)

    return claimed


def verify_grind_completion(
    session_id: int,
    run_num: int,
    output: str,
    returncode: int,
    workspace: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Verify that a grind run actually changed the files it claimed.

    This is intentionally lightweight and filesystem-based:
    - Extract `claimed_files` from output (JSON `files_modified` or text patterns)
    - Check existence of those files on disk

    Returns a dict consumed by legacy scripts/tests.
    """
    ws = (workspace or Path.cwd()).resolve()
    claimed_files = _extract_claimed_files(output or "")

    verified_files: List[str] = []
    for f in claimed_files:
        # Normalize to workspace-relative paths when possible
        p = Path(f)
        candidate = (ws / p) if not p.is_absolute() else p
        if candidate.exists():
            verified_files.append(str(p))

    hallucination_detected = False
    verification_status = "UNKNOWN"
    verified = False

    if returncode != 0:
        verification_status = "FAILED"
        verified = False
    elif claimed_files and not verified_files:
        hallucination_detected = True
        verification_status = "HALLUCINATION"
        verified = False
    elif claimed_files and verified_files:
        verification_status = "VERIFIED"
        verified = True
    else:
        # No explicit file claims. Consider successful exit as verified.
        verification_status = "VERIFIED"
        verified = True

    details = (
        f"session={session_id} run={run_num} returncode={returncode} "
        f"claimed={len(claimed_files)} verified={len(verified_files)}"
    )

    return {
        "verified": verified,
        "verification_status": verification_status,
        "hallucination_detected": hallucination_detected,
        "claimed_files": claimed_files,
        "verified_files": verified_files,
        "details": details,
    }


def main(argv: Optional[List[str]] = None) -> int:
    """Delegate to `grind_spawner_unified.main()`."""
    return grind_spawner_unified.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())

