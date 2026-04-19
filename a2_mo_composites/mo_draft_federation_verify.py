# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:845
# Component id: mo.source.ass_ade.federation_verify
from __future__ import annotations

__version__ = "0.1.0"

def federation_verify(self, token: str, **kwargs: Any) -> FederationVerify:
    """/v1/federation/verify — verify nxf_ token (AIF-101). $0.020/call"""
    return self._post_model("/v1/federation/verify", FederationVerify, {"token": token, **kwargs})
