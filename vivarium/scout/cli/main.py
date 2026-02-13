"""
Scout CLI — Configuration management.
"""

from __future__ import annotations

import argparse

import json
import os
import subprocess
import sys
from pathlib import Path

from vivarium.scout.config import EnvLoader, ScoutConfig

# TICKET-17: Auto-load .env for CLI
EnvLoader.load(Path.cwd() / ".env")
from vivarium.scout.router import TriggerRouter


def _cmd_config(args: argparse.Namespace) -> int:
    """Handle scout config subcommand."""
    config = ScoutConfig()

    if args.get:
        val = config.get(args.get)
        if val is None:
            print("(not set)", file=sys.stderr)
            return 1
        print(val)
        return 0

    if args.set:
        key, value_str = args.set[0], args.set[1]
        # TICKET-20: whimsy → ui.whimsy
        if key == "whimsy":
            key = "ui.whimsy"
            value = value_str.lower() in ("true", "1", "yes", "on")
        else:
            try:
                value = float(value_str)
            except ValueError:
                value = value_str
        if config.set(key, value):
            if key == "ui.whimsy":
                print(f"✅ Whimsy mode {'ON' if value else 'OFF'} — cave man CEO {'approved' if value else 'disabled'}")
            else:
                print(f"Set {key} = {value}")
            return 0
        print(f"Failed to set {key}", file=sys.stderr)
        return 1

    if args.tui:
        from vivarium.scout.tui import run_config_tui

        return 0 if run_config_tui() else 1

    if args.validate:
        ok, msg = config.validate_yaml()
        if ok:
            print("Valid YAML")
            return 0
        print(f"Invalid: {msg}", file=sys.stderr)
        return 1

    if args.effective:
        print(json.dumps(config.to_dict(), indent=2, default=str))
        return 0

    # Default: open in editor
    path = config.get_project_config_path()
    if not path.exists():
        path = config.get_user_config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            # Write defaults
            import yaml

            from vivarium.scout.config import DEFAULT_CONFIG

            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False)
    editor = os.environ.get("EDITOR", "nano")
    try:
        subprocess.run([editor, str(path)], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Failed to open editor: {e}", file=sys.stderr)
        return 1
    return 0


def _cmd_on_commit(args: argparse.Namespace) -> int:
    """Handle scout on-commit (git hook)."""
    files = args.files
    if not files and not sys.stdin.isatty():
        # Read from stdin if no args (e.g. from git hook piping)
        files = [f.strip() for f in sys.stdin.read().split() if f.strip()]
    # Git diff-tree outputs newline-separated; hook may pass as single arg
    expanded = []
    for f in files:
        expanded.extend(p.strip() for p in f.splitlines() if p.strip())
    paths = [Path(f) for f in expanded if f]
    router = TriggerRouter()
    router.on_git_commit(paths)
    return 0


def _cmd_prepare_commit_msg(args: argparse.Namespace) -> int:
    """Handle scout prepare-commit-msg (git hook). Populates commit message from drafts."""
    message_file = Path(args.message_file).resolve()
    if not message_file.exists():
        return 0
    router = TriggerRouter()
    router.prepare_commit_msg(message_file)
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="scout",
        description="Scout: zero-cost validation layer for LLM navigation",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_parser.add_argument(
        "--get",
        metavar="KEY",
        help="Print value (e.g. triggers.default)",
    )
    config_parser.add_argument(
        "--set",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Set value (e.g. limits.hourly_budget 2.00)",
    )
    config_parser.add_argument(
        "--tui",
        action="store_true",
        help="Interactive terminal UI",
    )
    config_parser.add_argument(
        "--validate",
        action="store_true",
        help="Check YAML syntax",
    )
    config_parser.add_argument(
        "--effective",
        action="store_true",
        help="Show merged effective config",
    )

    on_commit_parser = subparsers.add_parser("on-commit", help="Git post-commit hook (process changed files)")
    on_commit_parser.add_argument(
        "files",
        nargs="*",
        metavar="FILE",
        help="Changed files from git diff-tree",
    )

    prepare_parser = subparsers.add_parser(
        "prepare-commit-msg",
        help="Git prepare-commit-msg hook (populate message from drafts)",
    )
    prepare_parser.add_argument(
        "message_file",
        metavar="FILE",
        help="Path to commit message file (from git)",
    )

    args = parser.parse_args()

    if args.command == "on-commit":
        return _cmd_on_commit(args)
    if args.command == "prepare-commit-msg":
        return _cmd_prepare_commit_msg(args)
    if args.command == "config":
        return _cmd_config(args)
    parser.print_help()
    return 0
