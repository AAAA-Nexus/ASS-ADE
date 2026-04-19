# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:111
# Component id: at.source.ass_ade.test_cloud_provider_available_with_env_key
__version__ = "0.1.0"

    def test_cloud_provider_available_with_env_key(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        p = get_provider("groq")
        assert p.is_available() is True
