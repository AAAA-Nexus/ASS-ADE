# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:155
# Component id: qk.source.ass_ade.test_messages_to_evict_over_budget
__version__ = "0.1.0"

    def test_messages_to_evict_over_budget(self):
        budget = TokenBudget(context_window=50, reserve=10)  # very small
        messages = [
            Message(role="system", content="System prompt"),
            Message(role="user", content="A" * 200),
            Message(role="assistant", content="B" * 200),
            Message(role="user", content="C" * 50),
        ]
        evictions = budget.messages_to_evict(messages)
        assert evictions > 0
