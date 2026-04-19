# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_402_raises_payment_required.py:7
# Component id: at.source.a1_at_functions.test_402_raises_payment_required
from __future__ import annotations

__version__ = "0.1.0"

def test_402_raises_payment_required(self) -> None:
    with pytest.raises(NexusPaymentRequired) as exc_info:
        raise_for_status(402, endpoint="/v1/inference")
    assert exc_info.value.status_code == 402
