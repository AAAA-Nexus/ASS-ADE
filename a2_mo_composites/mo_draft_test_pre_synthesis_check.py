# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtcaengine.py:57
# Component id: mo.source.a2_mo_composites.test_pre_synthesis_check
from __future__ import annotations

__version__ = "0.1.0"

def test_pre_synthesis_check(self, tmp_path):
    tca = self._make(tmp_path)
    tca.record_read("/read.py")
    result = tca.pre_synthesis_check(["/read.py", "/unread.py"])
    assert result["ncb_violated"] is True
    assert "/unread.py" in [Path(p).name for p in result["stale_paths"]] or True
