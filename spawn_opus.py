"""Compatibility shim for legacy_swarm_gen.spawn_opus."""

from legacy_swarm_gen.spawn_opus import *  # noqa: F401,F403


if __name__ == "__main__":
    import runpy

    runpy.run_module("legacy_swarm_gen.spawn_opus", run_name="__main__")

