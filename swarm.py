"""
Root compatibility shim for the canonical Vivarium API server.

The implementation lives in ``vivarium.runtime.swarm_api``.
"""

from __future__ import annotations

import sys

if __name__ != "__main__":
    from vivarium.runtime import swarm_api as _impl

    sys.modules[__name__] = _impl
else:
    try:
        import uvicorn
    except ImportError as exc:  # pragma: no cover - convenience path
        raise SystemExit(f"uvicorn is required to run swarm.py directly: {exc}") from exc

    uvicorn.run("vivarium.runtime.swarm_api:app", host="127.0.0.1", port=8420)
