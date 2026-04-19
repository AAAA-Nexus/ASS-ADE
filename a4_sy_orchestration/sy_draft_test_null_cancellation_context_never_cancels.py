# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_cancellation.py:41
# Component id: sy.source.ass_ade.test_null_cancellation_context_never_cancels
__version__ = "0.1.0"

    def test_null_cancellation_context_never_cancels(self) -> None:
        ctx = NullCancellationContext()
        ctx.cancel()
        assert ctx.check() is False
        assert ctx.is_cancelled is False
