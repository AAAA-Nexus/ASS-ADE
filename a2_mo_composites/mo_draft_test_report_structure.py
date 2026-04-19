# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtcaengine.py:72
# Component id: mo.source.a2_mo_composites.test_report_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_report_structure(self, tmp_path):
    tca = self._make(tmp_path)
    rep = tca.report()
    assert rep["engine"] == "tca"
    assert "tracked_files" in rep
    assert "threshold_hours" in rep
