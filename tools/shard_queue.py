"""
Shard queue.json into queue_shards/queue_<id>.json files.

This keeps sharding logic consistent with worker.py so large resident counts
can read only their shard file without scanning the full queue.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, Dict, List

from utils import read_json, write_json


def _task_shard(task_id: str, shard_count: int) -> int:
    digest = hashlib.sha1(task_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % shard_count


def _clean_shards(out_dir: Path) -> None:
    if not out_dir.exists():
        return
    for path in out_dir.glob("queue_*.json"):
        try:
            path.unlink()
        except OSError:
            continue


def shard_queue(input_path: Path, out_dir: Path, shard_count: int, dry_run: bool) -> int:
    queue = read_json(input_path, default=None)
    if not isinstance(queue, dict):
        raise ValueError("queue.json must be an object")

    tasks = queue.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("queue.json tasks must be a list")

    base = dict(queue)
    base["tasks"] = []

    shards: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(shard_count)}
    skipped = 0
    for task in tasks:
        task_id = str(task.get("id", "")).strip()
        if not task_id:
            skipped += 1
            continue
        shard_id = _task_shard(task_id, shard_count)
        shards[shard_id].append(task)

    if dry_run:
        for shard_id in range(shard_count):
            print(f"shard {shard_id}: {len(shards[shard_id])} tasks")
        if skipped:
            print(f"skipped {skipped} tasks without id", file=sys.stderr)
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    for shard_id, shard_tasks in shards.items():
        shard_queue_data = dict(base)
        shard_queue_data["tasks"] = shard_tasks
        write_json(out_dir / f"queue_{shard_id}.json", shard_queue_data)

    if skipped:
        print(f"skipped {skipped} tasks without id", file=sys.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Shard queue.json into shard files.")
    parser.add_argument("--input", default="queue.json", help="Path to queue.json")
    parser.add_argument("--out-dir", default="queue_shards", help="Output directory")
    parser.add_argument("--shards", type=int, required=True, help="Number of shards")
    parser.add_argument("--clean", action="store_true", help="Remove existing shard files")
    parser.add_argument("--dry-run", action="store_true", help="Print shard sizes only")
    args = parser.parse_args()

    if args.shards <= 0:
        print("shards must be > 0", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    if args.clean:
        _clean_shards(out_dir)

    try:
        return shard_queue(input_path, out_dir, args.shards, args.dry_run)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
