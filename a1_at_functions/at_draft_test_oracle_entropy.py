# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:135
# Component id: at.source.ass_ade.test_oracle_entropy
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
