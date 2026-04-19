# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:135
# Component id: qk.source.ass_ade.test_utilization_after_update
__version__ = "0.1.0"

    def test_utilization_after_update(self):
        budget = TokenBudget(context_window=10_000)
        budget.update_from_usage({"prompt_tokens": 5000, "completion_tokens": 100})
        assert budget.utilization == 0.5
        assert budget.completion_tokens == 100
        assert budget.total_calls == 1
