"""
Scout Query CLI — Natural language repo search via living docs.

Takes a natural language query. Big brain (Gemini) interprets it into a scout call.
Outputs to clipboard and docs/temp/<timestamp>.md (gitignored).

Usage:
    ./devtools/scout-query "get me everything about scout at a deep level"
    ./devtools/scout-query "scout router and nav"
"""

from __future__ import annotations

import argparse
import asyncio
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _repo_root() -> Path:
    return Path.cwd().resolve()


def _collect_docs(
    repo_root: Path,
    scope: str,
    include_deep: bool,
) -> list[tuple[str, str, str]]:
    """
    Collect .tldr.md and optionally .deep.md for scope.
    Returns list of (module_path, suffix, content).
    """
    root = repo_root.resolve()
    scope_path = Path(scope)
    seen: set[tuple[str, str]] = set()
    results: list[tuple[str, str, str]] = []

    suffixes = [".tldr.md"]
    if include_deep:
        suffixes.append(".deep.md")

    # 1. Central docs: docs/livingDoc/<scope>/
    central = root / "docs" / "livingDoc" / scope_path
    if central.exists():
        for md_path in central.rglob("*.md"):
            stem = md_path.stem
            if stem.endswith(".tldr"):
                suffix = ".tldr.md"
                stem = stem.removesuffix(".tldr")
            elif stem.endswith(".deep"):
                suffix = ".deep.md"
                stem = stem.removesuffix(".deep")
            else:
                continue
            if suffix not in suffixes:
                continue
            try:
                rel = md_path.parent.relative_to(central)
                module_path = f"{rel / stem}".replace("\\", "/") if rel != Path(".") else stem
            except ValueError:
                module_path = stem
            key = (module_path, suffix)
            if key in seen:
                continue
            seen.add(key)
            try:
                content = md_path.read_text(encoding="utf-8", errors="replace").strip()
                results.append((module_path, suffix, content))
            except OSError:
                pass

    # 2. Local .docs/ under scope
    scope_dir = root / scope_path
    if scope_dir.exists():
        for docs_dir in scope_dir.rglob(".docs"):
            if not docs_dir.is_dir():
                continue
            for suffix in suffixes:
                for md_path in docs_dir.glob(f"*{suffix}"):
                    stem = md_path.stem.removesuffix(
                        suffix.removesuffix(".md")
                    )
                    try:
                        parent_rel = docs_dir.parent.relative_to(scope_dir)
                        module_path = f"{parent_rel / stem}".replace("\\", "/") if str(parent_rel) != "." else stem
                    except ValueError:
                        module_path = stem
                    key = (module_path, suffix)
                    if key in seen:
                        continue
                    seen.add(key)
                    try:
                        content = md_path.read_text(encoding="utf-8", errors="replace").strip()
                        results.append((module_path, suffix, content))
                    except OSError:
                        pass

    return results


def _build_markdown(
    results: list[tuple[str, str, str]],
    query: str,
    scope: str,
    include_deep: bool,
) -> str:
    """Assemble results into a single markdown document."""
    lines = [
        f"# Scout Query: {query}",
        "",
        f"**Scope:** `{scope}` | **Depth:** {'tldr + deep' if include_deep else 'tldr only'}",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "---",
        "",
    ]
    for module_path, suffix, content in sorted(results, key=lambda x: (x[0], x[1])):
        depth_label = "deep" if suffix == ".deep.md" else "tldr"
        lines.append(f"## {module_path} ({depth_label})")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).strip()


def _copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True on success."""
    try:
        proc = subprocess.run(
            ["pbcopy"],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=5,
        )
        if proc.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    try:
        proc = subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=5,
        )
        return proc.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False


async def run_query_async(query: str) -> tuple[str, Path]:
    """
    Interpret natural language via big brain, then run scout backend.
    Returns (markdown_content, output_file_path).
    """
    from vivarium.scout.big_brain import interpret_query_async

    repo_root = _repo_root()
    spec = await interpret_query_async(query)
    scope = spec.get("scope", "vivarium/scout")
    include_deep = spec.get("include_deep", False)
    copy_to_clipboard = spec.get("copy_to_clipboard", True)

    results = _collect_docs(repo_root, scope, include_deep)
    if not results:
        return (
            f"No docs found for scope `{scope}`. Run scout-doc-sync to generate .tldr.md and .deep.md.",
            Path(),
            False,
        )

    md = _build_markdown(results, query, scope, include_deep)

    temp_dir = repo_root / "docs" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_query = re.sub(r"[^\w\s-]", "", query)[:40].strip().replace(" ", "_") or "query"
    out_path = temp_dir / f"{timestamp}_{safe_query}.md"
    out_path.write_text(md, encoding="utf-8")

    did_copy = copy_to_clipboard and _copy_to_clipboard(md)
    return md, out_path, did_copy


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="scout-query",
        description="Natural language repo search. Big brain interprets your request; outputs to clipboard and docs/temp/.",
    )
    parser.add_argument(
        "query",
        nargs="+",
        metavar="Q",
        help="Natural language query",
    )
    args = parser.parse_args()

    query = " ".join(args.query)
    if not query.strip():
        parser.print_help()
        return 1

    md, out_path, did_copy = asyncio.run(run_query_async(query))

    if not out_path:
        print(md, file=sys.stderr)
        return 1

    print(f"Wrote {len(md)} chars to {out_path}")
    if did_copy:
        print("Copied to clipboard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
