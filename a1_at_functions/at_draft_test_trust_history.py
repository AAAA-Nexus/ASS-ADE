# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:225
# Component id: at.source.ass_ade.test_trust_history
__version__ = "0.1.0"

def test_trust_history(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.trust_history.return_value = TrustHistory(
        agent_id="agent-1", epochs=[{"epoch": 1, "score": 0.85}], current_score=0.92
    )
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["trust", "history", "agent-1", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "current_score" in result.stdout
