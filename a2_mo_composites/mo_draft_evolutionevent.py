# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/evolution.py:44
# Component id: mo.source.ass_ade.evolutionevent
__version__ = "0.1.0"

class EvolutionEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_id: str = Field(default=EVOLUTION_SCHEMA, alias="schema")
    event_id: str
    timestamp_utc: str
    event_type: str
    summary: str
    version: str
    root: str
    git: EvolutionGitState
    commands: list[EvolutionCommand] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    reports: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    rationale: str = ""
    next_steps: list[str] = Field(default_factory=list)
    rebuild: dict[str, Any] = Field(default_factory=dict)
    certificates: list[dict[str, Any]] = Field(default_factory=list)
    lineage_ids: list[str] = Field(default_factory=list)
