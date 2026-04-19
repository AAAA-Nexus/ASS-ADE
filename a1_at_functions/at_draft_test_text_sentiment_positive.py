# Extracted from C:/!ass-ade/tests/test_new_commands.py:266
# Component id: at.source.ass_ade.test_text_sentiment_positive
from __future__ import annotations

__version__ = "0.1.0"

def test_text_sentiment_positive(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.text_sentiment.return_value = TextSentiment(sentiment="positive", confidence=0.95, score=0.95)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["text", "sentiment", "I love this!", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "positive" in result.stdout
    assert "0.95" in result.stdout
