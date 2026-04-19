# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tcaengine.py:72
# Component id: mo.source.a2_mo_composites.ncb_contract
from __future__ import annotations

__version__ = "0.1.0"

def ncb_contract(self, target_path: str | Path) -> bool:
    """Return True if NCB contract is satisfied (file was read before writing)."""
    return self.check_freshness(target_path).fresh
