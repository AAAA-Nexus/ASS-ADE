# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_swarm_plan_success.py:7
# Component id: at.source.a1_at_functions.test_swarm_plan_success
from __future__ import annotations

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
