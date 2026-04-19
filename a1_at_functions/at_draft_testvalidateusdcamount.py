# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateusdcamount.py:7
# Component id: at.source.a1_at_functions.testvalidateusdcamount
from __future__ import annotations

__version__ = "0.1.0"

class TestValidateUsdcAmount:
    def test_valid_amounts(self) -> None:
        assert validate_usdc_amount(0.01) == 0.01
        assert validate_usdc_amount(1_000_000.0) == 1_000_000.0

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            validate_usdc_amount(0.0)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            validate_usdc_amount(-5.0)

    def test_too_large_raises(self) -> None:
        with pytest.raises(ValueError, match="maximum"):
            validate_usdc_amount(1_000_001.0)
