"""
TICKET-36: Symbol-level hydration tests.

Proves tiered hydration works: .tldr.md only, bounded, symbol-level.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from vivarium.scout.context import (
    _estimate_tokens,
    _truncate_to_tokens,
    hydrate_symbols,
)
from vivarium.scout.deps import DependencyGraph, SymbolRef


def test_estimate_tokens():
    """Rough token estimate: 4 chars ≈ 1 token."""
    assert _estimate_tokens("") == 0
    assert _estimate_tokens("abcd") == 1
    assert _estimate_tokens("a" * 400) == 100


def test_truncate_to_tokens():
    """Truncate oldest parts first to stay under cap."""
    parts = ["a" * 400, "b" * 400, "c" * 400]  # 300 tokens total (100 each)
    out = _truncate_to_tokens(parts, 150)
    # Cap 150: remove first (100), total 200; remove second (100), total 100 <= 150
    assert len(out) == 1
    assert out[0] == "c" * 400


def test_hydrate_middle_manager_gate_only():
    """Hydrate gate-related module: .tldr.md only, bounded, deps included.

    Uses router.py (has committed .tldr.md); middle_manager lacks docs in repo.
    """
    repo_root = Path(__file__).resolve().parent.parent.parent
    graph = DependencyGraph(repo_root)
    symbols = [
        SymbolRef(Path("vivarium/scout/router.py"), "TriggerRouter")
    ]

    context = asyncio.run(hydrate_symbols(
        symbols, graph, repo_root, max_depth=1, max_tokens=4000
    ))

    # Should contain .tldr.md for TriggerRouter
    assert "TriggerRouter" in context
    assert "budget" in context.lower() or "cost" in context.lower()

    # Should NOT contain entire file contents (.deep.md skipped)
    assert len(context) < 5000  # Reasonable size for 1-2 symbols

    # Should contain related symbols from router
    assert "NavResult" in context or "SymbolDoc" in context or "logger" in context


def test_hydrate_context_bounded():
    """Context always ≤ 4K tokens before gate."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    graph = DependencyGraph(repo_root)
    # Use multiple files to potentially exceed 4K
    symbols = [
        SymbolRef(Path("vivarium/scout/router.py"), ""),
        SymbolRef(Path("vivarium/scout/big_brain.py"), ""),
        SymbolRef(Path("vivarium/scout/middle_manager.py"), ""),
    ]

    context = asyncio.run(hydrate_symbols(
        symbols, graph, repo_root, max_depth=2, max_tokens=4000
    ))

    estimated = _estimate_tokens(context)
    assert estimated <= 4000, f"Context {estimated} tokens exceeds 4K cap"
