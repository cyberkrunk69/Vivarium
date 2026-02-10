"""Remote execution module disabled by security policy."""

DISABLED_MESSAGE = (
    "remote_execution is disabled by security hardening. "
    "Direct SSH command execution is not allowed."
)


def execute_command(command, ip_address):
    raise RuntimeError(DISABLED_MESSAGE)