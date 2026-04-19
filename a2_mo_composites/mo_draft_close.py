# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:193
# Component id: mo.source.ass_ade.close
from __future__ import annotations

__version__ = "0.1.0"

def close(self) -> None:
    self._client.close()
