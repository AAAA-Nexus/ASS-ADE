# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_vectormemoryqueryresult.py:5
# Component id: mo.source.ass_ade.vectormemoryqueryresult
__version__ = "0.1.0"

class VectorMemoryQueryResult(BaseModel):
    query: str
    namespace: str
    matches: list[VectorMemoryMatch] = Field(default_factory=list)
