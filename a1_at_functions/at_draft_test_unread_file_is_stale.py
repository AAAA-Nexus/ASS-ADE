# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_unread_file_is_stale.py:7
# Component id: at.source.a1_at_functions.test_unread_file_is_stale
from __future__ import annotations

__version__ = "0.1.0"

def test_unread_file_is_stale(self, tmp_path):
    tca = self._make(tmp_path)
    report = tca.check_freshness("/never/read.py")
    assert report.fresh is False
    assert report.last_read_ts is None
