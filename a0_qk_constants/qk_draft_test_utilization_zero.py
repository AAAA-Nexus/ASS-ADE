# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:131
# Component id: qk.source.ass_ade.test_utilization_zero
__version__ = "0.1.0"

    def test_utilization_zero(self):
        budget = TokenBudget(context_window=10_000)
        assert budget.utilization == 0.0
