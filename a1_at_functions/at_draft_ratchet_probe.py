# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_ratchet_probe.py:7
# Component id: at.source.a1_at_functions.ratchet_probe
from __future__ import annotations

__version__ = "0.1.0"

def ratchet_probe(self, session_ids: list[str], **kwargs: Any) -> RatchetProbeResult:
    """/v1/ratchet/probe — batch liveness check for up to 100 sessions. $0.008/call"""
    return self._post_model("/v1/ratchet/probe", RatchetProbeResult, {"session_ids": session_ids, **kwargs})
