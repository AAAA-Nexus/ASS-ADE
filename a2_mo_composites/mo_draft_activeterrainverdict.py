# Extracted from C:/!ass-ade/src/ass_ade/map_terrain.py:1180
# Component id: mo.source.ass_ade.activeterrainverdict
from __future__ import annotations

__version__ = "0.1.0"

class ActiveTerrainVerdict(BaseModel):
    """Result of the active MAP=TERRAIN loop."""

    verdict: Verdict
    stubs_created: list[InventionStub] = Field(default_factory=list)
    capabilities_present: list[str] = Field(default_factory=list)
    capabilities_missing: list[str] = Field(default_factory=list)
    next_action: str
