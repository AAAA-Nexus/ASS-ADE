"""Sample symbols for tier classification."""


def pure_helper(value: int) -> int:
    """Helper function to increment a given integer value.
    
    Args:
        value: The integer to be incremented.
    
    Returns:
        The incremented integer value.
    """
    return value + 1


def caller_uses_helper() -> int:
    """Calls pure_helper so Phase 3 can derive a made_of edge."""
    return pure_helper(0)


def invariant_metadata() -> str:
    """Name + path cue ``invariant`` → a0 tier for mini-rebuild tests."""
    return "meta"


class ExampleService:
    """Stateful-looking name for a2 default path."""

def run(self) -> str:
        """Runs the process and returns the result.

        Args:
            None

        Returns:
            str: The result of the process.
        """
        return "ok"
