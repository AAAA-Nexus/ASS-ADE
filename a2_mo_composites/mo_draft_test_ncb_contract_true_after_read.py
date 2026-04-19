# Extracted from C:/!ass-ade/tests/test_phase_engines.py:214
# Component id: mo.source.ass_ade.test_ncb_contract_true_after_read
from __future__ import annotations

__version__ = "0.1.0"

def test_ncb_contract_true_after_read(self, tmp_path):
    tca = self._make(tmp_path)
    tca.record_read("/project/main.py")
    assert tca.ncb_contract("/project/main.py") is True
