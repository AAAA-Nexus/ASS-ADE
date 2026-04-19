# Extracted from C:/!ass-ade/tests/test_validation.py:83
# Component id: at.source.ass_ade.test_too_large_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_too_large_raises(self) -> None:
    with pytest.raises(ValueError, match="maximum"):
        validate_usdc_amount(1_000_001.0)
