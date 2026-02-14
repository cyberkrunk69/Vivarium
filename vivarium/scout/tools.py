"""
Scout tools registry — Single source of truth for available tools.

Passed to big brain as data. No hardcoded capability strings in prompts.
"""

from __future__ import annotations

from typing import Any


def get_tools() -> list[dict[str, Any]]:
    """Return tool definitions. desc=deep for big brain. eliv=small words for user."""
    return [
        {
            "name": "index",
            "params": ["query"],
            "cost": "free",
            "speed": "instant",
            "desc": "Search code symbols (functions, classes, etc.) by name. Uses ctags+SQLite. No LLM. Use when user asks to find, search, or locate code by symbol name.",
            "eliv": "find code by name, no cost",
        },
        {
            "name": "query",
            "params": ["scope", "include_deep", "copy_to_clipboard", "output_path"],
            "cost": "free",
            "speed": "fast",
            "desc": "Read existing .tldr and .deep documentation for a package scope. Does not generate docs. Use when user asks about how something works, what a module does, or to read docs. Optional output_path: write the assembled markdown to this file (relative to repo root).",
            "eliv": "read docs we have",
        },
        {
            "name": "export",
            "params": ["scope", "output_path", "include_deep"],
            "cost": "free",
            "speed": "fast",
            "desc": "Collect .tldr (and optionally .deep) docs for a scope and write them to a single .md file. Use when user asks to write, export, or save docs to a file. Requires output_path (relative to repo root).",
            "eliv": "write docs to file",
        },
        {
            "name": "sync",
            "params": ["scope", "changed_only"],
            "cost": "expensive",
            "speed": "slow",
            "desc": "Regenerate documentation via LLM. Use only when docs are stale, missing, or user explicitly asks to generate/refresh docs.",
            "eliv": "make new docs, costs money",
        },
        {
            "name": "nav",
            "params": ["task"],
            "cost": "free_or_llm",
            "speed": "fast",
            "desc": "Find where in the codebase to implement or change something. Tries index first, then LLM. Use when user asks where to add/fix/implement something.",
            "eliv": "find where to change things",
        },
        {
            "name": "brief",
            "params": ["task"],
            "cost": "llm",
            "speed": "medium",
            "desc": "Create an investigation plan for a task. Use when user needs a structured plan before coding.",
            "eliv": "plan before you code",
        },
        {
            "name": "status",
            "params": [],
            "cost": "free",
            "speed": "instant",
            "desc": "Scout workflow dashboard: doc-sync state, drafts, spend, hooks. Use when user asks about scout's status, what's in progress, or workflow overview.",
            "eliv": "see scout workflow",
        },
        {
            "name": "branch_status",
            "params": [],
            "cost": "free",
            "speed": "fast",
            "desc": "Git branch status: current branch, commits ahead of base, PR info (if gh installed), diff stat. Use when user asks about branch status, what's on this branch, PR status, commits, or diff vs main/master.",
            "eliv": "branch info, commits, PR",
        },
        {
            "name": "help",
            "params": [],
            "cost": "llm",
            "speed": "medium",
            "desc": "List scout capabilities and suggest what to try based on repo state. Use when user asks what scout can do, or is unsure how to proceed.",
            "eliv": "ask what I do",
        },
    ]


def get_valid_tool_names() -> set[str]:
    """Tool names that can be dispatched."""
    return {t["name"] for t in get_tools()}


def get_tools_minimal() -> list[dict[str, str]]:
    """Minimal tool list for routing (name + desc only). Keeps Groq under context limits."""
    return [{"name": t["name"], "desc": t["desc"]} for t in get_tools()]
