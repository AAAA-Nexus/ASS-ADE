# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_ratchet_advance.py:7
# Component id: at.source.a1_at_functions.test_ratchet_advance
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchet_advance(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.ratchet_advance.return_value = RatchetAdvance(session_id="sess-abc", new_epoch=2, proof_token="tok-xyz")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["ratchet", "advance", "sess-abc", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "new_epoch" in result.stdout
