# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:839
# Component id: mo.source.a2_mo_composites.defi_contract_audit
from __future__ import annotations

__version__ = "0.1.0"

def defi_contract_audit(self, contract_address: str, source_code: str | None = None, **kwargs: Any) -> SmartContractAudit:
    """/v1/defi/contract-audit — 30-pattern smart contract audit cert (CVR-100). $0.15/audit"""
    return self._post_model("/v1/defi/contract-audit", SmartContractAudit, {
        "contract_address": contract_address, "source_code": source_code, **kwargs,
    })
