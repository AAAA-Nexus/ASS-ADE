# Extracted from C:/!ass-ade/tests/test_a2a.py:185
# Component id: at.source.ass_ade.test_fetch_network_error
from __future__ import annotations

__version__ = "0.1.0"

def test_fetch_network_error(self) -> None:
    import httpx as _httpx

    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
        with patch("ass_ade.a2a.httpx.get", side_effect=_httpx.ConnectError("refused")):
            report = fetch_agent_card("https://unreachable.com")
            assert not report.valid
            assert any("Network" in i.message for i in report.errors)
