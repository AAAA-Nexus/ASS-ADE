# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_vectormemorymatch.py:5
# Component id: mo.source.ass_ade.vectormemorymatch
__version__ = "0.1.0"

class VectorMemoryMatch(BaseModel):
    id: str
    namespace: str
    score: float
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str
