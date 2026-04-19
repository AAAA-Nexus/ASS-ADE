# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:556
# Component id: at.source.ass_ade.test_llm_chat_success
from __future__ import annotations

__version__ = "0.1.0"

def test_llm_chat_success(self, tmp_path: Path, hybrid_config: Path) -> None:
    """LLM chat should return inference result."""
    mock_nx = MagicMock()
    mock_nx.inference.return_value = InferenceResponse(
        result="The capital of France is Paris.",
        tokens_used=15,
        model="llama-3.1-8b",
    )

    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["llm", "chat", "What is the capital of France?", "--config", str(hybrid_config)],
        )

    assert result.exit_code == 0
    assert "Paris" in result.stdout or "capital" in result.stdout
