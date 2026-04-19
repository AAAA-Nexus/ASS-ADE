# Extracted from C:/!ass-ade/tests/test_new_commands.py:861
# Component id: at.source.ass_ade.test_identity_verify
from __future__ import annotations

__version__ = "0.1.0"

def test_identity_verify(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.identity_verify.return_value = IdentityVerification(decision="allow", uniqueness_coefficient=0.98)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["identity", "verify", "agent-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "allow" in result.stdout
