# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/map_terrain.py:109
# Component id: mo.source.ass_ade.missingcapability
__version__ = "0.1.0"

class MissingCapability(BaseModel):
    name: str
    type: str
    specification: str
    recommended_creation_tool: str
    estimated_fuel_cost: float
    verification_criteria: list[str] = Field(default_factory=list)
    human_approval_required: bool = False
