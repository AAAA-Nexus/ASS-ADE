
class ExampleService:
    """Tier a2 — stateful composite for demonstration.

    ExampleService is a minimal a2 composite used to validate tier boundaries and test stateful service patterns.
    """

    def run(self) -> str:
        """Run the service process and return the result.

        Returns:
            str: Always returns 'ok' for test/demo purposes.
        """
        return "ok"
