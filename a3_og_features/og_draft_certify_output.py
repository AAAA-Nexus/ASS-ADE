# Extracted from C:/!ass-ade/src/ass_ade/workflows.py:164
# Component id: og.source.ass_ade.certify_output
from __future__ import annotations

__version__ = "0.1.0"

def certify_output(client: NexusClient, text: str) -> CertifyResult:
    """Multi-step output certification: hallucination → ethics → compliance → certify → lineage.

    Returns a certificate ID that can be verified later.
    """
    text = validate_prompt(text)
    result = CertifyResult(text_preview=text[:120])

    # Step 1: Hallucination oracle
    try:
        hall = client.hallucination_oracle(text)
        result.hallucination_verdict = getattr(hall, "verdict", None)
    except _WORKFLOW_ERRORS:
        _LOG.warning("Hallucination oracle failed during certification", exc_info=True)
        result.hallucination_verdict = "error"

    # Step 2: Ethics check
    try:
        eth = client.ethics_check(text)
        eth_raw = eth.model_dump() if hasattr(eth, "model_dump") else {}
        result.ethics_verdict = "safe" if eth_raw.get("safe") else str(eth_raw.get("safe", "unknown"))
    except _WORKFLOW_ERRORS:
        _LOG.warning("Ethics check failed during certification", exc_info=True)
        result.ethics_verdict = "error"

    # Step 3: Compliance check
    try:
        comp = client.compliance_check(text)
        comp_raw = comp.model_dump() if hasattr(comp, "model_dump") else {}
        result.compliance_verdict = "compliant" if comp_raw.get("compliant") else str(comp_raw.get("compliant", "unknown"))
    except _WORKFLOW_ERRORS:
        _LOG.warning("Compliance check failed during certification", exc_info=True)
        result.compliance_verdict = "error"

    # Step 4: Certify output via AAAA-Nexus
    try:
        cert = client.certify_output(text, rubric=["accuracy", "safety", "compliance"])
        cert_raw = cert.model_dump() if hasattr(cert, "model_dump") else {}
        result.certificate_id = cert_raw.get("certificate_id")
    except _WORKFLOW_ERRORS:
        _LOG.warning("Output certification failed", exc_info=True)
        result.certificate_id = None

    # Step 5: Lineage record
    try:
        lin = client.lineage_record(
            intent="output_certification",
            constraints=["hallucination_check", "ethics_check", "compliance_check"],
            outcome=f"certificate={result.certificate_id or 'none'}",
        )
        lin_raw = lin.model_dump() if hasattr(lin, "model_dump") else {}
        result.lineage_id = lin_raw.get("record_id")
    except _WORKFLOW_ERRORS:
        _LOG.warning("Lineage recording failed during certification", exc_info=True)
        result.lineage_id = None

    result.passed = (
        result.hallucination_verdict not in (None, "error", "unsafe")
        and result.ethics_verdict not in (None, "error")
        and result.certificate_id is not None
    )

    return result
