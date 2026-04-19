# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testa2anegotiatecli.py:6
# Component id: at.source.ass_ade.test_negotiate_blocks_private_url
__version__ = "0.1.0"

    def test_negotiate_blocks_private_url(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["a2a", "negotiate", "http://192.168.1.1/.well-known/agent.json",
                   "--config", str(_hybrid_config(tmp_path))]
        )
        assert result.exit_code == 1
        assert "Blocked" in result.stdout
