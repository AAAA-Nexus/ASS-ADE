# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtcaengine.py:50
# Component id: mo.source.a2_mo_composites.test_record_gap
from __future__ import annotations

__version__ = "0.1.0"

def test_record_gap(self, tmp_path):
    tca = self._make(tmp_path)
    tca.record_gap("Missing API docs for endpoint X")
    gaps = tca.get_gaps()
    assert len(gaps) == 1
    assert "endpoint X" in gaps[0]["description"]
