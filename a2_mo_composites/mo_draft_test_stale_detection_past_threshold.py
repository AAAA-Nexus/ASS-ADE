# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtcaengine.py:42
# Component id: mo.source.a2_mo_composites.test_stale_detection_past_threshold
from __future__ import annotations

__version__ = "0.1.0"

def test_stale_detection_past_threshold(self, tmp_path):
    tca = self._make(tmp_path)
    # Manually plant an old timestamp (2 hours ago with 1h threshold)
    tca._reads["/old.py"] = time.time() - 7300
    stale = tca.get_stale_files(["/old.py"])
    assert len(stale) == 1
    assert not stale[0].fresh
