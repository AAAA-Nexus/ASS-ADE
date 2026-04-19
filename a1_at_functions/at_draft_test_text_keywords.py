# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_text_keywords.py:7
# Component id: at.source.a1_at_functions.test_text_keywords
from __future__ import annotations

__version__ = "0.1.0"

def test_text_keywords(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.text_keywords.return_value = TextKeywords(keywords=[{"word": "python", "score": 0.9}], top_keyword="python")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["text", "keywords", "Python is great for automation.", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "python" in result.stdout
