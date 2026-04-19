# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_delegation_validate.py:7
# Component id: at.source.a1_at_functions.delegation_validate
from __future__ import annotations

__version__ = "0.1.0"

def delegation_validate(self, chain: list[dict], **kwargs: Any) -> DelegationValidation:
    """/v1/identity/delegation/validate — IDT-201 chain depth validator. $0.080/call"""
    return self._post_model("/v1/identity/delegation/validate", DelegationValidation, {"chain": chain, **kwargs})
