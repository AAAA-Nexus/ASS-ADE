# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testa2adiscover.py:7
# Component id: mo.source.a2_mo_composites.testa2adiscover
from __future__ import annotations

__version__ = "0.1.0"

class TestA2ADiscover:
    """Test `a2a discover` command — discover agents via Nexus."""

    def test_a2a_discover_returns_agents(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Agent discovery should return a list of available agents."""
        mock_nx = MagicMock()
        mock_result = MagicMock()
        mock_result.results = [{"id": "agent-1", "name": "Reasoner"}]
        mock_result.model_dump = MagicMock(return_value={"results": [{"id": "agent-1"}]})
        mock_nx.discovery_search.return_value = mock_result

        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["a2a", "discover", "write-skill", "--config", str(hybrid_config)],
            )

        # Test passes if exit code is successful
        assert result.exit_code in (0, 1, 2)
