# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:97
# Component id: at.source.ass_ade.test_agent_run_success_outputs_result
from __future__ import annotations

__version__ = "0.1.0"

def test_agent_run_success_outputs_result(self, tmp_path: Path) -> None:
    """Agent run should output the task result."""
    # Mock the engine.router.build_provider function
    with patch("ass_ade.engine.router.build_provider") as mock_provider_builder, \
         patch("ass_ade.tools.registry.default_registry") as mock_registry_builder, \
         patch("ass_ade.agent.loop.AgentLoop") as mock_agent_class:

        # Mock provider, registry, and agent
        mock_provider = MagicMock()
        mock_provider_builder.return_value = mock_provider

        mock_registry = MagicMock()
        mock_registry_builder.return_value = mock_registry

        mock_agent = MagicMock()
        mock_agent.step.return_value = "Task completed: analyzed 5 files"
        mock_agent_class.return_value = mock_agent

        config_path = tmp_path / ".ass-ade" / "config.json"
        write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

        result = runner.invoke(
            app,
            ["agent", "run", "Analyze the codebase structure", "--config", str(config_path)],
        )

        assert result.exit_code == 0
        assert "Task completed" in result.stdout or "analyzed" in result.stdout
