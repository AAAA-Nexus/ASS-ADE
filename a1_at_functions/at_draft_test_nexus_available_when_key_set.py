# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:567
# Component id: at.source.ass_ade.test_nexus_available_when_key_set
__version__ = "0.1.0"

    def test_nexus_available_when_key_set(self, monkeypatch):
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
        profile = get_provider("nexus")
        assert profile is not None
        assert profile.is_available() is True
