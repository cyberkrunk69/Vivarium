"""Compatibility shim for legacy_swarm_gen.spawner."""

from legacy_swarm_gen.spawner import *  # noqa: F401,F403


def main():
    from legacy_swarm_gen.spawner import main as _main

    return _main()


if __name__ == "__main__":
    raise SystemExit(main())

