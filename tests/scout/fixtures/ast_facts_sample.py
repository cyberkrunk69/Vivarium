"""Fixture module for ast_facts tests. Do not import — used as Path target."""

from enum import Enum

# Module-level constant
FIXTURE_CONST = 42


# Module-level function (not async)
def module_func(x: int) -> str:
    """A module-level function."""
    return str(x)


# Module-level async function (with control flow for extraction test)
async def async_module_func(y: float) -> bool:
    """A module-level async function."""
    if y > 0:
        return True
    return False


# Regular class with methods
class SampleClass:
    """A sample class with methods."""

    def sync_method(self, a: int, b: int = 1) -> int:
        return a + b

    async def async_method(self, x: str) -> str:
        return x.upper()


# Enum class — members only, no methods to attribute
class SampleEnum(Enum):
    FOO = 1
    BAR = 2
