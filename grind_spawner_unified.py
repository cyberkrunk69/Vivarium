"""Compatibility shim for legacy_swarm_gen.grind_spawner_unified."""

from legacy_swarm_gen.grind_spawner_unified import *  # noqa: F401,F403


def main(argv=None):
    from legacy_swarm_gen.grind_spawner_unified import main as _main

    return _main(argv)


if __name__ == "__main__":
    raise SystemExit(main())

