# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testcancellationcontext.py:19
# Component id: at.source.ass_ade.test_null_cancellation_context_never_cancels
__version__ = "0.1.0"

    def test_null_cancellation_context_never_cancels(self) -> None:
        ctx = NullCancellationContext()
        ctx.cancel()
        assert ctx.check() is False
        assert ctx.is_cancelled is False
