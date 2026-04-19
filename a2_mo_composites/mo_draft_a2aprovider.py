# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_a2aprovider.py:5
# Component id: mo.source.ass_ade.a2aprovider
__version__ = "0.1.0"

class A2AProvider(BaseModel):
    """Organization or individual providing the agent."""

    organization: str = ""
    url: str = ""
