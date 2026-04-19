# Extracted from C:/!ass-ade/src/ass_ade/nexus/errors.py:44
# Component id: mo.source.ass_ade.nexusratelimited
from __future__ import annotations

__version__ = "0.1.0"

class NexusRateLimited(NexusError):
    """Rate limit exceeded (429).  Check ``retry_after``."""
