# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:24
# Component id: sy.source.ass_ade.test_system_prompt
__version__ = "0.1.0"

    def test_system_prompt(self):
        c = Conversation("You are helpful.")
        assert c.count() == 1
        assert c.messages[0].role == "system"
