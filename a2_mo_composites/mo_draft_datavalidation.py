# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_datavalidation.py:5
# Component id: mo.source.ass_ade.datavalidation
__version__ = "0.1.0"

class DataValidation(NexusModel):
    """/v1/data/validate-json"""
    valid: bool | None = None
    errors: list[dict] = Field(default_factory=list)
    error_paths: list[str] = Field(default_factory=list)
