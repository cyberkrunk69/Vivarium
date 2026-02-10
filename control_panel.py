"""
Root compatibility shim for the Vivarium control panel.

The implementation lives in ``vivarium.runtime.control_panel_app``.
"""

from __future__ import annotations

import runpy
import sys

if __name__ != "__main__":
    from vivarium.runtime import control_panel_app as _impl

    sys.modules[__name__] = _impl
else:
    runpy.run_module("vivarium.runtime.control_panel_app", run_name="__main__")
