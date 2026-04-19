# Extracted from C:/!ass-ade/tests/test_validation.py:71
# Component id: at.source.ass_ade.test_valid_amounts
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_amounts(self) -> None:
    assert validate_usdc_amount(0.01) == 0.01
    assert validate_usdc_amount(1_000_000.0) == 1_000_000.0
