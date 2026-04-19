# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1146
# Component id: mo.source.a2_mo_composites.mev_status
from __future__ import annotations

__version__ = "0.1.0"

def mev_status(self, bundle_id: str, **kwargs: Any) -> MevStatusResult:
    """GET /v1/mev/status — check MEV protection status for a bundle (MEV-101). Free."""
    return self._get_model("/v1/mev/status", MevStatusResult, bundle_id=bundle_id, **kwargs)
