# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testcancellationcontext.py:8
# Component id: at.source.ass_ade.test_cancellation_context_defaults_to_not_cancelled
__version__ = "0.1.0"

    def test_cancellation_context_defaults_to_not_cancelled(self) -> None:
        ctx = CancellationContext()
        assert ctx.check() is False
        assert ctx.is_cancelled is False
