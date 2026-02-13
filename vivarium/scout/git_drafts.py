"""
Git drafts — Assemble commit and PR drafts from docs/drafts/*.

Reads pre-generated drafts (from on-commit hooks or doc-sync).
No LLM calls. Agnostic: no IDE, no network, no state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

_MODULE_MD_NAME = "__init__.py.module.md"


def _stem_for_file(file_path: Path, root: Path) -> str:
    """Return stem for file path relative to repo root."""
    path = Path(file_path).resolve()
    try:
        return path.relative_to(root).stem
    except ValueError:
        return path.stem


def _find_package_root(file_path: Path, root: Path) -> Path | None:
    """Find the nearest package directory (with __init__.py) containing the file."""
    path = Path(file_path).resolve()
    try:
        parent = path.parent
        while parent != root and parent != root.parent:
            if (parent / "__init__.py").exists():
                return parent
            parent = parent.parent
        if (parent / "__init__.py").exists():
            return parent
    except (ValueError, OSError):
        pass
    return None


def _read_module_summary(repo_root: Path, package_dir: Path) -> str | None:
    """Read package __init__.py.module.md from central or local .docs/."""
    try:
        rel = package_dir.relative_to(repo_root)
    except ValueError:
        return None
    central = repo_root / "docs" / "livingDoc" / rel / _MODULE_MD_NAME
    if central.exists():
        try:
            return central.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            pass
    local = package_dir / ".docs" / _MODULE_MD_NAME
    if local.exists():
        try:
            return local.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            pass
    return None


def assemble_pr_description(repo_root: Path, staged_files: List[Path]) -> str:
    """
    Assemble a PR description from docs/drafts/{stem}.pr.md for each staged .py file.

    Enhanced with cascading context:
    - Groups changed files under their parent package headings
    - Includes package __init__.py.module.md summaries when available
    - Adds top-level "Architectural Impact" section using package summaries

    Args:
        repo_root: Repository root path.
        staged_files: List of staged file paths (absolute or relative to repo_root).

    Returns:
        Aggregated PR description as Markdown.
    """
    root = Path(repo_root).resolve()
    draft_dir = root / "docs" / "drafts"

    doc_extensions = {".py", ".js", ".mjs", ".cjs"}
    doc_files = [f for f in staged_files if Path(f).suffix in doc_extensions]
    if not doc_files:
        return "No staged doc files (.py, .js, .mjs, .cjs)."

    # Group files by package root; files without package go under root
    pkg_to_files: Dict[Path | None, List[Tuple[Path, str, str]]] = {}
    for file_path in doc_files:
        path = Path(file_path).resolve()
        stem = _stem_for_file(path, root)
        try:
            rel_str = str(path.relative_to(root))
        except ValueError:
            rel_str = path.name

        draft_path = draft_dir / f"{stem}.pr.md"
        if not draft_path.exists():
            draft_path = draft_dir / f"{stem}.pr.txt"
        if draft_path.exists():
            try:
                content = draft_path.read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                content = "No PR draft available."
        else:
            content = "No PR draft available."

        pkg = _find_package_root(path, root)
        if pkg not in pkg_to_files:
            pkg_to_files[pkg] = []
        pkg_to_files[pkg].append((path, rel_str, content))

    # Gather package summaries for Architectural Impact
    package_summaries: List[Tuple[str, str]] = []
    for pkg in pkg_to_files:
        if pkg is None:
            continue
        summary = _read_module_summary(root, pkg)
        if summary:
            try:
                rel = str(pkg.relative_to(root))
            except ValueError:
                rel = str(pkg)
            package_summaries.append((rel, summary))

    sections: List[str] = []

    # Top-level Architectural Impact section
    if package_summaries:
        impact_parts = ["## Architectural Impact\n"]
        for rel, summary in package_summaries:
            impact_parts.append(f"### {rel}\n\n{summary}\n")
        sections.append("\n".join(impact_parts))

    # Per-package sections with changed files (sort: None last, then by path)
    def _pkg_key(p: Path | None) -> str:
        return str(p) if p is not None else "\xff"  # None sorts last

    for pkg in sorted(pkg_to_files.keys(), key=_pkg_key):
        files_data = pkg_to_files[pkg]
        if pkg is not None:
            try:
                pkg_rel = str(pkg.relative_to(root))
            except ValueError:
                pkg_rel = str(pkg)
            pkg_summary = _read_module_summary(root, pkg)
            block = [f"## {pkg_rel}\n"]
            if pkg_summary:
                block.append(pkg_summary)
                block.append("")
            block.append("### Changed Files\n")
            for _, rel_str, content in files_data:
                block.append(f"- **{Path(rel_str).name}**")
                if content:
                    block.append("")
                    block.append(content)
                block.append("")
            sections.append("\n".join(block).rstrip())
        else:
            block = ["## Other\n", "### Changed Files\n"]
            for _, rel_str, content in files_data:
                block.append(f"### {rel_str}\n\n{content}")
            sections.append("\n".join(block))

    return "\n\n---\n\n".join(sections)


def _call_graph_summary_for_scope(
    repo_root: Path,
    scope_prefix: str,
    call_graph_path: Path,
) -> str:
    """
    Extract a brief call-graph summary for modules under scope_prefix.
    Returns markdown listing caller -> callee edges within the scope.
    """
    if not call_graph_path.exists():
        return ""
    try:
        data = json.loads(call_graph_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return ""
    edges = data.get("edges", [])
    # Normalize scope: ensure trailing slash for prefix match
    scope = scope_prefix.strip("/")
    if scope and not scope.endswith("/"):
        scope = scope + "/"
    if not scope:
        scope = ""

    # Collect edges where both from and to are in scope (or to external)
    lines: List[str] = []
    seen: set[tuple[str, str]] = set()
    for e in edges:
        fr = e.get("from", "")
        to = e.get("to", "")
        if "::" not in fr or "::" not in to:
            continue
        file_from = fr.split("::", 1)[0]
        file_to = to.split("::", 1)[0]
        # Include if caller is in scope
        in_scope = not scope or file_from.startswith(scope) or file_from == scope.rstrip("/")
        if not in_scope:
            continue
        key = (file_from, file_to)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- {file_from} → {file_to}")
    if not lines:
        return ""
    return "## Call graph (scope)\n\n" + "\n".join(sorted(lines)[:50])


def assemble_pr_description_from_docs(
    repo_root: Path,
    target_path: str,
    *,
    include_call_graph: bool = True,
) -> str:
    """
    Assemble a PR description from all .tldr.md files under target_path/.docs/.

    Ignores Git entirely. Uses tldr content + optional call graph summary.
    Works even when no files are "changed" — ideal for documenting a whole package.

    Args:
        repo_root: Repository root path.
        target_path: Path to package/module (e.g. vivarium/scout). .docs/ is
            resolved as (repo_root / target_path) / ".docs".
        include_call_graph: If True, appends call graph summary when available.

    Returns:
        Raw markdown suitable for synthesize_pr_description.
    """
    root = Path(repo_root).resolve()
    target = Path(target_path).resolve()
    if not target.is_absolute():
        target = (root / target_path).resolve()
    docs_dir = target / ".docs"
    if not docs_dir.exists() or not docs_dir.is_dir():
        return f"No .docs directory found at {docs_dir}."

    tldr_files = sorted(docs_dir.glob("*.tldr.md"))
    if not tldr_files:
        return f"No .tldr.md files found under {docs_dir}."

    try:
        scope_rel = str(target.relative_to(root))
    except ValueError:
        scope_rel = target_path

    sections: List[str] = []
    for tldr_path in tldr_files:
        stem = tldr_path.stem.removesuffix(".tldr")  # e.g. doc_generation.py from doc_generation.py.tldr
        try:
            content = tldr_path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            content = "(unable to read)"
        module_path = f"{scope_rel}/{stem}" if scope_rel else stem
        sections.append(f"## {module_path}\n\n{content}")

    raw = "\n\n---\n\n".join(sections)

    if include_call_graph:
        # Prefer call graph at vivarium/.docs; fallback to target/.docs
        for cg_candidate in [
            root / "vivarium" / ".docs" / "call_graph.json",
            docs_dir / "call_graph.json",
        ]:
            if cg_candidate.exists():
                summary = _call_graph_summary_for_scope(root, scope_rel, cg_candidate)
                if summary:
                    raw += "\n\n---\n\n" + summary
                break

    return raw


def assemble_commit_message(repo_root: Path, staged_files: List[Path]) -> str:
    """
    Assemble a single commit message from docs/drafts/{stem}.commit.txt for each staged .py file.

    For each staged .py file, reads docs/drafts/{stem}.commit.txt if it exists.
    Falls back to "No draft available" if missing.
    Aggregates all into a single message (one section per file).

    Args:
        repo_root: Repository root path.
        staged_files: List of staged file paths (absolute or relative to repo_root).

    Returns:
        Aggregated commit message string.
    """
    root = Path(repo_root).resolve()
    draft_dir = root / "docs" / "drafts"
    sections: List[str] = []

    doc_extensions = {".py", ".js", ".mjs", ".cjs"}
    doc_files = [f for f in staged_files if Path(f).suffix in doc_extensions]
    if not doc_files:
        return "No staged doc files (.py, .js, .mjs, .cjs)."

    for file_path in doc_files:
        path = Path(file_path).resolve()
        stem = _stem_for_file(path, root)

        draft_path = draft_dir / f"{stem}.commit.txt"
        if draft_path.exists():
            try:
                content = draft_path.read_text(encoding="utf-8", errors="replace").strip()
                sections.append(content if content else f"[{path.name}]: No draft available")
            except OSError:
                sections.append(f"[{path.name}]: No draft available")
        else:
            sections.append(f"[{path.name}]: No draft available")

    return "\n\n---\n\n".join(sections)
