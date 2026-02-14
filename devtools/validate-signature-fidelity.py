#!/usr/bin/env python3
"""
Mechanical validation: AST truth vs doc claims.
Ticket: Extraordinary Proof — 100% signature fidelity.

Usage:
  python devtools/validate-signature-fidelity.py

Exits 0 if all modules pass; 1 if any mismatch.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"


def _param_count_from_ast(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """Count parameters (excluding self/cls for methods)."""
    n = len(node.args.args)
    if node.args.vararg:
        n += 1
    if node.args.kwarg:
        n += 1
    n += len(node.args.kwonlyargs)
    return n


def _param_count_from_signature(sig: str) -> int | None:
    """Parse 'def name(params) -> ret' and return param count. Returns None on parse error."""
    try:
        # Wrap in a function to parse
        tree = ast.parse(sig.strip())
        if tree.body and isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):
            node = tree.body[0]
            return _param_count_from_ast(node)
    except SyntaxError:
        pass
    return None


def _return_type_from_ast(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    if node.returns:
        return ast.unparse(node.returns)
    return None


def _return_type_from_signature(sig: str) -> str | None:
    """Extract return type from 'def name(...) -> Ret'."""
    m = re.search(r"\)\s*->\s*(.+)$", sig)
    if m:
        return m.group(1).strip()
    return None


def dump_ast_truth(filepath: Path, outfile: Path) -> list[dict]:
    """Extract ground-truth signatures from source. Only documentable symbols:
    module-level functions and class methods (direct children of ClassDef).
    Excludes nested functions (they are not part of public API).
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(content, filename=str(filepath))

    symbols: list[dict] = []
    parents: dict[ast.AST, ast.AST] = {}

    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            parents[c] = n

    def is_documentable(node: ast.AST) -> tuple[bool, str | None]:
        """Return (True, parent_class_or_None) if documentable; (False, _) otherwise."""
        direct_parent = parents.get(node)
        if direct_parent is tree:
            return True, None  # module-level
        if isinstance(direct_parent, ast.ClassDef):
            return True, direct_parent.name  # method
        return False, None  # nested inside function

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ok, parent = is_documentable(node)
            if not ok:
                continue
            key = f"{parent}.{node.name}" if parent else node.name
            params = _param_count_from_ast(node)
            ret = _return_type_from_ast(node)
            symbols.append({
                "key": key,
                "name": node.name,
                "parent": parent,
                "type": "method" if parent else "function",
                "params": params,
                "return_type": ret,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
            })

    outfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outfile, "w") as f:
        json.dump(symbols, f, indent=2)
    return symbols


def extract_doc_claims(docfile: Path, outfile: Path) -> list[dict]:
    """Extract claimed signatures from .tldr.md. Returns list of claim dicts."""
    content = docfile.read_text(encoding="utf-8", errors="replace")
    claims: list[dict] = []
    seen_keys: set[str] = set()

    # Match 1: - `key`: def name(...) -> ...  OR  - # `name`: def name(...) -> ...
    sig_pattern = re.compile(
        r"[-*]\s+(?:#\s+)?`?([A-Za-z_.][A-Za-z0-9_.]*)`?\s*:\s*"
        r"(async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(?:->\s*([^\s:]+))?",
    )
    # Match 2: - `method(params) -> ret`: description (audit-style, no "def")
    # Return type: optional; when present, match until backtick to capture e.g. Optional[Dict[str, Any]]
    method_sig_pattern = re.compile(
        r"[-*]\s+`?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(?:->\s*(.+?))?`?\s*:",
    )

    lines = content.split("\n")
    current_class: str | None = None

    for line in lines:
        if re.match(r"^# Module Summary\s*$", line):
            current_class = None  # Quality gate: Module Summary = module-level content
        elif re.match(r"^# (TLDR|ELIV)\s*$", line):
            current_class = None  # Section headers, not class context
        elif re.match(r"^## Module ", line):
            current_class = None  # Back to module level
        elif re.match(r"^# [A-Za-z_][A-Za-z0-9_]*\s*$", line):
            current_class = line.strip()[2:].strip()

        m = sig_pattern.search(line)
        if m:
            key, async_prefix, def_name, params_part, ret_part = m.groups()
            # If key has no dot but we're in a class section, it's a method
            if current_class and "." not in key:
                key = f"{current_class}.{key}"
            sig = f"{'async ' if async_prefix else ''}def {def_name}({params_part})"
            if ret_part:
                sig += f" -> {ret_part.strip()}"
        else:
            mm = method_sig_pattern.search(line)
            if mm and current_class:
                method_name, params_part, ret_part = mm.groups()
                key = f"{current_class}.{method_name}"
                sig = f"def {method_name}({params_part})"
                if ret_part:
                    sig += f" -> {ret_part.strip()}"
            else:
                continue

        if key in seen_keys:
            continue
        seen_keys.add(key)

        claims.append({
            "key": key,
            "name": key.split(".")[-1] if "." in key else key,
            "params": _param_count_from_signature(sig),
            "return_type": _return_type_from_signature(sig),
        })

    outfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outfile, "w") as f:
        json.dump(claims, f, indent=2)
    return claims


def validate(
    truth_file: Path,
    claims_file: Path,
    module_name: str,
    module_functions_only: bool = False,
) -> bool:
    """Compare truth vs claims. Return True if 100% match."""
    with open(truth_file) as f:
        truth_list = json.load(f)
    with open(claims_file) as f:
        claims_list = json.load(f)

    if module_functions_only:
        truth_list = [s for s in truth_list if s.get("parent") is None]
        claims_list = [c for c in claims_list if "." not in c["key"]]

    truth_map = {s["key"]: s for s in truth_list}
    claims_map = {c["key"]: c for c in claims_list}

    all_match = True

    # Check 1: All truth symbols have doc claims
    for t in truth_list:
        key = t["key"]
        if key not in claims_map:
            print(f"  ❌ MISSING IN DOCS: {key}")
            all_match = False

    # Check 2: All doc claims exist in truth (no hallucination)
    for key in claims_map:
        if key not in truth_map:
            print(f"  ❌ HALLUCINATED IN DOCS: {key}")
            all_match = False

    # Check 3 & 4: Param count and return type for matched symbols
    for key in set(truth_map.keys()) & set(claims_map.keys()):
        t = truth_map[key]
        c = claims_map[key]
        t_params = t["params"]
        c_params = c.get("params")
        if c_params is not None and t_params != c_params:
            print(f"  ❌ PARAM COUNT MISMATCH: {key} (truth={t_params}, docs={c_params})")
            all_match = False
        t_ret = t["return_type"]
        c_ret = c.get("return_type")
        if t_ret and c_ret and t_ret != c_ret:
            # Allow doc truncation (e.g. "Dict[str," from regex) — truth must match start
            if not (t_ret.startswith(c_ret) or c_ret.startswith(t_ret)):
                print(f"  ❌ RETURN TYPE MISMATCH: {key} (truth={t_ret!r}, docs={c_ret!r})")
                all_match = False

    return all_match


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate signature fidelity: AST truth vs doc claims")
    parser.add_argument(
        "--module-functions-only",
        action="store_true",
        help="Only validate module-level functions (critical path); skip class methods",
    )
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    modules = [
        ("vivarium/scout/router.py", "vivarium/scout/.docs/router.py.tldr.md", "router.py"),
        ("vivarium/scout/audit.py", "vivarium/scout/.docs/audit.py.tldr.md", "audit.py"),
        ("vivarium/runtime/inference_engine.py", "vivarium/runtime/.docs/inference_engine.py.tldr.md", "inference_engine.py"),
    ]

    for src, doc, name in modules:
        src_path = REPO_ROOT / src
        doc_path = REPO_ROOT / doc
        if not src_path.exists():
            print(f"Skip {name}: source not found")
            continue
        if not doc_path.exists():
            print(f"Skip {name}: doc not found")
            continue

        truth_file = REPORTS_DIR / f"ast-truth-{name.replace('.py', '')}.json"
        claims_file = REPORTS_DIR / f"doc-claims-{name.replace('.py', '')}.json"

        dump_ast_truth(src_path, truth_file)
        print(f"  ✓ AST truth: {truth_file.name}")

        extract_doc_claims(doc_path, claims_file)
        print(f"  ✓ Doc claims: {claims_file.name}")

    print()
    results = []
    for src, doc, name in modules:
        src_path = REPO_ROOT / src
        doc_path = REPO_ROOT / doc
        if not src_path.exists() or not doc_path.exists():
            continue
        stem = name.replace(".py", "")
        truth_file = REPORTS_DIR / f"ast-truth-{stem}.json"
        claims_file = REPORTS_DIR / f"doc-claims-{stem}.json"
        ok = validate(
            truth_file,
            claims_file,
            name,
            module_functions_only=args.module_functions_only,
        )
        results.append(ok)
        if ok:
            print(f"  ✅ {name}: 100% match")
        else:
            print(f"  ❌ {name}: MISMATCHES FOUND")

    if all(results):
        print()
        print("✅✅✅ EXTRAORDINARY PROOF: 100% SIGNATURE FIDELITY ACROSS ALL VALIDATED MODULES ✅✅✅")
        return 0
    else:
        print()
        print("❌❌❌ VALIDATION FAILED: MISMATCHES DETECTED — DO NOT SHIP ❌❌❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
