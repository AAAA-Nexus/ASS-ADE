# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_safeexecuteresult.py:5
# Component id: og.source.ass_ade.safeexecuteresult
__version__ = "0.1.0"

class SafeExecuteResult(BaseModel):
    tool_name: str | None = None
    shield_passed: bool = False
    prompt_scan_passed: bool = False
    invocation_result: dict[str, Any] = Field(default_factory=dict)
    certificate_id: str | None = None
