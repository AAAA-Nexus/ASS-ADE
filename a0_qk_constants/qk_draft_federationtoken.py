# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_federationtoken.py:7
# Component id: qk.source.a0_qk_constants.federationtoken
from __future__ import annotations

__version__ = "0.1.0"

class FederationToken(NexusModel):
    """/v1/federation/mint — AIF-100"""
    token: str | None = None          # nxf_… prefixed
    identity_record: dict | None = None
    platforms: list[str] = Field(default_factory=list)
