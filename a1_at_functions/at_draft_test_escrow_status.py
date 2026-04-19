# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_escrow_status.py:7
# Component id: at.source.a1_at_functions.test_escrow_status
from __future__ import annotations

__version__ = "0.1.0"

def test_escrow_status(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.escrow_status.return_value = EscrowStatus(escrow_id="esc-1", status="funded", amount_usdc=10.0)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["escrow", "status", "esc-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "funded" in result.stdout
