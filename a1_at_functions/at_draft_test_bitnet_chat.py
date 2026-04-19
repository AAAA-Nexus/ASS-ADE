# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_bitnet_chat.py:7
# Component id: at.source.a1_at_functions.test_bitnet_chat
from __future__ import annotations

__version__ = "0.1.0"

def test_bitnet_chat(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.bitnet_inference.return_value = BitNetInferenceResponse(result="hello from bitnet", model="bitnet-b1.58-2B-4T")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["bitnet", "chat", "hi",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "bitnet" in result.stdout
