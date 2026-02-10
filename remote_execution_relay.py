#!/usr/bin/env python3
"""Remote execution relay intentionally disabled.

This repository previously contained multiple experimental relay servers in
this module. Those variants accepted and forwarded remote command execution,
which is too risky for default repository state.

The relay is now fail-closed. Reintroduction should happen only through a new,
reviewed implementation with strong authentication, authorization, and command
sandboxing.
"""

from __future__ import annotations

import sys


DISABLED_MESSAGE = (
    "remote_execution_relay is disabled by security hardening. "
    "Remote command relay is not available."
)


def start_relay() -> None:
    """Legacy entrypoint kept to fail closed."""
    raise RuntimeError(DISABLED_MESSAGE)


def create_app():
    """Compatibility helper retained to make disablement explicit."""
    raise RuntimeError(DISABLED_MESSAGE)


def main() -> int:
    print(DISABLED_MESSAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
