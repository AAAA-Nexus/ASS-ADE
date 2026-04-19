# Extracted from C:/!ass-ade/tests/test_search_x402.py:167
# Component id: at.source.ass_ade.handler
from __future__ import annotations

__version__ = "0.1.0"

def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        402,
        json={"amount": 0.008, "network": "base", "address": "0xTREASURY"},
    )
