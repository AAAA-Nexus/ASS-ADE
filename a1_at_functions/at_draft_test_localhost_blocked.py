# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testa2afetchagentcardssrf.py:14
# Component id: at.source.ass_ade.test_localhost_blocked
__version__ = "0.1.0"

    def test_localhost_blocked(self) -> None:
        """A2A should block attempts to fetch from localhost."""
        report = fetch_agent_card("https://localhost/.well-known/agent.json")
        assert not report.valid
        assert len(report.errors) > 0
        assert "blocked" in report.errors[0].message or "loopback" in report.errors[0].message
