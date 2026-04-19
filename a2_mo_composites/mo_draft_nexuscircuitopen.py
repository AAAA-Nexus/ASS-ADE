# Extracted from C:/!ass-ade/src/ass_ade/nexus/errors.py:56
# Component id: mo.source.ass_ade.nexuscircuitopen
from __future__ import annotations

__version__ = "0.1.0"

class NexusCircuitOpen(NexusError):
    """Client-side circuit breaker is open — calls are blocked temporarily."""
