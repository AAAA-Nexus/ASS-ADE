# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testproviderprofile.py:17
# Component id: at.source.ass_ade.test_resolve_api_key_returns_none_when_missing
__version__ = "0.1.0"

    def test_resolve_api_key_returns_none_when_missing(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        p = get_provider("groq")
        assert p.resolve_api_key() is None
