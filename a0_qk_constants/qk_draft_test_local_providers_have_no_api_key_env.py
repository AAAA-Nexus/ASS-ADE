# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testcataloginvariants.py:26
# Component id: qk.source.ass_ade.test_local_providers_have_no_api_key_env
__version__ = "0.1.0"

    def test_local_providers_have_no_api_key_env(self):
        for name, profile in FREE_PROVIDERS.items():
            if profile.local:
                assert profile.api_key_env is None, f"{name} is local but has api_key_env"
