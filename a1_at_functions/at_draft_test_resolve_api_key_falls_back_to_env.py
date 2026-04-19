# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testproviderprofile.py:12
# Component id: at.source.ass_ade.test_resolve_api_key_falls_back_to_env
__version__ = "0.1.0"

    def test_resolve_api_key_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "env-key-value")
        p = get_provider("groq")
        assert p.resolve_api_key() == "env-key-value"
