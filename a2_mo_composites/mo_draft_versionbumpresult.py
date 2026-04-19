# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_versionbumpresult.py:7
# Component id: mo.source.a2_mo_composites.versionbumpresult
from __future__ import annotations

__version__ = "0.1.0"

class VersionBumpResult(BaseModel):
    old_version: str
    new_version: str
    bump: str
    dry_run: bool
    files_updated: list[str] = Field(default_factory=list)
    backup_dir: str = ""
    files_backed_up: list[str] = Field(default_factory=list)
