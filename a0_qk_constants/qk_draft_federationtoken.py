# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:591
# Component id: qk.source.ass_ade.federationtoken
from __future__ import annotations

__version__ = "0.1.0"

class FederationToken(NexusModel):
    """/v1/federation/mint — AIF-100"""
    token: str | None = None          # nxf_… prefixed
    identity_record: dict | None = None
    platforms: list[str] = Field(default_factory=list)
