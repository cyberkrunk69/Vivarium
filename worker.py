"""
Root compatibility shim for the canonical worker runtime.

The implementation lives in ``vivarium.runtime.worker_runtime``.
"""

from __future__ import annotations

import runpy
import sys

if __name__ != "__main__":
    from vivarium.runtime import worker_runtime as _impl

    sys.modules[__name__] = _impl
else:
    runpy.run_module("vivarium.runtime.worker_runtime", run_name="__main__")
