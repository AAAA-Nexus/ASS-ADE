# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_ncb_contract.py:7
# Component id: at.source.a1_at_functions.ncb_contract
from __future__ import annotations

__version__ = "0.1.0"

def ncb_contract(self, target_path: str | Path) -> bool:
    """Return True if NCB contract is satisfied (file was read before writing)."""
    return self.check_freshness(target_path).fresh
