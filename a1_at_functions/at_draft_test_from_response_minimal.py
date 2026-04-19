# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpaymentchallenge.py:29
# Component id: at.source.a2_mo_composites.test_from_response_minimal
from __future__ import annotations

__version__ = "0.1.0"

def test_from_response_minimal(self) -> None:
    with pytest.raises(ValueError, match="recipient"):
        PaymentChallenge.from_response({})
