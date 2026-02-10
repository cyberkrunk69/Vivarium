"""Compatibility launcher for legacy_swarm_gen.fix_spawner_autodiscovery."""


def main() -> int:
    import runpy

    runpy.run_module("legacy_swarm_gen.fix_spawner_autodiscovery", run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

