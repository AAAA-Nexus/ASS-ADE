# Extracted from C:/!ass-ade/tests/test_new_commands.py:198
# Component id: at.source.ass_ade.test_ratchet_status
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchet_status(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.ratchet_status.return_value = RatchetStatus(session_id="sess-abc", epoch=2, remaining_calls=95, status="active")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["ratchet", "status", "sess-abc", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "remaining_calls" in result.stdout
