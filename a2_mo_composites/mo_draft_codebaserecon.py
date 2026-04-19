# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_codebaserecon.py:7
# Component id: mo.source.a2_mo_composites.codebaserecon
from __future__ import annotations

__version__ = "0.1.0"

class CodebaseRecon(BaseModel):
    root: str
    total_files: int
    total_dirs: int
    file_types: dict[str, int] = Field(default_factory=dict)
    top_level_entries: list[str] = Field(default_factory=list)
    relevant_files: list[str] = Field(default_factory=list)
    test_files: list[str] = Field(default_factory=list)
    docs_files: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)
