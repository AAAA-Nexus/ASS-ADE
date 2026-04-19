# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testcataloginvariants.py:22
# Component id: qk.source.ass_ade.test_all_profiles_have_display_name
__version__ = "0.1.0"

    def test_all_profiles_have_display_name(self):
        for name, profile in FREE_PROVIDERS.items():
            assert profile.display_name, f"{name} has no display_name"
