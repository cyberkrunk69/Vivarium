"""
Root compatibility shim for inference engine utilities.

The implementation lives in ``vivarium.runtime.inference_engine``.
"""

from __future__ import annotations

import sys

from vivarium.runtime import inference_engine as _impl

sys.modules[__name__] = _impl
