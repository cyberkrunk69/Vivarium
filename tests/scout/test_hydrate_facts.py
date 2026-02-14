"""
Tests for TICKET-43: hydrate_facts — structured facts only, never prose.
"""

import asyncio
from pathlib import Path

from vivarium.scout.context import hydrate_facts, _facts_cache_path
from vivarium.scout.deps import DependencyGraph, SymbolRef
from vivarium.scout.doc_sync.ast_facts import ModuleFacts


def test_hydrate_facts_loads_from_cache() -> None:
    """hydrate_facts loads .facts.json, never .tldr.md."""
    async def _run() -> None:
        repo_root = Path.cwd().resolve()
        # middle_manager has .facts.json from hybrid doc sync
        ref = SymbolRef(Path("vivarium/scout/middle_manager.py"), "")
        deps = DependencyGraph(repo_root)
        return await hydrate_facts(
            symbols=[ref],
            deps_graph=deps,
            repo_root=repo_root,
            max_facts=50,
            max_depth=0,
        )
    facts = asyncio.run(_run())
    assert len(facts.symbols) > 0
    # Should have logger or MAX_EXPANDED_CONTEXT from middle_manager
    keys = list(facts.symbols.keys())
    has_relevant = any(
        "logger" in k or "MAX_EXPANDED" in k or "middle_manager" in k
        for k in keys
    )
    assert has_relevant or len(keys) > 5


def test_facts_cache_path() -> None:
    """_facts_cache_path maps py file to .facts.json in .docs/."""
    repo = Path.cwd().resolve()
    path = Path("vivarium/scout/middle_manager.py")
    cache = _facts_cache_path(repo, path)
    assert cache.name == "middle_manager.py.facts.json"
    assert ".docs" in str(cache)


def test_module_facts_empty_and_merge() -> None:
    """ModuleFacts.empty() and merge() work for aggregation."""
    empty = ModuleFacts.empty()
    assert len(empty.symbols) == 0
    # Load one and merge
    facts_path = Path("vivarium/scout/.docs/middle_manager.py.facts.json")
    if facts_path.exists():
        loaded = ModuleFacts.from_json(facts_path.read_text())
        empty.merge(loaded)
        assert len(empty.symbols) > 0
