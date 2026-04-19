# Extracted from C:/!ass-ade/tests/test_new_commands.py:346
# Component id: at.source.ass_ade.test_security_pqc_sign
from __future__ import annotations

__version__ = "0.1.0"

def test_security_pqc_sign(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.security_pqc_sign.return_value = PqcSignResult(signature="aabbcc", algorithm="ML-DSA (Dilithium)", public_key="pub-xyz")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "pqc-sign", "my-data-to-sign", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "ML-DSA" in result.stdout
