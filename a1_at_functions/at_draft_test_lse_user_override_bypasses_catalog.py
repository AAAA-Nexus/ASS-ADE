# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:343
# Component id: at.source.ass_ade.test_lse_user_override_bypasses_catalog
__version__ = "0.1.0"

    def test_lse_user_override_bypasses_catalog(self):
        from ass_ade.agent.lse import LSEEngine
        lse = LSEEngine({})
        decision = lse.select(
            trs_score=0.8, complexity="medium", user_model_override="my-fixed-model",
        )
        assert decision.model == "my-fixed-model"
        assert decision.provider is None
        assert decision.reason == "user_override"
