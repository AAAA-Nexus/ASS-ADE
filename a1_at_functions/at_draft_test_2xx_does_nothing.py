# Extracted from C:/!ass-ade/tests/test_errors.py:51
# Component id: at.source.ass_ade.test_2xx_does_nothing
from __future__ import annotations

__version__ = "0.1.0"

def test_2xx_does_nothing(self) -> None:
    for code in (200, 201, 204, 299):
        raise_for_status(code)  # should not raise
