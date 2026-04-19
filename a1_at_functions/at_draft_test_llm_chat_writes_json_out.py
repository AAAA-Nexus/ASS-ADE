# Extracted from C:/!ass-ade/tests/test_new_commands.py:387
# Component id: at.source.ass_ade.test_llm_chat_writes_json_out
from __future__ import annotations

__version__ = "0.1.0"

def test_llm_chat_writes_json_out(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.inference.return_value = InferenceResponse(result="Hi there.", tokens_used=5)
    out_file = tmp_path / "llm.json"
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["llm", "chat", "Hello!", "--config", str(_hybrid_config(tmp_path)), "--allow-remote", "--json-out", str(out_file)],
        )
    assert result.exit_code == 0
    data = json.loads(out_file.read_text())
    assert data["result"] == "Hi there."
