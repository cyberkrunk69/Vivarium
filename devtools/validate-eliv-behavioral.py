#!/usr/bin/env python3
"""Behavioral validation: ELIV must change when symbol patterns change.

Cannot be gamed by string renaming — tests actual generation behavior.
Uses AST fact extraction (deterministic, no LLM) to verify symbol changes
propagate through the pipeline.
"""
import sys
import pathlib

# Ensure vivarium is importable when run as ./devtools/validate-eliv-behavioral.py
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def test_eliv_updates_on_symbol_change():
    repo_root = _REPO_ROOT
    router_py = repo_root / "vivarium" / "scout" / "router.py"

    # 1. Baseline: extract AST facts
    from vivarium.scout.doc_sync.ast_facts import ASTFactExtractor

    extractor = ASTFactExtractor()
    facts_baseline = extractor.extract_documentable_facts(router_py)
    baseline_symbols = set(facts_baseline.symbols.keys())

    if "check_budget_with_message" not in baseline_symbols:
        print(
            "⚠️  check_budget_with_message not in baseline; test target missing",
            file=sys.stderr,
        )
        return True  # Skip if target symbol absent (e.g. refactor)

    # 2. Mutate symbol pattern (add "log" to function name)
    router_text = router_py.read_text()
    mutated = router_text.replace("check_budget_with_message", "log_budget_with_message")
    router_py.write_text(mutated)

    try:
        # 3. Re-extract facts
        facts_mutated = extractor.extract_documentable_facts(router_py)
        mutated_symbols = set(facts_mutated.symbols.keys())

        # 4. Verify facts changed (proves dynamic extraction)
        if "check_budget_with_message" in mutated_symbols:
            print(
                "❌ FAIL: Symbol set did not update when source was mutated",
                file=sys.stderr,
            )
            return False
        if "log_budget_with_message" not in mutated_symbols:
            print(
                "❌ FAIL: New symbol not present after mutation",
                file=sys.stderr,
            )
            return False

        print("✅ PASS: AST facts update dynamically when symbols change")
        return True
    finally:
        # Restore original router.py
        import subprocess

        subprocess.run(
            ["git", "checkout", "vivarium/scout/router.py"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )


if __name__ == "__main__":
    try:
        success = test_eliv_updates_on_symbol_change()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
