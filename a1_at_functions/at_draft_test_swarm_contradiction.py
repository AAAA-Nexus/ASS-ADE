# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_swarm_contradiction.py:5
# Component id: at.source.ass_ade.test_swarm_contradiction
__version__ = "0.1.0"

def test_swarm_contradiction(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.agent_contradiction.return_value = ContradictionResult(contradicts=True, confidence=0.95)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["swarm", "contradiction", "A is true", "A is false",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "CONTRADICTS" in result.stdout
