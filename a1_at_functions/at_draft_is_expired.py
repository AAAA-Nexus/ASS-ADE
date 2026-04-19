# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_paymentchallenge.py:59
# Component id: at.source.a2_mo_composites.is_expired
from __future__ import annotations

__version__ = "0.1.0"

def is_expired(self) -> bool:
    return time.time() > self.expires if self.expires else False
