"""CLI bootstrap for the fresh swarm environment."""

from __future__ import annotations

import argparse
from pathlib import Path

from physics import DEFAULT_WORLD_CONTROLS, SwarmWorldControls
from swarm_environment.fresh_environment import FreshSwarmEnvironment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a fresh swarm environment")
    parser.add_argument(
        "--root",
        default="vivarium/world/fresh_swarm",
        help="Environment root directory (default: vivarium/world/fresh_swarm)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset queue and event log files after bootstrap",
    )
    parser.add_argument(
        "--max-tasks",
        type=int,
        default=DEFAULT_WORLD_CONTROLS.max_tasks,
        help=f"Maximum number of tasks in the fresh queue (default: {DEFAULT_WORLD_CONTROLS.max_tasks})",
    )
    parser.add_argument(
        "--max-instruction-chars",
        type=int,
        default=DEFAULT_WORLD_CONTROLS.max_instruction_chars,
        help=(
            "Maximum instruction payload length (default: "
            f"{DEFAULT_WORLD_CONTROLS.max_instruction_chars})"
        ),
    )
    parser.add_argument(
        "--max-metadata-keys",
        type=int,
        default=DEFAULT_WORLD_CONTROLS.max_metadata_keys,
        help=f"Maximum metadata keys per task (default: {DEFAULT_WORLD_CONTROLS.max_metadata_keys})",
    )
    parser.add_argument(
        "--max-metadata-bytes",
        type=int,
        default=DEFAULT_WORLD_CONTROLS.max_metadata_bytes,
        help=f"Maximum metadata payload bytes (default: {DEFAULT_WORLD_CONTROLS.max_metadata_bytes})",
    )
    parser.add_argument(
        "--max-result-chars",
        type=int,
        default=DEFAULT_WORLD_CONTROLS.max_result_chars,
        help=f"Maximum result payload length (default: {DEFAULT_WORLD_CONTROLS.max_result_chars})",
    )
    args = parser.parse_args(argv)

    controls = SwarmWorldControls(
        max_tasks=args.max_tasks,
        max_instruction_chars=args.max_instruction_chars,
        max_metadata_keys=args.max_metadata_keys,
        max_metadata_bytes=args.max_metadata_bytes,
        max_result_chars=args.max_result_chars,
    )
    env = FreshSwarmEnvironment(Path(args.root).resolve(), controls=controls)
    env.bootstrap(reset=args.reset)
    print(f"Fresh swarm environment ready at: {env.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

