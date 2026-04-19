# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:358
# Component id: at.source.ass_ade.test_security_pqc_sign_writes_json_out
__version__ = "0.1.0"

def test_security_pqc_sign_writes_json_out(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.security_pqc_sign.return_value = PqcSignResult(signature="deadbeef", algorithm="ML-DSA (Dilithium)")
    out_file = tmp_path / "sig.json"
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "pqc-sign", "data", "--config", str(_hybrid_config(tmp_path)), "--allow-remote", "--json-out", str(out_file)],
        )
    assert result.exit_code == 0
    data = json.loads(out_file.read_text())
    assert data["signature"] == "deadbeef"
