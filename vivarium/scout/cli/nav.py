"""
Scout Navigation CLI — Find code in 2 seconds.

Usage:
    ./devtools/scout-nav --task "fix auth timeout bug"
    ./devtools/scout-nav --task "add OAuth provider" --entry vivarium/runtime/
    ./devtools/scout-nav --file vivarium/runtime/auth.py --question "where is token refresh?"
    ./devtools/scout-nav --task "fix race condition" --json
    ./devtools/scout-nav --task "optimize query" --output briefing.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Callable, Optional

from vivarium.scout.router import TriggerRouter
from vivarium.scout.validator import Validator, validate_location


def _parse_nav_json(content: str) -> dict:
    """Extract JSON from LLM response (may be wrapped in markdown)."""
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"file": "", "function": "", "line": 0, "confidence": 0}


def _quick_parse(file_path: Path, max_chars: int = 3000) -> str:
    """Quick parse for context (first N chars)."""
    try:
        if not file_path.exists():
            return ""
        content = file_path.read_text(encoding="utf-8", errors="replace")
        return content[:max_chars]
    except OSError:
        return ""


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="scout-nav",
        description="Scout: Find code in 2 seconds",
    )
    parser.add_argument(
        "--task",
        metavar="TASK",
        help="Navigation task (e.g. 'fix auth timeout bug')",
    )
    parser.add_argument(
        "--entry",
        metavar="PATH",
        help="Entry point hint (e.g. vivarium/runtime/)",
    )
    parser.add_argument(
        "--file",
        metavar="FILE",
        help="File for Q&A mode (use with --question)",
    )
    parser.add_argument(
        "--question",
        metavar="Q",
        help="Specific question about --file",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON for scripting",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Save briefing to file",
    )
    return parser.parse_args()


async def query_file(
    file_path: Path,
    question: str,
    repo_root: Path,
    validator: Validator,
    llm_client: Optional[Callable] = None,
) -> dict:
    """Answer specific question about a file."""
    from vivarium.scout.llm import call_groq_async

    context = _quick_parse(file_path)
    try:
        rel = str(file_path.relative_to(repo_root))
    except ValueError:
        rel = str(file_path)

    prompt = f"""File: {rel}

Content (first 100 lines):
{context[:3000]}

Question: {question}

Answer with JSON only:
{{"file": "{rel}", "line": <number>, "function": "<name>", "explanation": "<brief>"}}
"""

    response = await call_groq_async(
        prompt,
        model="llama-3.1-8b-instant",
        llm_client=llm_client,
    )

    parsed = _parse_nav_json(response.content)
    if isinstance(parsed, list) and parsed:
        parsed = parsed[0]
    elif not isinstance(parsed, dict):
        parsed = {}
    suggestion = {
        "file": parsed.get("file", rel),
        "line": parsed.get("line"),
        "function": parsed.get("function", ""),
        "confidence": parsed.get("confidence", 85),
    }
    validated = validate_location(suggestion, repo_root)

    return {
        "file": rel,
        "answer": response.content,
        "validated": validated.is_valid,
        "cost": response.cost_usd,
        "target_file": suggestion.get("file"),
        "target_function": suggestion.get("function"),
        "line_estimate": suggestion.get("line"),
        "reasoning": parsed.get("explanation", ""),
    }


def print_pretty(result: dict) -> None:
    """Pretty-print navigation result."""
    print("🎯 Scout Navigation Result")
    print(f"   Task: \"{result.get('task', '')}\"")
    model = result.get("model_used", "")
    retries = result.get("retries", 0)
    esc = result.get("escalated", False)
    if retries or esc:
        suffix = " (retried once, escalated to 70b)" if esc else f" (retried {retries}x)"
        print(f"   Model: {model}{suffix}")
    else:
        print(f"   Model: {model}")
    print(f"   Cost: ${result.get('cost_usd', 0):.4f}")
    print(f"   Time: {result.get('duration_ms', 0) / 1000:.1f}s")
    print(f"   Confidence: {result.get('confidence', 0)}%")
    print()
    print(f"📍 Target: {result.get('target_file', '')}:{result.get('line_estimate', 0)}")
    fn = result.get("target_function", "")
    if fn:
        print(f"   Function: {fn}()")
    sig = result.get("signature", "")
    if sig:
        print(f"   Signature: {sig}")
    print()
    reasoning = result.get("reasoning", "")
    if reasoning:
        print(f"🧭 Reasoning: {reasoning}")
    sugg = result.get("suggestion", "")
    if sugg:
        print(f"\n💡 Suggestion: {sugg}")
    related = result.get("related_files", [])
    if related:
        print("\n🔗 Related Files:")
        for r in related:
            print(f"   • {r}")


async def generate_brief(result: dict, task: str) -> str:
    """Generate markdown briefing from result."""
    lines = [
        f"# Scout Briefing: {task}",
        "",
        f"**Target:** `{result.get('target_file', '')}:{result.get('line_estimate', 0)}`",
        f"**Function:** {result.get('target_function', '')}",
        f"**Confidence:** {result.get('confidence', 0)}%",
        "",
        "## Reasoning",
        result.get("reasoning", ""),
        "",
        "## Suggestion",
        result.get("suggestion", ""),
        "",
        f"*Generated by scout-nav (cost: ${result.get('cost_usd', 0):.4f})*",
    ]
    return "\n".join(lines)


async def _main_async(args: argparse.Namespace) -> int:
    """Async main entry."""
    repo_root = Path.cwd().resolve()

    # Try scout-index first (free) when we have a task — before any LLM/audit
    if args.task and not (args.file and args.question):
        try:
            from vivarium.scout.cli.index import query_for_nav

            suggestions_list = query_for_nav(repo_root, args.task)
            if suggestions_list:
                # Pick first result (index returns best-first list)
                index_result = suggestions_list[0] if isinstance(suggestions_list[0], dict) else None
                if index_result and index_result.get("confidence", 0) >= 80:
                    # Normalize to router output format for print_pretty
                    result = {
                        "task": index_result.get("task", args.task),
                        "target_file": index_result.get("target_file", ""),
                        "target_function": index_result.get("target_function", ""),
                        "line_estimate": index_result.get("line_estimate", 0),
                        "confidence": index_result.get("confidence", 85),
                        "model_used": index_result.get("model_used", "scout-index"),
                        "cost_usd": index_result.get("cost_usd", 0.0),
                        "duration_ms": index_result.get("duration_ms", 0),
                        "retries": 0,
                        "escalated": False,
                        "related_files": index_result.get("related_files", []),
                        "reasoning": index_result.get("reasoning", ""),
                        "suggestion": index_result.get("suggestion", ""),
                    }
                    if args.json:
                        print(json.dumps(result, indent=2))
                    else:
                        print_pretty(result)
                    if args.output:
                        brief = await generate_brief(result, args.task)
                        Path(args.output).write_text(brief)
                    return 0
        except Exception:
            pass  # Fall through to LLM

    router = TriggerRouter(repo_root=repo_root)

    if args.file and args.question:
        # File-specific Q&A mode
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = (repo_root / file_path).resolve()
        result = await query_file(file_path, args.question, repo_root, router.validator)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"📄 File: {result.get('file', '')}")
            print(f"   Answer: {result.get('answer', '')[:500]}")
            if result.get("validated"):
                print(f"   ✓ Validated: {result.get('target_file')}:{result.get('line_estimate')}")
            print(f"   Cost: ${result.get('cost', 0):.4f}")
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2))
        return 0

    if not args.task:
        print("Error: --task required for navigation mode", file=sys.stderr)
        return 1

    # General navigation mode — use router
    entry = Path(args.entry) if args.entry else None
    result = await router.navigate_task(task=args.task, entry=entry)

    if result is None:
        print("Estimated cost exceeds limit. Aborting.", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_pretty(result)

    if args.output:
        brief = await generate_brief(result, args.task)
        Path(args.output).write_text(brief)

    return 0


def main() -> int:
    """Main entry point."""
    args = parse_args()
    return asyncio.run(_main_async(args))


if __name__ == "__main__":
    sys.exit(main())
