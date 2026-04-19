# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:853
# Component id: mo.source.ass_ade.datavalidation
from __future__ import annotations

__version__ = "0.1.0"

class DataValidation(NexusModel):
    """/v1/data/validate-json"""
    valid: bool | None = None
    errors: list[dict] = Field(default_factory=list)
    error_paths: list[str] = Field(default_factory=list)
