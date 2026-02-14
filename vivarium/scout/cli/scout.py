"""
Scout natural-language CLI — Single entry point for nat-lang commands.

LLM always picks the tool from user input. Execution is programmatic. When reasoning
on data: always use tldr/deep docs first; only look at raw code when docs insufficient.

Usage:
    scout "user input"
"""

from __future__ import annotations

# Suppress noisy warnings from transitive deps (Python 3.9 EOL, urllib3/LibreSSL)
import warnings

warnings.filterwarnings("ignore", message=".*Python version 3.9.*")
warnings.filterwarnings("ignore", message=".*urllib3.*OpenSSL.*")
warnings.filterwarnings("ignore", message=".*LibreSSL.*")

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from vivarium.scout.config import EnvLoader

# TICKET-17: Auto-load .env for CLI (no manual source required)
EnvLoader.load(Path.cwd() / ".env")

# Chat history for single-turn: so "what did I just say?" works across invocations
CHAT_HISTORY_FILE = ".scout/chat_history.json"
MAX_HISTORY_MESSAGES = 20  # last N messages (10 exchanges)


def _repo_root() -> Path:
    return Path.cwd().resolve()


def _load_chat_history(repo_root: Path) -> list[dict]:
    """Load prior user/assistant messages from repo .scout/chat_history.json."""
    path = repo_root / CHAT_HISTORY_FILE
    if not path.exists():
        return []
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if isinstance(data, list):
            return data[-MAX_HISTORY_MESSAGES:]
        return []
    except (OSError, json.JSONDecodeError):
        return []


def _save_chat_history(repo_root: Path, messages: list[dict]) -> None:
    """Save user/assistant messages (no tool internals) for next run."""
    path = repo_root / CHAT_HISTORY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps(messages[-MAX_HISTORY_MESSAGES:], indent=0), encoding="utf-8")
    except OSError:
        pass


def _cwd_scope(repo_root: Path) -> str:
    """Infer package scope from current directory (e.g. vivarium/scout if in that dir)."""
    cwd = Path.cwd().resolve()
    try:
        rel = cwd.relative_to(repo_root)
        parts = rel.parts
        if not parts:
            return "vivarium"
        # If we're inside vivarium/, use that path
        if parts[0] == "vivarium":
            return "/".join(parts)
        return "vivarium"
    except ValueError:
        return "vivarium"


async def _run_index(spec: dict, repo_root: Path) -> int:
    """Run scout-index query. Zero LLM, instant."""
    q = spec.get("query") or spec.get("task", "")
    if not q:
        print("Error: index tool requires query string", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, "-m", "vivarium.scout.cli.index", "query", q],
        cwd=repo_root,
    )
    return result.returncode


async def _run_nav(spec: dict, repo_root: Path) -> int:
    """Run scout-nav. Uses index when confident (free), else LLM."""
    task = spec.get("task") or spec.get("query", "")
    if not task:
        print("Error: nav tool requires task", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, "-m", "vivarium.scout.cli.nav", "--task", task],
        cwd=repo_root,
    )
    return result.returncode


async def _run_brief(spec: dict, repo_root: Path) -> int:
    """Run scout-brief. Investigation plan."""
    task = spec.get("task") or spec.get("query", "")
    if not task:
        print("Error: brief tool requires task", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, "-m", "vivarium.scout.cli.brief", "--task", task],
        cwd=repo_root,
    )
    return result.returncode


async def _run_status(spec: dict, repo_root: Path) -> int:
    """Run scout-status. Workflow dashboard."""
    result = subprocess.run(
        [sys.executable, "-m", "vivarium.scout.cli.root", "status"],
        cwd=repo_root,
    )
    return result.returncode


def _gather_repo_state(repo_root: Path, caveman: bool = False) -> dict:
    """Gather repo state for big brain. Data only."""
    state = {"cwd_scope": _cwd_scope(repo_root), "caveman_mode": caveman}
    try:
        from vivarium.scout.git_analyzer import get_changed_files

        staged = get_changed_files(staged_only=True, repo_root=repo_root)
        state["staged_files"] = [str(p) for p in staged[:20]]
        state["staged_count"] = len(staged)
    except Exception:
        state["staged_files"] = []
        state["staged_count"] = 0
    index_db = repo_root / ".scout" / "index.db"
    state["has_index"] = index_db.exists()
    return state


async def _run_help(spec: dict, repo_root: Path, query: str = "") -> int:
    """User asked what scout can do. Big brain lists capabilities, suggests one, you be the judge."""
    from vivarium.scout.big_brain import answer_help_async

    caveman = spec.get("caveman_mode", False)
    state = _gather_repo_state(repo_root, caveman=caveman)
    response = await answer_help_async(state, query=query)
    print(response)
    return 0


async def _run_sync(spec: dict, repo_root: Path) -> int:
    """Run scout-doc-sync generate for the given scope."""
    scope = spec.get("scope", "vivarium")
    changed_only = spec.get("changed_only", False)
    target = repo_root / scope
    if not target.exists():
        print(f"Error: Scope path does not exist: {target}", file=sys.stderr)
        return 1

    args = [
        sys.executable,
        "-m",
        "vivarium.scout.cli.doc_sync",
        "generate",
        "--target",
        str(target),
        "--recursive",
        "--changed-only",
        "--budget",
        "0.15",
        "-q",
    ]
    if changed_only:
        args.append("--staged")
    result = subprocess.run(args, cwd=repo_root)
    return result.returncode


async def _run_query(spec: dict, query: str, repo_root: Path) -> int:
    """Run scout-query (collect docs, clipboard, temp file)."""
    import re
    from datetime import datetime

    from vivarium.scout.cli.query import (
        _build_markdown,
        _collect_docs,
        _copy_to_clipboard,
    )

    scope = spec.get("scope", "vivarium/scout")
    include_deep = spec.get("include_deep", False)
    copy_to_clipboard = spec.get("copy_to_clipboard", True)

    results = _collect_docs(repo_root, scope, include_deep)
    if not results:
        print(
            f"No docs found for scope `{scope}`. Run scout doc-sync or: scout \"refresh the docs\"",
            file=sys.stderr,
        )
        return 1

    md = _build_markdown(results, query, scope, include_deep)
    temp_dir = repo_root / "docs" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_query = re.sub(r"[^\w\s-]", "", query)[:40].strip().replace(" ", "_") or "query"
    out_path = temp_dir / f"{timestamp}_{safe_query}.md"
    out_path.write_text(md, encoding="utf-8")

    did_copy = copy_to_clipboard and _copy_to_clipboard(md)
    print(f"Wrote {len(md)} chars to {out_path}")
    if did_copy:
        print("Copied to clipboard.")
    return 0


async def _run_tool(spec: dict, tool: str, query: str, repo_root: Path) -> int:
    """Run a tool and return exit code."""
    spec["caveman_mode"] = spec.get("caveman_mode", False)
    runners = {
        "index": _run_index,
        "query": lambda s, r: _run_query(s, query, r),
        "sync": _run_sync,
        "nav": _run_nav,
        "brief": _run_brief,
        "status": _run_status,
        "help": lambda s, r: _run_help(s, r, query),
    }
    if tool not in runners:
        return 1
    return await runners[tool](spec, repo_root)


async def _run_tool_and_capture_async(spec: dict, tool: str, query: str, repo_root: Path) -> str:
    """Run help, query, or export (async tools) with captured output."""
    from vivarium.scout.cli.query import _build_markdown, _collect_docs

    if tool == "query":
        scope = spec.get("scope", "vivarium/scout")
        output_path = spec.get("output_path")

        # TICKET-43: Gated path — hydrate FACTS (never prose), gate consumes structured truth
        if not output_path:
            from vivarium.scout.context import (
                _route_query_to_files,
                hydrate_facts,
            )
            from vivarium.scout.deps import DependencyGraph, SymbolRef
            from vivarium.scout.big_brain import call_big_brain_gated_async

            files = _route_query_to_files(query, scope, repo_root)
            deps = DependencyGraph(repo_root)
            query_syms = [SymbolRef(f, "") for f in files] if files else None

            if not files:
                return f"No files found for scope {scope}. Run scout \"refresh the docs\" first."

            # TICKET-43: Load STRUCTURED FACTS only — never prose
            facts = await hydrate_facts(
                symbols=query_syms or [],
                deps_graph=deps,
                repo_root=repo_root,
                max_facts=300,
                max_depth=2,
            )
            if not facts.symbols:
                return f"No .facts.json found for scope {scope}. Run: ./devtools/scout-doc-sync generate -t {scope} --hybrid --force"

            # TICKET-27: Gate whimsy when SCOUT_WHIMSY=1
            on_decision = None
            on_decision_async = None
            try:
                from vivarium.scout.config import ScoutConfig
                from vivarium.scout.middle_manager import GateDecision
                from vivarium.scout.ui.whimsy import (
                    generate_gate_whimsy,
                    decision_to_whimsy_params,
                )
                if ScoutConfig().whimsy_mode:
                    async def _print_whimsy(d: GateDecision) -> None:
                        cost = getattr(d, "cost_usd", 0) or (
                            0.05 if d.decision == "pass" else 0.50
                        )
                        params = decision_to_whimsy_params(d, cost)
                        line = await generate_gate_whimsy(**params)
                        print(line, file=sys.stderr)
                    on_decision_async = _print_whimsy
            except ImportError:
                pass

            response = await call_big_brain_gated_async(
                question=query,
                facts=facts,
                task_type="query",
                deps_graph=deps,
                query_symbols=query_syms,
                on_decision_async=on_decision_async,
            )
            content = response.content.strip()
            if not content:
                return (
                    "The gate escalated (low confidence) but the synthesis returned empty. "
                    "Try: ./devtools/scout-doc-sync generate -t vivarium/scout --hybrid --force "
                    "to refresh facts, then run again."
                )
            return content

        # Export path (output_path set): legacy behavior, full docs
        include_deep = spec.get("include_deep", True)
        results = _collect_docs(repo_root, scope, include_deep)
        if not results:
            return f"No docs found for scope {scope}. Run scout \"refresh the docs\" first."
        md = _build_markdown(results, query, scope, include_deep)
        p = (repo_root / output_path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md, encoding="utf-8")
        return f"Wrote {len(md)} chars to {p}"

    if tool == "export":
        scope = spec.get("scope", "vivarium")
        output_path = spec.get("output_path")
        include_deep = spec.get("include_deep", False)
        if not output_path:
            return "Error: export requires output_path (relative to repo root)."
        results = _collect_docs(repo_root, scope, include_deep)
        if not results:
            return f"No docs found for scope {scope}. Run scout \"refresh the docs\" first."
        md = _build_markdown(results, query, scope, include_deep)
        p = (repo_root / output_path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md, encoding="utf-8")
        return f"Wrote {len(md)} chars to {p}"

    import io
    buf = io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    try:
        sys.stdout = sys.stderr = buf
        await _run_tool(spec, tool, query, repo_root)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
    return buf.getvalue().strip()


async def _run_tool_captured(spec: dict, tool: str, query: str, repo_root: Path) -> str:
    """Run tool with captured stdout+stderr. Returns combined output."""
    q = spec.get("query") or spec.get("task", "") or query
    scope = spec.get("scope", "vivarium")
    changed_only = spec.get("changed_only", False)
    target = repo_root / scope
    script_branch = repo_root / "devtools" / "branch-status.sh"
    if not script_branch.exists():
        script_branch = repo_root / "devtools" / "scripts" / "branch-status.sh"
    args_map = {
        "index": [sys.executable, "-m", "vivarium.scout.cli.index", "query", q],
        "nav": [sys.executable, "-m", "vivarium.scout.cli.nav", "--task", q],
        "brief": [sys.executable, "-m", "vivarium.scout.cli.brief", "--task", q],
        "status": [sys.executable, "-m", "vivarium.scout.cli.root", "status"],
        "branch_status": ["bash", str(script_branch)] if script_branch.exists() else None,
        "sync": [
            sys.executable, "-m", "vivarium.scout.cli.doc_sync", "generate",
            "--target", str(target), "--recursive", "--changed-only", "--budget", "0.15", "-q"
        ] + (["--staged"] if changed_only else []),
    }
    if tool in ("help", "query", "export"):
        return await _run_tool_and_capture_async(spec, tool, query, repo_root)
    if tool == "branch_status" and args_map.get("branch_status"):
        result = subprocess.run(args_map["branch_status"], cwd=repo_root, capture_output=True, text=True)
        out = (result.stdout or "").strip()
        err = (result.stderr or "").strip()
        out_dir = repo_root / "devtools" / "branch-status"
        if out_dir.exists():
            latest = sorted(out_dir.glob("branch-status_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
            if latest:
                out = latest[0].read_text(encoding="utf-8", errors="replace") + "\n\n" + out
        return f"{out}\n{err}".strip()
    if tool not in args_map or args_map.get(tool) is None:
        return ""
    result = subprocess.run(
        args_map[tool],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    out = (result.stdout or "").strip()
    err = (result.stderr or "").strip()
    return f"{out}\n{err}".strip()


MAX_TOOL_STEPS = 5  # Max tool calls per user message before forcing a reply

# ANSI color codes (only used when stderr is a TTY and SCOUT_NO_COLOR not set)
def _color(s: str, code: str) -> str:
    if not getattr(sys.stderr, "isatty", lambda: False)():
        return s
    if os.environ.get("SCOUT_NO_COLOR", "").lower() in ("1", "true", "yes"):
        return s
    return f"\033[{code}m{s}\033[0m"


MAX_DISPLAY_LINES = 80  # Truncate long output to avoid terminal overflow


def _truncate_output(text: str, repo_root: Path) -> str:
    """If output is very long, write full to temp file and return truncated + note."""
    lines = text.split("\n")
    if len(lines) <= MAX_DISPLAY_LINES:
        return text
    temp_dir = repo_root / "docs" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = temp_dir / f"scout_output_{ts}.md"
    out_path.write_text(text, encoding="utf-8")
    head = "\n".join(lines[:MAX_DISPLAY_LINES])
    return f"{head}\n\n... [truncated: {len(lines) - MAX_DISPLAY_LINES} more lines]\nFull output: {out_path}"


def _color_output(text: str) -> str:
    """Color markdown-style output when stdout is a TTY."""
    if not text or not getattr(sys.stdout, "isatty", lambda: False)():
        return text
    if os.environ.get("SCOUT_NO_COLOR", "").lower() in ("1", "true", "yes"):
        return text
    dim, green, green_bold, table = "\033[2m", "\033[32m", "\033[32;1m", "\033[90m"
    reset = "\033[0m"
    out = []
    in_code = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            out.append(f"{dim}{line}{reset}" if in_code else line)
        elif in_code:
            out.append(f"{dim}{line}{reset}")
        elif line.startswith("## "):
            out.append(f"{green_bold}{line}{reset}")
        elif line.startswith("### "):
            out.append(f"{green}{line}{reset}")
        elif line.startswith("|") and "|" in line[1:]:
            out.append(f"{table}{line}{reset}")
        else:
            out.append(line)
    return "\n".join(out)


def _last_tool_output(messages: list[dict]) -> str | None:
    """Return content of the most recent tool result in messages, or None."""
    for m in reversed(messages):
        content = m.get("content", "")
        if "[Tool " in content and "result]" in content:
            match = re.search(r"\[Tool (\w+) result\]:\s*\n(.*)", content, re.DOTALL)
            if match and match.group(2).strip():
                return match.group(2).strip()
    return None


def _progress(msg: str) -> None:
    """Print progress to stderr so user sees what's happening."""
    prefix = _color("Scout:", "36")  # cyan
    print(f"  {prefix} {msg}", file=sys.stderr, flush=True)


def _get_cost_since(since) -> tuple[float, dict[str, float]]:
    """Sum audit costs since timestamp. Returns (total, breakdown_by_event)."""
    from vivarium.scout.audit import AuditLog

    audit = AuditLog()
    try:
        events = audit.query(since=since)
    finally:
        audit.close()
    total = 0.0
    by_event: dict[str, float] = {}
    for e in events:
        c = e.get("cost") or 0
        if c <= 0:
            continue
        total += c
        ev = e.get("event", "?")
        by_event[ev] = by_event.get(ev, 0) + c
    return total, by_event


def _print_cost(since) -> None:
    """Print cost summary for this response if SCOUT_HIDE_COST not set."""
    if os.environ.get("SCOUT_HIDE_COST", "").lower() in ("1", "true", "yes"):
        return
    total, by_event = _get_cost_since(since)
    if total <= 0:
        return
    parts = [_color(f"${total:.4f}", "33")]  # yellow for total
    for ev, c in sorted(by_event.items(), key=lambda x: -x[1]):
        parts.append(f"{ev}: ${c:.4f}")
    line = "  [cost: " + ", ".join(parts) + "]"
    print(line, file=sys.stderr, flush=True)


async def _turn_async(
    messages: list[dict],
    query: str,
    repo_root: Path,
    caveman: bool,
) -> tuple[str, int]:
    """Chat turn. Uses tools to gather info, then answers. Returns (output_text, exit_code)."""
    from vivarium.scout.big_brain import chat_turn_async, parse_chat_response

    since = datetime.now(timezone.utc)
    state = _gather_repo_state(repo_root, caveman=caveman)
    state["cwd_scope"] = _cwd_scope(repo_root)
    steps = 0

    while steps < MAX_TOOL_STEPS:
        _progress("routing..." if steps == 0 else "synthesizing...")
        raw = await chat_turn_async(
            messages, repo_state=state, caveman=caveman, progress_cb=_progress
        )
        kind, payload = parse_chat_response(raw)

        if kind == "message":
            if payload is not None:
                _print_cost(since)
                return payload, 0
            # Empty: return tool output if we have it, else bail (no nudge loop)
            last_out = _last_tool_output(messages)
            if last_out:
                _print_cost(since)
                return last_out, 0
            _print_cost(since)
            return "No response. Try rephrasing.", 0

        # Tool: run it, add output to messages, loop so model can answer from it
        spec = payload
        _progress(f"running {spec['tool']}...")
        spec.setdefault("scope", state["cwd_scope"])
        spec.setdefault("include_deep", False)
        spec.setdefault("copy_to_clipboard", True)
        spec.setdefault("changed_only", False)
        spec["caveman_mode"] = caveman
        output = await _run_tool_captured(spec, spec["tool"], query, repo_root)
        messages.append({"role": "assistant", "content": f"[Tool {spec['tool']} result]:\n{output}"})
        steps += 1
        # query/export output IS the answer—no synthesis needed, avoids Groq context limit
        if spec["tool"] in ("query", "export") and output:
            _print_cost(since)
            return output, 0

    # Max steps: one more synthesis attempt, then return tool output or short message
    _progress("synthesizing...")
    raw = await chat_turn_async(
        messages, repo_state=state, caveman=caveman, progress_cb=_progress
    )
    kind, payload = parse_chat_response(raw)
    if kind == "message" and payload:
        _print_cost(since)
        return payload, 0
    last_out = _last_tool_output(messages)
    _print_cost(since)
    return last_out if last_out else "No response. Try rephrasing.", 0


def _is_explain_how_question(query: str) -> bool:
    """True if query clearly needs the query tool (codebase explanation)."""
    q = query.lower().strip()
    return any(
        q.startswith(p) or p in q[:50]
        for p in ("explain how", "how does", "how do ", "what does ", "how does ")
    )


async def _main_async(query: str | None, caveman: bool = False) -> int:
    repo_root = _repo_root()
    cwd_scope = _cwd_scope(repo_root)
    state = _gather_repo_state(repo_root, caveman=caveman)
    state["cwd_scope"] = cwd_scope

    if query is None:
        # REPL mode
        messages: list[dict] = []
        prompt = "scout> "
        while True:
            try:
                line = input(prompt)
            except EOFError:
                break
            line = line.strip()
            if not line:
                continue
            if line.lower() in ("quit", "exit", "q"):
                break
            messages.append({"role": "user", "content": line})
            output, _ = await _turn_async(messages, line, repo_root, caveman)
            display = _truncate_output(output, repo_root)
            print(_color_output(display))
            messages.append({"role": "assistant", "content": output})
        return 0

    # Single turn: shortcut for "explain how" questions — run query directly (avoids wrong tool pick)
    history = _load_chat_history(repo_root)
    messages = list(history)
    messages.append({"role": "user", "content": query})

    if _is_explain_how_question(query):
        # Bypass LLM routing: run query tool directly for codebase explanation questions
        since = datetime.now(timezone.utc)
        spec = {"tool": "query", "scope": cwd_scope, "include_deep": False}
        output = await _run_tool_and_capture_async(spec, "query", query, repo_root)
        if output:
            _print_cost(since)
            display = _truncate_output(output, repo_root)
            print(_color_output(display))
            _save_chat_history(
                repo_root,
                history + [{"role": "user", "content": query}, {"role": "assistant", "content": output}],
            )
            return 0
        # Fall through to normal flow if query returned empty

    output, _ = await _turn_async(messages, query, repo_root, caveman)
    display = _truncate_output(output, repo_root)
    print(_color_output(display))
    history = _load_chat_history(repo_root)
    _save_chat_history(repo_root, history + [{"role": "user", "content": query}, {"role": "assistant", "content": output}])
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="scout",
        description="Scout: natural language chat. scout \"message\" or scout for REPL.",
    )
    parser.add_argument(
        "query",
        nargs="*",
        metavar="MESSAGE",
        help="Natural language command (omit for interactive REPL)",
    )
    args = parser.parse_args()
    query = " ".join(args.query).strip() if args.query else None
    caveman = os.environ.get("SCOUT_CAVEMAN", "").lower() in ("1", "true", "yes")
    try:
        return asyncio.run(_main_async(query, caveman=caveman))
    except (EnvironmentError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
