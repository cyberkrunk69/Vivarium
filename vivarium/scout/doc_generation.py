"""
Scout doc generation — process files and directories for documentation sync.

Supports Python, JavaScript, and plain-text fallback via language adapters.
Provides process_single_file and process_directory for use by doc_sync CLI.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from vivarium.scout.adapters.base import SymbolTree
from vivarium.scout.adapters.registry import get_adapter_for_path
from vivarium.scout.audit import AuditLog
from vivarium.scout.config import ScoutConfig
from vivarium.scout.ignore import IgnorePatterns
from vivarium.scout.big_brain import call_big_brain_async
from vivarium.scout.llm import call_groq_async

logger = logging.getLogger(__name__)

# ANSI escape codes for terminal output (no extra deps)
_RESET = "\033[0m"
_RED = "\033[91m"
_CLEAR_SCREEN = "\033[H\033[J"  # cursor home + clear
_INVERSE = "\033[7m"   # inverse video (pulse)
_INVERSE_OFF = "\033[27m"


class BudgetExceededError(RuntimeError):
    """Raised when doc-sync exceeds the --budget limit."""

    def __init__(self, total_cost: float, budget: float) -> None:
        super().__init__(f"Budget exceeded: ${total_cost:.4f} >= ${budget}")
        self.total_cost = total_cost
        self.budget = budget


@dataclass
class FileProcessResult:
    """Result of processing a single file for doc generation."""

    success: bool
    cost_usd: float
    symbols_count: int
    calls_count: int
    types_count: int
    exports_count: int
    model: str
    skipped: bool = False  # True when skipped due to freshness (up to date)
    error: Optional[str] = None
    call_chain: Optional[str] = None  # e.g. "funcA → pkgB.funcB → pkgC.funcC"


@dataclass
class TraceResult:
    """Result of pure static analysis (no LLM)."""

    root_tree: SymbolTree
    symbols_to_doc: List[SymbolTree]
    all_calls: set
    all_types: set
    all_exports: set
    adapter: Any
    dependencies: List[str]


def _get_tldr_meta_path(file_path: Path, output_dir: Optional[Path]) -> Path:
    """Path to .tldr.md.meta for freshness check. Mirrors write_documentation_files logic."""
    file_path = Path(file_path).resolve()
    if output_dir is not None:
        out = Path(output_dir).resolve()
        base_name = file_path.stem
        return out / f"{base_name}.tldr.md.meta"
    local_dir = file_path.parent / ".docs"
    base_name = file_path.name
    return local_dir / f"{base_name}.tldr.md.meta"


def _compute_source_hash(file_path: Path) -> str:
    """SHA256 of file content for freshness check."""
    data = file_path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def _compute_symbol_hash(symbol: SymbolTree, file_path: Path) -> str:
    """SHA256 of symbol's source range for diff-aware patching."""
    snippet = extract_source_snippet(file_path, symbol.lineno, symbol.end_lineno)
    return hashlib.sha256(snippet.encode("utf-8")).hexdigest()


def _read_freshness_meta(meta_path: Path) -> Optional[Dict[str, Any]]:
    """Read .tldr.md.meta JSON. Returns None if missing or invalid."""
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _is_up_to_date(file_path: Path, output_dir: Optional[Path]) -> bool:
    """True if .tldr.md.meta exists and source_hash matches current file."""
    meta_path = _get_tldr_meta_path(file_path, output_dir)
    meta = _read_freshness_meta(meta_path)
    if not meta:
        return False
    current_hash = _compute_source_hash(file_path)
    return meta.get("source_hash") == current_hash


def _module_to_file_path(repo_root: Path, qual: str) -> Optional[Tuple[str, str]]:
    """
    Resolve qualified name (e.g. vivarium.scout.llm.call_groq_async) to (file_path, symbol).
    Returns (repo_relative_path, symbol_name) or None if unresolvable.
    """
    parts = qual.split(".")
    if len(parts) < 2:
        return None
    symbol = parts[-1]  # e.g. call_groq_async
    # Try progressively shorter module paths: vivarium.scout.llm -> vivarium.scout -> vivarium
    for i in range(len(parts) - 1, 0, -1):
        mod = ".".join(parts[:i])
        path_str = mod.replace(".", "/")
        for candidate in [
            repo_root / f"{path_str}.py",
            repo_root / path_str / "__init__.py",
        ]:
            if candidate.exists():
                try:
                    rel = str(candidate.relative_to(repo_root))
                    return (rel, symbol)
                except ValueError:
                    pass
    return None


def export_call_graph(
    target_path: Path,
    *,
    output_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> Path:
    """
    Build and export call graph as JSON (nodes: path::symbol, edges: calls).
    Used by scout-pr for impact analysis.

    Format:
      nodes: { "path::symbol": { "type": "function", "file": "path" } }
      edges: [ { "from": "path::symbol", "to": "path::symbol", "type": "calls" } ]
    """
    target_path = Path(target_path).resolve()
    root = repo_root or Path.cwd().resolve()
    if output_path is None:
        docs_dir = target_path / ".docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        output_path = docs_dir / "call_graph.json"
    output_path = Path(output_path).resolve()

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, str]] = []

    for py_path in target_path.rglob("*.py"):
        if "__pycache__" in str(py_path):
            continue
        try:
            adapter = get_adapter_for_path(py_path, "python")
        except Exception:
            continue
        try:
            root_tree = adapter.parse(py_path)
        except (SyntaxError, UnicodeDecodeError):
            continue

        try:
            rel = str(py_path.relative_to(root))
        except ValueError:
            rel = str(py_path)

        for symbol in root_tree.iter_symbols():
            if symbol.name.startswith("_") and not symbol.name.startswith("__"):
                continue
            node_key = f"{rel}::{symbol.name}"
            if node_key not in nodes:
                nodes[node_key] = {"type": symbol.type, "file": rel}

            for call in getattr(symbol, "calls", None) or []:
                resolved = _module_to_file_path(root, call)
                if resolved:
                    callee_path, callee_sym = resolved
                    callee_key = f"{callee_path}::{callee_sym}"
                    if callee_key not in nodes:
                        nodes[callee_key] = {"type": "function", "file": callee_path}
                    edges.append({"from": node_key, "to": callee_key, "type": "calls"})

    payload = {"nodes": nodes, "edges": edges}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def get_downstream_impact(
    changed_files: List[Path],
    call_graph_path: Path,
    repo_root: Path,
) -> List[str]:
    """
    Given changed files and call_graph.json, return list of module paths
    affected (changed files + their downstream callees).
    """
    if not call_graph_path.exists():
        return []
    try:
        data = json.loads(call_graph_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    def _rel(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(repo_root))
        except ValueError:
            return str(p)

    changed_set: Set[str] = set()
    for f in changed_files:
        if f.suffix == ".py":
            changed_set.add(_rel(f))

    # Build reverse: callee -> callers (we need forward: caller -> callees)
    # Affected = changed files + all files they call (transitively)
    affected: Set[str] = set(changed_set)
    from_to: Dict[str, Set[str]] = {}
    for e in edges:
        fr = e.get("from", "")
        to = e.get("to", "")
        if "::" in fr and "::" in to:
            file_from = fr.split("::", 1)[0]
            file_to = to.split("::", 1)[0]
            if file_from not in from_to:
                from_to[file_from] = set()
            from_to[file_from].add(file_to)

    # Transitive closure: from each changed file, add all reachable callees
    work = list(changed_set)
    while work:
        f = work.pop()
        for callee in from_to.get(f, []):
            if callee not in affected:
                affected.add(callee)
                work.append(callee)

    return sorted(affected)


def export_knowledge_graph(
    target_path: Path,
    *,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Build and export knowledge graph as JSON (nodes: files/funcs/classes, edges: calls/uses/exports).

    Format compatible with Neo4j, Obsidian, or RAG ingestion.
    Returns path to written file.
    """
    target_path = Path(target_path).resolve()
    if output_path is None:
        output_path = target_path / "vivarium.kg.json"
    output_path = Path(output_path).resolve()

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    node_ids: Dict[str, str] = {}

    def _id(typ: str, path: str, name: str = "") -> str:
        key = f"{typ}:{path}:{name}"
        if key not in node_ids:
            nid = f"n{len(node_ids)}"
            node_ids[key] = nid
        return node_ids[key]

    for py_path in target_path.rglob("*.py"):
        if "__pycache__" in str(py_path):
            continue
        try:
            adapter = get_adapter_for_path(py_path, "python")
        except Exception:
            continue
        try:
            root = adapter.parse(py_path)
        except (SyntaxError, UnicodeDecodeError):
            continue

        rel = str(py_path.relative_to(target_path))
        file_id = _id("file", rel)
        nodes.append({
            "id": file_id,
            "type": "file",
            "path": rel,
            "name": py_path.stem,
            "tldr": None,
        })

        for symbol in root.iter_symbols():
            if symbol.name.startswith("_") and not symbol.name.startswith("__"):
                continue
            sym_type = symbol.type
            qual = f"{rel}::{symbol.name}"
            sym_id = _id("symbol", rel, symbol.name)
            nodes.append({
                "id": sym_id,
                "type": sym_type,
                "path": rel,
                "name": symbol.name,
                "qual": qual,
            })
            edges.append({"from": sym_id, "to": file_id, "type": "defined_in"})

            for call in getattr(symbol, "calls", None) or []:
                edges.append({"from": sym_id, "to": call, "type": "calls"})
            for typ in getattr(symbol, "uses_types", None) or []:
                edges.append({"from": sym_id, "to": typ, "type": "uses"})
            for exp in getattr(symbol, "exports", None) or []:
                edges.append({"from": sym_id, "to": exp, "type": "exports"})

    kg = {"nodes": nodes, "edges": edges}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(kg, indent=2), encoding="utf-8")
    return output_path


def find_stale_files(
    target_path: Path,
    *,
    recursive: bool = True,
    output_dir: Optional[Path] = None,
) -> List[Path]:
    """
    Find .py files whose docs are stale (meta exists but source_hash mismatch).

    Returns list of file paths that need reprocessing.
    """
    if not target_path.exists():
        return []
    if target_path.is_file():
        if target_path.suffix == ".py":
            meta = _read_freshness_meta(_get_tldr_meta_path(target_path, output_dir))
            if meta and meta.get("source_hash") != _compute_source_hash(target_path):
                return [target_path]
        return []

    patterns = _DIRECTORY_PATTERNS if recursive else ["*.py", "*.js", "*.mjs", "*.cjs"]
    files: List[Path] = []
    for pattern in patterns:
        for f in target_path.glob(pattern):
            if f.is_file() and "__pycache__" not in str(f) and f.suffix == ".py":
                meta = _read_freshness_meta(_get_tldr_meta_path(f, output_dir))
                if meta and meta.get("source_hash") != _compute_source_hash(f):
                    files.append(f)
    return files


def _write_freshness_meta(
    meta_path: Path,
    source_hash: str,
    model: str,
    symbols: Optional[Dict[str, Dict[str, str]]] = None,
) -> None:
    """Write .tldr.md.meta. Not mirrored to docs/livingDoc/."""
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta: Dict[str, Any] = {
        "source_hash": source_hash,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
    }
    if symbols:
        meta["symbols"] = symbols
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


# Fallback models when config does not specify
TLDR_MODEL = "llama-3.1-8b-instant"
DEEP_MODEL = "llama-3.1-8b-instant"
ELIV_MODEL = "llama-3.1-8b-instant"


def _resolve_doc_model(kind: str) -> str:
    """Resolve model from config (models.tldr, models.deep, models.eliv, models.pr_synthesis)."""
    config = ScoutConfig()
    models = config.get("models") or {}
    model = models.get(kind)
    if model:
        return model
    fallbacks = {
        "tldr": TLDR_MODEL,
        "deep": DEEP_MODEL,
        "eliv": ELIV_MODEL,
        "pr_synthesis": TLDR_MODEL,
    }
    return fallbacks.get(kind, TLDR_MODEL)

# File extensions to process in directory mode (Python + JavaScript + common fallbacks)
_DIRECTORY_PATTERNS = ["**/*.py", "**/*.js", "**/*.mjs", "**/*.cjs"]

# Path to groq model specs (relative to this package)
_GROQ_SPECS_PATH = Path(__file__).parent / "config" / "groq_model_specs.json"

_groq_specs_cache: Optional[Dict[str, Any]] = None


def get_model_specs() -> Dict[str, Any]:
    """Load groq_model_specs.json. Cached after first load."""
    global _groq_specs_cache
    if _groq_specs_cache is not None:
        return _groq_specs_cache
    if _GROQ_SPECS_PATH.exists():
        try:
            with open(_GROQ_SPECS_PATH, encoding="utf-8") as f:
                _groq_specs_cache = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Could not load groq_model_specs.json: %s", e)
    _groq_specs_cache = _groq_specs_cache or {}
    return _groq_specs_cache


def _safe_workers_from_rpm(model_name: str, rpm: int) -> int:
    """Compute safe worker count: 80% of RPM, divided by 60 (per sec) and 3 (tldr/deep/eliv per file)."""
    safe = max(1, int((rpm * 0.8) / 60 / 3))
    return safe


def _max_concurrent_from_rpm(rpm: int) -> int:
    """Max concurrent LLM calls to stay just below rate limit.
    Assumes ~2 sec avg latency: rpm/60 req/sec * 2 sec ≈ rpm/30 in-flight. Use 85% for safety."""
    return min(100, max(1, int(rpm * 0.85 / 30)))


def _default_workers() -> int:
    """Default max concurrent LLM calls: min(8, cpu_count)."""
    n = os.cpu_count()
    return min(8, n if n is not None else 1)


def extract_source_snippet(file_path: Path, start_line: int, end_line: int) -> str:
    """
    Read a file and return the raw source code lines between
    start_line and end_line inclusive.

    Args:
        file_path: Path to the file to read.
        start_line: First line number (1-indexed, inclusive).
        end_line: Last line number (1-indexed, inclusive).

    Returns:
        The source code snippet as a string, preserving original line endings.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be read.
        UnicodeDecodeError: If the file cannot be decoded as UTF-8.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="strict") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except OSError as e:
        raise IOError(f"Could not read file {file_path}: {e}") from e
    except UnicodeDecodeError:
        raise

    if not lines:
        return ""

    start_idx = max(0, min(start_line - 1, len(lines) - 1))
    end_idx = max(0, min(end_line - 1, len(lines) - 1))
    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx

    return "".join(lines[start_idx : end_idx + 1])


def _fallback_template_content(symbol: SymbolTree, kind: str) -> str:
    """
    Generate template doc content when LLM fails or budget exceeded.
    Returns [FALLBACK] header + template. kind: tldr, deep, eliv.
    """
    sig = getattr(symbol, "signature", None) or f"{symbol.name}(...)"
    args = "?"
    if "(" in sig:
        try:
            args = sig.split("(", 1)[1].rsplit(")", 1)[0] or "..."
        except IndexError:
            args = "..."
    call_list = ", ".join((symbol.calls or [])[:10]) or "none"
    type_list = ", ".join((symbol.uses_types or [])[:10]) or "none"
    header = "[FALLBACK]\n\n"
    if kind == "tldr":
        return f"{header}[AUTO] {symbol.name}({args}) → ?\nCalls: {call_list}\nTypes: {type_list}"
    if kind == "deep":
        return f"{header}[AUTO] {symbol.name}({args})\nCalls: {call_list}\nTypes: {type_list}\n\n(Generated from template; LLM unavailable.)"
    if kind == "eliv":
        return f"{header}{symbol.name} does something with {call_list or 'nothing'}."
    return f"{header}{symbol.name}"


def validate_generated_docs(
    symbol: SymbolTree | Dict[str, Any],
    tldr_content: str,
    deep_content: str,
) -> Tuple[bool, List[str]]:
    """
    Validate generated documentation content for a symbol.

    Args:
        symbol: SymbolTree or dict (for context in error messages).
        tldr_content: Generated TL;DR content.
        deep_content: Generated deep content.

    Returns:
        (is_valid, list of error messages).
    """
    errors: List[str] = []
    name = symbol.name if isinstance(symbol, SymbolTree) else symbol.get("name", "?")

    if not tldr_content or not tldr_content.strip():
        errors.append(f"TL;DR content is empty for symbol '{name}'")
    elif tldr_content.strip().startswith("[TL;DR generation failed:"):
        errors.append(f"TL;DR generation failed for symbol '{name}'")
    elif len(tldr_content) > 100_000:
        errors.append(f"TL;DR content exceeds size limit for symbol '{name}'")

    if not deep_content or not deep_content.strip():
        errors.append(f"Deep content is empty for symbol '{name}'")
    elif deep_content.strip().startswith("[Deep content generation failed:"):
        errors.append(f"Deep content generation failed for symbol '{name}'")
    elif len(deep_content) > 500_000:
        errors.append(f"Deep content exceeds size limit for symbol '{name}'")

    return (len(errors) == 0, errors)


def write_documentation_files(
    file_path: Path,
    tldr_content: str,
    deep_content: str,
    eliv_content: str = "",
    output_dir: Optional[Path] = None,
    generate_eliv: bool = True,
    versioned_mirror_dir: Optional[Path] = None,
) -> Tuple[Path, Path, Path]:
    """
    Write documentation files for a source file.

    If output_dir is provided:
        Writes <stem>.tldr.md, <stem>.deep.md, and <name>.eliv.md inside output_dir.
    If output_dir is None (default):
        Writes to local .docs/ next to source and mirrors to central docs/livingDoc/.

    If versioned_mirror_dir is set (e.g. docs/livingDoc/v0.1.0-dev/), also mirrors there.

    Returns:
        Tuple of (tldr_path, deep_path, eliv_path) for the primary (local) files.
        When generate_eliv is False, eliv_path is still returned but not written.
    """
    file_path = Path(file_path).resolve()
    repo_root = Path.cwd().resolve()

    if output_dir is not None:
        out = Path(output_dir).resolve()
        out.mkdir(parents=True, exist_ok=True)
        base_name = file_path.stem
        tldr_path = out / f"{base_name}.tldr.md"
        deep_path = out / f"{base_name}.deep.md"
        eliv_path = (out / file_path.name).with_suffix(file_path.suffix + ".eliv.md")
        mirror_to_central = False
    else:
        local_dir = file_path.parent / ".docs"
        local_dir.mkdir(parents=True, exist_ok=True)
        base_name = file_path.name
        tldr_path = local_dir / f"{base_name}.tldr.md"
        deep_path = local_dir / f"{base_name}.deep.md"
        eliv_path = local_dir / f"{base_name}.eliv.md"
        mirror_to_central = True

    tldr_path.write_text(tldr_content, encoding="utf-8")
    deep_path.write_text(deep_content, encoding="utf-8")
    if generate_eliv:
        eliv_path.write_text(eliv_content, encoding="utf-8")

    if mirror_to_central:
        try:
            rel = file_path.relative_to(repo_root)
            central_dir = repo_root / "docs" / "livingDoc" / rel.parent
            central_dir.mkdir(parents=True, exist_ok=True)
            central_tldr = central_dir / f"{file_path.name}.tldr.md"
            central_deep = central_dir / f"{file_path.name}.deep.md"
            central_eliv = central_dir / f"{file_path.name}.eliv.md"
            central_tldr.write_text(tldr_content, encoding="utf-8")
            central_deep.write_text(deep_content, encoding="utf-8")
            if generate_eliv:
                central_eliv.write_text(eliv_content, encoding="utf-8")
            if versioned_mirror_dir is not None:
                try:
                    vdir = versioned_mirror_dir / rel.parent
                    vdir.mkdir(parents=True, exist_ok=True)
                    (vdir / f"{file_path.name}.tldr.md").write_text(tldr_content, encoding="utf-8")
                    (vdir / f"{file_path.name}.deep.md").write_text(deep_content, encoding="utf-8")
                    if generate_eliv:
                        (vdir / f"{file_path.name}.eliv.md").write_text(eliv_content, encoding="utf-8")
                except (ValueError, OSError) as e:
                    logger.warning("Could not mirror to versioned dir for %s: %s", file_path, e)
        except (ValueError, OSError) as e:
            logger.warning(
                "Could not mirror docs to docs/livingDoc/ for %s: %s",
                file_path,
                e,
            )

    return (tldr_path, deep_path, eliv_path)


async def _generate_single_symbol_docs(
    adapter: Any,
    symbol: SymbolTree,
    dependencies: List[str],
    source_snippet: str,
    semaphore: asyncio.Semaphore,
    generate_eliv: bool = True,
    fallback_template: bool = False,
) -> Tuple[str, bool, str, str, str, float, str]:
    """
    Generate TL;DR, deep, and ELIV content for a single symbol using the adapter.

    Returns:
        Tuple of (symbol_name, is_valid, tldr_content, deep_content, eliv_content, cost_usd, model).
    """
    cost_usd = 0.0
    model_used = _resolve_doc_model("tldr")

    async with semaphore:
        # TL;DR — try auto-generation for simple symbols (skip LLM)
        tldr_content = None
        if hasattr(adapter, "try_auto_tldr"):
            tldr_content = adapter.try_auto_tldr(symbol, source_snippet)
        if tldr_content is not None:
            audit = AuditLog()
            audit.log(
                "tldr_auto_generated",
                cost=0.0,
                symbol=symbol.name,
            )
        else:
            try:
                tldr_prompt = adapter.get_tldr_prompt(symbol, dependencies)
                tldr_response = await call_groq_async(
                    tldr_prompt,
                    model=_resolve_doc_model("tldr"),
                    system="You are a documentation assistant. Be concise and accurate.",
                )
                tldr_content = tldr_response.content
                cost_usd += tldr_response.cost_usd
                model_used = tldr_response.model
                audit = AuditLog()
                audit.log(
                    "tldr",
                    cost=tldr_response.cost_usd,
                    model=tldr_response.model,
                    input_t=tldr_response.input_tokens,
                    output_t=tldr_response.output_tokens,
                    symbol=symbol.name,
                )
            except RuntimeError:
                raise
            except Exception as e:
                logger.warning("TL;DR generation failed for %s: %s", symbol.name, e)
                if fallback_template:
                    tldr_content = _fallback_template_content(symbol, "tldr")
                    AuditLog().log("tldr_fallback_template", cost=0.0, symbol=symbol.name)
                else:
                    tldr_content = f"[TL;DR generation failed: {e}]"

        # Deep
        try:
            deep_prompt = adapter.get_deep_prompt(symbol, dependencies, source_snippet)
            deep_response = await call_groq_async(
                deep_prompt,
                model=_resolve_doc_model("deep"),
                system="You are a documentation assistant. Provide structured, detailed analysis of code.",
                max_tokens=1500,
            )
            deep_content = deep_response.content
            cost_usd += deep_response.cost_usd
            model_used = deep_response.model
            audit = AuditLog()
            audit.log(
                "deep",
                cost=deep_response.cost_usd,
                model=deep_response.model,
                input_t=deep_response.input_tokens,
                output_t=deep_response.output_tokens,
                symbol=symbol.name,
            )
        except RuntimeError:
            raise
        except Exception as e:
            logger.warning("Deep content generation failed for %s: %s", symbol.name, e)
            if fallback_template:
                deep_content = _fallback_template_content(symbol, "deep")
                AuditLog().log("deep_fallback_template", cost=0.0, symbol=symbol.name)
            else:
                deep_content = f"[Deep content generation failed: {e}]"

        # ELIV (skip if generate_eliv disabled)
        eliv_content = ""
        if generate_eliv:
            try:
                eliv_prompt = adapter.get_eliv_prompt(symbol, dependencies, source_snippet)
                eliv_response = await call_groq_async(
                    eliv_prompt,
                    model=_resolve_doc_model("eliv"),
                    system="You are a friendly assistant that explains code in very simple terms for young children.",
                    max_tokens=450,
                )
                eliv_content = eliv_response.content
                cost_usd += eliv_response.cost_usd
                model_used = eliv_response.model
                audit = AuditLog()
                audit.log(
                    "eliv",
                    cost=eliv_response.cost_usd,
                    model=eliv_response.model,
                    input_t=eliv_response.input_tokens,
                    output_t=eliv_response.output_tokens,
                    symbol=symbol.name,
                )
            except RuntimeError:
                raise
            except Exception as e:
                logger.warning("ELIV generation failed for %s: %s", symbol.name, e)
                if fallback_template:
                    eliv_content = _fallback_template_content(symbol, "eliv")
                    AuditLog().log("eliv_fallback_template", cost=0.0, symbol=symbol.name)
                else:
                    eliv_content = f"[ELIV generation failed: {e}]"

        is_valid, errors = validate_generated_docs(symbol, tldr_content, deep_content)
        if not is_valid:
            for err in errors:
                logger.warning("Validation failed for %s: %s", symbol.name, err)

        return (symbol.name, is_valid, tldr_content, deep_content, eliv_content, cost_usd, model_used)


def _merge_symbol_content(
    symbols: List[SymbolTree],
    cached: Dict[str, Dict[str, str]],
    generated: Dict[str, Tuple[str, str, str]],
) -> Tuple[str, str, str, Dict[str, Dict[str, str]]]:
    """Merge cached + generated per-symbol content in symbol order. Return aggregated docs + symbols_for_meta."""
    tldr_agg = ""
    deep_agg = ""
    eliv_agg = ""
    symbols_for_meta: Dict[str, Dict[str, str]] = {}

    for symbol in symbols:
        name = symbol.name
        if name in generated:
            tldr_c, deep_c, eliv_c = generated[name]
        elif name in cached:
            tldr_c = cached[name].get("tldr", "")
            deep_c = cached[name].get("deep", "")
            eliv_c = cached[name].get("eliv", "")
        else:
            continue

        header = f"# {name}\n\n"
        if tldr_agg:
            tldr_agg += "\n---\n\n"
        tldr_agg += header + tldr_c
        if deep_agg:
            deep_agg += "\n---\n\n"
        deep_agg += header + deep_c
        if eliv_agg:
            eliv_agg += "\n---\n\n"
        eliv_agg += f"# {name} ELIV\n\n{eliv_c}"

        symbols_for_meta[name] = {
            "tldr": tldr_c,
            "deep": deep_c,
            "eliv": eliv_c,
        }

    return (tldr_agg, deep_agg, eliv_agg, symbols_for_meta)


async def _generate_docs_for_symbols(
    target_path: Path,
    trace: TraceResult,
    *,
    output_dir: Optional[Path] = None,
    generate_eliv: bool = True,
    per_file_concurrency: int = 3,
    slot_id: Optional[int] = None,
    shared_display: Optional[Dict[str, Any]] = None,
    progress_callback: Optional[Callable[[float], None]] = None,
    fallback_template: bool = False,
) -> Tuple[str, str, str, float, str, Dict[str, Dict[str, str]]]:
    """
    Generate docs via LLM for traced symbols. Diff-aware: only re-generate for symbols whose hash changed.

    Returns (tldr_agg, deep_agg, eliv_agg, total_cost, model_used, symbols_for_meta).
    symbols_for_meta: {name: {hash, tldr, deep, eliv}} for persistence.
    """
    symbols_to_doc = trace.symbols_to_doc
    adapter = trace.adapter
    dependencies = trace.dependencies

    meta_path = _get_tldr_meta_path(target_path, output_dir)
    meta = _read_freshness_meta(meta_path)
    meta_symbols = (meta or {}).get("symbols") or {}

    # Partition: unchanged (reuse from meta) vs changed (generate)
    to_reuse: Dict[str, Dict[str, str]] = {}
    to_generate: List[SymbolTree] = []

    for symbol in symbols_to_doc:
        current_hash = _compute_symbol_hash(symbol, target_path)
        prev = meta_symbols.get(symbol.name)
        if prev and prev.get("hash") == current_hash:
            to_reuse[symbol.name] = {
                "hash": current_hash,
                "tldr": prev.get("tldr", ""),
                "deep": prev.get("deep", ""),
                "eliv": prev.get("eliv", ""),
            }
        else:
            to_generate.append(symbol)

    if to_reuse or to_generate:
        logger.debug(
            "Diff-aware: %d reused, %d to generate",
            len(to_reuse),
            len(to_generate),
        )

    per_file_semaphore = asyncio.Semaphore(per_file_concurrency)
    running_cost = [0.0]

    # Show symbol-level progress for large files so users know it's not frozen
    if slot_id is not None and shared_display is not None and slot_id in shared_display:
        shared_display[slot_id]["symbols_total"] = len(to_generate)
        shared_display[slot_id]["symbols_done"] = 0

    def _on_symbol_done(sym_cost: float) -> None:
        running_cost[0] += sym_cost
        if progress_callback:
            progress_callback(running_cost[0])
        if slot_id is not None and shared_display is not None and slot_id in shared_display:
            shared_display[slot_id]["cost"] = running_cost[0]
            shared_display[slot_id]["symbols_done"] = (
                shared_display[slot_id].get("symbols_done", 0) + 1
            )

    async def _wrapped(symbol: SymbolTree) -> Tuple[str, str, str, str, float, str]:
        res = await _generate_single_symbol_docs(
            adapter,
            symbol,
            symbol.dependencies if symbol.dependencies else dependencies,
            extract_source_snippet(target_path, symbol.lineno, symbol.end_lineno),
            per_file_semaphore,
            generate_eliv,
            fallback_template=fallback_template,
        )
        _on_symbol_done(res[5])
        return (res[0], res[2], res[3], res[4], res[5], res[6])

    generated: Dict[str, Tuple[str, str, str]] = {}
    total_cost = 0.0
    model_used = _resolve_doc_model("tldr")

    if to_generate:
        tasks = [asyncio.create_task(_wrapped(s)) for s in to_generate]
        results = await asyncio.gather(*tasks)

        for (symbol, res) in zip(to_generate, results):
            sym_name, tldr_content, deep_content, eliv_content, sym_cost, sym_model = res
            total_cost += sym_cost
            if sym_model:
                model_used = sym_model
            generated[sym_name] = (tldr_content, deep_content, eliv_content)

    # Merge cached (to_reuse) + generated, preserving symbol order
    cached_for_merge: Dict[str, Dict[str, str]] = {}
    for name, data in to_reuse.items():
        cached_for_merge[name] = {
            "tldr": data["tldr"],
            "deep": data["deep"],
            "eliv": data["eliv"],
        }

    tldr_agg, deep_agg, eliv_agg, symbols_for_meta = _merge_symbol_content(
        symbols_to_doc, cached_for_merge, generated
    )

    # Add hashes to symbols_for_meta for persistence
    for symbol in symbols_to_doc:
        name = symbol.name
        if name in symbols_for_meta:
            symbols_for_meta[name]["hash"] = _compute_symbol_hash(symbol, target_path)

    return (tldr_agg, deep_agg, eliv_agg, total_cost, model_used, symbols_for_meta)


def _rel_path_for_display(path: Path) -> str:
    """Return path relative to cwd for compact display."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def _trace_file(
    target_path: Path,
    *,
    language_override: Optional[str] = None,
    dependencies_func: Optional[Callable[[Path], List[str]]] = None,
    slot_id: Optional[int] = None,
    shared_display: Optional[Dict[str, Any]] = None,
) -> TraceResult:
    """
    Pure static analysis: AST + import map. No LLM calls.

    Returns SymbolTree with calls, types, exports. Updates dashboard with
    live call chain immediately (tracing is instant).
    """
    adapter = get_adapter_for_path(target_path, language_override)
    root_tree = adapter.parse(target_path)

    dependencies: List[str] = []
    if dependencies_func:
        dependencies = dependencies_func(target_path) or []

    symbols_to_doc: List[SymbolTree] = []
    for child in root_tree.children:
        symbols_to_doc.extend(list(child.iter_symbols()))
    if not symbols_to_doc:
        symbols_to_doc = [root_tree]

    all_calls: set = set()
    all_types: set = set()
    all_exports: set = set()
    for s in symbols_to_doc:
        all_calls.update(s.calls or [])
        all_types.add(s.type)
        all_exports.update(s.exports or [])
    root_exports = getattr(root_tree, "exports", None) or []
    all_exports.update(root_exports)

    chain = _build_rolling_call_trace(symbols_to_doc)
    if slot_id is not None and shared_display is not None:
        rel = _rel_path_for_display(target_path)
        shared_display[slot_id] = {
            "file": rel,
            "chain": chain or "…",
            "cost": 0.0,
            "status": "running",
            "pulse_hop": None,
        }

    return TraceResult(
        root_tree=root_tree,
        symbols_to_doc=symbols_to_doc,
        all_calls=all_calls,
        all_types=all_types,
        all_exports=all_exports,
        adapter=adapter,
        dependencies=dependencies,
    )


# ANSI colors for tagged hops in rolling trace (blue, magenta, cyan, green, yellow)
_TRACE_COLORS = ("\033[34m", "\033[35m", "\033[36m", "\033[32m", "\033[33m")
_MAX_CHAIN_LEN = 80
_ARROW = "\u27F6"  # ⟶

def _strip_ansi(s: str) -> str:
    """Return string with ANSI codes removed, for length calculation."""
    result = []
    i = 0
    while i < len(s):
        if s[i] == "\033" and i + 1 < len(s) and s[i + 1] == "[":
            j = i + 2
            while j < len(s) and s[j] != "m":
                j += 1
            i = j + 1
            continue
        result.append(s[i])
        i += 1
    return "".join(result)


def _build_rolling_call_trace(symbols_to_doc: List[SymbolTree]) -> Optional[str]:
    """
    Build a colorized, tagged rolling call chain for display.

    Collects all qualified calls from the file, tags each by module, colorizes,
    and truncates from the left if over 80 chars to keep latest context visible.
    """
    def _skip_call(qname: str) -> bool:
        parts = qname.split(".")
        last = parts[-1] if parts else ""
        return last == "__init__" or last.startswith("_")

    # Collect all calls in file order (entrypoint first, then calls per symbol)
    hops: List[str] = []
    seen: set = set()

    for symbol in symbols_to_doc:
        if symbol.name.startswith("_") and not symbol.name.startswith("__"):
            continue
        if symbol.name == "__init__":
            continue
        # Add entrypoint on first symbol with calls
        if not hops and (symbol.calls or []):
            hops.append(symbol.name)
        for qname in symbol.calls or []:
            if _skip_call(qname) or qname in seen:
                continue
            seen.add(qname)
            parts = qname.split(".")
            if len(parts) >= 2:
                module = parts[-2]
                func = parts[-1]
                tag = module[:3] if len(module) > 3 else module  # doc, llm, aud
            else:
                tag, func = "", qname

            color_idx = hash(tag) % len(_TRACE_COLORS) if tag else 0
            color = _TRACE_COLORS[color_idx]
            hop_str = f"{color}[{tag}]{_RESET} {func}" if tag else func
            hops.append(hop_str)

    if not hops:
        return None

    chain = f" {_ARROW} ".join(hops)

    # Truncate from left until it fits (keep latest context visible)
    while len(_strip_ansi(chain)) > _MAX_CHAIN_LEN and len(hops) > 1:
        hops = hops[1:]
        chain = f" {_ARROW} ".join(hops)

    return chain if chain else None


def _format_single_hop(qname: str) -> Optional[Tuple[str, str]]:
    """Format a qualified call to (tag, hop_str). Returns None if skip."""
    parts = qname.split(".")
    last = parts[-1] if parts else ""
    if last == "__init__" or last.startswith("_"):
        return None
    if len(parts) >= 2:
        module, func = parts[-2], parts[-1]
        tag = module[:3] if len(module) > 3 else module
        color_idx = hash(tag) % len(_TRACE_COLORS)
        hop_str = f"{_TRACE_COLORS[color_idx]}[{tag}]{_RESET} {func}"
        return (tag, hop_str)
    return ("", qname)


def _build_chain_from_hops(entrypoint: str, hop_strs: List[str]) -> str:
    """Build chain from entrypoint + hop strings, truncate from left if > 80 chars."""
    if not hop_strs:
        return entrypoint
    hops = [entrypoint] + hop_strs
    chain = f" {_ARROW} ".join(hops)
    while len(_strip_ansi(chain)) > _MAX_CHAIN_LEN and len(hops) > 1:
        hops = hops[1:]
        chain = f" {_ARROW} ".join(hops)
    return chain


async def process_single_file_async(
    target_path: Path,
    *,
    output_dir: Optional[Path] = None,
    dependencies_func: Optional[Callable[[Path], List[str]]] = None,
    per_file_concurrency: int = 3,
    language_override: Optional[str] = None,
    generate_eliv: Optional[bool] = None,
    quiet: bool = False,
    force: bool = False,
    slot_id: Optional[int] = None,
    shared_display: Optional[Dict[str, Any]] = None,
    progress_callback: Optional[Callable[[float], None]] = None,
    fallback_template: bool = False,
    versioned_mirror_dir: Optional[Path] = None,
) -> FileProcessResult:
    """
    Process a single file for documentation generation (async).

    Phase 0: freshness check — skip if up to date (unless --force).
    Phase 1: _trace_file() — pure static analysis, instant chain in dashboard.
    Phase 2: _generate_docs_for_symbols() — LLM only, updates cost in dashboard.
    """
    if not target_path.exists() or not target_path.is_file():
        raise FileNotFoundError(f"Target file not found: {target_path}")

    # Phase 0: skip if up to date (hash-based freshness)
    if not force and _is_up_to_date(target_path, output_dir):
        if slot_id is not None and shared_display is not None:
            rel = _rel_path_for_display(target_path)
            shared_display[slot_id] = {
                "file": rel,
                "chain": None,
                "cost": 0.0,
                "status": "done",
                "success": True,
                "skipped": True,
            }
        if not quiet:
            rel = _rel_path_for_display(target_path)
            print(f"✓ {rel} (up to date)", file=sys.stdout)
        return FileProcessResult(
            success=True,
            cost_usd=0.0,
            symbols_count=0,
            calls_count=0,
            types_count=0,
            exports_count=0,
            model="",
            skipped=True,
        )

    if generate_eliv is None:
        config = ScoutConfig()
        doc_gen = config.get("doc_generation") or {}
        generate_eliv = doc_gen.get("generate_eliv", True)

    # Phase 1: pure static analysis — instant, no LLM
    try:
        trace = _trace_file(
            target_path,
            language_override=language_override,
            dependencies_func=dependencies_func,
            slot_id=slot_id,
            shared_display=shared_display,
        )
    except (ValueError, SyntaxError, UnicodeDecodeError, IOError) as e:
        logger.warning("Parse error for %s: %s", target_path, e)
        if slot_id is not None and shared_display is not None:
            shared_display[slot_id] = {
                "file": _rel_path_for_display(target_path),
                "chain": None,
                "cost": 0.0,
                "status": "done",
                "success": False,
                "error": str(e),
            }
        if not quiet:
            rel = _rel_path_for_display(target_path)
            print(f"{_RED}✗ {rel}: {e}{_RESET}", file=sys.stderr)
        return FileProcessResult(
            success=False,
            cost_usd=0.0,
            symbols_count=0,
            calls_count=0,
            types_count=0,
            exports_count=0,
            model="",
            error=str(e),
        )

    symbols_to_doc = trace.symbols_to_doc
    all_calls = trace.all_calls
    all_types = trace.all_types
    all_exports = trace.all_exports

    # Phase 2: LLM doc generation — diff-aware, only changed symbols
    tldr_agg_content, deep_agg_content, eliv_agg_content, total_cost, model_used, symbols_for_meta = (
        await _generate_docs_for_symbols(
            target_path,
            trace,
            output_dir=output_dir,
            generate_eliv=generate_eliv,
            per_file_concurrency=per_file_concurrency,
            fallback_template=fallback_template,
            slot_id=slot_id,
            shared_display=shared_display,
            progress_callback=progress_callback,
        )
    )

    if not tldr_agg_content.strip() and not deep_agg_content.strip():
        msg = (
            f"No valid content to write for {target_path}: "
            "all symbols failed validation (empty LLM response or generation error)."
        )
        logger.warning(msg)
        if slot_id is not None and shared_display is not None and slot_id in shared_display:
            shared_display[slot_id]["cost"] = total_cost
            shared_display[slot_id]["status"] = "done"
            shared_display[slot_id]["success"] = False
            shared_display[slot_id]["error"] = msg
        if not quiet:
            rel = _rel_path_for_display(target_path)
            print(f"{_RED}✗ {rel}: {msg}{_RESET}", file=sys.stderr)
        return FileProcessResult(
            success=False,
            cost_usd=total_cost,
            symbols_count=len(symbols_to_doc),
            calls_count=len(all_calls),
            types_count=len(all_types),
            exports_count=len(all_exports),
            model=model_used,
            error=msg,
        )

    tldr_path, deep_path, eliv_path = write_documentation_files(
        target_path,
        tldr_agg_content,
        deep_agg_content,
        eliv_agg_content,
        output_dir,
        generate_eliv,
        versioned_mirror_dir=versioned_mirror_dir,
    )
    logger.info("Wrote %s, %s, and %s", tldr_path, deep_path, eliv_path)

    # Write freshness meta with per-symbol hashes (not mirrored to docs/livingDoc/)
    meta_path = _get_tldr_meta_path(target_path, output_dir)
    _write_freshness_meta(
        meta_path,
        _compute_source_hash(target_path),
        model_used,
        symbols=symbols_for_meta,
    )

    call_chain = _build_rolling_call_trace(symbols_to_doc)
    result = FileProcessResult(
        success=True,
        cost_usd=total_cost,
        symbols_count=len(symbols_to_doc),
        calls_count=len(all_calls),
        types_count=len(all_types),
        exports_count=len(all_exports),
        model=model_used,
        call_chain=call_chain,
    )

    if slot_id is not None and shared_display is not None and slot_id in shared_display:
        shared_display[slot_id]["cost"] = total_cost
        shared_display[slot_id]["status"] = "done"
        shared_display[slot_id]["success"] = True
        shared_display[slot_id]["chain"] = call_chain  # final chain (canonical order)
        shared_display[slot_id]["pulse_hop"] = None  # clear pulse for done

    if not quiet:
        rel = _rel_path_for_display(target_path)
        if call_chain:
            line = f"✔ {rel} ━╸ {call_chain} | {model_used} | ${total_cost:.4f}"
        else:
            line = (
                f"✔ {rel} — traced {len(all_calls)} calls, {len(all_types)} types, "
                f"{len(all_exports)} exports | {model_used} | ${total_cost:.4f}"
            )
        print(line, file=sys.stdout)

    return result


def process_single_file(
    target_path: Path,
    *,
    output_dir: Optional[Path] = None,
    dependencies_func: Optional[Callable[[Path], List[str]]] = None,
    language_override: Optional[str] = None,
    quiet: bool = False,
) -> bool:
    """
    Process a single file for documentation generation (sync wrapper).

    Args:
        target_path: Path to the file to process.
        output_dir: Optional directory to write generated docs.
        dependencies_func: Optional function to resolve dependencies.
        language_override: Optional explicit language (e.g., "python", "javascript").
        quiet: If True, suppress completion line output.

    Returns:
        True if parsing and writing succeeded, False otherwise.
    """
    result = asyncio.run(
        process_single_file_async(
            target_path,
            output_dir=output_dir,
            dependencies_func=dependencies_func,
            language_override=language_override,
            quiet=quiet,
        )
    )
    return result.success


def _gather_package_component_roles(package_dir: Path, repo_root: Path) -> List[str]:
    """Parse each .py file in package to extract exports and top-level calls for truth-based cascading."""
    lines: List[str] = []
    for py_path in sorted(package_dir.glob("*.py")):
        if py_path.name.startswith("_"):
            continue
        try:
            adapter = get_adapter_for_path(py_path, "python")
            root = adapter.parse(py_path)
            exports = getattr(root, "exports", None) or []
            exports_str = ", ".join(exports) if exports else "(top-level defs/classes)"
            all_calls: List[str] = []
            for child in root.children:
                calls = getattr(child, "calls", None) or []
                all_calls.extend(calls)
            seen: set = set()
            unique_calls = [c for c in all_calls if c not in seen and not seen.add(c)]
            calls_str = ", ".join(unique_calls[:12]) if unique_calls else "(none traced)"
            lines.append(f"- {py_path.name}: Exports {exports_str}. Calls: {calls_str}")
        except Exception as e:
            logger.debug("Skip tracing %s: %s", py_path, e)
    return lines


async def _update_module_brief_async(package_dir: Path, repo_root: Path) -> bool:
    """
    Generate module-level brief (__init__.py.module.md) from real component roles + child .tldr.md.

    Truth-based cascading: uses traced exports/calls from each file, then synthesizes orchestration.
    Async: uses await call_groq_async (no asyncio.run nesting).
    """
    config = ScoutConfig()
    drafts = config.get("drafts") or {}
    if not drafts.get("enable_module_briefs", True):
        return False

    ignore = IgnorePatterns(repo_root=repo_root)
    init_py = package_dir / "__init__.py"
    if not init_py.exists():
        return False

    try:
        rel = package_dir.relative_to(repo_root)
    except ValueError:
        return False

    if ignore.matches(package_dir, repo_root):
        return False

    docs_dir = package_dir / ".docs"
    if not docs_dir.exists():
        return False

    component_roles = _gather_package_component_roles(package_dir, repo_root)
    roles_block = "\n".join(component_roles) if component_roles else "(no traced components)"

    tldr_parts: List[str] = []
    for md in sorted(docs_dir.glob("*.tldr.md")):
        try:
            tldr_parts.append(f"### {md.stem}\n\n{md.read_text(encoding='utf-8', errors='replace')}")
        except OSError:
            pass

    if not tldr_parts:
        return False

    combined = "\n\n".join(tldr_parts)
    if len(combined) > 8000:
        combined = combined[:8000] + "\n\n[... truncated ...]"

    module_name = ".".join(rel.parts)
    prompt = f"""Synthesize a package overview from REAL component roles. Do not guess.

Package: {module_name}
Path: {rel}

Component roles (traced from call graph):
{roles_block}

Child summaries (.tldr.md) for context:
{combined}

Output a concise Markdown overview with ## headings:
1. ## Purpose — What this package does (one sentence).
2. ## Components — Ingress/Processing/Egress: which file handles what (from traced roles).
3. ## Key Invariants — Constraints from the code (e.g. plain-text Git workflow, no external deps).
Use only facts from the traced roles and summaries. No speculation."""

    system = "You are a documentation assistant. Be concise and accurate."
    use_big_brain = bool(os.environ.get("GEMINI_API_KEY"))
    try:
        if use_big_brain:
            response = await call_big_brain_async(
                prompt,
                system=system,
                max_tokens=800,
                task_type="module_brief",
            )
        else:
            response = await call_groq_async(
                prompt,
                model=_resolve_doc_model("tldr"),
                system=system,
                max_tokens=800,
            )
    except Exception as e:
        logger.warning("Module brief LLM failed for %s: %s", package_dir, e)
        return False

    if not use_big_brain:
        audit = AuditLog()
        audit.log(
            "module_brief",
            cost=response.cost_usd,
            model=response.model,
            package=str(rel),
        )

    content = response.content.strip()
    module_md_name = "__init__.py.module.md"
    local_path = docs_dir / module_md_name
    central_dir = repo_root / "docs" / "livingDoc" / rel
    central_dir.mkdir(parents=True, exist_ok=True)
    central_path = central_dir / module_md_name
    try:
        local_path.write_text(content, encoding="utf-8")
        central_path.write_text(content, encoding="utf-8")
        logger.info("Wrote module brief: %s (mirrored to %s)", local_path, central_path)
    except OSError as e:
        logger.warning("Could not write module brief for %s: %s", package_dir, e)
        return False
    return True


def _update_module_brief(package_dir: Path, repo_root: Path, *, is_async: bool = False):
    """
    Sync wrapper for _update_module_brief_async.
    is_async=False (default): uses asyncio.run for CLI/sync callers.
    is_async=True: returns coroutine for caller to await (use _update_module_brief_async directly instead).
    """
    if is_async:
        return _update_module_brief_async(package_dir, repo_root)
    return asyncio.run(_update_module_brief_async(package_dir, repo_root))


async def _process_file_with_semaphore(
    semaphore: asyncio.Semaphore,
    file_path: Path,
    *,
    output_dir: Optional[Path] = None,
    dependencies_func: Optional[Callable[[Path], List[str]]] = None,
    language_override: Optional[str] = None,
    generate_eliv: Optional[bool] = None,
    quiet: bool = False,
    force: bool = False,
    slot_queue: Optional[asyncio.Queue] = None,
    shared_display: Optional[Dict[str, Any]] = None,
    fallback_template: bool = False,
    versioned_mirror_dir: Optional[Path] = None,
) -> FileProcessResult:
    """Process a single file with semaphore for concurrency control."""
    async with semaphore:
        slot_id = None
        if slot_queue is not None:
            slot_id = await slot_queue.get()
        try:
            def _progress_cb(cost: float) -> None:
                if slot_id is not None and shared_display is not None and slot_id in shared_display:
                    shared_display[slot_id]["cost"] = cost

            return await process_single_file_async(
                file_path,
                output_dir=output_dir,
                dependencies_func=dependencies_func,
                language_override=language_override,
                generate_eliv=generate_eliv,
                quiet=quiet,
                force=force,
                slot_id=slot_id,
                shared_display=shared_display,
                progress_callback=_progress_cb,
                fallback_template=fallback_template,
                versioned_mirror_dir=versioned_mirror_dir,
            )
        finally:
            if slot_queue is not None and slot_id is not None:
                slot_queue.put_nowait(slot_id)


def _format_status_bar(
    completed: int,
    total: int,
    last_file: Optional[str],
    last_calls: int,
    last_cost: float,
    total_cost: float,
    processed: int = 0,
) -> str:
    """Build status bar: [✓ 24/114] file → traced N calls, $X.XXXX | Est. total: $X.XX"""
    denom = processed if processed > 0 else completed
    est_total = total_cost * total / denom if denom > 0 else 0.0
    file_part = f" {last_file} →" if last_file else ""
    stats = f"traced {last_calls} calls, ${last_cost:.4f}" if last_file else "…"
    return f"[✓ {completed}/{total}]{file_part} {stats} | Est. total: ${est_total:.2f}"


async def process_directory_async(
    target_path: Path,
    *,
    recursive: bool = False,
    output_dir: Optional[Path] = None,
    dependencies_func: Optional[Callable[[Path], List[str]]] = None,
    language_override: Optional[str] = None,
    workers: Optional[int] = None,
    show_progress: bool = True,
    generate_eliv: Optional[bool] = None,
    quiet: bool = False,
    budget: Optional[float] = None,
    force: bool = False,
    changed_files: Optional[List[Path]] = None,
    fallback_template: bool = False,
    versioned_mirror_dir: Optional[Path] = None,
) -> None:
    """
    Process a directory of files for documentation generation (async).

    Uses asyncio.Semaphore to limit concurrent LLM calls. Preserves idempotency:
    same input produces same output regardless of execution order.

    Args:
        target_path: Path to the directory to process.
        recursive: If True, process subdirectories recursively.
        output_dir: Optional directory to write generated docs.
        dependencies_func: Optional function to resolve dependencies per file.
        language_override: Optional explicit language for all files.
        workers: Max concurrent file processing (default: min(8, cpu_count)).
        show_progress: If True and stdout is a TTY, show progress.
        quiet: If True, suppress status bar and completion lines (CI mode).
        budget: Optional hard USD limit. Stops all workers immediately when exceeded.
    """
    if not target_path.exists() or not target_path.is_dir():
        raise NotADirectoryError(f"Target directory not found: {target_path}")

    if output_dir is not None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Auto-set workers and LLM concurrency from model RPM if not explicitly provided
    specs = get_model_specs()
    model_name = _resolve_doc_model("deep")
    spec = specs.get(model_name, {})
    rpm = spec.get("rpm_limit", 1000)

    if workers is None:
        workers = _safe_workers_from_rpm(model_name, rpm)
        logger.info(
            "Auto-set workers to %d based on %s RPM limit (%d)",
            workers,
            model_name,
            rpm,
        )
    workers = max(1, workers)
    semaphore = asyncio.Semaphore(workers)

    files: List[Path] = []
    for pattern in _DIRECTORY_PATTERNS:
        for f in target_path.glob(pattern):
            if f.is_file() and "__pycache__" not in str(f):
                files.append(f)

    if changed_files is not None:
        changed_set = {p.resolve() for p in changed_files}
        files = [f for f in files if f.resolve() in changed_set]
        if not files:
            logger.info("No changed files to process (--changed-only)")
            return

    total = len(files)

    # Doc-sync: set LLM concurrency just below rate limit for bulk runs.
    if (
        total > 1
        and "SCOUT_MAX_CONCURRENT_CALLS" not in os.environ
    ):
        desired = _max_concurrent_from_rpm(rpm)
        os.environ["SCOUT_MAX_CONCURRENT_CALLS"] = str(desired)
        # Bump workers so file-level parallelism doesn't bottleneck LLM throughput
        workers = min(16, max(workers, desired // 2))
        semaphore = asyncio.Semaphore(workers)
        logger.info(
            "Doc-sync: set SCOUT_MAX_CONCURRENT_CALLS=%d, workers=%d (just below %d RPM limit)",
            desired,
            workers,
            rpm,
        )

    if generate_eliv is None:
        config = ScoutConfig()
        doc_gen = config.get("doc_generation") or {}
        generate_eliv = doc_gen.get("generate_eliv", True)
    repo_root = Path.cwd().resolve()
    use_progress = (
        show_progress and not quiet and total > 1 and sys.stdout.isatty()
    )
    use_dashboard = use_progress  # full parallel trace dashboard
    processed_package_dirs: set = set()
    completed = [0]  # use list for closure
    processed = [0]  # files that ran LLM (not skipped), for ETA
    total_cost = [0.0]
    last_result: List[Optional[FileProcessResult]] = [None]
    last_file: List[Optional[str]] = [None]
    lock = asyncio.Lock()

    slot_queue: Optional[asyncio.Queue] = None
    shared_display: Dict[int, Dict[str, Any]] = {}
    dashboard_done = asyncio.Event()
    if use_dashboard:
        slot_queue = asyncio.Queue()
        for i in range(workers):
            slot_queue.put_nowait(i)

    def _apply_pulse(chain: str, pulse_hop: Optional[str]) -> str:
        """Wrap pulse_hop in inverse video for 1 frame, then clear."""
        if not pulse_hop or pulse_hop not in chain:
            return chain
        plain = _strip_ansi(pulse_hop)
        return chain.replace(
            pulse_hop,
            f"{_INVERSE}{plain}{_INVERSE_OFF}",
            1,
        )

    async def _display_refresh_task() -> None:
        """Refresh dashboard every 100ms (10 FPS): clear screen, slots, status bar."""
        while not dashboard_done.is_set():
            await asyncio.sleep(0.1)
            if dashboard_done.is_set():
                break
            async with lock:
                display_completed = completed[0]
                display_processed = processed[0]
                display_total_cost = total_cost[0]
            sys.stdout.write(_CLEAR_SCREEN)
            est_total = (
                display_total_cost * total / display_processed
                if display_processed > 0
                else 0.0
            )
            for slot_id in range(workers):
                entry = shared_display.get(slot_id)
                if entry:
                    status = entry.get("status", "running")
                    file_str = entry.get("file", "…")
                    chain = entry.get("chain")
                    cost = entry.get("cost", 0.0)
                    pulse_hop = entry.pop("pulse_hop", None)  # clear after 1 frame
                    if chain and pulse_hop:
                        chain = _apply_pulse(chain, pulse_hop)
                    slot_prefix = f"[{slot_id}] "
                    if status == "done":
                        if entry.get("skipped"):
                            line = f"{slot_prefix}✓ {file_str} (up to date)"
                        else:
                            success = entry.get("success", False)
                            if success and chain:
                                line = f"{slot_prefix}✔ {file_str} ━╸ {chain} | ${cost:.4f}"
                            elif success:
                                line = f"{slot_prefix}✔ {file_str} | ${cost:.4f}"
                            else:
                                err = entry.get("error", "failed")
                                line = f"{slot_prefix}{_RED}✗ {file_str}: {err}{_RESET}"
                        sys.stdout.write(line + "\n")
                    else:
                        sym_done = entry.get("symbols_done", 0)
                        sym_total = entry.get("symbols_total", 0)
                        sym_progress = (
                            f" [{sym_done}/{sym_total}]" if sym_total > 1 else ""
                        )
                        if chain:
                            line = f"{slot_prefix}{file_str}{sym_progress} ━╸ {chain} | ${cost:.4f}"
                        else:
                            line = f"{slot_prefix}{file_str}{sym_progress} | ${cost:.4f}"
                        sys.stdout.write(line + "\n")
            bar = f"[✓ {display_completed}/{total}] | ${display_total_cost:.4f} spent | Est. total: ${est_total:.2f}"
            sys.stdout.write("\n" + bar)
            sys.stdout.flush()

    def _render_status() -> None:
        if not use_progress or use_dashboard:
            return
        r = last_result[0]
        bar = _format_status_bar(
            completed[0],
            total,
            last_file[0],
            r.calls_count if r else 0,
            r.cost_usd if r else 0.0,
            total_cost[0],
            processed=processed[0],
        )
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()

    async def _process_and_track(f: Path) -> None:
        result: Optional[FileProcessResult] = None
        try:
            result = await _process_file_with_semaphore(
                semaphore,
                f,
                output_dir=output_dir,
                dependencies_func=dependencies_func,
                language_override=language_override,
                generate_eliv=generate_eliv,
                quiet=True,  # we print our own completion/error lines
                force=force,
                slot_queue=slot_queue,
                shared_display=shared_display,
                fallback_template=fallback_template,
                versioned_mirror_dir=versioned_mirror_dir,
            )
        except (ValueError, OSError) as e:
            logger.warning("Skip %s: %s", f, e)
            result = FileProcessResult(
                success=False,
                cost_usd=0.0,
                symbols_count=0,
                calls_count=0,
                types_count=0,
                exports_count=0,
                model="",
                error=str(e),
            )
        finally:
            async with lock:
                completed[0] += 1
                if result:
                    if not result.skipped:
                        total_cost[0] += result.cost_usd
                        processed[0] += 1
                        if budget is not None and total_cost[0] > budget:
                            raise BudgetExceededError(total_cost[0], budget)
                    last_result[0] = result
                    last_file[0] = _rel_path_for_display(f)
                    if result.success and output_dir is None and (f.parent / "__init__.py").exists():
                        processed_package_dirs.add(f.parent)

            if quiet:
                return
            if use_dashboard:
                return  # dashboard shows completion

            # Completion line or error (replaces "Wrote..." messages)
            if result:
                rel = _rel_path_for_display(f)
                if result.skipped:
                    if use_progress:
                        sys.stdout.write("\r" + " " * 100 + "\r")
                    print(f"✓ {rel} (up to date)", file=sys.stdout)
                elif result.success:
                    if result.call_chain:
                        line = f"✔ {rel} ━╸ {result.call_chain} | {result.model} | ${result.cost_usd:.4f}"
                    else:
                        line = (
                            f"✔ {rel} — traced {result.calls_count} calls, "
                            f"{result.types_count} types, {result.exports_count} exports | "
                            f"{result.model} | ${result.cost_usd:.4f}"
                        )
                    if use_progress:
                        sys.stdout.write("\r" + " " * 100 + "\r")
                    print(line, file=sys.stdout)
                else:
                    err_msg = f"{_RED}✗ {rel}: {result.error}{_RESET}"
                    if use_progress:
                        sys.stdout.write("\r" + " " * 100 + "\r")
                    print(err_msg, file=sys.stderr)

            if use_progress and not use_dashboard:
                _render_status()

    if use_dashboard:
        refresh_task = asyncio.create_task(_display_refresh_task())

    task_objs = [asyncio.create_task(_process_and_track(f)) for f in files]
    try:
        await asyncio.gather(*task_objs)
    except BudgetExceededError:
        for t in task_objs:
            t.cancel()
        await asyncio.gather(*task_objs, return_exceptions=True)
        raise

    if use_dashboard:
        dashboard_done.set()
        refresh_task.cancel()
        try:
            await refresh_task
        except asyncio.CancelledError:
            pass
        # Do not clear screen—preserves last dashboard frame so output doesn't "disappear"
        # when chained with another command (e.g. scout-doc-sync; scout-pr > file)
        sys.stdout.write("\n")
        sys.stdout.flush()
    elif use_progress:
        sys.stdout.write("\r" + " " * 100 + "\r")
        sys.stdout.write("\n")
        sys.stdout.flush()

    if output_dir is None:
        for pkg_dir in sorted(processed_package_dirs):
            try:
                await _update_module_brief_async(pkg_dir, repo_root)
            except Exception as e:
                logger.warning("Skip module brief for %s: %s", pkg_dir, e)


def process_directory(
    target_path: Path,
    *,
    recursive: bool = False,
    output_dir: Optional[Path] = None,
    dependencies_func: Optional[Callable[[Path], List[str]]] = None,
    language_override: Optional[str] = None,
    workers: Optional[int] = None,
    show_progress: bool = True,
    generate_eliv: Optional[bool] = None,
    quiet: bool = False,
    budget: Optional[float] = None,
    force: bool = False,
    changed_files: Optional[List[Path]] = None,
    fallback_template: bool = False,
    versioned_mirror_dir: Optional[Path] = None,
) -> None:
    """
    Process a directory of files for documentation generation.

    Supports Python, JavaScript, and plain-text fallback. When recursive and
    processing Python packages (directories with __init__.py), auto-generates
    module briefs when enable_module_briefs is true.

    Args:
        target_path: Path to the directory to process.
        recursive: If True, process subdirectories recursively.
        output_dir: Optional directory to write generated docs.
        dependencies_func: Optional function to resolve dependencies per file.
        language_override: Optional explicit language for all files.
        workers: Max concurrent file processing (default: min(8, cpu_count)).
        show_progress: If True and stdout is a TTY, show progress.
        quiet: If True, suppress status bar and completion lines (CI mode).
    """
    asyncio.run(
        process_directory_async(
            target_path,
            recursive=recursive,
            output_dir=output_dir,
            dependencies_func=dependencies_func,
            language_override=language_override,
            workers=workers,
            show_progress=show_progress,
            generate_eliv=generate_eliv,
            quiet=quiet,
            budget=budget,
            force=force,
            changed_files=changed_files,
            fallback_template=fallback_template,
            versioned_mirror_dir=versioned_mirror_dir,
        )
    )


async def _synthesize_pr_description_async(
    raw_summaries: str,
    *,
    fallback_template: bool = False,
) -> str:
    """
    Async implementation: uses await call_groq_async (no asyncio.run nesting).
    When fallback_template=False (default), raises on LLM failure.
    When fallback_template=True, returns raw_summaries on LLM failure.
    """
    prompt = f"""You are a senior staff engineer writing a PR description for a code review.
Summarize the following technical summaries into a single, cohesive narrative that explains:
- The overall goal of the changes
- Key architectural components introduced or modified
- Cross-cutting concerns (e.g., cost tracking, auditability, language support)
- Why this matters to the team

Be concise, professional, and insightful. Do not list files—group by theme.

Technical summaries:
{raw_summaries}"""

    system = "You are a senior staff engineer. Write concise, professional PR descriptions."
    use_big_brain = bool(os.environ.get("GEMINI_API_KEY"))
    try:
        if use_big_brain:
            response = await call_big_brain_async(
                prompt,
                system=system,
                max_tokens=1200,
                task_type="pr_synthesis",
            )
        else:
            response = await call_groq_async(
                prompt,
                model=_resolve_doc_model("pr_synthesis") or _resolve_doc_model("tldr"),
                system=system,
                max_tokens=1200,
            )
    except Exception as e:
        if fallback_template:
            logger.warning("PR synthesis LLM failed, falling back to raw: %s", e)
            return raw_summaries
        raise

    if not use_big_brain:
        audit = AuditLog()
        audit.log(
            "pr_synthesis",
            cost=response.cost_usd,
            model=response.model,
            input_t=response.input_tokens,
            output_t=response.output_tokens,
        )

    content = response.content.strip()
    return content if content else raw_summaries


def synthesize_pr_description(
    raw_summaries: str,
    *,
    is_async: bool = False,
    fallback_template: bool = False,
):
    """
    Synthesize a unified PR description from raw file/module summaries via LLM.

    Uses the same model as doc generation (TLDR_MODEL). Logs to audit.jsonl as
    "pr_synthesis". Raises on LLM failure unless fallback_template=True.

    Args:
        raw_summaries: Concatenated technical summaries from assemble_pr_description.
        is_async: If True, returns coroutine for caller to await (avoids asyncio.run nesting).
                  If False (default), uses asyncio.run for CLI/sync callers.
        fallback_template: If True, returns raw_summaries on LLM failure. If False (default), raises.

    Returns:
        Cohesive narrative PR description.
        When is_async=True, returns Awaitable[str] for caller to await.
    """
    if is_async:
        return _synthesize_pr_description_async(raw_summaries, fallback_template=fallback_template)
    return asyncio.run(
        _synthesize_pr_description_async(raw_summaries, fallback_template=fallback_template)
    )


# Backward compatibility: parse_python_file delegates to PythonAdapter
def parse_python_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a Python file using the AST and extract top-level symbols.

    Legacy API; new code should use get_adapter_for_path().parse().
    """
    from vivarium.scout.adapters.python import PythonAdapter

    adapter = PythonAdapter()
    tree = adapter.parse(file_path)
    symbols: List[Dict[str, Any]] = []
    for child in tree.children:
        for s in child.iter_symbols():
            symbols.append({
                "name": s.name,
                "type": s.type,
                "lineno": s.lineno,
                "end_lineno": s.end_lineno,
                "docstring": s.docstring,
                "signature": s.signature,
                "logic_hints": s.logic_hints or [],
            })
    return {
        "path": str(file_path),
        "symbols": symbols,
        "error": None,
    }
