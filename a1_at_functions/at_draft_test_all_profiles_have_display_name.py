# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:50
# Component id: at.source.ass_ade.test_all_profiles_have_display_name
__version__ = "0.1.0"

    def test_all_profiles_have_display_name(self):
        for name, profile in FREE_PROVIDERS.items():
            assert profile.display_name, f"{name} has no display_name"
