# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:495
# Component id: at.source.ass_ade.test_security_prompt_scan_http_error_exits_1
__version__ = "0.1.0"

def test_security_prompt_scan_http_error_exits_1(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.prompt_inject_scan.side_effect = _http_error(500)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "prompt-scan", "injected text", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 1
    assert "API request failed" in result.stdout
