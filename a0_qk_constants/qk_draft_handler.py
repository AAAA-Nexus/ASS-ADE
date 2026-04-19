# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_internal_search_sends_session_token.py:11
# Component id: qk.source.a0_qk_constants.handler
from __future__ import annotations

__version__ = "0.1.0"

def handler(request: httpx.Request) -> httpx.Response:
    requests_made.append(request)
    return httpx.Response(200, json={"success": True, "result": {}})
