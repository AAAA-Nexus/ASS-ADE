# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexusasprovider.py:14
# Component id: at.source.ass_ade.test_nexus_unavailable_without_key
__version__ = "0.1.0"

    def test_nexus_unavailable_without_key(self, monkeypatch):
        monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
        profile = get_provider("nexus")
        assert profile.is_available() is False
