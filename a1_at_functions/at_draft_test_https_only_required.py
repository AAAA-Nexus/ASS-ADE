# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testa2afetchagentcardssrf.py:8
# Component id: at.source.ass_ade.test_https_only_required
__version__ = "0.1.0"

    def test_https_only_required(self) -> None:
        """A2A fetching should require HTTPS."""
        report = fetch_agent_card("http://example.com/.well-known/agent.json")
        assert not report.valid
        assert "HTTPS" in report.errors[0].message
