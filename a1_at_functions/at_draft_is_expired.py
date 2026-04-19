# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:102
# Component id: at.source.ass_ade.is_expired
from __future__ import annotations

__version__ = "0.1.0"

def is_expired(self) -> bool:
    return time.time() > self.expires if self.expires else False
