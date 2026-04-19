# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_2xx_does_nothing.py:7
# Component id: at.source.a1_at_functions.test_2xx_does_nothing
from __future__ import annotations

__version__ = "0.1.0"

def test_2xx_does_nothing(self) -> None:
    for code in (200, 201, 204, 299):
        raise_for_status(code)  # should not raise
