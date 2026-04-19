# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testcancellationcontext.py:13
# Component id: at.source.ass_ade.test_cancellation_context_can_be_marked_cancelled
__version__ = "0.1.0"

    def test_cancellation_context_can_be_marked_cancelled(self) -> None:
        ctx = CancellationContext()
        ctx.cancel()
        assert ctx.check() is True
        assert ctx.is_cancelled is True
