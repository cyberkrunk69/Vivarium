"""Compatibility shim for legacy_swarm_gen.opus_orchestrator."""

from legacy_swarm_gen.opus_orchestrator import *  # noqa: F401,F403


def main():
    from legacy_swarm_gen.opus_orchestrator import main as _main

    return _main()


if __name__ == "__main__":
    raise SystemExit(main())

