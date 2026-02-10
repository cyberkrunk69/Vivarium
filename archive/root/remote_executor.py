"""Remote executor disabled by security policy."""

DISABLED_MESSAGE = (
    "remote_executor is disabled by security hardening. "
    "Remote command execution is not allowed."
)


def execute_remotely(command, ip_address):
    raise RuntimeError(DISABLED_MESSAGE)