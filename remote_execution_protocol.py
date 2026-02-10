"""Remote execution protocol module disabled by security policy."""

DISABLED_MESSAGE = (
    "remote_execution_protocol is disabled by security hardening. "
    "Remote host command channels are not allowed."
)


def execute_command_on_own_machine(ip, command):
    raise RuntimeError(DISABLED_MESSAGE)