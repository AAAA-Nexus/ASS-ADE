# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testa2adiscovercli.py:7
# Component id: mo.source.a2_mo_composites.testa2adiscovercli
from __future__ import annotations

__version__ = "0.1.0"

class TestA2ADiscoverCLI:
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

    def test_discover_requires_remote(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".ass-ade" / "config.json"
        write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)
        result = runner.invoke(app, ["a2a", "discover", "search", "--config", str(config_path)])
        assert result.exit_code == 2
        assert "disabled in the local profile" in result.stdout
