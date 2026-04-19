# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_versionbumpresult.py:5
# Component id: mo.source.ass_ade.versionbumpresult
__version__ = "0.1.0"

class VersionBumpResult(BaseModel):
    old_version: str
    new_version: str
    bump: str
    dry_run: bool
    files_updated: list[str] = Field(default_factory=list)
    backup_dir: str = ""
    files_backed_up: list[str] = Field(default_factory=list)
