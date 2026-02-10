#!/usr/bin/env python3
"""Remote execution client intentionally disabled.

This repository previously contained multiple experimental remote execution
client implementations in this module. Because those variants included unsafe
command execution patterns, the module is now reduced to a hard fail-safe.

Any attempt to run or import-and-start this client should fail closed.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


DISABLED_MESSAGE = (
    "remote_execution_client is disabled by security hardening. "
    "Do not execute remote commands from this repository."
)


@dataclass(frozen=True)
class RemoteExecutionClient:
    """Fail-closed placeholder retained for import compatibility."""

    reason: str = DISABLED_MESSAGE

    def start(self) -> None:
        raise RuntimeError(self.reason)

    def stop(self) -> None:
        raise RuntimeError(self.reason)


def start_client() -> None:
    """Legacy entrypoint kept to fail closed."""
    raise RuntimeError(DISABLED_MESSAGE)


def main() -> int:
    print(DISABLED_MESSAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
