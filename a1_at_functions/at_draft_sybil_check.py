# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_sybil_check.py:7
# Component id: at.source.a1_at_functions.sybil_check
from __future__ import annotations

__version__ = "0.1.0"

def sybil_check(self, actor: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> SybilCheckResult:
    """/v1/identity/sybil-check — sybil resistance check. $0.020/call"""
    return self._post_model("/v1/identity/sybil-check", SybilCheckResult, {"actor": actor or agent_id or "", **kwargs})
