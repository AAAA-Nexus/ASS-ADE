# Extracted from C:/!ass-ade/src/ass_ade/map_terrain.py:134
# Component id: mo.source.ass_ade.missingcapability
from __future__ import annotations

__version__ = "0.1.0"

class MissingCapability(BaseModel):
    name: str
    type: str
    type_key: CapabilityType
    specification: str
    recommended_creation_tool: str
    estimated_fuel_cost: float
    verification_criteria: list[str] = Field(default_factory=list)
    human_approval_required: bool = False
