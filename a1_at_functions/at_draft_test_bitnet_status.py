# Extracted from C:/!ass-ade/tests/test_new_commands.py:753
# Component id: at.source.ass_ade.test_bitnet_status
from __future__ import annotations

__version__ = "0.1.0"

def test_bitnet_status(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.bitnet_status.return_value = BitNetStatus(status="healthy", models_loaded=4)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["bitnet", "status",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "healthy" in result.stdout
