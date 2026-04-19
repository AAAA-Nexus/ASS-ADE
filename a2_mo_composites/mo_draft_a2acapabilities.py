# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_a2acapabilities.py:5
# Component id: mo.source.ass_ade.a2acapabilities
__version__ = "0.1.0"

class A2ACapabilities(BaseModel):
    """Agent capability flags per A2A spec."""

    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False
