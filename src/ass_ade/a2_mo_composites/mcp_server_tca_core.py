"""Tier a2 — assimilated method 'MCPServer.tca'

Assimilated from: server.py:552-557
"""

from __future__ import annotations


# --- assimilated symbol ---
def tca(self) -> Any:
    if self._tca is None:
        from ass_ade.agent.tca import TCAEngine

        self._tca = TCAEngine({"working_dir": self._working_dir})
    return self._tca

