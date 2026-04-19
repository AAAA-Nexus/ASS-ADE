# Extracted from C:/!ass-ade/tests/test_new_commands.py:696
# Component id: at.source.ass_ade.test_discovery_search
from __future__ import annotations

__version__ = "0.1.0"

def test_discovery_search(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.discovery_search.return_value = DiscoveryResult(agents=[], total=0)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["discovery", "search", "code review",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
