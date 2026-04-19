# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_developmentplan.py:7
# Component id: mo.source.a2_mo_composites.developmentplan
from __future__ import annotations

__version__ = "0.1.0"

class DevelopmentPlan(BaseModel):
    steps: list[str] = Field(default_factory=list)
    total_estimated_time_seconds: int = 0
    auto_invent_triggered: bool = False
    created_assets: list[str] = Field(default_factory=list)
