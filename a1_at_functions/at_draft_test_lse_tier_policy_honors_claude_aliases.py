# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:333
# Component id: at.source.ass_ade.test_lse_tier_policy_honors_claude_aliases
__version__ = "0.1.0"

    def test_lse_tier_policy_honors_claude_aliases(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
        from ass_ade.agent.lse import LSEEngine
        # Users configuring with claude tier names should also work
        lse = LSEEngine({
            "tier_policy": {"sonnet": "gemini"},  # sonnet → balanced
        })
        decision = lse.select(trs_score=0.8, complexity="medium")
        assert decision.provider == "gemini"
