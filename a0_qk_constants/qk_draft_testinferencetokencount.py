# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:183
# Component id: qk.source.ass_ade.testinferencetokencount
from __future__ import annotations

__version__ = "0.1.0"

class TestInferenceTokenCount:
    """Test `llm token-count` command — estimate token costs."""

    def test_llm_token_count_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Token count should return cost estimates across models."""
        mock_nx = MagicMock()
        mock_nx.agent_token_budget.return_value = {
            "task": "write a test",
            "estimates": [
                {"model": "gpt-4", "tokens": 142, "cost_usd": 0.004},
                {"model": "llama-3.1-8b", "tokens": 89, "cost_usd": 0.001},
            ],
        }

        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["llm", "token-count", "write a test", "--config", str(hybrid_config)],
            )

        assert result.exit_code == 0
        assert "estimates" in result.stdout or "token" in result.stdout.lower()
