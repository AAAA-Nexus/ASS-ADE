# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:142
# Component id: qk.source.ass_ade.test_update_none_usage
__version__ = "0.1.0"

    def test_update_none_usage(self):
        budget = TokenBudget(context_window=10_000)
        budget.update_from_usage(None)
        assert budget.total_calls == 0
