# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testchutesprovider.py:11
# Component id: at.source.ass_ade.test_chutes_available_with_env_key
__version__ = "0.1.0"

    def test_chutes_available_with_env_key(self, monkeypatch):
        monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
        profile = get_provider("chutes")
        assert profile.is_available() is True
