"""Basic lifecycle test for DependencyGraph — TICKET-1 acceptance."""

from pathlib import Path

import pytest

from vivarium.scout.deps import DependencyGraph, DependencyNode, SymbolRef


def test_basic_lifecycle(tmp_path: Path, monkeypatch):
    """Create graph, add node, save, load, verify node exists."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    ref = SymbolRef(Path("test.py"), "foo")
    graph.nodes[str(ref)] = DependencyNode(ref, "hash123")
    graph._save_cache()

    graph2 = DependencyGraph(tmp_path)
    assert str(ref) in graph2.nodes
    assert graph2.nodes[str(ref)].ast_hash == "hash123"


def test_import_works():
    """import vivarium.scout.deps works without error."""
    import vivarium.scout.deps as deps_module
    assert deps_module.DependencyGraph is not None
    assert deps_module.SymbolRef is not None
    assert deps_module.DependencyNode is not None


def test_symbols_importable():
    """SymbolRef, DependencyNode, DependencyGraph classes importable."""
    from vivarium.scout.deps import DependencyGraph, DependencyNode, SymbolRef

    ref = SymbolRef(Path("a/b.py"), "my_func")
    assert str(ref) == "a/b.py::my_func"
    node = DependencyNode(ref, "abc")
    assert node.ast_hash == "abc"
    graph = DependencyGraph(Path.cwd())
    assert hasattr(graph, "nodes")


def test_cache_writes_to_scout_dir(tmp_path: Path, monkeypatch):
    """Cache writes to ~/.scout/dependency_graph.v2.json."""
    # Use tmp_path as home to avoid polluting real ~/.scout
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    ref = SymbolRef(Path("x.py"), "y")
    graph.nodes[str(ref)] = DependencyNode(ref, "h1")
    graph._save_cache()

    scout_dir = fake_home / ".scout"
    cache_file = scout_dir / "dependency_graph.v2.json"
    assert scout_dir.exists()
    assert cache_file.exists()
    assert cache_file.stat().st_size > 0


def test_get_context_package_max_depth(tmp_path: Path, monkeypatch):
    """TICKET-6: BFS stops at max_depth. Chain A→B→C→D→E, query A with max_depth=2 → A,B,C only."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    p = Path("pkg")
    ref_a = SymbolRef(p / "a.py", "A")
    ref_b = SymbolRef(p / "b.py", "B")
    ref_c = SymbolRef(p / "c.py", "C")
    ref_d = SymbolRef(p / "d.py", "D")
    ref_e = SymbolRef(p / "e.py", "E")

    # Chain: A depends on B, B on C, C on D, D on E
    graph.nodes[str(ref_a)] = DependencyNode(ref_a, "h", depends_on={ref_b})
    graph.nodes[str(ref_b)] = DependencyNode(ref_b, "h", depends_on={ref_c})
    graph.nodes[str(ref_c)] = DependencyNode(ref_c, "h", depends_on={ref_d})
    graph.nodes[str(ref_d)] = DependencyNode(ref_d, "h", depends_on={ref_e})
    graph.nodes[str(ref_e)] = DependencyNode(ref_e, "h", depends_on=set())

    result = graph.get_context_package([ref_a], max_depth=2)
    refs_returned = {n.ref for n in result}
    assert refs_returned == {ref_a, ref_b, ref_c}
    assert ref_d not in refs_returned
    assert ref_e not in refs_returned


def test_get_trust_metadata_mix_fresh_stale(tmp_path: Path, monkeypatch):
    """TICKET-4: Mix of fresh/stale nodes, verify metadata correct."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    p = Path("pkg")
    ref_a = SymbolRef(p / "a.py", "A")
    ref_b = SymbolRef(p / "b.py", "B")
    ref_c = SymbolRef(p / "c.py", "C")
    ref_d = SymbolRef(p / "d.py", "D")

    # Fresh nodes (no invalidated_at)
    node_a = DependencyNode(ref_a, "h1")
    node_b = DependencyNode(ref_b, "h2")

    # Stale nodes with different reasons and timestamps
    node_c = DependencyNode(ref_c, "h3")
    node_c.mark_stale(reason="cascade")
    node_d = DependencyNode(ref_d, "h4")
    node_d.mark_stale(reason="hash_mismatch")

    nodes = [node_a, node_b, node_c, node_d]
    meta = graph.get_trust_metadata(nodes)

    assert meta["invalidation_cascade_triggered"] is True
    assert set(meta["invalidation_reasons"]) == {"cascade", "hash_mismatch"}
    assert meta["oldest_invalidation"] is not None
    assert meta["total_symbols"] == 4
    assert meta["stale_ratio"] == 0.5  # 2 stale / 4 total


def test_get_trust_metadata_all_fresh(tmp_path: Path, monkeypatch):
    """TICKET-4: All fresh nodes — no cascade, stale_ratio 0."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    nodes = [
        DependencyNode(SymbolRef(Path("x.py"), "a"), "h1"),
        DependencyNode(SymbolRef(Path("y.py"), "b"), "h2"),
    ]
    meta = graph.get_trust_metadata(nodes)

    assert meta["invalidation_cascade_triggered"] is False
    assert meta["invalidation_reasons"] == []
    assert meta["oldest_invalidation"] is None
    assert meta["total_symbols"] == 2
    assert meta["stale_ratio"] == 0.0


def test_get_trust_metadata_empty_nodes(tmp_path: Path, monkeypatch):
    """TICKET-4: Empty nodes list — no division by zero."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    meta = graph.get_trust_metadata([])

    assert meta["invalidation_cascade_triggered"] is False
    assert meta["invalidation_reasons"] == []
    assert meta["oldest_invalidation"] is None
    assert meta["total_symbols"] == 0
    assert meta["stale_ratio"] == 0.0


def test_get_stats(tmp_path: Path, monkeypatch):
    """TICKET-5: get_stats returns total/orphaned/stale counts and cache_version."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    graph = DependencyGraph(tmp_path)
    # Create existing file and orphan (path doesn't exist)
    (tmp_path / "real.py").write_text("def foo(): pass\n")
    ref_real = SymbolRef(Path("real.py"), "foo")
    ref_orphan = SymbolRef(Path("deleted.py"), "bar")
    ref_stale = SymbolRef(Path("real.py"), "baz")

    node_real = DependencyNode(ref_real, "h1")
    node_orphan = DependencyNode(ref_orphan, "h2")
    node_stale = DependencyNode(ref_stale, "h3")
    node_stale.mark_stale(reason="cascade")

    graph.nodes[str(ref_real)] = node_real
    graph.nodes[str(ref_orphan)] = node_orphan
    graph.nodes[str(ref_stale)] = node_stale

    stats = graph.get_stats()
    assert stats["total"] == 3
    assert stats["stale"] == 1
    assert stats["orphaned"] == 1
    assert stats["cache_version"] == "v2"
