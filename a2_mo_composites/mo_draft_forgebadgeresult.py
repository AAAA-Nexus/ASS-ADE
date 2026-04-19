# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_forgebadgeresult.py:7
# Component id: mo.source.a2_mo_composites.forgebadgeresult
from __future__ import annotations

__version__ = "0.1.0"

class ForgeBadgeResult(NexusModel):
    """GET /v1/forge/badge/{id}"""
    badge_id: str | None = None
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    issued_at: str | None = None
    valid: bool | None = None
