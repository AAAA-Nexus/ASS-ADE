# Extracted from C:/!ass-ade/tests/test_engine_integration.py:163
# Component id: mo.source.ass_ade.test_report_returns_engine_info
from __future__ import annotations

__version__ = "0.1.0"

def test_report_returns_engine_info(self) -> None:
    w = WisdomEngine({})
    r = w.report()
    assert r["engine"] == "wisdom"
    assert "conviction" in r and "conviction_required" in r
