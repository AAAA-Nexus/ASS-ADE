# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/map_terrain.py:126
# Component id: mo.source.ass_ade.mapterrainresult
__version__ = "0.1.0"

class MapTerrainResult(BaseModel):
    verdict: Verdict
    missing_capabilities: list[MissingCapability] = Field(default_factory=list)
    inventory_check: dict[str, dict[str, str]] = Field(default_factory=dict)
    development_plan: DevelopmentPlan | None = None
    next_action: str
