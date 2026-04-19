# Extracted from C:/!ass-ade/tests/test_phase_engines.py:230
# Component id: mo.source.ass_ade.test_stale_detection_past_threshold
from __future__ import annotations

__version__ = "0.1.0"

def test_stale_detection_past_threshold(self, tmp_path):
    tca = self._make(tmp_path)
    # Manually plant an old timestamp (2 hours ago with 1h threshold)
    tca._reads["/old.py"] = time.time() - 7300
    stale = tca.get_stale_files(["/old.py"])
    assert len(stale) == 1
    assert not stale[0].fresh
