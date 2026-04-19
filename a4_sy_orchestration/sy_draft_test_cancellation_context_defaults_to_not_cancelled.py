# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_cancellation.py:30
# Component id: sy.source.ass_ade.test_cancellation_context_defaults_to_not_cancelled
__version__ = "0.1.0"

    def test_cancellation_context_defaults_to_not_cancelled(self) -> None:
        ctx = CancellationContext()
        assert ctx.check() is False
        assert ctx.is_cancelled is False
