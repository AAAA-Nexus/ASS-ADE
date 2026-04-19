# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_low_conviction_warning_fires_on_second_audit.py:7
# Component id: at.source.a1_at_functions.test_low_conviction_warning_fires_on_second_audit
from __future__ import annotations

__version__ = "0.1.0"

def test_low_conviction_warning_fires_on_second_audit(self) -> None:
    w = WisdomEngine({})
    r1 = w.run_audit({})   # first audit — no warning even if low
    assert not any("low_conviction" in warn for warn in r1.warnings)
    r2 = w.run_audit({})   # second with still-low score — warning fires
    assert any("low_conviction" in warn for warn in r2.warnings)
