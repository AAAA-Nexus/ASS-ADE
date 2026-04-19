# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlseengine.py:79
# Component id: mo.source.ass_ade.test_claude_tier_alias_in_tier_policy
__version__ = "0.1.0"

    def test_claude_tier_alias_in_tier_policy(self):
        """tier_policy should accept 'haiku'/'sonnet'/'opus' aliases."""
        lse = self._make({"tier_policy": {"sonnet": "groq"}})
        # The policy key should have been normalized to 'balanced'
        assert lse._tier_policy == {"balanced": "groq"}
