# Extracted from C:/!ass-ade/src/ass_ade/agent/tca.py:107
# Component id: at.source.ass_ade.ncb_contract
from __future__ import annotations

__version__ = "0.1.0"

def ncb_contract(self, target_path: str | Path) -> bool:
    """Return True if NCB contract is satisfied (file was read before writing)."""
    return self.check_freshness(target_path).fresh
