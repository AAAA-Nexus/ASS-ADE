# Extracted from C:/!ass-ade/tests/test_new_commands.py:162
# Component id: at.source.ass_ade.test_ratchet_register_shows_session
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchet_register_shows_session(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.ratchet_register.return_value = RatchetSession(session_id="sess-abc", epoch=1, fips_203_compliant=True)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["ratchet", "register", "my-agent", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "sess-abc" in result.stdout
