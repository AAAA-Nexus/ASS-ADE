# Extracted from C:/!ass-ade/tests/test_new_commands.py:852
# Component id: at.source.ass_ade.test_aegis_certify_epoch
from __future__ import annotations

__version__ = "0.1.0"

def test_aegis_certify_epoch(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.aegis_certify_epoch.return_value = MagicMock(model_dump=lambda: {"cert_id": "cert-1", "valid": True})
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["aegis", "certify-epoch", "agent-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
