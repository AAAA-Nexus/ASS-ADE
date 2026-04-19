# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_oracle_hallucination_returns_verdict.py:5
# Component id: at.source.ass_ade.test_oracle_hallucination_returns_verdict
__version__ = "0.1.0"

def test_oracle_hallucination_returns_verdict(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.hallucination_oracle.return_value = HallucinationResult(
        policy_epsilon=0.03, verdict="safe", ceiling="proved-not-estimated", confidence=0.97
    )
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["oracle", "hallucination", "AI is always correct", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "safe" in result.stdout or "policy_epsilon" in result.stdout
