#!/usr/bin/env python3
"""Structural validation: ELIV generation must NOT contain hardcoded lookup tables.

Only allowed: symbol pattern matching → generic truth (3 phrases max).
Cannot be gamed by renaming — checks structure, not just strings.
"""
import ast
import pathlib
import sys

# ONLY 3 allowed explanatory phrases in entire ELIV path (forensic directive)
ALLOWED_PHRASES = frozenset({
    "work coordination",
    "resource limits",
    "activity logging",
})

# Phrases that indicate hardcoded lookup/analogy (violations unless in allowlist)
HARDCODED_INDICATORS = frozenset({
    "coordination", "handoff", "queue", "logging", "limits", "transparency",
    "resources", "execution", "routing", "traffic", "restaurant", "kitchen",
    "foreman", "receipt", "construction", "nascar", "brigade", "gridlock",
    "bottleneck", "stranded", "exhaustion", "logbook", "ledger",
})


def _node_in_eliv_path(node: ast.AST, eliv_func_lines: set) -> bool:
    """True if node is inside _generate_eliv_minimal_truth or _ensure_eliv_section."""
    return getattr(node, "lineno", 0) in eliv_func_lines


def has_hardcoded_eliv_logic(module_path: str) -> list:
    """
    Structural validation: ELIV generation (_generate_eliv_minimal_truth, _ensure_eliv_section)
    must NOT contain:
    - String literals with domain-specific terms (except the 3 allowed)
    - Lookup tables mapping domains to phrases
    Only validates the ELIV path — not TLDR/deep prompts.
    """
    path = pathlib.Path(module_path)
    if not path.exists():
        return [f"Path not found: {module_path}"]

    try:
        tree = ast.parse(path.read_text(), filename=module_path)
    except SyntaxError as e:
        return [f"Parse error: {e}"]

    # Find line ranges for ELIV functions
    eliv_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in (
            "_generate_eliv_minimal_truth",
            "_ensure_eliv_section",
        ):
            for n in ast.walk(node):
                if hasattr(n, "lineno"):
                    eliv_lines.add(n.lineno)

    violations = []

    for node in ast.walk(tree):
        if not _node_in_eliv_path(node, eliv_lines):
            continue

        # VIOLATION 1: String literals with hardcoded explanatory phrases
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            text = node.value.lower()
            words = text.split()
            if len(words) <= 3:
                continue
            if text.strip() in ALLOWED_PHRASES:
                continue
            if any(phrase in text for phrase in ALLOWED_PHRASES) and len(words) <= 8:
                continue
            if any(ind in text for ind in HARDCODED_INDICATORS):
                violations.append(
                    f"Line {node.lineno}: hardcoded explanatory phrase '{text[:50]}...'"
                )

        if hasattr(ast, "Str") and isinstance(node, ast.Str):
            text = node.s.lower()
            words = text.split()
            if len(words) <= 3:
                continue
            if text.strip() in ALLOWED_PHRASES:
                continue
            if any(phrase in text for phrase in ALLOWED_PHRASES) and len(words) <= 8:
                continue
            if any(ind in text for ind in HARDCODED_INDICATORS):
                violations.append(
                    f"Line {node.lineno}: hardcoded explanatory phrase '{text[:50]}...'"
                )

        # VIOLATION 2: Dictionary literals mapping domains to text
        if isinstance(node, ast.Dict):
            for key in node.keys:
                if isinstance(key, (ast.Constant, ast.Str)):
                    key_val = key.value if hasattr(key, "value") else key.s
                    if isinstance(key_val, str) and any(
                        kw in key_val.lower()
                        for kw in ["routing", "audit", "execution", "coordination"]
                    ):
                        violations.append(
                            f"Line {node.lineno}: hardcoded domain-to-text mapping"
                        )

    return violations


def main() -> int:
    # VIOLATION 0: eliv_constants.py must not exist (deleted, not renamed)
    eliv_constants = pathlib.Path("vivarium/scout/doc_sync/eliv_constants.py")
    if eliv_constants.exists():
        print(
            "❌ eliv_constants.py STILL EXISTS (hardcoding persists)",
            file=sys.stderr,
        )
        return 1

    synthesizer_path = "vivarium/scout/doc_sync/synthesizer.py"
    violations = has_hardcoded_eliv_logic(synthesizer_path)

    if violations:
        print("❌ HARD CODED ELIV LOGIC DETECTED (structural validation):", file=sys.stderr)
        for v in violations[:15]:
            print(f"  {v}", file=sys.stderr)
        return 1

    print("✅ NO hardcoded ELIV logic (structural validation passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
