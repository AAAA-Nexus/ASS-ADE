# Extracted from C:/!ass-ade/tests/test_validation.py:75
# Component id: at.source.ass_ade.test_zero_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_zero_raises(self) -> None:
    with pytest.raises(ValueError, match="positive"):
        validate_usdc_amount(0.0)
