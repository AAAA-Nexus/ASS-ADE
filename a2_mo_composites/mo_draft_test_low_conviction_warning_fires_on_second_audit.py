# Extracted from C:/!ass-ade/tests/test_engine_integration.py:106
# Component id: mo.source.ass_ade.test_low_conviction_warning_fires_on_second_audit
from __future__ import annotations

__version__ = "0.1.0"

def test_low_conviction_warning_fires_on_second_audit(self) -> None:
    w = WisdomEngine({})
    r1 = w.run_audit({})   # first audit — no warning even if low
    assert not any("low_conviction" in warn for warn in r1.warnings)
    r2 = w.run_audit({})   # second with still-low score — warning fires
    assert any("low_conviction" in warn for warn in r2.warnings)
