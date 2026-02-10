#!/usr/bin/env python3
"""
Mutable-world rollback utility.

Usage:
  python vivarium_rollback.py --list
  python vivarium_rollback.py --list --limit 50
  python vivarium_rollback.py --rollback <commit-sha> --reason "why"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

from vivarium_scope import CHANGE_JOURNAL_FILE, get_mutable_version_control


def _read_journal(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _print_entries(entries: List[Dict[str, Any]]) -> None:
    if not entries:
        print("No journal entries.")
        return
    for item in entries:
        timestamp = item.get("timestamp", "unknown-time")
        event = item.get("event", "unknown-event")
        task_id = item.get("task_id", "-")
        commit_sha = item.get("commit_sha", "-")
        reason = item.get("reason", "")
        details = item.get("details", "")
        summary = item.get("summary", "")
        print(f"{timestamp} | {event:<20} | task={task_id} | sha={commit_sha}")
        if summary:
            print(f"  summary: {summary}")
        if reason:
            print(f"  reason: {reason}")
        if details:
            print(f"  details: {details}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Vivarium mutable-world rollback utility")
    parser.add_argument("--list", action="store_true", help="List change journal entries")
    parser.add_argument("--limit", type=int, default=20, help="How many latest entries to show")
    parser.add_argument("--rollback", type=str, default="", help="Commit SHA to rollback to")
    parser.add_argument("--reason", type=str, default="", help="Rollback reason")
    args = parser.parse_args()

    if args.list:
        rows = _read_journal(CHANGE_JOURNAL_FILE)
        if args.limit > 0:
            rows = rows[-args.limit :]
        _print_entries(rows)
        return 0

    if args.rollback:
        manager = get_mutable_version_control()
        ok = manager.rollback_to(args.rollback.strip(), reason=args.reason.strip())
        if ok:
            print(f"Rollback succeeded: {args.rollback.strip()}")
            return 0
        print(f"Rollback failed: {args.rollback.strip()}")
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
