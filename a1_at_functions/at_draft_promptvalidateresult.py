# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_promptvalidateresult.py:7
# Component id: at.source.a1_at_functions.promptvalidateresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptValidateResult(BaseModel):
    source: str
    sha256: str
    expected_sha256: str | None = None
    valid: bool = False
    manifest_path: str | None = None
    manifest_signature_present: bool = False
    signature_verified: bool = False
    notes: list[str] = Field(default_factory=list)
