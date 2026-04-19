# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:146
# Component id: at.source.ass_ade.test_oracle_trust_decay
__version__ = "0.1.0"

def test_oracle_trust_decay(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.trust_decay.return_value = TrustDecayResult(decayed_score=0.72, original_score=0.88, epochs_elapsed=3)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["oracle", "trust-decay", "agent-99", "--epochs", "3", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "decayed_score" in result.stdout
