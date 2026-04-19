# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_oracle_entropy.py:7
# Component id: at.source.a1_at_functions.test_oracle_entropy
from __future__ import annotations

__version__ = "0.1.0"

def test_oracle_entropy(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.entropy_oracle.return_value = EntropyResult(entropy_bits=127.4, epoch=5, verdict="healthy")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["oracle", "entropy", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "entropy_bits" in result.stdout
