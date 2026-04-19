# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_datavalidation.py:7
# Component id: mo.source.a2_mo_composites.datavalidation
from __future__ import annotations

__version__ = "0.1.0"

class DataValidation(NexusModel):
    """/v1/data/validate-json"""
    valid: bool | None = None
    errors: list[dict] = Field(default_factory=list)
    error_paths: list[str] = Field(default_factory=list)
