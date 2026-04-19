# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_escrow_create.py:7
# Component id: at.source.a1_at_functions.test_escrow_create
from __future__ import annotations

__version__ = "0.1.0"

def test_escrow_create(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.escrow_create.return_value = EscrowCreated(escrow_id="esc-1", status="funded", amount_usdc=10.0)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["escrow", "create", "payer-1", "payee-1", "10.0",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "esc-1" in result.stdout
