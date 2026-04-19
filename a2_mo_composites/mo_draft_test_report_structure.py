# Extracted from C:/!ass-ade/tests/test_phase_engines.py:260
# Component id: mo.source.ass_ade.test_report_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_report_structure(self, tmp_path):
    tca = self._make(tmp_path)
    rep = tca.report()
    assert rep["engine"] == "tca"
    assert "tracked_files" in rep
    assert "threshold_hours" in rep
