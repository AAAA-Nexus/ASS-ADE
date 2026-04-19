# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bitnetmodelsresponse.py:5
# Component id: mo.source.ass_ade.bitnetmodelsresponse
__version__ = "0.1.0"

class BitNetModelsResponse(NexusModel):
    """GET /v1/bitnet/models"""
    models: list[BitNetModel] = Field(default_factory=list)
    count: int | None = None
