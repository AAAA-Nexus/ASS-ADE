# Extracted from C:/!ass-ade/tests/test_new_commands.py:784
# Component id: at.source.ass_ade.test_mev_status
from __future__ import annotations

__version__ = "0.1.0"

def test_mev_status(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.mev_status.return_value = MevStatusResult(bundle_id="bun-1", status="confirmed")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["mev", "status", "bun-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "confirmed" in result.stdout
