# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:85
# Component id: at.source.ass_ade.test_https_only_required
from __future__ import annotations

__version__ = "0.1.0"

def test_https_only_required(self) -> None:
    """A2A fetching should require HTTPS."""
    report = fetch_agent_card("http://example.com/.well-known/agent.json")
    assert not report.valid
    assert "HTTPS" in report.errors[0].message
