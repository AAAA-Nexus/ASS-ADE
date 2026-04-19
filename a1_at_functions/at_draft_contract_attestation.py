# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_contract_attestation.py:7
# Component id: at.source.a1_at_functions.contract_attestation
from __future__ import annotations

__version__ = "0.1.0"

def contract_attestation(self, contract_id: str) -> ContractAttestation:
    """/v1/contract/attestation/{id} — fetch Nexus-Certified attestation (BCV-101). $0.020/call"""
    return self._get_model(f"/v1/contract/attestation/{_pseg(contract_id, 'contract_id')}", ContractAttestation)
