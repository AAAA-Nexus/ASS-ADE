# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_security_compliance_happy_path.py:7
# Component id: at.source.a1_at_functions.test_security_compliance_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_security_compliance_happy_path(method_name, response_json):
    """Test security & compliance methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "threat_score":
            result = client.threat_score(payload={"action": "execute"})
        elif method_name == "security_shield":
            result = client.security_shield(payload={"tool_call": "execute"})
        elif method_name == "security_pqc_sign":
            result = client.security_pqc_sign(data="data_to_sign")
        elif method_name == "compliance_check":
            result = client.compliance_check(system_description="system desc")
        elif method_name == "compliance_eu_ai_act":
            result = client.compliance_eu_ai_act(system_description="system desc")
        elif method_name == "aibom_drift":
            result = client.aibom_drift(model_id="model_1")
        elif method_name == "audit_log":
            result = client.audit_log(event={"action": "login"})
        elif method_name == "audit_verify":
            result = client.audit_verify()
        else:  # agent_quarantine
            result = client.agent_quarantine(agent_id="agent_1", reason="security_risk")
        assert result is not None
