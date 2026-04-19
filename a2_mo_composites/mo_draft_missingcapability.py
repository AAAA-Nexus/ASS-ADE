# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_missingcapability.py:7
# Component id: mo.source.a2_mo_composites.missingcapability
from __future__ import annotations

__version__ = "0.1.0"

class MissingCapability(BaseModel):
    name: str
    type: str
    specification: str
    recommended_creation_tool: str
    estimated_fuel_cost: float
    verification_criteria: list[str] = Field(default_factory=list)
    human_approval_required: bool = False
