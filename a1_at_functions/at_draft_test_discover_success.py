# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testa2adiscovercli.py:6
# Component id: at.source.ass_ade.test_discover_success
__version__ = "0.1.0"

    def test_discover_success(self, tmp_path: Path) -> None:
        mock_nx = MagicMock()
        mock_nx.discovery_search.return_value = DiscoveryResult(
            agents=[DiscoveredAgent(agent_id="agent-1", name="DiscoverMe")],
            total=1,
            query="search",
        )
        with patch("ass_ade.commands.a2a.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app, ["a2a", "discover", "search",
                       "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
            )
        assert result.exit_code == 0
        assert "DiscoverMe" in result.stdout
