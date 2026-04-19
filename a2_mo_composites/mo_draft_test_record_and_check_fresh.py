# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtcaengine.py:13
# Component id: mo.source.a2_mo_composites.test_record_and_check_fresh
from __future__ import annotations

__version__ = "0.1.0"

def test_record_and_check_fresh(self, tmp_path):
    tca = self._make(tmp_path)
    tca.record_read("/some/file.py")
    report = tca.check_freshness("/some/file.py")
    assert report.fresh is True
    assert report.age_hours < 0.01
