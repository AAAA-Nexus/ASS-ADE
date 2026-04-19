# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:827
# Component id: mo.source.ass_ade.contract_attestation
from __future__ import annotations

__version__ = "0.1.0"

def contract_attestation(self, contract_id: str) -> ContractAttestation:
    """/v1/contract/attestation/{id} — fetch Nexus-Certified attestation (BCV-101). $0.020/call"""
    return self._get_model(f"/v1/contract/attestation/{_pseg(contract_id, 'contract_id')}", ContractAttestation)
