# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateusdcamount.py:16
# Component id: at.source.a1_at_functions.test_negative_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_negative_raises(self) -> None:
    with pytest.raises(ValueError, match="positive"):
        validate_usdc_amount(-5.0)
