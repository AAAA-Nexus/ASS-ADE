# Extracted from C:/!ass-ade/tests/test_new_commands.py:665
# Component id: at.source.ass_ade.test_escrow_http_error
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
