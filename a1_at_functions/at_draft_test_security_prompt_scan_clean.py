# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:293
# Component id: at.source.ass_ade.test_security_prompt_scan_clean
__version__ = "0.1.0"

def test_security_prompt_scan_clean(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.prompt_inject_scan.return_value = PromptScanResult(threat_detected=False, threat_level="none", confidence=0.99)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "prompt-scan", "Tell me about Python.", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "CLEAN" in result.stdout
