# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_get_stale_files_empty_when_all_fresh.py:7
# Component id: at.source.a1_at_functions.test_get_stale_files_empty_when_all_fresh
from __future__ import annotations

__version__ = "0.1.0"

def test_get_stale_files_empty_when_all_fresh(self, tmp_path):
    tca = self._make(tmp_path)
    tca.record_read("/a.py")
    tca.record_read("/b.py")
    stale = tca.get_stale_files(["/a.py", "/b.py"])
    assert len(stale) == 0
