# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testselectproviderfortier.py:19
# Component id: at.source.ass_ade.test_policy_overrides_chain_order
__version__ = "0.1.0"

    def test_policy_overrides_chain_order(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
        # Policy forces gemini for balanced
        match = select_provider_for_tier(
            "balanced",
            tier_policy={"balanced": "gemini"},
        )
        assert match is not None
        profile, _ = match
        assert profile.name == "gemini"
