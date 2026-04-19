# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:122
# Component id: qk.source.ass_ade.test_for_model
__version__ = "0.1.0"

    def test_for_model(self):
        budget = TokenBudget.for_model("gpt-4o")
        assert budget.context_window == 128_000
        assert budget.reserve == RESPONSE_RESERVE
