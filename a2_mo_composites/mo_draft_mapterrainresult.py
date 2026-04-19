# Extracted from C:/!ass-ade/src/ass_ade/map_terrain.py:152
# Component id: mo.source.ass_ade.mapterrainresult
from __future__ import annotations

__version__ = "0.1.0"

class MapTerrainResult(BaseModel):
    verdict: Verdict
    missing_capabilities: list[MissingCapability] = Field(default_factory=list)
    inventory_check: dict[str, dict[str, str]] = Field(default_factory=dict)
    development_plan: DevelopmentPlan | None = None
    next_action: str
