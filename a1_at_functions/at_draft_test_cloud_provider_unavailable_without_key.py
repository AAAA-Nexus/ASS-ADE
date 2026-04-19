# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:106
# Component id: at.source.ass_ade.test_cloud_provider_unavailable_without_key
__version__ = "0.1.0"

    def test_cloud_provider_unavailable_without_key(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        p = get_provider("groq")
        assert p.is_available() is False
