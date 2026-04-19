# Extracted from C:/!ass-ade/tests/test_errors.py:64
# Component id: at.source.ass_ade.test_402_raises_payment_required
from __future__ import annotations

__version__ = "0.1.0"

def test_402_raises_payment_required(self) -> None:
    with pytest.raises(NexusPaymentRequired) as exc_info:
        raise_for_status(402, endpoint="/v1/inference")
    assert exc_info.value.status_code == 402
