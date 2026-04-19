# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:73
# Component id: mo.source.ass_ade.versionbumpresult
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
