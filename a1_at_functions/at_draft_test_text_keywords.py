# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:254
# Component id: at.source.ass_ade.test_text_keywords
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
