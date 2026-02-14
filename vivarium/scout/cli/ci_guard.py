"""
Scout CI guard — Validate docs coverage, draft confidence, and spend limits.

No LLM calls. Exits 0 if all pass, 1 + error message if any fail.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from vivarium.scout.audit import AuditLog
from vivarium.scout.doc_generation import validate_content_for_placeholders
from vivarium.scout.git_analyzer import get_changed_files
from vivarium.scout.ignore import IgnorePatterns

DEFAULT_BASE_BRANCH = "origin/main"
DEFAULT_HOURLY_SPEND_LIMIT = 5.0
DEFAULT_MIN_CONFIDENCE = 0.7


def _check_tldr_coverage(
    repo_root: Path,
    changed_py: List[Path],
    ignore: IgnorePatterns,
) -> Tuple[bool, List[str]]:
    """Check all .py files have .tldr.md unless ignored. Returns (ok, errors)."""
    errors: List[str] = []
    for f in changed_py:
        if ignore.matches(f, repo_root):
            continue
        docs_dir = f.parent / ".docs"
        tldr_path = docs_dir / f"{f.name}.tldr.md"
        if not tldr_path.exists():
            try:
                rel = f.relative_to(repo_root)
            except ValueError:
                rel = f
            errors.append(f"Missing .tldr.md for {rel}")
    return (len(errors) == 0, errors)


def _check_draft_confidence(
    audit: AuditLog,
    min_confidence: float,
    hours: int = 24,
) -> Tuple[bool, List[str]]:
    """Check no draft/nav events (last N hours) have confidence < min_confidence."""
    errors: List[str] = []
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    events = audit.query(since=since)
    for obj in events:
        event = obj.get("event")
        if event not in ("nav", "commit_draft", "pr_snippet"):
            continue
        conf = obj.get("confidence")
        if conf is None:
            continue
        conf_val = conf / 100.0 if isinstance(conf, (int, float)) and conf > 1 else conf
        if isinstance(conf_val, (int, float)) and conf_val < min_confidence:
            errors.append(
                f"Audit event {event} has confidence {conf_val} < {min_confidence}"
            )
    return (len(errors) == 0, errors)


def _check_hourly_spend(
    audit: AuditLog,
    limit: float,
) -> Tuple[bool, List[str]]:
    """Check hourly spend < limit. Returns (ok, errors)."""
    spend = audit.hourly_spend(hours=1)
    if spend >= limit:
        return (False, [f"Hourly spend ${spend:.2f} >= limit ${limit:.2f}"])
    return (True, [])


def _check_no_placeholders(
    repo_root: Path,
    target: Path,
) -> Tuple[bool, List[str]]:
    """Check no generated docs contain [FALLBACK]/[GAP]/[PLACEHOLDER]. Returns (ok, errors)."""
    errors: List[str] = []
    all_clean, violations = validate_content_for_placeholders(target, recursive=True)
    if not all_clean:
        for filepath, markers in violations:
            errors.append(f"Placeholder {markers} in {filepath}")
    return (len(errors) == 0, errors)


def _check_draft_events_recent(
    audit: AuditLog,
    hours: int = 24,
) -> Tuple[bool, List[str]]:
    """Check audit has commit_draft events in last N hours (draft system health)."""
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    events = audit.query(since=since)
    has_commit_draft = any(e.get("event") == "commit_draft" for e in events)
    if not has_commit_draft:
        return (False, [f"No commit_draft events in last {hours}h — draft system may be broken"])
    return (True, [])


def run_ci_guard(
    repo_root: Path,
    base_branch: str = DEFAULT_BASE_BRANCH,
    hourly_limit: float = DEFAULT_HOURLY_SPEND_LIMIT,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    require_draft_events: bool = False,
    draft_events_hours: int = 24,
    check_placeholders: bool = True,
    placeholders_target: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """
    Run all CI checks. Returns (all_passed, list of error messages).

    When require_draft_events=True, fails if no commit_draft events in audit
    (last N hours). Use to guard against draft system regressions.
    """
    root = Path(repo_root).resolve()
    errors: List[str] = []

    changed: List[Path] = []
    try:
        changed = get_changed_files(
            staged_only=False,
            repo_root=root,
            base_branch=base_branch,
        )
    except Exception:
        try:
            changed = get_changed_files(staged_only=False, repo_root=root)
        except Exception as e:
            return (False, [f"Could not get changed files: {e}"])

    changed_py = [f for f in changed if f.suffix == ".py"]
    ignore = IgnorePatterns(repo_root=root)

    ok, errs = _check_tldr_coverage(root, changed_py, ignore)
    if not ok:
        errors.extend(errs)

    audit = AuditLog()
    ok, errs = _check_draft_confidence(audit, min_confidence)
    if not ok:
        errors.extend(errs)

    ok, errs = _check_hourly_spend(audit, hourly_limit)
    if not ok:
        errors.extend(errs)

    if require_draft_events:
        ok, errs = _check_draft_events_recent(audit, hours=draft_events_hours)
        if not ok:
            errors.extend(errs)

    if check_placeholders:
        target = placeholders_target or root / "vivarium"
        if target.exists():
            ok, errs = _check_no_placeholders(root, target)
            if not ok:
                errors.extend(errs)

    audit.close()
    return (len(errors) == 0, errors)


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="scout-ci-guard",
        description="CI validation: .tldr.md coverage, draft confidence, hourly spend.",
    )
    parser.add_argument(
        "--base-branch",
        default=DEFAULT_BASE_BRANCH,
        help=f"Base branch for diff (default: {DEFAULT_BASE_BRANCH})",
    )
    parser.add_argument(
        "--hourly-limit",
        type=float,
        default=DEFAULT_HOURLY_SPEND_LIMIT,
        help=f"Max hourly spend in USD (default: {DEFAULT_HOURLY_SPEND_LIMIT})",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=DEFAULT_MIN_CONFIDENCE,
        help=f"Min confidence for drafts (0-1, default: {DEFAULT_MIN_CONFIDENCE})",
    )
    parser.add_argument(
        "--require-draft-events",
        action="store_true",
        help="Fail if no commit_draft events in audit (last 24h). Use to guard draft system.",
    )
    parser.add_argument(
        "--draft-events-hours",
        type=int,
        default=24,
        help="Hours to look back for commit_draft events (default: 24)",
    )
    parser.add_argument(
        "--no-placeholders-check",
        action="store_true",
        dest="no_placeholders_check",
        help="Skip check for [FALLBACK]/[GAP]/[PLACEHOLDER] in generated docs",
    )
    parser.add_argument(
        "--placeholders-target",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to scan for placeholders (default: vivarium)",
    )
    args = parser.parse_args()

    ok, errors = run_ci_guard(
        repo_root=Path.cwd().resolve(),
        base_branch=args.base_branch,
        hourly_limit=args.hourly_limit,
        min_confidence=args.min_confidence,
        require_draft_events=args.require_draft_events,
        draft_events_hours=args.draft_events_hours,
        check_placeholders=not getattr(args, "no_placeholders_check", False),
        placeholders_target=getattr(args, "placeholders_target", None),
    )

    if not ok:
        for e in errors:
            print(f"scout-ci-guard: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
