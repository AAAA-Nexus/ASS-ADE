# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:459
# Component id: at.source.ass_ade.test_ratchet_register_http_error_exits_1
__version__ = "0.1.0"

def test_ratchet_register_http_error_exits_1(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.ratchet_register.side_effect = _http_error(429)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["ratchet", "register", "agent-x", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 1
    assert "rate limit" in result.stdout
