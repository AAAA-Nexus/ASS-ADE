# Extracted from C:/!ass-ade/tests/test_new_commands.py:173
# Component id: at.source.ass_ade.test_ratchet_register_writes_json_out
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchet_register_writes_json_out(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.ratchet_register.return_value = RatchetSession(session_id="sess-def", epoch=1, fips_203_compliant=True)
    out_file = tmp_path / "session.json"
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["ratchet", "register", "agent-z", "--config", str(_hybrid_config(tmp_path)), "--allow-remote", "--json-out", str(out_file)],
        )
    assert result.exit_code == 0
    data = json.loads(out_file.read_text())
    assert data["session_id"] == "sess-def"
