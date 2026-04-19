# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusratelimited.py:7
# Component id: mo.source.a2_mo_composites.nexusratelimited
from __future__ import annotations

__version__ = "0.1.0"

class NexusRateLimited(NexusError):
    """Rate limit exceeded (429).  Check ``retry_after``."""
