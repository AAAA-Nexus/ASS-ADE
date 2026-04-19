# Extracted from C:/!ass-ade/src/ass_ade/map_terrain.py:145
# Component id: mo.source.ass_ade.developmentplan
from __future__ import annotations

__version__ = "0.1.0"

class DevelopmentPlan(BaseModel):
    steps: list[str] = Field(default_factory=list)
    total_estimated_time_seconds: int = 0
    auto_invent_triggered: bool = False
    created_assets: list[str] = Field(default_factory=list)
