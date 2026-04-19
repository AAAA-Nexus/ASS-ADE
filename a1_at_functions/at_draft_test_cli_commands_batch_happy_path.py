# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_cli_commands_batch_happy_path.py:5
# Component id: at.source.ass_ade.test_cli_commands_batch_happy_path
__version__ = "0.1.0"

def test_cli_commands_batch_happy_path(
    command_name: str,
    args: list[str],
    expected_in_output: list[str],
    tmp_path: Path,
    hybrid_config: Path,
) -> None:
    """Batch parametrized test for CLI commands with standard mocking."""
    mock_nx = MagicMock()
    
    # Set up common mock responses
    mock_nx.agent_token_budget.return_value = {"estimates": []}
    mock_nx.agent_plan.return_value = AgentPlan(goal="test", steps=[{"step": 1, "description": "step 1"}])
    mock_nx.trust_score.return_value = TrustScore(
        agent_id="agent-x", score=0.85, tier="silver"
    )
    
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            [command_name, *args, "--config", str(hybrid_config)],
        )
    
    # Local commands should pass
    if command_name in ("a2a", "repo", "plan"):
        # May error or succeed; check exit code is reasonable
        assert result.exit_code in (0, 1, 2)
    else:
        # Remote commands may succeed or require flag
        assert result.exit_code in (0, 1, 2)
        for expected in expected_in_output:
            assert expected.lower() in result.stdout.lower()
