# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_escrow_http_error.py:7
# Component id: at.source.a1_at_functions.test_escrow_http_error
from __future__ import annotations

__version__ = "0.1.0"

def test_escrow_http_error(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    req = _httpx.Request("POST", "https://x.y/v1/escrow/create")
    resp = _httpx.Response(402, request=req)
    mock_nx.escrow_create.side_effect = _httpx.HTTPStatusError("402", request=req, response=resp)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["escrow", "create", "a", "b", "5.0",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 1
