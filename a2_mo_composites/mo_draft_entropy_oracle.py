# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:251
# Component id: mo.source.a2_mo_composites.entropy_oracle
from __future__ import annotations

__version__ = "0.1.0"

def entropy_oracle(self, **kwargs: Any) -> EntropyResult:
    """/v1/oracle/entropy — session entropy measurement. $0.004/call"""
    return self._post_model("/v1/oracle/entropy", EntropyResult, kwargs or {})
