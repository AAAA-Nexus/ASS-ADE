# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_activeterrainverdict.py:7
# Component id: mo.source.a2_mo_composites.activeterrainverdict
from __future__ import annotations

__version__ = "0.1.0"

class ActiveTerrainVerdict(BaseModel):
    """Result of the active MAP=TERRAIN loop."""
    verdict: Verdict
    stubs_created: list[InventionStub] = Field(default_factory=list)
    capabilities_present: list[str] = Field(default_factory=list)
    capabilities_missing: list[str] = Field(default_factory=list)
    next_action: str
