# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_report_structure.py:7
# Component id: at.source.a1_at_functions.test_report_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_report_structure(self) -> None:
    b = BAS({})
    r = b.report()
    assert r["engine"] == "bas"
    assert "alerts_total" in r
    assert "alerts_session" in r
    assert "unflushed" in r
    assert "cooldown_s" in r
