# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/prompt_toolkit.py:35
# Component id: at.source.ass_ade.promptvalidateresult
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
