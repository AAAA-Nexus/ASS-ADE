# Extracted from C:/!ass-ade/src/ass_ade/protocol/cycle.py:19
# Component id: mo.source.ass_ade.protocolassessment
from __future__ import annotations

__version__ = "0.1.0"

class ProtocolAssessment(BaseModel):
    root: str
    total_files: int
    total_dirs: int
    top_level_entries: list[str]
    file_types: dict[str, int]
    toolchain: list[dict[str, str | bool | None]]
    profile: str
    local_mode_default: bool
