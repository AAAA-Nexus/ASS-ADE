# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:332
# Component id: at.source.ass_ade.test_security_shield
__version__ = "0.1.0"

def test_security_shield(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.security_shield.return_value = ShieldResult(sanitized=True, blocked=False, payload={"data": "clean"})
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps({"data": "possibly-dangerous"}), encoding="utf-8")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "shield", str(payload_file), "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "sanitized" in result.stdout
