# Extracted from C:/!ass-ade/tests/test_engine_integration.py:134
# Component id: mo.source.ass_ade.test_distill_principles_fallback_defaults
from __future__ import annotations

__version__ = "0.1.0"

def test_distill_principles_fallback_defaults(self) -> None:
    w = WisdomEngine({})
    principles = w.distill_principles(None)
    assert len(principles) >= 3
