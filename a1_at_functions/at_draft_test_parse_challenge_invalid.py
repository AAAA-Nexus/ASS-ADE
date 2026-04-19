# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:166
# Component id: at.source.ass_ade.test_parse_challenge_invalid
__version__ = "0.1.0"

    def test_parse_challenge_invalid(self) -> None:
        """X402ClientFlow should set last_error on parse failure."""
        flow = X402ClientFlow()
        challenge = flow.parse_challenge({})  # Missing required fields
        assert challenge is None
        assert flow.last_error  # Error should be set
