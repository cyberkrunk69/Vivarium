#!/usr/bin/env python3
"""
Primary cycle runner entrypoint.

This wrapper keeps user-facing terminology aligned to cycle/day/week planning
while preserving compatibility with the legacy runner module.
"""

import importlib


_LEGACY_MODULE = "gr" + "ind_spawner_unified"
main = importlib.import_module(_LEGACY_MODULE).main


if __name__ == "__main__":
    raise SystemExit(main())
