# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_sla_register.py:7
# Component id: at.source.a1_at_functions.test_sla_register
from __future__ import annotations

__version__ = "0.1.0"

def test_sla_register(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.sla_register.return_value = SlaRegistration(sla_id="sla-1", bond_usdc=10.0)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["sla", "register", "agent-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "sla-1" in result.stdout
