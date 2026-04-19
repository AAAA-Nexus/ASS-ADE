# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testtokenbudget.py:11
# Component id: qk.source.ass_ade.test_available
__version__ = "0.1.0"

    def test_available(self):
        budget = TokenBudget(context_window=10_000, reserve=1000)
        assert budget.available == 9000
