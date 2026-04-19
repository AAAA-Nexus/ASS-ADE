# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_dev_crypto_toolkit.py:7
# Component id: at.source.a1_at_functions.test_dev_crypto_toolkit
from __future__ import annotations

__version__ = "0.1.0"

def test_dev_crypto_toolkit(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.crypto_toolkit.return_value = CryptoToolkit(blake3_hash="abc", merkle_proof="def", nonce="123")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["dev", "crypto-toolkit", "my data",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "abc" in result.stdout
