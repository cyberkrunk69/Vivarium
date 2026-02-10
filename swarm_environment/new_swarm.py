"""CLI bootstrap for the fresh swarm environment."""

from __future__ import annotations

import argparse
from pathlib import Path

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
    args = parser.parse_args(argv)

    env = FreshSwarmEnvironment(Path(args.root).resolve())
    env.bootstrap(reset=args.reset)
    print(f"Fresh swarm environment ready at: {env.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

