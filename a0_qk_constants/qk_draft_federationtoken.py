# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_federationtoken.py:5
# Component id: qk.source.ass_ade.federationtoken
__version__ = "0.1.0"

class FederationToken(NexusModel):
    """/v1/federation/mint — AIF-100"""
    token: str | None = None          # nxf_… prefixed
    identity_record: dict | None = None
    platforms: list[str] = Field(default_factory=list)
