# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1168
# Component id: mo.source.a2_mo_composites.forge_badge
from __future__ import annotations

__version__ = "0.1.0"

def forge_badge(self, badge_id: str, **kwargs: Any) -> ForgeBadgeResult:
    """GET /v1/forge/badge/{id} — retrieve Forge badge metadata. Free."""
    return self._get_model(f"/v1/forge/badge/{_pseg(badge_id, 'badge_id')}", ForgeBadgeResult, **kwargs)
