# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtcaengine.py:31
# Component id: mo.source.a2_mo_composites.test_ncb_contract_false_before_read
from __future__ import annotations

__version__ = "0.1.0"

def test_ncb_contract_false_before_read(self, tmp_path):
    tca = self._make(tmp_path)
    assert tca.ncb_contract("/project/unread.py") is False
