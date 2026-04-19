# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_reputation_score.py:5
# Component id: at.source.ass_ade.test_reputation_score
__version__ = "0.1.0"

def test_reputation_score(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.reputation_score.return_value = ReputationScore(agent_id="ag-1", score=0.9, tier="gold", fee_multiplier=0.9)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["reputation", "score", "ag-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "gold" in result.stdout
