# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlseengine.py:64
# Component id: mo.source.a2_mo_composites.test_report_tracks_decisions
from __future__ import annotations

__version__ = "0.1.0"

def test_report_tracks_decisions(self):
    lse = self._make()
    lse.select(trs_score=0.8)
    lse.select(trs_score=0.5)
    rep = lse.report()
    assert rep["decisions"] == 2
    assert "tier_distribution" in rep
    assert "provider_distribution" in rep
    assert "avg_trs" in rep
