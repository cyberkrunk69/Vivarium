#!/usr/bin/env python3
"""
commit-message-lib.py — Analyze staged diff and generate conventional commit message.
Reads diff from stdin, receives branch-status path as arg, outputs commit message to stdout.
"""

import re
import sys
from pathlib import Path


# Conventional commit types and patterns to detect them
FIX_KEYWORDS = frozenset([
    "fix", "bug", "error", "fail", "crash", "broken", "incorrect", "wrong",
    "resolve", "repair", "patch", "address", "prevent", "avoid"
])
FEAT_KEYWORDS = frozenset([
    "add", "new", "implement", "create", "introduce", "support", "enable",
    "feature", "feat", "allow", "provide"
])
DOCS_KEYWORDS = frozenset([
    "doc", "readme", "comment", "document", "changelog", "license"
])
STYLE_KEYWORDS = frozenset([
    "format", "style", "whitespace", "indent", "lint", "trim"
])
REFACTOR_KEYWORDS = frozenset([
    "refactor", "extract", "simplify", "reorganize", "restructure", "rename",
    "move", "clean", "consolidate"
])
TEST_KEYWORDS = frozenset([
    "test", "spec", "mock", "fixture", "coverage", "pytest", "unittest"
])
CHORE_KEYWORDS = frozenset([
    "chore", "config", "ci", "build", "deps", "dependency", "version",
    "ignore", "gitignore", "upgrade"
])
# Breaking change: only flag when explicitly stated (avoids false positives from code)


def infer_scope_from_paths(paths: list[str]) -> str:
    """Infer scope from changed file paths (e.g., 'runtime', 'devtools', 'ci')."""
    top_dirs = {}
    for p in paths:
        parts = p.split("/")
        if len(parts) >= 2:
            top = parts[0]
        elif len(parts) == 1:
            top = Path(p).stem if "." in p else p
        else:
            continue
        top_dirs[top] = top_dirs.get(top, 0) + 1

    if not top_dirs:
        return ""

    # Prefer src dirs over config
    for preferred in ("vivarium", "src", "tests"):
        if preferred in top_dirs:
            # If vivarium, subdir like runtime/meta is more specific
            subdirs = {}
            for p in paths:
                if p.startswith(preferred + "/") and "/" in p[len(preferred) + 1:]:
                    sub = p.split("/")[1]
                    subdirs[sub] = subdirs.get(sub, 0) + 1
            if subdirs:
                return max(subdirs, key=subdirs.get)
            return preferred

    return max(top_dirs, key=top_dirs.get)


def categorize_from_content(diff_text: str, paths: list[str]) -> tuple[str, str, bool]:
    """
    Analyze diff content and paths to infer type, summary, and breaking-change.
    Returns (type, summary, is_breaking).
    """
    text_lower = diff_text.lower()
    combined = " ".join(paths) + " " + text_lower

    # Only flag breaking when explicit intent; skip when diff contains our own template
    is_own_tool = any("commit-message" in p for p in paths)
    is_breaking = False
    if not is_own_tool:
        is_breaking = "breaking change" in text_lower or "breaking:" in text_lower

    # Check path-based hints first
    path_str = " ".join(paths).lower()
    if any(p.startswith("test") or "test_" in p or "_test." in p for p in paths):
        if not any(kw in text_lower for kw in FIX_KEYWORDS):
            return ("test", "add or update tests", is_breaking)
    if any("doc" in p or "readme" in p or "md" in p for p in paths) and not any(
        p.startswith("vivarium") or p.startswith("src") for p in paths
    ):
        if all("doc" in p or "readme" in p or "md" in p for p in paths):
            return ("docs", "update documentation", is_breaking)
    if any(".github" in p or "ci" in p or "workflow" in p for p in paths):
        if all(
            ".github" in p or "ci" in p or "workflow" in p or "lint" in p
            for p in paths
        ):
            return ("ci", "update CI configuration", is_breaking)

    # Path-based: devtools changes are usually chore/feat
    if all("devtools" in p for p in paths):
        scope = infer_scope_from_paths(paths)
        summary = _summarize_diff(diff_text, paths)
        if any(kw in combined for kw in FEAT_KEYWORDS):
            return ("feat", summary or "add devtools utility", is_breaking)
        return ("chore", summary or f"update {scope}", is_breaking)

    # Content-based
    for kw_set, ctype in [
        (FIX_KEYWORDS, "fix"),
        (FEAT_KEYWORDS, "feat"),
        (DOCS_KEYWORDS, "docs"),
        (STYLE_KEYWORDS, "style"),
        (REFACTOR_KEYWORDS, "refactor"),
        (TEST_KEYWORDS, "test"),
        (CHORE_KEYWORDS, "chore"),
    ]:
        if any(kw in combined for kw in kw_set):
            summary = _summarize_diff(diff_text, paths)
            return (ctype, summary, is_breaking)

    # Default from path structure
    scope = infer_scope_from_paths(paths)
    if scope:
        return ("chore", f"update {scope}", is_breaking)
    return ("chore", "miscellaneous changes", is_breaking)


def _summarize_diff(diff_text: str, paths: list[str]) -> str:
    """Produce a short summary from diff content (first meaningful line, ~50 chars)."""
    lines = []
    skip = frozenset(['"', "'", "```", "---", "===", "#"])
    for line in diff_text.split("\n"):
        line = line.strip()
        if line.startswith("+") and not line.startswith("+++"):
            content = line[1:].strip()
            if content and not content.startswith("#") and len(content) < 80:
                if content[:3] not in ('"""', "'''") and len(content) > 3:
                    lines.append(content)
        elif line.startswith("-") and not line.startswith("---"):
            content = line[1:].strip()
            if content and not content.startswith("#") and len(content) < 80:
                if content[:3] not in ('"""', "'''") and len(content) > 3:
                    lines.append(content)

    for cand in lines:
        first = cand[:60].strip()
        # Skip lines that are mostly punctuation or quotes
        if first and sum(c.isalnum() or c.isspace() for c in first) > 10:
            return first

    # Fallback: describe from paths
    if len(paths) == 1:
        return f"update {Path(paths[0]).name}"
    top = infer_scope_from_paths(paths)
    return f"update {top or 'files'}" if top else "miscellaneous changes"


def parse_diff_and_paths(diff_text: str) -> tuple[list[str], str]:
    """Extract file paths from diff header lines (+++ ---) and return (paths, body)."""
    paths = []
    for line in diff_text.split("\n"):
        if line.startswith("+++ ") or line.startswith("--- "):
            p = line[4:].strip()
            if p != "/dev/null":
                # Strip a/b/ prefix from git diff
                if p.startswith("a/") or p.startswith("b/"):
                    p = p[2:]
                paths.append(p)

    seen = set()
    unique = []
    for p in paths:
        norm = p.strip()
        if norm and norm not in seen:
            seen.add(norm)
            unique.append(norm)

    return unique, diff_text


def format_commit_message(ctype: str, scope: str, summary: str, is_breaking: bool) -> str:
    """Format conventional commit message."""
    summary = summary.strip()
    if len(summary) > 72:
        summary = summary[:69] + "..."

    scope_part = f"({scope})" if scope else ""
    subject = f"{ctype}{scope_part}: {summary}".strip()

    lines = [subject]
    if is_breaking:
        lines.append("")
        lines.append("BREAKING CHANGE: <describe the breaking change>")

    return "\n".join(lines)


def main() -> None:
    """Read diff from stdin, optional paths from argv, output commit message."""
    diff_text = sys.stdin.read()

    paths_raw = []
    if len(sys.argv) > 1 and sys.argv[1].strip():
        # Paths passed as arg (space-separated)
        paths_raw = sys.argv[1].split()

    paths_from_diff, _ = parse_diff_and_paths(diff_text)
    paths = paths_raw or paths_from_diff

    if not paths:
        sys.stderr.write("No changed files detected in diff.\n")
        sys.exit(1)

    ctype, summary, is_breaking = categorize_from_content(diff_text, paths)
    scope = infer_scope_from_paths(paths)

    msg = format_commit_message(ctype, scope, summary, is_breaking)
    print(msg)


if __name__ == "__main__":
    main()
