# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_federation_verify.py:7
# Component id: at.source.a1_at_functions.federation_verify
from __future__ import annotations

__version__ = "0.1.0"

def federation_verify(self, token: str, **kwargs: Any) -> FederationVerify:
    """/v1/federation/verify — verify nxf_ token (AIF-101). $0.020/call"""
    return self._post_model("/v1/federation/verify", FederationVerify, {"token": token, **kwargs})
