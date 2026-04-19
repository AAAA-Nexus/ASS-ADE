# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compliance_products_happy_path.py:7
# Component id: at.source.a1_at_functions.test_compliance_products_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_compliance_products_happy_path(method_name, response_json):
    """Test compliance products methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "compliance_fairness":
            result = client.compliance_fairness(dataset_description="dataset desc")
        elif method_name == "compliance_explain":
            result = client.compliance_explain(output="model output", input_features={"f1": 1.0})
        elif method_name == "compliance_lineage":
            result = client.compliance_lineage(dataset_stages=[{"stage": "raw"}, {"stage": "processed"}])
        elif method_name == "compliance_oversight":
            result = client.compliance_oversight(reviewer="reviewer_1", decision="approved")
        elif method_name == "compliance_incident":
            result = client.compliance_incident(system_id="system_1", description="incident description", severity="high")
        elif method_name == "compliance_incidents":
            result = client.compliance_incidents(system_id="system_1")
        elif method_name == "compliance_transparency":
            result = client.compliance_transparency(system_id="system_1", period="Q1 2026")
        elif method_name == "drift_check":
            result = client.drift_check(model_id="model_1", reference_data={}, current_data={})
        else:  # drift_certificate
            result = client.drift_certificate(check_id="check_123")
        assert result is not None
