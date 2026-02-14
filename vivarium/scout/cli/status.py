"""
Scout status CLI — Dashboard for dev workflow.

Shows: last doc-sync time, missing drafts, hourly spend, accuracy, git hook status.
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional

from vivarium.scout.audit import AuditLog
from vivarium.scout.deps import DependencyGraph
from vivarium.scout.git_analyzer import get_changed_files
from vivarium.scout.ignore import IgnorePatterns


def _last_doc_sync_time(repo_root: Path, py_files: List[Path]) -> List[tuple[Path, Optional[float]]]:
    """Return (file, mtime) for each .py file's .docs/*.tldr.md or .deep.md. mtime=None if missing."""
    result: List[tuple[Path, Optional[float]]] = []
    for f in py_files:
        docs_dir = f.parent / ".docs"
        latest: Optional[float] = None
        for suffix in (".tldr.md", ".deep.md"):
            doc_path = docs_dir / f"{f.name}{suffix}"
            if doc_path.exists():
                try:
                    m = doc_path.stat().st_mtime
                    if latest is None or m > latest:
                        latest = m
                except OSError:
                    pass
        result.append((f, latest))
    return result


def _missing_drafts(repo_root: Path, staged_py: List[Path]) -> List[Path]:
    """Return staged .py files that don't have docs/drafts/{stem}.commit.txt."""
    draft_dir = repo_root / "docs" / "drafts"
    missing: List[Path] = []
    for f in staged_py:
        stem = f.stem
        draft_path = draft_dir / f"{stem}.commit.txt"
        if not draft_path.exists():
            missing.append(f)
    return missing


def _git_hook_status(repo_root: Path) -> dict[str, bool]:
    """Check if prepare-commit-msg and post-commit hooks are installed."""
    hooks_dir = repo_root / ".git" / "hooks"
    return {
        "prepare-commit-msg": (hooks_dir / "prepare-commit-msg").exists(),
        "post-commit": (hooks_dir / "post-commit").exists(),
    }


def run_status(repo_root: Path) -> str:
    """Generate status output (git status style)."""
    lines: List[str] = []
    root = Path(repo_root).resolve()

    # Staged files
    staged = get_changed_files(staged_only=True, repo_root=root)
    staged_py = [f for f in staged if f.suffix == ".py"]
    ignore = IgnorePatterns(repo_root=root)
    staged_py = [f for f in staged_py if not ignore.matches(f, root)]

    # Last doc-sync
    lines.append("Doc-sync status (last .tldr.md/.deep.md mtime):")
    if staged_py:
        sync_times = _last_doc_sync_time(root, staged_py)
        for f, mtime in sync_times:
            try:
                rel = f.relative_to(root)
            except ValueError:
                rel = f
            if mtime is None:
                lines.append(f"  ?? {rel}  (no docs)")
            else:
                dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
                lines.append(f"  ok {rel}  ({dt.strftime('%Y-%m-%d %H:%M')})")
    else:
        lines.append("  (no staged .py files)")
    lines.append("")

    # Dependency graph health
    graph = DependencyGraph(root)
    stats = graph.get_stats()
    if graph.is_graph_stale():
        lines.append("⚠️  Dependency graph stale — run scout-index")
    else:
        lines.append(
            f"Dependency Graph: {stats['total']:,} symbols | "
            f"{stats['stale']} stale | {stats['orphaned']} orphaned | "
            f"{stats['cache_version']} cache"
        )
    lines.append("")

    # Missing drafts
    lines.append("Missing commit drafts (docs/drafts/*.commit.txt):")
    missing = _missing_drafts(root, staged_py)
    if missing:
        for f in missing:
            try:
                rel = f.relative_to(root)
            except ValueError:
                rel = f
            lines.append(f"  !! {rel}")
    else:
        lines.append("  (none)")
    lines.append("")

    # Audit: hourly spend
    audit = AuditLog()
    spend = audit.hourly_spend(hours=1)
    lines.append(f"Hourly LLM spend: ${spend:.4f}")
    lines.append("")

    # Gate health (TICKET-10)
    gate = audit.gate_metrics(last_n=10)
    if gate["total"] > 0:
        lines.append(
            f"Gate Health: {gate['pass_rate_pct']}% pass rate | "
            f"{gate['avg_confidence']} avg confidence | "
            f"{gate['escalate_rate_pct']}% escalate to raw"
        )
        last = gate["last_queries"]
        pass_last = sum(1 for q in last if q["outcome"] == "pass")
        esc_last = sum(1 for q in last if q["outcome"] == "escalate")
        reasons = [q["reason"] for q in last if q["outcome"] == "escalate" and q["reason"]]
        reason_str = ", ".join(f"{r}: {c}" for r, c in sorted(Counter(reasons).items()))
        lines.append(
            f"Last {len(last)} queries: {pass_last} pass, {esc_last} escalate"
            + (f" ({reason_str})" if reason_str else "")
        )
    else:
        lines.append("Gate Health: (no gate_compress events yet)")
    lines.append("")

    # Accuracy
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    metrics = audit.accuracy_metrics(since=since)
    lines.append("Accuracy (last 24h):")
    lines.append(
        f"  nav: {metrics['total_nav']}, fails: {metrics['validation_fail_count']}, "
        f"accuracy: {metrics['accuracy_pct']}%"
    )
    lines.append("")

    # Git hooks
    hooks = _git_hook_status(root)
    lines.append("Git hooks:")
    for name, installed in hooks.items():
        status = "ok" if installed else "??"
        lines.append(f"  {status} {name}")
    audit.close()

    return "\n".join(lines)


def main() -> int:
    """CLI entry point."""
    repo_root = Path.cwd().resolve()
    output = run_status(repo_root)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
