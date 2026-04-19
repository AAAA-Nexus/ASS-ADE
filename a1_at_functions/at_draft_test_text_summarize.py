# Extracted from C:/!ass-ade/tests/test_new_commands.py:242
# Component id: at.source.ass_ade.test_text_summarize
from __future__ import annotations

__version__ = "0.1.0"

def test_text_summarize(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.text_summarize.return_value = TextSummary(summary="Short summary.", compression_ratio=0.1, sentences=1)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["text", "summarize", "A very long text that needs summarizing.", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "Short summary." in result.stdout
