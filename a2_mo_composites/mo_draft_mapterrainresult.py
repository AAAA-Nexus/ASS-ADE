# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_mapterrainresult.py:7
# Component id: mo.source.a2_mo_composites.mapterrainresult
from __future__ import annotations

__version__ = "0.1.0"

class MapTerrainResult(BaseModel):
    verdict: Verdict
    missing_capabilities: list[MissingCapability] = Field(default_factory=list)
    inventory_check: dict[str, dict[str, str]] = Field(default_factory=dict)
    development_plan: DevelopmentPlan | None = None
    next_action: str
