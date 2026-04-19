# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_llm_chat_uses_text_field_fallback.py:7
# Component id: at.source.a1_at_functions.test_llm_chat_uses_text_field_fallback
from __future__ import annotations

__version__ = "0.1.0"

def test_llm_chat_uses_text_field_fallback(tmp_path: Path) -> None:
    """InferenceResponse.result can be None; .text is the fallback field."""
    mock_nx = MagicMock()
    mock_nx.inference.return_value = InferenceResponse(text="Fallback text.", tokens_used=8)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["llm", "chat", "Hi", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "Fallback text." in result.stdout
