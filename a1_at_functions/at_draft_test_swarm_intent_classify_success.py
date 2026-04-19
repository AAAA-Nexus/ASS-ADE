# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:260
# Component id: at.source.ass_ade.test_swarm_intent_classify_success
from __future__ import annotations

__version__ = "0.1.0"

def test_swarm_intent_classify_success(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Intent classification should return top intents with confidence."""
    mock_nx = MagicMock()
    mock_nx.agent_intent_classify.return_value = IntentClassification(
        text="Please analyze this code for bugs",
        intents=[
            {"intent": "code_review", "confidence": 0.98},
            {"intent": "testing", "confidence": 0.72},
            {"intent": "debugging", "confidence": 0.65},
        ],
    )

    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["swarm", "intent-classify", "analyze code for bugs", "--config", str(hybrid_config)],
        )

    assert result.exit_code == 0
