"""Tier a2 — assimilated method 'MCPServer.cie'

Assimilated from: server.py:560-565
"""

from __future__ import annotations


# --- assimilated symbol ---
def cie(self) -> Any:
    if self._cie is None:
        from ass_ade.agent.cie import CIEPipeline

        self._cie = CIEPipeline()
    return self._cie

