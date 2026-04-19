# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1095
# Component id: mo.source.a2_mo_composites.bitnet_status
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_status(self, **kwargs: Any) -> BitNetStatus:
    """GET /v1/bitnet/status — BitNet engine health and metrics (BIT-105). Free."""
    return self._get_model("/v1/bitnet/status", BitNetStatus, **kwargs)
