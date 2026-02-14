"""
Scout Context — Symbol-level hydration with tiered docs and hard token bounds.

TICKET-34/35: Tiered context hydration. Always .tldr.md first; .deep.md only when needed.
TICKET-43: hydrate_facts() loads STRUCTURED FACTS ONLY — never prose. Prose flows one way: out.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, List

from vivarium.scout.deps import SymbolRef

if TYPE_CHECKING:
    from vivarium.scout.doc_sync.ast_facts import ModuleFacts

def _query_index_safely(query: str, repo_root: Path) -> List[Path]:
    """TICKET-48b: Index lookup returning Paths. Returns [] on failure."""
    try:
        from vivarium.scout.cli.index import query_for_nav

        suggestions = query_for_nav(repo_root, query, limit=5)
        if not suggestions:
            return []
        files: List[Path] = []
        seen: set[str] = set()
        for s in suggestions:
            if isinstance(s, dict):
                fp = s.get("target_file") or s.get("file", "")
                if fp and fp not in seen:
                    seen.add(fp)
                    p = repo_root / fp
                    if p.exists() and p.suffix == ".py":
                        files.append(p.relative_to(repo_root))
                        seen.add(fp)
        return files
    except Exception:
        return []


def _route_query_to_files(query: str, scope: str, repo_root: Path) -> List[Path]:
    """
    Route query to relevant files. Uses index when available, else expands scope.
    TICKET-48b: Prioritize scout/ for gate-related queries; cap files to prevent context explosion.
    """
    repo_root = Path(repo_root).resolve()
    scope_path = repo_root / scope

    # 1. Try index first (cheap, targeted)
    index_results = _query_index_safely(query, repo_root)
    if index_results:
        # Prioritize scout/ for gate-related queries
        gate_kw = ["gate", "confidence", "hallucination", "middlemanager"]
        if any(kw in query.lower() for kw in gate_kw):
            scout_first = [r for r in index_results if "scout" in str(r).lower()]
            other = [r for r in index_results if "scout" not in str(r).lower()]
            index_results = scout_first + other
        return index_results[:5]

    # 2. Fallback: expand scope (with scout/ prioritization for gate queries)
    if not scope_path.exists():
        return []
    if scope_path.is_file() and scope_path.suffix == ".py":
        try:
            return [scope_path.relative_to(repo_root)]
        except ValueError:
            return []

    all_py: List[Path] = []
    for p in sorted(scope_path.rglob("*.py")):
        if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts:
            try:
                rel = p.relative_to(repo_root)
                if "test" in str(rel).lower() and "tests" not in str(rel.parts[0]):
                    continue
                all_py.append(rel)
            except ValueError:
                pass

    gate_kw = ["gate", "confidence", "hallucination"]
    if any(kw in query.lower() for kw in gate_kw):
        scout_files = [p for p in all_py if "scout" in str(p).lower()]
        other_files = [p for p in all_py if "scout" not in str(p).lower()]
        # Prioritize files matching query symbols (e.g. middle_manager for "MiddleManagerGate")
        q_symbols = re.findall(r"[A-Z][a-z]+(?:[A-Z][a-z]+)*|[A-Z][A-Z0-9_]{2,}", query)
        prioritized: List[Path] = []
        for sym in q_symbols[:3]:
            needle = sym.lower().replace("_", "")
            for p in list(scout_files):
                if needle in str(p).lower().replace("_", ""):
                    prioritized.append(p)
                    scout_files = [x for x in scout_files if x != p]
        if prioritized:
            scout_files = list(dict.fromkeys(prioritized)) + scout_files
        return (scout_files + other_files)[:15]

    # Prioritize files containing query symbols in their facts
    symbol_candidates = re.findall(r"[A-Z][A-Z0-9_]{2,}", query)
    if symbol_candidates:
        prioritized: List[Path] = []
        for sym in symbol_candidates[:3]:
            for f in list(all_py):
                full = (repo_root / f).resolve()
                facts_path = full.parent / ".docs" / f"{full.name}.facts.json"
                if facts_path.exists() and sym in facts_path.read_text(encoding="utf-8"):
                    prioritized.append(f)
                    all_py = [x for x in all_py if x != f]
        if prioritized:
            all_py = list(dict.fromkeys(prioritized)) + all_py

    return all_py[:10]


if TYPE_CHECKING:
    from vivarium.scout.deps import DependencyGraph


def _estimate_tokens(text: str) -> int:
    """Rough token estimate (4 chars ≈ 1 token for English)."""
    return len(text) // 4


def _truncate_to_tokens(parts: List[str], max_tokens: int) -> List[str]:
    """Truncate oldest parts first to stay under token cap."""
    total = sum(_estimate_tokens(p) for p in parts)
    while total > max_tokens and parts:
        removed = parts.pop(0)  # FIFO — oldest symbols truncated first
        total -= _estimate_tokens(removed)
    return parts


def _load_tldr(ref: SymbolRef, repo_root: Path) -> str:
    """Load .tldr.md for a symbol's file. Returns empty string if not found."""
    full_path = (repo_root / ref.path).resolve()
    if not full_path.exists():
        return ""

    # 1. Local .docs/ next to source
    docs_dir = full_path.parent / ".docs"
    tldr_path = docs_dir / f"{full_path.name}.tldr.md"
    if tldr_path.exists():
        try:
            return tldr_path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            pass

    # 2. Central docs/livingDoc/
    try:
        rel = full_path.relative_to(repo_root)
        central = repo_root / "docs" / "livingDoc" / rel.parent
        tldr_path = central / f"{full_path.name}.tldr.md"
        if tldr_path.exists():
            try:
                return tldr_path.read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                pass
    except ValueError:
        pass

    return ""


def _facts_cache_path(repo_root: Path, py_path: Path) -> Path:
    """Map Python file → .facts.json cache. Uses local .docs/ next to source."""
    full_path = (repo_root / py_path).resolve()
    return full_path.parent / ".docs" / f"{full_path.name}.facts.json"


async def hydrate_facts(
    symbols: List[SymbolRef],
    deps_graph: "DependencyGraph",
    repo_root: Path,
    *,
    max_facts: int = 50,
    max_depth: int = 2,
) -> "ModuleFacts":
    """
    TICKET-43: Load STRUCTURED FACTS ONLY — never prose.

    BFS over symbol graph, load .facts.json caches. Returns combined ModuleFacts.
    Prose is not truth. Facts are.
    """
    from vivarium.scout.doc_sync.ast_facts import ModuleFacts

    combined = ModuleFacts.empty()
    fact_count = 0
    queue: List[tuple[SymbolRef, int]] = [(s, 0) for s in symbols]
    visited: set[str] = {str(s) for s in symbols}

    while queue and fact_count < max_facts:
        ref, depth = queue.pop(0)
        full_path = (repo_root / ref.path).resolve()
        facts_path = _facts_cache_path(repo_root, ref.path)

        if facts_path.exists():
            try:
                loaded = ModuleFacts.from_json(facts_path.read_text(encoding="utf-8"))
                loaded.path = full_path
                combined.merge(loaded)
                fact_count += len(loaded.symbols)
            except Exception:
                pass

        if depth < max_depth and deps_graph and len(queue) < 20:
            for dep_ref in _get_deps_for_ref(ref, deps_graph):
                dep_key = str(dep_ref)
                if dep_key not in visited:
                    visited.add(dep_key)
                    queue.append((dep_ref, depth + 1))

    return combined


def _get_deps_for_ref(ref: SymbolRef, deps_graph: "DependencyGraph") -> List[SymbolRef]:
    """Get dependencies for a ref. Handles file-level (empty symbol) by matching path."""
    # Direct match
    node = deps_graph.nodes.get(str(ref))
    if node:
        return list(node.depends_on)
    # File-level ref: aggregate deps from all symbols in that file
    path_str = ref.path.as_posix()
    deps: set[SymbolRef] = set()
    for node_ref, node in deps_graph.nodes.items():
        if node_ref.startswith(path_str + "::"):
            deps.update(node.depends_on)
    return list(deps)


async def hydrate_symbols(
    symbols: List[SymbolRef],
    deps_graph: "DependencyGraph",
    repo_root: Path,
    *,
    max_depth: int = 2,
    max_tokens: int = 4000,
) -> str:
    """
    Hydrate symbols tiered: .tldr.md first, .deep.md only if needed.

    BFS through dependency graph (symbol-level). Hard cap at max_tokens.
    """
    context_parts: List[str] = []
    token_count = 0

    # BFS: (ref, depth)
    queue: List[tuple[SymbolRef, int]] = [(s, 0) for s in symbols]
    visited: set[str] = {str(s) for s in symbols}
    seen_files: set[str] = set()  # Avoid duplicate file docs

    while queue and token_count < max_tokens:
        ref, depth = queue.pop(0)

        # Tier 1: .tldr.md (ALWAYS used)
        file_key = str(ref.path)
        if file_key not in seen_files:
            tldr = _load_tldr(ref, repo_root)
            if tldr:
                seen_files.add(file_key)
                part = f"## {ref}\n{tldr}"
                context_parts.append(part)
                token_count += _estimate_tokens(part)

        # Enqueue dependencies (bounded by max_depth)
        if depth < max_depth:
            for dep in _get_deps_for_ref(ref, deps_graph):
                if str(dep) not in visited:
                    visited.add(str(dep))
                    queue.append((dep, depth + 1))

    # Hard cap — truncate if over limit
    if token_count > max_tokens:
        context_parts = _truncate_to_tokens(context_parts, max_tokens)

    return "\n\n".join(context_parts)
