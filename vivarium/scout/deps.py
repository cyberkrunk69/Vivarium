"""
Dependency graph with reverse indexing for proactive echo chains.
Pure programmatic — zero LLM cost. Cached to .scout/dependency_graph.v2.json.

Core invariant: When file X changes, invalidate_cascade(changed=[X]) returns
all symbols that depend *transitively* on X — enabling pre-query cache invalidation.
"""
from __future__ import annotations

import ast
import hashlib
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Set, Dict, Optional, Tuple, Any

logger = logging.getLogger(__name__)

# Cache schema version — bump when structure changes to force rebuild
GRAPH_VERSION = 2


@dataclass(frozen=True)
class SymbolRef:
    """Immutable symbol identifier: path::symbol_name (path always repo-relative)"""
    path: Path  # Always relative to repo_root
    symbol: str

    def __post_init__(self):
        # Normalize to repo-relative, POSIX paths for consistent hashing
        if not isinstance(self.path, Path):
            object.__setattr__(self, 'path', Path(self.path))
        # Force relative path representation (caller must handle resolution)
        object.__setattr__(self, 'path', Path(self.path.as_posix()))

    def __str__(self) -> str:
        return f"{self.path.as_posix()}::{self.symbol}"

    @classmethod
    def from_string(cls, s: str) -> SymbolRef:
        path_str, symbol = s.split("::", 1)
        return cls(Path(path_str), symbol)

    def __hash__(self) -> int:
        return hash((self.path.as_posix(), self.symbol))

    def __eq__(self, other) -> bool:
        return isinstance(other, SymbolRef) and str(self) == str(other)


@dataclass
class DependencyNode:
    """
    Node in the dependency graph with bidirectional edges.

    Freshness states:
    - FRESH: invalidated_at is None AND ast_hash matches current source
    - STALE (cascade): invalidated_at set by proactive echo (invalidation_reason="cascade")
    - STALE (hash): invalidated_at not set BUT ast_hash mismatch on query-time check
    - ORPHAN: path no longer exists in repo (handled lazily during rebuild)
    """
    ref: SymbolRef
    ast_hash: str  # SHA256 of symbol's source snippet (lineno:end_lineno)
    depends_on: Set[SymbolRef] = field(default_factory=set)   # forward edges: what I import/call
    depended_by: Set[SymbolRef] = field(default_factory=set)  # REVERSE INDEX: who depends on me
    invalidated_at: Optional[datetime] = None                 # explicit invalidation timestamp
    invalidation_reason: Optional[str] = None                 # "cascade", "hash_mismatch", "manual"

    def is_stale(self, current_hash: Optional[str] = None) -> bool:
        """Check freshness — respects proactive invalidation first, then hash."""
        if self.invalidated_at is not None:
            return True
        if current_hash is not None and self.ast_hash != current_hash:
            return True
        return False

    def mark_stale(self, reason: str) -> None:
        """Proactive invalidation — preserves original ast_hash for diagnostics."""
        self.invalidated_at = datetime.now(timezone.utc)
        self.invalidation_reason = reason


def _extract_symbols_from_scope(scope: Path, repo_root: Path) -> List[Any]:
    """
    Extract symbols from Python files in scope using existing PythonAdapter.
    Returns list of objects with: file_path, name, ast_hash, dependencies.
    """
    from vivarium.scout.adapters.python import PythonAdapter

    adapter = PythonAdapter()
    symbols_out: List[Any] = []

    if scope.is_file():
        py_files = [scope] if scope.suffix == ".py" else []
    else:
        py_files = list(scope.rglob("*.py"))

    for file_path in py_files:
        if not file_path.is_file():
            continue
        try:
            tree = adapter.parse(file_path)
            content = file_path.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()
        except Exception as e:
            logger.debug("Skipping %s: %s", file_path, e)
            continue

        try:
            rel_path = file_path.relative_to(repo_root)
        except ValueError:
            continue

        for sym in tree.iter_symbols():
            if sym.type == "module" and sym.name == file_path.stem:
                continue  # Skip module-level; we index top-level defs/classes
            lineno = getattr(sym, "lineno", 1)
            end_lineno = getattr(sym, "end_lineno", lineno)
            snippet = "\n".join(lines[lineno - 1 : end_lineno]) if lines else ""
            ast_hash = hashlib.sha256(snippet.encode()).hexdigest()

            # Collect deps: imports + calls. Resolve to (Path, str) where possible.
            # For minimal impl, use empty — full resolution is a follow-up.
            deps: List[Tuple[Path, str]] = []

            symbols_out.append(
                _SymbolInfo(
                    file_path=rel_path,
                    name=sym.name,
                    ast_hash=ast_hash,
                    dependencies=deps,
                )
            )

    return symbols_out


@dataclass
class _SymbolInfo:
    """Internal symbol info for build_for_scope."""
    file_path: Path
    name: str
    ast_hash: str
    dependencies: List[Tuple[Path, str]]


class DependencyGraph:
    """Bidirectional graph with proactive invalidation support."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()
        self.nodes: Dict[str, DependencyNode] = {}  # key: str(SymbolRef)
        self._load_cache()

    # === BUILD (query-time or proactive) ===
    async def build_for_scope(self, scope: Path, force: bool = False) -> None:
        """
        AST-parse scope, build forward/backward edges. Concurrent-safe.

        Args:
            scope: Directory or file to index (relative to repo_root)
            force: Rebuild even if cache appears fresh
        """
        scope = (self.repo_root / scope).resolve()

        if not force and self._is_fresh(scope):
            logger.debug(f"Dependency graph for {scope} is fresh — skipping rebuild")
            return

        logger.info(f"Building dependency graph for {scope}")
        symbols = _extract_symbols_from_scope(scope, self.repo_root)

        # Phase 1: Create/update nodes for discovered symbols
        for sym in symbols:
            rel_path = sym.file_path
            ref = SymbolRef(rel_path, sym.name)
            node = self.nodes.setdefault(str(ref), DependencyNode(ref, sym.ast_hash))
            node.ast_hash = sym.ast_hash

            node.depends_on.clear()

            for dep_path, dep_name in sym.dependencies:
                dep_rel_path = dep_path.relative_to(self.repo_root) if dep_path.is_absolute() else dep_path
                dep_ref = SymbolRef(dep_rel_path, dep_name)
                node.depends_on.add(dep_ref)

                dep_node = self.nodes.setdefault(
                    str(dep_ref),
                    DependencyNode(dep_ref, "")
                )
                dep_node.depended_by.add(ref)

        # Phase 2: Orphan cleanup
        if scope == self.repo_root:
            self._cleanup_orphans()

        self._save_cache()
        logger.info(f"Dependency graph built: {len(self.nodes)} symbols indexed")

    def _cleanup_orphans(self) -> None:
        """Remove nodes for files that no longer exist in the repo."""
        orphans = [
            ref_str for ref_str, node in self.nodes.items()
            if not (self.repo_root / node.ref.path).exists()
        ]
        for orphan in orphans:
            logger.debug(f"Removing orphaned node: {orphan}")
            del self.nodes[orphan]

    # === PROACTIVE ECHO (the new piece) ===
    def invalidate_cascade(self, changed_files: List[Path]) -> Set[SymbolRef]:
        """
        Proactive invalidation: mark stale + return transitive dependents for re-compression.

        Called by git hooks/filesystem watchers BEFORE query time.
        Uses REVERSE edges (depended_by) to propagate invalidation downstream.

        Returns:
            Set of SymbolRef that were invalidated (including transitive dependents)
        """
        affected: Set[SymbolRef] = set()

        for path in changed_files:
            try:
                rel_path = path.resolve().relative_to(self.repo_root)
            except ValueError:
                logger.debug(f"Changed file {path} is outside repo root — skipping")
                continue

            stale_refs = [
                node.ref for node in self.nodes.values()
                if node.ref.path == rel_path
            ]

            if not stale_refs:
                logger.debug(f"No indexed symbols found in changed file: {rel_path}")
                continue

            queue: List[SymbolRef] = stale_refs.copy()
            visited: Set[SymbolRef] = set(queue)

            while queue:
                current = queue.pop(0)
                affected.add(current)

                node = self.nodes.get(str(current))
                if not node:
                    continue

                node.mark_stale(reason="cascade")

                for dependent in node.depended_by:
                    if dependent not in visited:
                        visited.add(dependent)
                        queue.append(dependent)

        if affected:
            logger.info(f"Invalidation cascade triggered: {len(affected)} symbols marked stale")
            self._save_cache()
        else:
            logger.debug("No symbols affected by invalidation cascade")

        return affected

    # === QUERY-TIME RESOLUTION (for doc_sync.py) ===
    async def get_transitive_dependents(self, changed_files: List[Path]) -> List[Path]:
        """
        Returns file paths (not symbols) that need re-doc-sync.

        WARNING: This triggers LAZY rebuild if graph missing — log perf regression.
        """
        if not self.nodes:
            logger.warning(
                "Dependency graph built lazily at query-time — performance regression. "
                "Consider running `scout-index` proactively or enabling git hooks."
            )
            for path in changed_files:
                if path.exists() and path.suffix == ".py":
                    await self.build_for_scope(path.parent)

        affected_symbols = self.invalidate_cascade(changed_files)
        return list({ref.path for ref in affected_symbols})

    def get_trust_metadata(self, nodes: List[DependencyNode]) -> dict:
        """
        Trust chain metadata for middle manager consumption.

        Returns aggregate stats about invalidation state of the given nodes.
        """
        stale_nodes = [n for n in nodes if n.invalidated_at]
        return {
            "invalidation_cascade_triggered": len(stale_nodes) > 0,
            "invalidation_reasons": list(
                {n.invalidation_reason for n in stale_nodes if n.invalidation_reason}
            ),
            "oldest_invalidation": min(
                (n.invalidated_at for n in stale_nodes), default=None
            ),
            "total_symbols": len(nodes),
            "stale_ratio": len(stale_nodes) / len(nodes) if nodes else 0.0,
        }

    def get_stats(self) -> dict:
        """
        Observability stats for dependency graph health dashboard.

        Returns:
            Dict with total, orphaned, stale counts and cache_version.
        """
        total = len(self.nodes)
        stale = sum(1 for n in self.nodes.values() if n.invalidated_at is not None)
        orphaned = sum(
            1 for n in self.nodes.values()
            if not (self.repo_root / n.ref.path).exists()
        )
        return {
            "total": total,
            "stale": stale,
            "orphaned": orphaned,
            "cache_version": f"v{GRAPH_VERSION}",
        }

    def is_graph_stale(self) -> bool:
        """True if graph is missing (empty) or cache is older than repo source files."""
        if not self.nodes:
            return True
        return not self._is_fresh(self.repo_root)

    def get_context_package(
        self, query_symbols: List[SymbolRef], max_depth: int = 3
    ) -> List[DependencyNode]:
        """
        What to hydrate for a query? Returns minimal transitive closure via FORWARD edges.

        Used by middle manager to gather context before compression.
        BFS stops at max_depth to prevent context explosion on broad queries.

        Args:
            query_symbols: Starting symbols (depth 0).
            max_depth: Maximum BFS depth; nodes beyond this are excluded. Default 3.
        """
        closure: Set[SymbolRef] = set(query_symbols)
        # Queue: (ref, depth). Query symbols are depth 0.
        queue: List[Tuple[SymbolRef, int]] = [(r, 0) for r in query_symbols]

        while queue:
            current, depth = queue.pop(0)
            if depth >= max_depth:
                continue
            node = self.nodes.get(str(current))
            if node:
                for dep in node.depends_on:
                    if dep not in closure:
                        closure.add(dep)
                        queue.append((dep, depth + 1))

        return [self.nodes[str(ref)] for ref in closure if str(ref) in self.nodes]

    # === PERSISTENCE ===
    def _load_cache(self) -> None:
        cache_path = Path.home() / ".scout" / "dependency_graph.v2.json"
        if not cache_path.exists():
            logger.debug("No dependency graph cache found — will build on first use")
            return

        try:
            data = json.loads(cache_path.read_text())

            if data.get("version", 0) != GRAPH_VERSION:
                logger.info(f"Dependency graph cache version mismatch ({data.get('version')} != {GRAPH_VERSION}) — rebuilding")
                return

            self.nodes = {}
            for ref_str, node_data in data["nodes"].items():
                self.nodes[ref_str] = DependencyNode(
                    SymbolRef.from_string(ref_str),
                    node_data["ast_hash"],
                    {SymbolRef.from_string(d) for d in node_data.get("depends_on", [])},
                    {SymbolRef.from_string(d) for d in node_data.get("depended_by", [])},
                    datetime.fromisoformat(node_data["invalidated_at"]) if node_data.get("invalidated_at") else None,
                    node_data.get("invalidation_reason")
                )
            logger.debug(f"Loaded dependency graph cache: {len(self.nodes)} symbols")
        except Exception as e:
            logger.warning(f"Failed to load dependency graph cache: {e} — rebuilding")
            self.nodes = {}

    def _save_cache(self) -> None:
        cache_dir = Path.home() / ".scout"
        cache_dir.mkdir(exist_ok=True)
        cache_path = cache_dir / "dependency_graph.v2.json"

        cache_data = {
            "version": GRAPH_VERSION,
            "ts": datetime.now(timezone.utc).isoformat(),
            "nodes": {
                ref_str: {
                    "ast_hash": node.ast_hash,
                    "depends_on": [str(d) for d in node.depends_on],
                    "depended_by": [str(d) for d in node.depended_by],
                    "invalidated_at": node.invalidated_at.isoformat() if node.invalidated_at else None,
                    "invalidation_reason": node.invalidation_reason
                }
                for ref_str, node in self.nodes.items()
            }
        }

        temp_path = cache_path.with_suffix(f".json.tmp.{os.getpid()}")
        temp_path.write_text(json.dumps(cache_data, indent=2))
        temp_path.rename(cache_path)
        logger.debug(f"Saved dependency graph cache: {len(self.nodes)} symbols")

    def _is_fresh(self, scope: Path) -> bool:
        """
        Heuristic freshness check — graph exists and scope modified time < graph modified time.
        Conservative: prefers rebuild over stale data.
        """
        if not self.nodes:
            return False

        cache_path = Path.home() / ".scout" / "dependency_graph.v2.json"
        if not cache_path.exists():
            return False

        try:
            if scope.is_file():
                latest_mtime = scope.stat().st_mtime
            else:
                latest_mtime = max(
                    f.stat().st_mtime for f in scope.rglob("*.py") if f.is_file()
                )
        except (FileNotFoundError, ValueError):
            return False

        graph_mtime = cache_path.stat().st_mtime
        return graph_mtime > latest_mtime


# === LEGACY COMPATIBILITY SHIM (for doc_sync.py) ===
async def get_dependencies_for_doc(path: Path) -> List[str]:
    """
    For doc_generation: returns dependency paths (as strings) for a single file.
    Uses DependencyGraph forward edges (what this file imports).
    """
    repo_root = Path.cwd()
    graph = DependencyGraph(repo_root)
    try:
        rel = path.resolve().relative_to(repo_root)
    except ValueError:
        return []
    refs = [node.ref for node in graph.nodes.values() if node.ref.path == rel]
    if not refs:
        return []
    nodes = graph.get_context_package(refs)
    return list({str(n.ref.path) for n in nodes})


async def query_for_deps(changed_files: List[Path]) -> List[Path]:
    """
    Shim for doc_sync.py — wraps DependencyGraph with lazy initialization.
    Properly async — must be awaited by callers.
    """
    from vivarium.scout.config import ScoutConfig

    config = ScoutConfig()
    repo_root = Path.cwd()  # ScoutConfig has no repo_root; use cwd
    graph = DependencyGraph(repo_root)

    if not graph.nodes:
        logger.warning(
            "Dependency graph built lazily at query-time — performance regression. "
            "Run `scout-index` proactively or enable git hooks via `scout-autonomy enable`."
        )

    return await graph.get_transitive_dependents(changed_files)
