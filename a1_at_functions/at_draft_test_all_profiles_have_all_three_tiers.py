# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:44
# Component id: at.source.ass_ade.test_all_profiles_have_all_three_tiers
__version__ = "0.1.0"

    def test_all_profiles_have_all_three_tiers(self):
        for name, profile in FREE_PROVIDERS.items():
            for tier in ALL_TIERS:
                assert tier in profile.models_by_tier, f"{name} missing {tier} tier"
                assert profile.models_by_tier[tier], f"{name} {tier} is empty"
