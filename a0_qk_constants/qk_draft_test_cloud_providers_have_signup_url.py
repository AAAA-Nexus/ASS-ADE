# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testcataloginvariants.py:31
# Component id: qk.source.ass_ade.test_cloud_providers_have_signup_url
__version__ = "0.1.0"

    def test_cloud_providers_have_signup_url(self):
        exempt = {"pollinations"}  # no signup needed
        for name, profile in FREE_PROVIDERS.items():
            if not profile.local and name not in exempt:
                assert profile.signup_url, f"{name} is cloud without signup_url"
