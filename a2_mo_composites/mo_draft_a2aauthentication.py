# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_a2aauthentication.py:5
# Component id: mo.source.ass_ade.a2aauthentication
__version__ = "0.1.0"

class A2AAuthentication(BaseModel):
    """Authentication requirements for the agent."""

    schemes: list[str] = Field(default_factory=list)  # e.g. ["bearer", "x402"]
    credentials: str | None = None  # human-readable note
