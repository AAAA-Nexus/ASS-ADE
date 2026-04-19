# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testwisdomengine.py:114
# Component id: mo.source.a2_mo_composites.test_report_returns_engine_info
from __future__ import annotations

__version__ = "0.1.0"

def test_report_returns_engine_info(self) -> None:
    w = WisdomEngine({})
    r = w.report()
    assert r["engine"] == "wisdom"
    assert "conviction" in r and "conviction_required" in r
