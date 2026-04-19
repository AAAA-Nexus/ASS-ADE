# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:235
# Component id: at.source.ass_ade.test_swarm_plan_success
__version__ = "0.1.0"

    def test_swarm_plan_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Swarm plan should return a numbered list of steps."""
        mock_nx = MagicMock()
        mock_nx.agent_plan.return_value = AgentPlan(
            goal="Build a Python CLI",
            steps=[
                {"step": 1, "description": "Design command structure"},
                {"step": 2, "description": "Implement core commands"},
                {"step": 3, "description": "Add test coverage"},
                {"step": 4, "description": "Document API"},
            ],
        )
        
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["swarm", "plan", "Build a Python CLI", "--config", str(hybrid_config)],
            )
        
        assert result.exit_code == 0
