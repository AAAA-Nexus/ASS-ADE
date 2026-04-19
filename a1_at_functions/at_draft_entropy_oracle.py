# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_entropy_oracle.py:7
# Component id: at.source.a1_at_functions.entropy_oracle
from __future__ import annotations

__version__ = "0.1.0"

def entropy_oracle(self, **kwargs: Any) -> EntropyResult:
    """/v1/oracle/entropy — session entropy measurement. $0.004/call"""
    return self._post_model("/v1/oracle/entropy", EntropyResult, kwargs or {})
