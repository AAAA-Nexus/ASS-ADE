"""Sample symbols for tier classification."""


def pure_helper(value: int) -> int:
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
        return "ok"
